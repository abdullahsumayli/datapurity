"""Export model for data export jobs."""

from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum

from sqlalchemy import String, Integer, DateTime, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ExportFormat(str, PyEnum):
    """Export format enumeration."""

    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    VCARD = "vcard"


class ExportStatus(str, PyEnum):
    """Export status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Export(Base):
    """Data export model."""

    __tablename__ = "exports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)  # TODO: Add ForeignKey
    dataset_id: Mapped[Optional[int]] = mapped_column(Integer)  # TODO: Add ForeignKey
    
    # Export configuration
    format: Mapped[ExportFormat] = mapped_column(Enum(ExportFormat), nullable=False)
    status: Mapped[ExportStatus] = mapped_column(Enum(ExportStatus), default=ExportStatus.PENDING)
    
    # Filters and options
    filters: Mapped[Optional[dict]] = mapped_column(JSON)  # Query filters applied
    options: Mapped[Optional[dict]] = mapped_column(JSON)  # Export-specific options
    
    # Result
    file_path: Mapped[Optional[str]] = mapped_column(String(512))  # S3 key or file path
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    record_count: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Download tracking
    download_url: Mapped[Optional[str]] = mapped_column(String(512))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # TODO: Add relationships
    # user: Mapped["User"] = relationship(back_populates="exports")
    # dataset: Mapped["Dataset"] = relationship(back_populates="exports")
