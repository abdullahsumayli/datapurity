"""Contact model for cleaned contact records."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Contact(Base):
    """Cleaned contact record model."""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    dataset_id: Mapped[int] = mapped_column(Integer, index=True)  # TODO: Add ForeignKey
    
    # Contact information
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    company: Mapped[Optional[str]] = mapped_column(String(255))
    job_title: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Contact details
    email: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    mobile: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Address
    address_line1: Mapped[Optional[str]] = mapped_column(String(255))
    address_line2: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    state: Mapped[Optional[str]] = mapped_column(String(100))
    postal_code: Mapped[Optional[str]] = mapped_column(String(20))
    country: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Data quality scores
    email_valid: Mapped[Optional[bool]] = mapped_column(Boolean)
    phone_valid: Mapped[Optional[bool]] = mapped_column(Boolean)
    overall_quality_score: Mapped[Optional[float]] = mapped_column(Float)  # 0.0-100.0
    
    # Flags
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False)
    duplicate_of_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)

    # TODO: Add relationships
    # dataset: Mapped["Dataset"] = relationship(back_populates="contacts")
