"""Dataset model for uploaded data files."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Dataset(Base):
    """Uploaded dataset model."""

    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)  # TODO: Add ForeignKey
    
    # File information
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer)  # in bytes
    storage_path: Mapped[str] = mapped_column(String(512))  # S3 key or file path
    
    # Data statistics
    row_count: Mapped[Optional[int]] = mapped_column(Integer)
    column_count: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Processing status
    is_processed: Mapped[bool] = mapped_column(default=False)
    health_score: Mapped[Optional[float]] = mapped_column(Float)  # 0.0-100.0
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)

    # TODO: Add relationships
    # owner: Mapped["User"] = relationship(back_populates="datasets")
    # contacts: Mapped[List["Contact"]] = relationship(back_populates="dataset")
