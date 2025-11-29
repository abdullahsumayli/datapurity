"""Main FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi import UploadFile, File, HTTPException
from google.cloud import vision
from app.utils.business_card_parser import detect_language, parse_business_card

from app.core.settings import get_settings
# Scheduler disabled - requires marketing features (ScheduledTask model)
# from app.core.scheduler import start_scheduler, stop_scheduler
from app.routers import api_router, ocr

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
)

# إضافة مسار صريح لخدمة test-auth.html مباشرة بعد تعريف app
FRONTEND_DIST = Path(__file__).parent.parent.parent / "frontend" / "dist"

@app.get("/test-auth.html", include_in_schema=False)
async def test_auth():
    test_auth_path = FRONTEND_DIST / "test-auth.html"
    if test_auth_path.exists():
        return FileResponse(str(test_auth_path))
    return {"error": "test-auth.html not found"}

# Startup/shutdown events disabled - scheduler requires marketing features
# @app.on_event("startup")
# async def startup_event():
#     """Initialize scheduler on startup."""
#     start_scheduler(app)

# @app.on_event("shutdown")
# async def shutdown_event():
#     """Stop scheduler on shutdown."""
#     stop_scheduler(app)

# Session middleware (required for OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET,  # Use same secret as JWT
    session_cookie="datapurity_session",
    max_age=3600,  # 1 hour
    same_site="lax",
    https_only=True,  # Enable in production with HTTPS
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aidotoo.com",
        "https://www.aidotoo.com",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include all API routers
app.include_router(api_router, prefix=settings.API_PREFIX)
app.include_router(ocr.router)


# Compatibility endpoint: legacy clients posting to /api/v1/cards/ocr
@app.post(f"{settings.API_PREFIX}/cards/ocr")
async def legacy_cards_ocr(file: UploadFile = File(...)):
    """Compatibility endpoint that mirrors the old `/api/v1/cards/ocr` behavior.

    This runs the same OCR -> parse flow and returns the same JSON shape.
    """
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if getattr(response, "error", None) and getattr(response.error, "message", None):
        raise HTTPException(status_code=500, detail=response.error.message)

    full_text = response.full_text_annotation.text or ""
    language = detect_language(full_text)
    fields = parse_business_card(full_text)

    return {"raw_text": full_text, "language": language, "fields": fields}

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

    @app.get("/test-auth.html", include_in_schema=False)
    async def test_auth():
        test_auth_path = FRONTEND_DIST / "test-auth.html"
        if test_auth_path.exists():
            return FileResponse(str(test_auth_path))
        return {"error": "test-auth.html not found"}
    
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
    
    # SPA catch-all - serve React app for all non-API routes
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        """Serve React SPA for all routes."""
        index_path = FRONTEND_DIST / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"error": "Frontend not built"}
