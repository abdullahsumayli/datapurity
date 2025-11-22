"""Lead service for marketing funnel."""

import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.lead import Lead
from app.schemas.lead import LeadCreate

logger = logging.getLogger(__name__)


async def create_lead(
    db: AsyncSession,
    lead_data: LeadCreate,
    source: str = "landing_page",
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> Lead:
    """
    Create a new marketing lead.
    
    Args:
        db: Database session
        lead_data: Lead data from request
        source: Lead source (landing_page, api, etc.)
        ip_address: Client IP address
        user_agent: Client user agent string
        
    Returns:
        Created Lead instance
    """
    # Normalize phone number (basic cleaning)
    phone = lead_data.phone
    if phone:
        # Remove common separators
        phone = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    
    # Create lead instance
    lead = Lead(
        full_name=lead_data.full_name.strip(),
        email=lead_data.email.lower().strip(),
        phone=phone,
        company=lead_data.company.strip() if lead_data.company else None,
        sector=lead_data.sector.strip() if lead_data.sector else None,
        source=source,
        status="new",
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    
    logger.info(f"Created lead: {lead.email} (ID: {lead.id})")
    
    return lead


async def update_lead_status(db: AsyncSession, lead_id: int, status: str) -> Optional[Lead]:
    """
    Update lead status.
    
    Args:
        db: Database session
        lead_id: Lead ID
        status: New status (new, trial_started, trial_completed, subscribed, lost)
        
    Returns:
        Updated Lead instance or None if not found
    """
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    
    if lead:
        lead.status = status
        await db.commit()
        await db.refresh(lead)
        logger.info(f"Updated lead {lead_id} status to: {status}")
    
    return lead


async def get_lead(db: AsyncSession, lead_id: int) -> Optional[Lead]:
    """
    Get lead by ID.
    
    Args:
        db: Database session
        lead_id: Lead ID
        
    Returns:
        Lead instance if found, None otherwise
    """
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    return result.scalar_one_or_none()


async def get_lead_by_email(db: AsyncSession, email: str) -> Optional[Lead]:
    """
    Get lead by email address.
    
    Args:
        db: Database session
        email: Email to search for
        
    Returns:
        Lead instance if found, None otherwise
    """
    result = await db.execute(select(Lead).where(Lead.email == email.lower().strip()))
    return result.scalar_one_or_none()
