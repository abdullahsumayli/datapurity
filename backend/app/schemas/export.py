"""Export schemas."""

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict

from app.models.export import ExportFormat, ExportStatus


class ExportBase(BaseModel):
    """Base export schema."""

    format: ExportFormat


class ExportCreate(ExportBase):
    """Export creation schema."""

    dataset_id: Optional[int] = None
    filters: Optional[dict[str, Any]] = None
    options: Optional[dict[str, Any]] = None


class ExportResponse(ExportBase):
    """Export response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    dataset_id: Optional[int] = None
    status: ExportStatus
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    record_count: Optional[int] = None
    download_url: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
