"""Billing schemas."""

from datetime import datetime
from pydantic import BaseModel


class UsageInfo(BaseModel):
    """Usage information."""
    contacts: int
    limit: int


class SubscriptionResponse(BaseModel):
    """Subscription response."""
    plan: str
    status: str
    current_period_end: datetime
    usage: UsageInfo

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    """Invoice response."""
    id: str
    amount: float
    status: str
    date: datetime
    invoice_url: str

    class Config:
        from_attributes = True
