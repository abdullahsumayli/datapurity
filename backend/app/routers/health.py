"""Health check endpoints."""

from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "datapurity-api",
    }


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """Readiness check - verify all dependencies are available."""
    # TODO: Check database connection
    # TODO: Check Redis connection
    # TODO: Check S3 access
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": "ok",  # TODO: implement actual check
            "redis": "ok",  # TODO: implement actual check
            "storage": "ok",  # TODO: implement actual check
        },
    }
