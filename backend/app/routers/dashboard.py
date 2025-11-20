"""Dashboard statistics router."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.db.session import get_db
from app.models.contact import Contact
from app.models.job import Job
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard statistics for the current user."""
    
    # Total contacts for this user
    total_contacts_query = select(func.count(Contact.id)).where(
        Contact.user_id == current_user.id
    )
    total_contacts_result = await db.execute(total_contacts_query)
    total_contacts = total_contacts_result.scalar() or 0
    
    # Cleaned contacts (assuming there's a status field or is_cleaned field)
    # For now, we'll count all contacts as cleaned
    cleaned_contacts = total_contacts
    
    # Pending jobs
    pending_jobs_query = select(func.count(Job.id)).where(
        Job.user_id == current_user.id,
        Job.status.in_(["pending", "processing"])
    )
    pending_jobs_result = await db.execute(pending_jobs_query)
    pending_jobs = pending_jobs_result.scalar() or 0
    
    # Success rate calculation
    completed_jobs_query = select(func.count(Job.id)).where(
        Job.user_id == current_user.id,
        Job.status == "completed"
    )
    completed_jobs_result = await db.execute(completed_jobs_query)
    completed_jobs = completed_jobs_result.scalar() or 0
    
    total_jobs_query = select(func.count(Job.id)).where(
        Job.user_id == current_user.id
    )
    total_jobs_result = await db.execute(total_jobs_query)
    total_jobs = total_jobs_result.scalar() or 0
    
    success_rate = (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0
    
    return {
        "total_contacts": total_contacts,
        "cleaned_contacts": cleaned_contacts,
        "pending_jobs": pending_jobs,
        "success_rate": round(success_rate, 1)
    }
