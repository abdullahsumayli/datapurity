"""
اختبار نظام تنظيف البطاقات
========================

هذا السكربت يقوم بـ:
1. إنشاء بطاقات تجريبية قديمة
2. تشغيل التنظيف
3. التحقق من النتائج
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.db.session import AsyncSessionLocal
from app.models.card import Card
from cleanup_old_cards import CardCleanupService


async def create_test_cards():
    """إنشاء بطاقات تجريبية للاختبار."""
    async with AsyncSessionLocal() as db:
        now = datetime.utcnow()
        
        # 1. Create old unreviewed card (100 days old)
        old_unreviewed = Card(
            user_id=1,
            original_filename="old_unreviewed.jpg",
            storage_path="tmp/cards/old_unreviewed.jpg",
            file_size=1024,
            ocr_text="مركز البيانات المتقدم",
            ocr_confidence=85.0,
            extracted_name="أحمد محمد",
            extracted_company="مركز البيانات",
            extracted_phone="+966501234567",
            extracted_email="ahmed@data.com",
            is_processed=True,
            is_reviewed=False,
            created_at=now - timedelta(days=100)
        )
        db.add(old_unreviewed)
        
        # 2. Create old reviewed card (200 days old)
        old_reviewed = Card(
            user_id=1,
            original_filename="old_reviewed.jpg",
            storage_path="tmp/cards/old_reviewed.jpg",
            file_size=2048,
            ocr_text="شركة التقنية الحديثة",
            ocr_confidence=92.0,
            extracted_name="سارة علي",
            extracted_company="التقنية الحديثة",
            extracted_phone="+966507654321",
            extracted_email="sara@tech.com",
            is_processed=True,
            is_reviewed=True,
            created_at=now - timedelta(days=200)
        )
        db.add(old_reviewed)
        
        # 3. Create low-confidence card (40 days old)
        low_confidence = Card(
            user_id=1,
            original_filename="low_confidence.jpg",
            storage_path="tmp/cards/low_confidence.jpg",
            file_size=512,
            ocr_text="نص غير واضح",
            ocr_confidence=35.0,  # Low confidence
            extracted_name=None,
            extracted_company=None,
            extracted_phone=None,
            extracted_email=None,
            is_processed=True,
            is_reviewed=False,
            created_at=now - timedelta(days=40)
        )
        db.add(low_confidence)
        
        # 4. Create recent card (5 days old) - should NOT be deleted
        recent = Card(
            user_id=1,
            original_filename="recent.jpg",
            storage_path="tmp/cards/recent.jpg",
            file_size=1536,
            ocr_text="بطاقة حديثة",
            ocr_confidence=88.0,
            extracted_name="خالد الرشيد",
            extracted_company="شركة المستقبل",
            extracted_phone="+966501111111",
            extracted_email="khalid@future.com",
            is_processed=True,
            is_reviewed=False,
            created_at=now - timedelta(days=5)
        )
        db.add(recent)
        
        await db.commit()
        print("✅ تم إنشاء 4 بطاقات تجريبية:")
        print(f"   1. بطاقة قديمة غير مراجعة (100 يوم)")
        print(f"   2. بطاقة قديمة مراجعة (200 يوم)")
        print(f"   3. بطاقة ضعيفة الثقة (40 يوم، 35% ثقة)")
        print(f"   4. بطاقة حديثة (5 أيام) - يجب أن تبقى")
        print()


async def count_cards():
    """عد البطاقات في قاعدة البيانات."""
    from sqlalchemy import select, func
    
    async with AsyncSessionLocal() as db:
        # Total count
        result = await db.execute(select(func.count(Card.id)))
        total = result.scalar()
        
        # Unreviewed count
        result = await db.execute(
            select(func.count(Card.id))
            .where(Card.is_reviewed == False)
        )
        unreviewed = result.scalar()
        
        # Reviewed count
        result = await db.execute(
            select(func.count(Card.id))
            .where(Card.is_reviewed == True)
        )
        reviewed = result.scalar()
        
        return total, unreviewed, reviewed


async def main():
    """تشغيل الاختبار الكامل."""
    print("=" * 60)
    print("اختبار نظام تنظيف البطاقات")
    print("=" * 60)
    print()
    
    # Step 1: Count existing cards
    print("📊 الخطوة 1: إحصاء البطاقات الحالية")
    total_before, unreviewed_before, reviewed_before = await count_cards()
    print(f"   إجمالي البطاقات: {total_before}")
    print(f"   غير مراجعة: {unreviewed_before}")
    print(f"   مراجعة: {reviewed_before}")
    print()
    
    # Step 2: Create test cards
    print("📝 الخطوة 2: إنشاء بطاقات تجريبية")
    await create_test_cards()
    
    # Count after creation
    total_after_create, unreviewed_after_create, reviewed_after_create = await count_cards()
    print(f"📊 إجمالي البطاقات الآن: {total_after_create}")
    print()
    
    # Step 3: Run cleanup
    print("🧹 الخطوة 3: تشغيل التنظيف")
    service = CardCleanupService()
    stats = await service.run_full_cleanup(
        unreviewed_days=90,
        reviewed_days=180,
        low_confidence_days=30,
        min_confidence=50.0
    )
    print()
    
    # Step 4: Count after cleanup
    print("📊 الخطوة 4: إحصاء البطاقات بعد التنظيف")
    total_after, unreviewed_after, reviewed_after = await count_cards()
    print(f"   إجمالي البطاقات: {total_after}")
    print(f"   غير مراجعة: {unreviewed_after}")
    print(f"   مراجعة: {reviewed_after}")
    print()
    
    # Step 5: Verify results
    print("✅ الخطوة 5: التحقق من النتائج")
    expected_deleted = 3  # Should delete 3 old/low-confidence cards
    actual_deleted = total_after_create - total_after
    
    if actual_deleted == expected_deleted:
        print(f"   ✅ ممتاز! تم حذف {actual_deleted} بطاقات كما هو متوقع")
        print(f"   ✅ البطاقة الحديثة (5 أيام) لم تُحذف")
    else:
        print(f"   ⚠️  تحذير: تم حذف {actual_deleted} بطاقات بدلاً من {expected_deleted}")
    
    print()
    print("=" * 60)
    print("انتهى الاختبار!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
