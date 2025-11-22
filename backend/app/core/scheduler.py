"""Background scheduler for processing marketing automation tasks."""

import logging
from datetime import datetime
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from sqlalchemy import select, text

from app.core.settings import get_settings
from app.db.session import AsyncSessionLocal
from app.models.scheduled_task import ScheduledTask
from app.models.card import Card
from app.services.email_service import build_template, send_email
from app.services.campaigns_service import log_campaign_event

logger = logging.getLogger(__name__)
settings = get_settings()


async def process_scheduled_tasks() -> None:
    """
    Process pending scheduled tasks that are due.
    
    This function:
    1. Queries tasks where run_at <= now and status = "pending"
    2. Processes each task (sends emails, etc.)
    3. Updates task status and logs campaign events
    """
    try:
        async with AsyncSessionLocal() as db:
            # Get pending tasks that are due
            now = datetime.utcnow()
            result = await db.execute(
                select(ScheduledTask)
                .where(ScheduledTask.run_at <= now)
                .where(ScheduledTask.status == "pending")
                .where(ScheduledTask.retry_count < 3)  # Max 3 retries
                .limit(50)  # Process in batches
            )
            tasks = result.scalars().all()
            
            if not tasks:
                return
            
            logger.info(f"Processing {len(tasks)} scheduled tasks")
            
            for task in tasks:
                try:
                    if task.task_type == "send_email":
                        # Extract payload
                        template_name = task.payload.get("template")
                        to_email = task.payload.get("to")
                        lead_name = task.payload.get("lead_name", "العميل")
                        
                        # Build email
                        subject, body = build_template(template_name, {
                            "lead_name": lead_name
                        })
                        
                        # Send email
                        success = send_email(to_email, subject, body)
                        
                        if success or not settings.EMAIL_USERNAME:  # Succeed if no email config (dev mode)
                            # Mark as done
                            task.status = "done"
                            task.completed_at = datetime.utcnow()
                            
                            # Log campaign event
                            await log_campaign_event(
                                db,
                                lead_id=task.lead_id,
                                event_type="email_sent",
                                meta={
                                    "template": template_name,
                                    "subject": subject,
                                    "to": to_email
                                }
                            )
                            
                            logger.info(f"Task {task.id} completed successfully")
                        else:
                            # Increment retry count
                            task.retry_count += 1
                            task.error_message = "Failed to send email"
                            
                            if task.retry_count >= 3:
                                task.status = "failed"
                                logger.error(f"Task {task.id} failed after 3 retries")
                            else:
                                logger.warning(f"Task {task.id} retry {task.retry_count}/3")
                    
                    else:
                        logger.warning(f"Unknown task type: {task.task_type}")
                        task.status = "failed"
                        task.error_message = f"Unknown task type: {task.task_type}"
                
                except Exception as e:
                    logger.error(f"Error processing task {task.id}: {str(e)}")
                    task.retry_count += 1
                    task.error_message = str(e)[:500]
                    
                    if task.retry_count >= 3:
                        task.status = "failed"
            
            # Commit all changes
            await db.commit()
            logger.info(f"Processed {len(tasks)} tasks successfully")
            
    except Exception as e:
        logger.error(f"Error in process_scheduled_tasks: {str(e)}")


def process_tasks_sync() -> None:
    """Synchronous wrapper for async task processing."""
    import asyncio
    try:
        asyncio.run(process_scheduled_tasks())
    except Exception as e:
        logger.error(f"Error in process_tasks_sync: {str(e)}")


