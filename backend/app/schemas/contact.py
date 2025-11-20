"""Contact schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class ContactBase(BaseModel):
    """Base contact schema."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ContactCreate(ContactBase):
    """Contact creation schema."""

    dataset_id: int


class ContactUpdate(BaseModel):
    """Contact update schema."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class ContactResponse(ContactBase):
    """Contact response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_id: int
    job_title: Optional[str] = None
    mobile: Optional[str] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    email_valid: Optional[bool] = None
    phone_valid: Optional[bool] = None
    overall_quality_score: Optional[float] = None
    is_duplicate: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
