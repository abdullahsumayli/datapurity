"""Job schemas."""

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict

from app.models.job import JobStatus, JobType


class JobBase(BaseModel):
    """Base job schema."""

    job_type: JobType


class JobCreate(JobBase):
    """Job creation schema."""

    pass


class JobUpdate(BaseModel):
    """Job update schema."""

    status: Optional[JobStatus] = None
    progress: Optional[int] = None
    result: Optional[dict[str, Any]] = None


class JobResponse(JobBase):
    """Job response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: JobStatus
    progress: int
    total_items: Optional[int] = None
    processed_items: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
