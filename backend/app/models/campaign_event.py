"""Campaign event model for tracking marketing activities."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CampaignEvent(Base):
    """Campaign event tracking model."""

    __tablename__ = "campaign_events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Event details
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("leads.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)  # email_sent, trial_started, trial_completed, etc.
    meta: Mapped[Optional[dict]] = mapped_column(JSON)  # Additional metadata
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
