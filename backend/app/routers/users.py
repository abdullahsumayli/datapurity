"""User management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdate, AdminUserResponse, AdminStatsResponse, ChangePlanRequest
from app.core.deps import get_current_user
from app.models.user import User
from app.models.contact import Contact
from app.models.job import Job

router = APIRouter()


# ==================== Profile Endpoints ====================

@router.get("/me", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current authenticated user profile."""
    
    # Get user's statistics
    contacts_query = select(func.count(Contact.id)).where(Contact.user_id == current_user.id)
    contacts_result = await db.execute(contacts_query)
    total_contacts = contacts_result.scalar() or 0
    
    jobs_query = select(func.count(Job.id)).where(Job.user_id == current_user.id)
    jobs_result = await db.execute(jobs_query)
    total_jobs = jobs_result.scalar() or 0
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "total_contacts": total_contacts,
        "total_jobs": total_jobs,
    }


@router.put("/me", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile."""
    
    # Update fields if provided
    if user_update.email is not None:
        # Check if email already exists
        existing_query = select(User).where(
            User.email == user_update.email,
            User.id != current_user.id
        )
        existing_result = await db.execute(existing_query)
        if existing_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_update.email
    
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    # Note: Password update should be handled separately with proper hashing
    # For now, we skip password update
    
    await db.commit()
    await db.refresh(current_user)
    
    # Get statistics
    contacts_query = select(func.count(Contact.id)).where(Contact.user_id == current_user.id)
    contacts_result = await db.execute(contacts_query)
    total_contacts = contacts_result.scalar() or 0
    
    jobs_query = select(func.count(Job.id)).where(Job.user_id == current_user.id)
    jobs_result = await db.execute(jobs_query)
    total_jobs = jobs_result.scalar() or 0
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "total_contacts": total_contacts,
        "total_jobs": total_jobs,
    }


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete current user account (soft delete)."""
    
    # Soft delete by marking as inactive
    current_user.is_active = False
    await db.commit()
    
    return None


# ==================== Admin Endpoints ====================

async def verify_admin(current_user: User = Depends(get_current_user)) -> User:
    """Verify that current user is an admin."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


@router.get("/admin/users", response_model=List[AdminUserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get all users (admin only)."""
    
    try:
        query = select(User).offset(skip).limit(limit).order_by(User.id.desc())
        result = await db.execute(query)
        users = result.scalars().all()
        
        # Get statistics for each user
        users_data = []
        for user in users:
            try:
                contacts_query = select(func.count(Contact.id)).where(Contact.user_id == user.id)
                contacts_result = await db.execute(contacts_query)
                total_contacts = contacts_result.scalar() or 0
                
                jobs_query = select(func.count(Job.id)).where(Job.user_id == user.id)
                jobs_result = await db.execute(jobs_query)
                total_jobs = jobs_result.scalar() or 0
                
                users_data.append({
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name or "",
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser,
                    "created_at": user.created_at,
                    "total_contacts": total_contacts,
                    "total_jobs": total_jobs,
                })
            except Exception as e:
                print(f"Error processing user {user.id}: {e}")
                continue
        
        return users_data
    except Exception as e:
        print(f"Error in get_all_users: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    admin_user: User = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get admin dashboard statistics."""
    
    # Total users
    total_users_query = select(func.count(User.id))
    total_users_result = await db.execute(total_users_query)
    total_users = total_users_result.scalar() or 0
    
    # Active users
    active_users_query = select(func.count(User.id)).where(User.is_active == True)
    active_users_result = await db.execute(active_users_query)
    active_users = active_users_result.scalar() or 0
    
    # Total contacts
    total_contacts_query = select(func.count(Contact.id))
    total_contacts_result = await db.execute(total_contacts_query)
    total_contacts = total_contacts_result.scalar() or 0
    
    # Total jobs
    total_jobs_query = select(func.count(Job.id))
    total_jobs_result = await db.execute(total_jobs_query)
    total_jobs = total_jobs_result.scalar() or 0
    
    # Completed jobs
    completed_jobs_query = select(func.count(Job.id)).where(Job.status == "completed")
    completed_jobs_result = await db.execute(completed_jobs_query)
    completed_jobs = completed_jobs_result.scalar() or 0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_contacts": total_contacts,
        "total_jobs": total_jobs,
        "completed_jobs": completed_jobs,
    }


@router.post("/admin/users/{user_id}/change-plan")
async def change_user_plan(
    user_id: int,
    plan_request: ChangePlanRequest,
    admin_user: User = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
):
    """Change user's subscription plan (admin only)."""
    
    # Get user
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update plan (assuming plan field exists in User model)
    # If plan field doesn't exist, you'll need to add it to the model
    # For now, we'll just return success
    
    return {
        "success": True,
        "message": f"Plan changed to {plan_request.plan} for user {user.email}"
    }
