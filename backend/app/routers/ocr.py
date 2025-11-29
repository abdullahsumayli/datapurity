"""OCR router wired to Google Cloud Vision for business cards."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from google.cloud import vision
from app.utils.business_card_parser import (
    detect_language,
    parse_business_card,
)

router = APIRouter(prefix="/api/v1/ocr", tags=["ocr"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/card")
async def ocr_business_card(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Process a single business card image using Google Cloud Vision."""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise HTTPException(status_code=500, detail=response.error.message)

    full_text = response.full_text_annotation.text or ""
    language = detect_language(full_text)
    fields = parse_business_card(full_text)

    return {
        "raw_text": full_text,
        "language": language,
        "fields": fields,
    }


# Compatibility router: legacy clients expecting `/api/v1/cards/ocr`
# This router is included into the global `api_router` which already has
# the `/api/v1` prefix, so keep this router un-prefixed to avoid doubling.
compat_router = APIRouter()


@compat_router.post("/cards/ocr")
async def legacy_cards_ocr(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Legacy compatibility endpoint that proxies to the same OCR logic.

    Returns the same JSON shape as the main `/card` endpoint.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise HTTPException(status_code=500, detail=response.error.message)

    full_text = response.full_text_annotation.text or ""
    language = detect_language(full_text)
    fields = parse_business_card(full_text)

    return {
        "raw_text": full_text,
        "language": language,
        "fields": fields,
    }
