"""Marketing funnel endpoints."""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import create_lead, get_lead_by_email
from app.services.campaigns_service import schedule_welcome_sequence, log_campaign_event

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/leads", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def capture_lead(
    lead_data: LeadCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Capture a new marketing lead from the landing page.
    
    This endpoint accepts lead information and stores it in the database
    for follow-up by the sales team. It also schedules an automated
    welcome email sequence.
    """
    try:
        # Extract client metadata
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Check for duplicate email (optional - could be removed if duplicates are allowed)
        existing_lead = await get_lead_by_email(db, lead_data.email)
        if existing_lead:
            logger.info(f"Duplicate lead submission: {lead_data.email}")
            # Return existing lead instead of error for better UX
            return existing_lead
        
        # Create new lead
        lead = await create_lead(
            db=db,
            lead_data=lead_data,
            source="landing_page",
            ip_address=ip_address,
            user_agent=user_agent,
        )
        
        # Schedule welcome email sequence
        await schedule_welcome_sequence(db, lead)
        
        # Log event
        await log_campaign_event(
            db,
            lead_id=lead.id,
            event_type="lead_created",
            meta={"source": "landing_page"}
        )
        
        await db.commit()
        
        logger.info(f"New lead captured: {lead.email} from {ip_address}")
        
        return lead
        
    except Exception as e:
        logger.error(f"Error creating lead: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process lead submission",
        )


@router.get("/health")
async def marketing_health():
    """Health check for marketing endpoints."""
    return {"status": "ok", "service": "marketing"}
