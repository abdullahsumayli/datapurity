"""Scheduled task model for marketing automation."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ScheduledTask(Base):
    """Scheduled task model for background processing."""

    __tablename__ = "scheduled_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Task details
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("leads.id"), index=True)
    task_type: Mapped[str] = mapped_column(String(50))  # send_email, send_whatsapp, etc.
    payload: Mapped[dict] = mapped_column(JSON)  # template_name, context, etc.
    
    # Scheduling
    run_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)  # pending, done, failed
    
    # Error tracking
    error_message: Mapped[Optional[str]] = mapped_column(String(500))
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
