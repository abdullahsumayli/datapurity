"""Campaign and marketing automation service."""

import logging
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.models.scheduled_task import ScheduledTask
from app.models.campaign_event import CampaignEvent

logger = logging.getLogger(__name__)


async def schedule_welcome_sequence(db: AsyncSession, lead: Lead) -> None:
    """
    Schedule welcome email sequence for a new lead.
    
    Args:
        db: Database session
        lead: Lead instance
    """
    now = datetime.utcnow()
    
    # Define the email sequence
    tasks = [
        {
            "run_at": now,  # Immediate
            "template": "welcome_0",
            "description": "Welcome email"
        },
        {
            "run_at": now + timedelta(days=1),
            "template": "trial_reminder_1",
            "description": "Trial reminder (Day 1)"
        },
        {
            "run_at": now + timedelta(days=3),
            "template": "case_study_3",
            "description": "Case study (Day 3)"
        },
        {
            "run_at": now + timedelta(days=7),
            "template": "discount_push_7",
            "description": "Discount offer (Day 7)"
        },
    ]
    
    # Create scheduled tasks
    for task_config in tasks:
        task = ScheduledTask(
            lead_id=lead.id,
            task_type="send_email",
            payload={
                "template": task_config["template"],
                "to": lead.email,
                "lead_name": lead.full_name,
            },
            run_at=task_config["run_at"],
            status="pending"
        )
        db.add(task)
    
    await db.flush()
    logger.info(f"Scheduled {len(tasks)} emails for lead {lead.id} ({lead.email})")


async def schedule_trial_followup_sequence(db: AsyncSession, lead: Lead) -> None:
    """
    Schedule follow-up emails after trial completion.
    
    Args:
        db: Database session
        lead: Lead instance
    """
    now = datetime.utcnow()
    
    # Additional follow-up after trial
    tasks = [
        {
            "run_at": now + timedelta(hours=2),
            "template": "discount_push_7",  # Reuse discount template
            "description": "Post-trial offer"
        },
    ]
    
    for task_config in tasks:
        task = ScheduledTask(
            lead_id=lead.id,
            task_type="send_email",
            payload={
                "template": task_config["template"],
                "to": lead.email,
                "lead_name": lead.full_name,
            },
            run_at=task_config["run_at"],
            status="pending"
        )
        db.add(task)
    
    await db.flush()
    logger.info(f"Scheduled trial follow-up for lead {lead.id}")


async def log_campaign_event(
    db: AsyncSession,
    lead_id: int,
    event_type: str,
    meta: dict | None = None
) -> CampaignEvent:
    """
    Log a campaign event.
    
    Args:
        db: Database session
        lead_id: Lead ID
        event_type: Event type (email_sent, trial_started, etc.)
        meta: Additional metadata
        
    Returns:
        Created CampaignEvent instance
    """
    event = CampaignEvent(
        lead_id=lead_id,
        event_type=event_type,
        meta=meta or {}
    )
    db.add(event)
    await db.flush()
    
    logger.info(f"Logged campaign event: {event_type} for lead {lead_id}")
    return event
