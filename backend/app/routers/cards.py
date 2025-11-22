"""Business card OCR endpoints."""

from typing import List
from pathlib import Path
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.card import CardResponse, CardUpdate
from app.services.business_card_ocr import BusinessCardProcessor

router = APIRouter()


@router.post("/ocr", status_code=status.HTTP_200_OK)
async def ocr_business_cards(
    files: List[UploadFile] = File(...)
):
    """
    Process multiple business card images with OCR.
    
    This endpoint:
    1. Accepts multiple image files (JPG, PNG)
    2. Saves them temporarily
    3. Processes them with Tesseract OCR
    4. Extracts structured data (name, company, phone, email, etc.)
    5. Returns results as JSON
    
    No authentication required for OCR processing.
    Future enhancement: Save results to database contacts table.
    """
    # Create temp directory for uploaded files
    temp_dir = Path("tmp/cards")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Save uploaded files
    saved_paths = []
    try:
        for file in files:
            # Validate file type
            if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid file type: {file.filename}. Only JPG and PNG are supported."
                )
            
            # Save file
            file_path = temp_dir / file.filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            saved_paths.append(file_path)
        
        # Process with OCR
        processor = BusinessCardProcessor(saved_paths)
        df = processor.run(dedupe=True)
        
        # Convert to dict for JSON response
        records = df.to_dict(orient="records")
        
        return {
            "success": True,
            "count": len(records),
            "records": records,
            "message": f"Successfully processed {len(records)} business cards"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OCR processing failed: {str(e)}"
        )
    
    finally:
        # Cleanup: remove temporary files
        for path in saved_paths:
            try:
                if path.exists():
                    path.unlink()
            except Exception:
                pass


@router.post("/upload", response_model=List[CardResponse], status_code=status.HTTP_201_CREATED)
async def upload_card(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload business card images for OCR."""
    from datetime import datetime
    import random
    
    # Process all uploaded files
    results = []
    
    for idx, file in enumerate(files):
        # Mock OCR processing - في الإنتاج سيتم معالجة الصور واستخراج البيانات
        # يمكن استخدام Tesseract OCR أو Google Vision API هنا
        
        # Generate mock extracted data
        card_data = {
            "id": idx + 1,
            "user_id": current_user.id,
            "original_filename": file.filename,
            "storage_path": f"/uploads/cards/{file.filename}",
            "ocr_text": None,
            "ocr_confidence": round(85 + random.random() * 15, 1),
            "extracted_name": f"جهة اتصال {idx + 1}",
            "extracted_company": f"شركة {idx + 1}",
            "extracted_phone": f"+966 50 123 {str(1000 + idx).zfill(4)}",
            "extracted_email": f"contact{idx + 1}@company.com",
            "extracted_address": "الرياض، المملكة العربية السعودية",
            "is_processed": True,
            "is_reviewed": False,
            "created_at": datetime.now(),
            "updated_at": None
        }
        results.append(card_data)
    
    return results


@router.get("/", response_model=List[CardResponse])
async def list_cards(
    skip: int = 0,
    limit: int = 100,
    reviewed: bool = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all business cards."""
    from datetime import datetime
    # Mock data
    cards = [
        {
            "id": 1,
            "user_id": current_user.id,
            "original_filename": "card1.jpg",
            "storage_path": "/uploads/cards/card1.jpg",
            "ocr_text": None,
            "ocr_confidence": None,
            "extracted_name": "أحمد محمد",
            "extracted_company": "شركة التقنية",
            "extracted_phone": "+966501234567",
            "extracted_email": "ahmed@tech.com",
            "extracted_address": None,
            "is_processed": True,
            "is_reviewed": False,
            "created_at": datetime.now(),
            "updated_at": None
        },
        {
            "id": 2,
            "user_id": current_user.id,
            "original_filename": "card2.jpg",
            "storage_path": "/uploads/cards/card2.jpg",
            "ocr_text": None,
            "ocr_confidence": None,
            "extracted_name": "سارة علي",
            "extracted_company": "شركة التسويق",
            "extracted_phone": "+966507654321",
            "extracted_email": "sara@marketing.com",
            "extracted_address": None,
            "is_processed": True,
            "is_reviewed": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
    ]
    
    if reviewed is not None:
        cards = [c for c in cards if c["is_reviewed"] == reviewed]
    
    return cards[skip:skip + limit]


@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get card details."""
    from datetime import datetime
    # Mock data
    return {
        "id": int(card_id),
        "user_id": current_user.id,
        "original_filename": f"card{card_id}.jpg",
        "storage_path": f"/uploads/cards/card{card_id}.jpg",
        "ocr_text": None,
        "ocr_confidence": None,
        "extracted_name": "أحمد محمد",
        "extracted_company": "شركة التقنية",
        "extracted_phone": "+966501234567",
        "extracted_email": "ahmed@tech.com",
        "extracted_address": "الرياض، المملكة العربية السعودية",
        "is_processed": True,
        "is_reviewed": False,
        "created_at": datetime.now(),
        "updated_at": None
    }


@router.put("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: str,
    card_update: CardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update extracted card data (manual correction)."""
    from datetime import datetime
    # Mock response - تحديث البيانات
    return {
        "id": int(card_id),
        "user_id": current_user.id,
        "original_filename": f"card{card_id}.jpg",
        "storage_path": f"/uploads/cards/card{card_id}.jpg",
        "ocr_text": None,
        "ocr_confidence": None,
        "extracted_name": card_update.extracted_name,
        "extracted_company": card_update.extracted_company,
        "extracted_phone": card_update.extracted_phone,
        "extracted_email": card_update.extracted_email,
        "extracted_address": card_update.extracted_address,
        "is_processed": True,
        "is_reviewed": card_update.is_reviewed if card_update.is_reviewed is not None else False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a card."""
    # Mock - في الإنتاج سيتم حذف الملف والسجل
    return None
