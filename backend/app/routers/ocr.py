"""OCR router wired to Google Cloud Vision for business cards."""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from google.cloud import vision
from app.utils.business_card_parser import (
    detect_language,
    parse_business_card,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ocr", tags=["ocr"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/card")
async def ocr_business_card(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Process a single business card image using Google Cloud Vision."""
    logger.info(f"OCR request received: filename={file.filename}, content_type={file.content_type}")
    
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        logger.warning(f"Rejected unsupported content type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Unsupported image type")

    content = await file.read()
    content_size = len(content)
    logger.info(f"File read: size={content_size} bytes")
    
    if not content:
        logger.error("Empty file received")
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content)
        logger.info("Calling Google Vision API with language hints [ar, en]...")
        response = client.text_detection(
            image=image,
            image_context=vision.ImageContext(language_hints=["ar", "en"]),
        )
        logger.info(f"Vision API responded: error={bool(response.error.message)}")

        if response.error.message:
            logger.error(f"Vision API error: {response.error.message}")
            raise HTTPException(status_code=500, detail=response.error.message)

        full_text = response.full_text_annotation.text or ""
        text_length = len(full_text)
        logger.info(f"Extracted text length: {text_length} chars")
        
        language = detect_language(full_text)
        fields = parse_business_card(full_text)
        
        logger.info(f"OCR completed: lang={language}, fields_extracted={len([k for k, v in fields.items() if v])}")
        
        return {
            "raw_text": full_text,
            "language": language,
            "fields": fields,
        }
    except Exception as e:
        logger.exception(f"OCR processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


# Legacy endpoint `/api/v1/cards/ocr` has been removed. Use `/api/v1/ocr/card`.
