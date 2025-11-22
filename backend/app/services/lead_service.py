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
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> Lead:
    """
    Create a new marketing lead.
    
    Args:
        db: Database session
        lead_data: Lead data from request
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
        source="landing_page",
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    
    logger.info(f"Created lead: {lead.email} (ID: {lead.id})")
    
    return lead


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
