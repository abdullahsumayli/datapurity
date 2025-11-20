"""Job tracking endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.job import JobResponse

router = APIRouter()


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """List all jobs for current user."""
    # TODO: Query jobs with pagination
    # TODO: Order by created_at desc
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="List jobs not yet implemented",
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Get job details and status."""
    # TODO: Retrieve job by ID
    # TODO: Verify ownership
    # TODO: Update status from Celery if running
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get job not yet implemented",
    )


@router.post("/{job_id}/cancel", response_model=JobResponse)
async def cancel_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Cancel a running job."""
    # TODO: Retrieve job
    # TODO: Cancel Celery task
    # TODO: Update job status
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Cancel job not yet implemented",
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Delete a job record."""
    # TODO: Verify job is not running
    # TODO: Delete job
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Delete job not yet implemented",
    )
