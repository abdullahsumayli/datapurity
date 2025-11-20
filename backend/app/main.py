"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import get_settings
from app.routers import api_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    # TODO: Initialize database connection pool
    # TODO: Initialize Redis connection
    # TODO: Initialize S3 client
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    # TODO: Close database connections
    # TODO: Close Redis connections
    pass
