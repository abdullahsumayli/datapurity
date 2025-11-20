"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency from JWT token
):
    """Get current authenticated user."""
    # TODO: Return current user from JWT token
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get current user not yet implemented",
    )


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Update current user profile."""
    # TODO: Update user fields
    # TODO: Hash password if provided
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Update user not yet implemented",
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Delete current user account."""
    # TODO: Soft delete or hard delete user
    # TODO: Delete all associated data
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Delete user not yet implemented",
    )
