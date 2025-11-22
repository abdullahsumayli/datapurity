"""Lead model for marketing funnel."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Lead(Base):
    """Marketing lead model."""

    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Lead information
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    company: Mapped[Optional[str]] = mapped_column(String(255))
    sector: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Metadata
    source: Mapped[str] = mapped_column(String(50), default="landing_page")
    status: Mapped[str] = mapped_column(String(50), default="new")  # new, trial_started, trial_completed, subscribed, lost
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
