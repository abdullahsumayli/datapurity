"""Card model for business card OCR processing."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Card(Base):
    """Business card OCR model."""

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)  # TODO: Add ForeignKey
    
    # Image information
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(512))  # S3 key or file path
    file_size: Mapped[int] = mapped_column(Integer)
    
    # OCR extracted data (raw)
    ocr_text: Mapped[Optional[str]] = mapped_column(Text)
    ocr_confidence: Mapped[Optional[float]] = mapped_column()
    
    # Parsed structured data
    extracted_name: Mapped[Optional[str]] = mapped_column(String(255))
    extracted_company: Mapped[Optional[str]] = mapped_column(String(255))
    extracted_phone: Mapped[Optional[str]] = mapped_column(String(50))
    extracted_email: Mapped[Optional[str]] = mapped_column(String(255))
    extracted_address: Mapped[Optional[str]] = mapped_column(Text)
    
    # Processing status
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)

    # TODO: Add relationships
    # user: Mapped["User"] = relationship(back_populates="cards")