async def cleanup_old_cards_task() -> None:
    """
    تنظيف البطاقات القديمة وغير المستخدمة.
    
    يقوم بـ:
    1. حذف البطاقات غير المراجعة > 90 يوم
    2. حذف البطاقات المراجعة > 180 يوم
    3. حذف البطاقات ضعيفة الثقة > 30 يوم
    4. حذف الملفات اليتيمة > 24 ساعة
    """
    try:
        from datetime import timedelta
        
        async with AsyncSessionLocal() as db:
            now = datetime.utcnow()
            total_deleted = 0
            
            # 1. Delete unreviewed cards older than 90 days
            unreviewed_cutoff = now - timedelta(days=90)
            result = await db.execute(
                select(Card)
                .where(Card.is_reviewed == False)
                .where(Card.created_at < unreviewed_cutoff)
            )
            unreviewed_cards = result.scalars().all()
            
            for card in unreviewed_cards:
                # Delete file
                if card.storage_path:
                    try:
                        file_path = Path(card.storage_path)
                        if file_path.exists():
                            file_path.unlink()
                    except Exception as e:
                        logger.error(f"Failed to delete file {card.storage_path}: {str(e)}")
                
                await db.delete(card)
                total_deleted += 1
            
            # 2. Delete reviewed cards older than 180 days
            reviewed_cutoff = now - timedelta(days=180)
            result = await db.execute(
                select(Card)
                .where(Card.is_reviewed == True)
                .where(Card.created_at < reviewed_cutoff)
            )
            reviewed_cards = result.scalars().all()
            
            for card in reviewed_cards:
                if card.storage_path:
                    try:
                        file_path = Path(card.storage_path)
                        if file_path.exists():
                            file_path.unlink()
                    except Exception as e:
                        logger.error(f"Failed to delete file {card.storage_path}: {str(e)}")
                
                await db.delete(card)
                total_deleted += 1
            
            # 3. Delete low-confidence cards older than 30 days
            low_confidence_cutoff = now - timedelta(days=30)
            result = await db.execute(
                select(Card)
                .where(Card.ocr_confidence < 50.0)
                .where(Card.is_reviewed == False)
                .where(Card.created_at < low_confidence_cutoff)
            )
            low_confidence_cards = result.scalars().all()
            
            for card in low_confidence_cards:
                if card.storage_path:
                    try:
                        file_path = Path(card.storage_path)
                        if file_path.exists():
                            file_path.unlink()
                    except Exception as e:
                        logger.error(f"Failed to delete file {card.storage_path}: {str(e)}")
                
                await db.delete(card)
                total_deleted += 1
            
            await db.commit()
            
            if total_deleted > 0:
                logger.info(f"Cards cleanup: Deleted {total_deleted} old cards from database")
            
            # 4. Clean orphaned files from tmp/cards
            temp_dir = Path("tmp/cards")
            if temp_dir.exists():
                orphaned_count = 0
                for file_path in temp_dir.glob("*"):
                    if file_path.is_file():
                        file_age = datetime.now() - datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        )
                        
                        # Delete files older than 24 hours
                        if file_age > timedelta(hours=24):
                            try:
                                file_path.unlink()
                                orphaned_count += 1
                            except Exception as e:
                                logger.error(f"Failed to delete orphaned file {file_path}: {str(e)}")
                
                if orphaned_count > 0:
                    logger.info(f"Cards cleanup: Deleted {orphaned_count} orphaned files")
            
    except Exception as e:
        logger.error(f"Error in cleanup_old_cards_task: {str(e)}")


def cleanup_cards_sync() -> None:
    """Synchronous wrapper for card cleanup."""
    import asyncio
    try:
        asyncio.run(cleanup_old_cards_task())
    except Exception as e:
        logger.error(f"Error in cleanup_cards_sync: {str(e)}")


def start_scheduler(app: FastAPI) -> None:
    """
    Start the background scheduler.
    
    Args:
        app: FastAPI application instance
    """
    if not settings.MARKETING_SCHEDULER_ENABLED:
        logger.info("Marketing scheduler is disabled (MARKETING_SCHEDULER_ENABLED=False)")
        return
    
    try:
        scheduler = BackgroundScheduler()
        
        # Add job to process marketing tasks
        scheduler.add_job(
            process_tasks_sync,
            "interval",
            seconds=settings.SCHEDULER_INTERVAL_SECONDS,
            id="process_scheduled_tasks",
            replace_existing=True,
            max_instances=1  # Only one instance running at a time
        )
        
        # Add job to cleanup old cards (runs daily at 2 AM)
        scheduler.add_job(
            cleanup_cards_sync,
            "cron",
            hour=2,
            minute=0,
            id="cleanup_old_cards",
            replace_existing=True,
            max_instances=1
        )
        
        # Start scheduler
        scheduler.start()
        
        # Attach to app state to prevent garbage collection
        app.state.scheduler = scheduler
        
        logger.info(
            f"Marketing scheduler started successfully "
            f"(interval: {settings.SCHEDULER_INTERVAL_SECONDS}s, daily cleanup at 2 AM)"
        )
        
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}")


def stop_scheduler(app: FastAPI) -> None:
    """
    Stop the background scheduler.
    
    Args:
        app: FastAPI application instance
    """
    if hasattr(app.state, "scheduler"):
        app.state.scheduler.shutdown()
        logger.info("Marketing scheduler stopped")
