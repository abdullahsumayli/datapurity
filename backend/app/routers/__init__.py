"""API routers package."""

from fastapi import APIRouter

from app.routers import (
    auth,
    users,
    datasets,
    jobs,
    cards,
    contacts,
    exports,
    health,
    dashboard,
    billing,
    marketing,
)

api_router = APIRouter()

# Include all routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(cards.router, prefix="/cards", tags=["cards"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(exports.router, prefix="/exports", tags=["exports"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(marketing.router, prefix="/marketing", tags=["marketing"])
