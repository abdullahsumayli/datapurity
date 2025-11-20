"""Dataset schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class DatasetBase(BaseModel):
    """Base dataset schema."""

    name: str


class DatasetCreate(DatasetBase):
    """Dataset creation schema."""

    original_filename: str
    file_size: int
    storage_path: str


class DatasetUpdate(BaseModel):
    """Dataset update schema."""

    name: Optional[str] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    is_processed: Optional[bool] = None
    health_score: Optional[float] = None


class DatasetResponse(DatasetBase):
    """Dataset response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    original_filename: str
    file_size: int
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    is_processed: bool
    health_score: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class DatasetStats(BaseModel):
    """Dataset statistics schema."""

    total_records: int
    valid_emails: int
    valid_phones: int
    duplicates: int
    average_quality_score: float
