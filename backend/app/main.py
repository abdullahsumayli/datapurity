"""Main FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routers
app.include_router(api_router, prefix=settings.API_PREFIX)

# Static files and SPA setup
FRONTEND_DIST = Path(__file__).parent.parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    # Mount static files
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")
    
    # Check if icons directory exists before mounting
    icons_dir = FRONTEND_DIST / "icons"
    if icons_dir.exists():
        app.mount("/icons", StaticFiles(directory=str(icons_dir)), name="icons")
    
    # Serve specific files
    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        favicon_path = FRONTEND_DIST / "favicon.ico"
        if favicon_path.exists():
            return FileResponse(str(favicon_path))
        return {"error": "favicon not found"}
    
    @app.get("/robots.txt", include_in_schema=False)
    async def robots():
        robots_path = FRONTEND_DIST / "robots.txt"
        if robots_path.exists():
            return FileResponse(str(robots_path))
        return {"error": "robots.txt not found"}
    
    # Catch-all for SPA routing - MUST BE LAST
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        """Serve SPA for all non-API routes."""
        # Check if it's a file request
        file_path = FRONTEND_DIST / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        
        # Otherwise serve index.html for client-side routing
        index_path = FRONTEND_DIST / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        
        return {"error": "Frontend not built. Run: cd frontend && npm run build"}
