"""
OCR API Router - Google Cloud Vision.

Provides REST endpoints for business card OCR processing
using Google Cloud Vision API.
"""

from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
import logging

from app.services.ocr_google import ocr_business_card
from app.services.business_card_parser import parse_business_card_text

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ocr", tags=["OCR"])


# Response Models
class BusinessCardData(BaseModel):
    """Extracted business card data."""
    name: str | None = None
    company: str | None = None
    job_title: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    raw_text: str = ""


class SingleCardResponse(BaseModel):
    """Response for single card OCR."""
    status: str = "success"
    data: BusinessCardData


class BatchCardItem(BaseModel):
    """Single item in batch processing response."""
    filename: str
    success: bool
    data: BusinessCardData | None = None
    error: str | None = None


class BatchCardsResponse(BaseModel):
    """Response for batch cards OCR."""
    status: str = "success"
    items: List[BatchCardItem]


# Endpoints
@router.post("/business-card", response_model=SingleCardResponse)
async def process_single_business_card(
    file: UploadFile = File(..., description="Business card image (JPG/PNG)")
) -> SingleCardResponse:
    """
    OCR single business card using Google Cloud Vision.
    
    Extracts structured contact information including:
    - Name
    - Company
    - Job title
    - Phone number
    - Email address
    - Website
    
    Args:
        file: Uploaded image file (JPEG, PNG, etc.)
        
    Returns:
        Structured business card data
        
    Raises:
        HTTPException 400: If file is not an image
        HTTPException 500: If OCR processing fails
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image (JPEG, PNG, etc.)"
        )
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty file")
        
        logger.info(
            f"Processing business card: {file.filename}, "
            f"size={len(image_bytes)} bytes"
        )
        
        # Perform OCR
        ocr_result = ocr_business_card(image_bytes)
        raw_text = ocr_result["raw_text"]
        
        # Parse extracted text
        parsed_data = parse_business_card_text(raw_text)
        
        # Build response
        card_data = BusinessCardData(**parsed_data)
        
        logger.info(f"OCR completed: {len(raw_text)} chars extracted")
        
        return SingleCardResponse(data=card_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR processing failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )


@router.post("/business-cards/batch", response_model=BatchCardsResponse)
async def process_batch_business_cards(
    files: List[UploadFile] = File(..., description="Multiple business card images")
) -> BatchCardsResponse:
    """
    OCR multiple business cards using Google Cloud Vision.
    
    Processes each card independently - failures in individual cards
    won't stop the entire batch.
    
    Args:
        files: List of uploaded image files
        
    Returns:
        List of results for each card, including success/failure status
        
    Note:
        Invalid files or processing errors are captured per-item
        and don't halt the entire batch operation.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    logger.info(f"Processing batch of {len(files)} business cards")
    
    results = []
    
    for file in files:
        item = BatchCardItem(
            filename=file.filename or "unknown",
            success=False
        )
        
        try:
            # Validate file type
            if not file.content_type or not file.content_type.startswith("image/"):
                item.error = "File is not an image"
                results.append(item)
                continue
            
            # Read image bytes
            image_bytes = await file.read()
            
            if not image_bytes:
                item.error = "Empty file"
                results.append(item)
                continue
            
            # Perform OCR
            ocr_result = ocr_business_card(image_bytes)
            raw_text = ocr_result["raw_text"]
            
            # Parse extracted text
            parsed_data = parse_business_card_text(raw_text)
            
            # Success
            item.success = True
            item.data = BusinessCardData(**parsed_data)
            
        except Exception as e:
            logger.error(
                f"Failed to process {file.filename}: {str(e)}",
                exc_info=True
            )
            item.error = str(e)
        
        results.append(item)
    
    # Count successes
    success_count = sum(1 for item in results if item.success)
    
    logger.info(
        f"Batch processing completed: {success_count}/{len(files)} successful"
    )
    
    return BatchCardsResponse(items=results)
