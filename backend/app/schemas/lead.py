"""Lead schemas for marketing funnel."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class LeadBase(BaseModel):
    """Base lead schema."""

    full_name: str = Field(..., min_length=1, max_length=255, description="Full name of the lead")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    sector: Optional[str] = Field(None, max_length=100, description="Industry sector")


class LeadCreate(LeadBase):
    """Lead creation schema for API requests."""

    pass


class LeadResponse(LeadBase):
    """Lead response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
