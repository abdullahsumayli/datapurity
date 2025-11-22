"""Main FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from app.core.settings import get_settings
from app.core.scheduler import start_scheduler, stop_scheduler
from app.routers import api_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize scheduler on startup."""
    start_scheduler(app)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Stop scheduler on shutdown."""
    stop_scheduler(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://46.62.239.119",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
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
    
    @app.get("/manifest.json", include_in_schema=False)
    async def manifest():
        manifest_path = FRONTEND_DIST / "manifest.json"
        if manifest_path.exists():
            return FileResponse(str(manifest_path))
        return {"error": "manifest.json not found"}
    
    @app.get("/registerSW.js", include_in_schema=False)
    async def register_sw():
        sw_path = FRONTEND_DIST / "registerSW.js"
        if sw_path.exists():
            return FileResponse(str(sw_path))
        return {"error": "registerSW.js not found"}
    
    # SPA catch-all - only for root and app routes
    @app.get("/", include_in_schema=False)
    async def root():
        """Serve landing page for marketing funnel."""
        landing_page = Path(__file__).parent / "templates" / "landing.html"
        if landing_page.exists():
            return HTMLResponse(content=landing_page.read_text(encoding="utf-8"))
        # Fallback to React SPA if landing page doesn't exist
        index_path = FRONTEND_DIST / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"error": "Frontend not built"}
    
    @app.get("/app/{full_path:path}", include_in_schema=False)
    async def serve_app(full_path: str):
        """Serve SPA for /app/* routes."""
        index_path = FRONTEND_DIST / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"error": "Frontend not built"}
