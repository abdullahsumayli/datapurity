"""Job model for tracking background processing tasks."""

from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum

from sqlalchemy import String, Integer, DateTime, Enum, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JobStatus(str, PyEnum):
    """Job status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobType(str, PyEnum):
    """Job type enumeration."""

    DATASET_CLEANING = "dataset_cleaning"
    CARD_OCR = "card_ocr"
    EXPORT_GENERATION = "export_generation"
    BATCH_VALIDATION = "batch_validation"


class Job(Base):
    """Background job tracking model."""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)  # TODO: Add ForeignKey
    job_type: Mapped[JobType] = mapped_column(Enum(JobType), nullable=False)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.PENDING)
    
    # Task tracking
    celery_task_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)  # 0-100
    total_items: Mapped[Optional[int]] = mapped_column(Integer)
    processed_items: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    
    # Results and errors
    result: Mapped[Optional[dict]] = mapped_column(JSON)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # TODO: Add relationships
    # user: Mapped["User"] = relationship(back_populates="jobs")
