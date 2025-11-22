"""
سكربت مسح البطاقات القديمة وغير المستخدمة
====================================

هذا السكربت يقوم بـ:
1. حذف البطاقات غير المراجعة الأقدم من 90 يوم
2. حذف البطاقات المعالجة الأقدم من 180 يوم
3. حذف الملفات اليتيمة (orphaned files) من tmp/cards
4. تنظيف البطاقات ذات الثقة المنخفضة (< 50%)
5. إزالة السجلات المكررة

يمكن تشغيله يدوياً أو جدولته مع cron/scheduler
"""

import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.card import Card

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CardCleanupService:
    """خدمة تنظيف البطاقات القديمة."""
    
    def __init__(self):
        self.stats = {
            "unreviewed_deleted": 0,
            "old_reviewed_deleted": 0,
            "low_confidence_deleted": 0,
            "orphaned_files_deleted": 0,
            "total_deleted": 0
        }
    
    async def cleanup_unreviewed_cards(
        self,
        db: AsyncSession,
        days: int = 90
    ) -> int:
        """
        حذف البطاقات غير المراجعة الأقدم من X يوم.
        
        Args:
            db: Database session
            days: عدد الأيام (افتراضي 90)
        
        Returns:
            عدد البطاقات المحذوفة
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Query unreviewed cards older than cutoff date
            result = await db.execute(
                select(Card)
                .where(Card.is_reviewed == False)
                .where(Card.created_at < cutoff_date)
            )
            cards = result.scalars().all()
            
            deleted_count = 0
            for card in cards:
                # Delete associated files
                await self._delete_card_file(card.storage_path)
                
                # Delete database record
                await db.delete(card)
                deleted_count += 1
            
            await db.commit()
            
            logger.info(f"Deleted {deleted_count} unreviewed cards older than {days} days")
            self.stats["unreviewed_deleted"] = deleted_count
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning unreviewed cards: {str(e)}")
            await db.rollback()
            return 0
    
    async def cleanup_old_reviewed_cards(
        self,
        db: AsyncSession,
        days: int = 180
    ) -> int:
        """
        حذف البطاقات المراجعة الأقدم من X يوم.
        
        Args:
            db: Database session
            days: عدد الأيام (افتراضي 180)
        
        Returns:
            عدد البطاقات المحذوفة
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            result = await db.execute(
                select(Card)
                .where(Card.is_reviewed == True)
                .where(Card.created_at < cutoff_date)
            )
            cards = result.scalars().all()
            
            deleted_count = 0
            for card in cards:
                await self._delete_card_file(card.storage_path)
                await db.delete(card)
                deleted_count += 1
            
            await db.commit()
            
            logger.info(f"Deleted {deleted_count} reviewed cards older than {days} days")
            self.stats["old_reviewed_deleted"] = deleted_count
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning reviewed cards: {str(e)}")
            await db.rollback()
            return 0
    
    async def cleanup_low_confidence_cards(
        self,
        db: AsyncSession,
        min_confidence: float = 50.0,
        days: int = 30
    ) -> int:
        """
        حذف البطاقات ذات الثقة المنخفضة والأقدم من X يوم.
        
        Args:
            db: Database session
            min_confidence: الحد الأدنى للثقة (افتراضي 50%)
            days: عدد الأيام (افتراضي 30)
        
        Returns:
            عدد البطاقات المحذوفة
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            result = await db.execute(
                select(Card)
                .where(Card.ocr_confidence < min_confidence)
                .where(Card.is_reviewed == False)
                .where(Card.created_at < cutoff_date)
            )
            cards = result.scalars().all()
            
            deleted_count = 0
            for card in cards:
                await self._delete_card_file(card.storage_path)
                await db.delete(card)
                deleted_count += 1
            
            await db.commit()
            
            logger.info(
                f"Deleted {deleted_count} low-confidence cards "
                f"(< {min_confidence}%) older than {days} days"
            )
            self.stats["low_confidence_deleted"] = deleted_count
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning low-confidence cards: {str(e)}")
            await db.rollback()
            return 0
    
    async def cleanup_orphaned_files(self) -> int:
        """
        حذف الملفات اليتيمة من tmp/cards.
        
        Returns:
            عدد الملفات المحذوفة
        """
        try:
            temp_dir = Path("tmp/cards")
            if not temp_dir.exists():
                return 0
            
            deleted_count = 0
            for file_path in temp_dir.glob("*"):
                if file_path.is_file():
                    # Check file age
                    file_age = datetime.now() - datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    )
                    
                    # Delete files older than 24 hours
                    if file_age > timedelta(hours=24):
                        try:
                            file_path.unlink()
                            deleted_count += 1
                        except Exception as e:
                            logger.error(f"Failed to delete {file_path}: {str(e)}")
            
            logger.info(f"Deleted {deleted_count} orphaned files from tmp/cards")
            self.stats["orphaned_files_deleted"] = deleted_count
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning orphaned files: {str(e)}")
            return 0
    
    async def _delete_card_file(self, storage_path: str) -> bool:
        """
        حذف ملف البطاقة من التخزين.
        
        Args:
            storage_path: مسار الملف
        
        Returns:
            True إذا تم الحذف بنجاح
        """
        try:
            if not storage_path:
                return False
            
            file_path = Path(storage_path)
            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete file {storage_path}: {str(e)}")
            return False
    
    async def run_full_cleanup(
        self,
        unreviewed_days: int = 90,
        reviewed_days: int = 180,
        low_confidence_days: int = 30,
        min_confidence: float = 50.0
    ) -> Dict[str, int]:
        """
        تشغيل تنظيف كامل للبطاقات.
        
        Args:
            unreviewed_days: أيام البطاقات غير المراجعة
            reviewed_days: أيام البطاقات المراجعة
            low_confidence_days: أيام البطاقات ضعيفة الثقة
            min_confidence: الحد الأدنى للثقة
        
        Returns:
            إحصائيات التنظيف
        """
        logger.info("=" * 60)
        logger.info("بدء تنظيف البطاقات القديمة...")
        logger.info("=" * 60)
        
        async with AsyncSessionLocal() as db:
            # 1. Clean unreviewed cards
            await self.cleanup_unreviewed_cards(db, unreviewed_days)
            
            # 2. Clean old reviewed cards
            await self.cleanup_old_reviewed_cards(db, reviewed_days)
            
            # 3. Clean low-confidence cards
            await self.cleanup_low_confidence_cards(
                db,
                min_confidence,
                low_confidence_days
            )
        
        # 4. Clean orphaned files (no DB needed)
        await self.cleanup_orphaned_files()
        
        # Calculate total
        self.stats["total_deleted"] = (
            self.stats["unreviewed_deleted"] +
            self.stats["old_reviewed_deleted"] +
            self.stats["low_confidence_deleted"]
        )
        
        logger.info("=" * 60)
        logger.info("نتائج التنظيف:")
        logger.info(f"  - بطاقات غير مراجعة: {self.stats['unreviewed_deleted']}")
        logger.info(f"  - بطاقات قديمة مراجعة: {self.stats['old_reviewed_deleted']}")
        logger.info(f"  - بطاقات ضعيفة الثقة: {self.stats['low_confidence_deleted']}")
        logger.info(f"  - ملفات يتيمة: {self.stats['orphaned_files_deleted']}")
        logger.info(f"  - إجمالي السجلات المحذوفة: {self.stats['total_deleted']}")
        logger.info("=" * 60)
        
        return self.stats


async def main():
    """تشغيل التنظيف."""
    service = CardCleanupService()
    
    # Run with default settings
    stats = await service.run_full_cleanup(
        unreviewed_days=90,      # حذف غير المراجعة بعد 90 يوم
        reviewed_days=180,       # حذف المراجعة بعد 180 يوم
        low_confidence_days=30,  # حذف ضعيفة الثقة بعد 30 يوم
        min_confidence=50.0      # ثقة أقل من 50%
    )
    
    return stats


if __name__ == "__main__":
    asyncio.run(main())
