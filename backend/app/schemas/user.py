"""User schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""

    password: str


class UserUpdate(BaseModel):
    """User update schema."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """User in database schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserResponse(UserBase):
    """User response schema (public) with statistics."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    total_contacts: int = 0
    total_jobs: int = 0


class AdminUserResponse(UserBase):
    """Admin user response with full details."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    total_contacts: int = 0
    total_jobs: int = 0


class AdminStatsResponse(BaseModel):
    """Admin dashboard statistics."""

    total_users: int
    active_users: int
    total_contacts: int
    total_jobs: int
    completed_jobs: int


class ChangePlanRequest(BaseModel):
    """Request to change user's subscription plan."""

    plan: str  # e.g., "free", "pro", "enterprise"
