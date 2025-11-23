"""
Business Card OCR API endpoints using production-grade EasyOCR.
"""

import logging
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.contact import Contact
from app.services.ocr_business_cards import extract_business_card_data_from_bytes

logger = logging.getLogger(__name__)

router = APIRouter()


# =====================================================================
# PYDANTIC MODELS
# =====================================================================

class OcrMetadata(BaseModel):
    """OCR processing metadata."""
    total_lines: int = Field(..., description="Total number of lines extracted")
    avg_confidence: float = Field(..., description="Average OCR confidence (0-1)")


class BusinessCardOcrResponse(BaseModel):
    """Response model for OCR extraction."""
    full_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    other_lines: list[str] = Field(default_factory=list)
    all_lines: list[str] = Field(default_factory=list)
    metadata: Optional[OcrMetadata] = None


class ContactSavedResponse(BaseModel):
    """Response after saving contact."""
    success: bool
    contact_id: Optional[int] = None
    message: str
    extracted_data: BusinessCardOcrResponse


# =====================================================================
# ENDPOINTS
# =====================================================================

@router.post("/business-card", response_model=BusinessCardOcrResponse)
async def ocr_business_card(
    file: UploadFile = File(..., description="Business card image (JPG/PNG)")
):
    """
    Extract data from business card image using OCR.
    
    Returns structured data without saving to database.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        content = await file.read()
        
        if not content:
            raise HTTPException(status_code=400, detail="Empty file")
        
        logger.info(f"Processing business card: {file.filename}, size={len(content)} bytes")
        
        # Perform OCR extraction
        result = extract_business_card_data_from_bytes(content)
        
        # Build response
        response = BusinessCardOcrResponse(
            **result["structured"],
            all_lines=result.get("lines", []),
            metadata=OcrMetadata(**result["metadata"]) if result.get("metadata") else None
        )
        
        logger.info(f"OCR completed: {response.metadata.total_lines if response.metadata else 0} lines")
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@router.post("/business-card/save", response_model=ContactSavedResponse)
async def ocr_and_save_business_card(
    file: UploadFile = File(..., description="Business card image (JPG/PNG)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Extract data from business card and save to database.
    
    Returns extracted data and saved contact ID.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        content = await file.read()
        
        if not content:
            raise HTTPException(status_code=400, detail="Empty file")
        
        logger.info(f"Processing and saving business card: {file.filename}")
        
        # Perform OCR extraction
        result = extract_business_card_data_from_bytes(content)
        structured = result["structured"]
        
        # Create contact from extracted data
        contact = Contact(
            full_name=structured.get("full_name"),
            company=structured.get("company"),
            job_title=structured.get("job_title"),
            email=structured.get("email"),
            phone=structured.get("phone"),
            mobile=structured.get("mobile"),
            # Parse address if available
            address_line1=structured.get("address"),  # For now, store full address in line1
        )
        
        # Save to database
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        
        logger.info(f"Contact saved: ID={contact.id}, name={contact.full_name}")
        
        # Build extracted data response
        extracted_data = BusinessCardOcrResponse(
            **structured,
            all_lines=result.get("lines", []),
            metadata=OcrMetadata(**result["metadata"]) if result.get("metadata") else None
        )
        
        return ContactSavedResponse(
            success=True,
            contact_id=contact.id,
            message="Contact saved successfully",
            extracted_data=extracted_data
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save contact: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save contact: {str(e)}")
