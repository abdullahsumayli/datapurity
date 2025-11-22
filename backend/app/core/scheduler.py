"""Background scheduler for processing marketing automation tasks."""

import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from sqlalchemy import select, text

from app.core.settings import get_settings
from app.db.session import AsyncSessionLocal
from app.models.scheduled_task import ScheduledTask
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
        
        # Add job to process tasks
        scheduler.add_job(
            process_tasks_sync,
            "interval",
            seconds=settings.SCHEDULER_INTERVAL_SECONDS,
            id="process_scheduled_tasks",
            replace_existing=True,
            max_instances=1  # Only one instance running at a time
        )
        
        # Start scheduler
        scheduler.start()
        
        # Attach to app state to prevent garbage collection
        app.state.scheduler = scheduler
        
        logger.info(
            f"Marketing scheduler started successfully "
            f"(interval: {settings.SCHEDULER_INTERVAL_SECONDS}s)"
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
