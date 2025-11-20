"""Business card OCR endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.card import CardResponse, CardUpdate

router = APIRouter()


@router.post("/upload", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def upload_card(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload business card images for OCR."""
    # Mock response - في الإنتاج سيتم معالجة الصور واستخراج البيانات
    return {
        "id": "1",
        "image_url": "/uploads/cards/sample.jpg",
        "extracted_data": {
            "name": "أحمد محمد",
            "title": "مدير تقني",
            "company": "شركة التقنية",
            "email": "ahmed@tech.com",
            "phone": "+966501234567"
        },
        "reviewed": False
    }


@router.get("/", response_model=List[CardResponse])
async def list_cards(
    skip: int = 0,
    limit: int = 100,
    reviewed: bool = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all business cards."""
    # Mock data
    cards = [
        {
            "id": "1",
            "image_url": "/uploads/cards/card1.jpg",
            "extracted_data": {
                "name": "أحمد محمد",
                "title": "مدير تقني",
                "company": "شركة التقنية",
                "email": "ahmed@tech.com",
                "phone": "+966501234567"
            },
            "reviewed": False
        },
        {
            "id": "2",
            "image_url": "/uploads/cards/card2.jpg",
            "extracted_data": {
                "name": "سارة علي",
                "title": "مديرة مبيعات",
                "company": "شركة التسويق",
                "email": "sara@marketing.com",
                "phone": "+966507654321"
            },
            "reviewed": True
        }
    ]
    
    if reviewed is not None:
        cards = [c for c in cards if c["reviewed"] == reviewed]
    
    return cards[skip:skip + limit]


@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get card details."""
    # Mock data
    return {
        "id": card_id,
        "image_url": f"/uploads/cards/card{card_id}.jpg",
        "extracted_data": {
            "name": "أحمد محمد",
            "title": "مدير تقني",
            "company": "شركة التقنية",
            "email": "ahmed@tech.com",
            "phone": "+966501234567"
        },
        "reviewed": False
    }


@router.put("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: str,
    card_update: CardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update extracted card data (manual correction)."""
    # Mock response - تحديث البيانات
    return {
        "id": card_id,
        "image_url": f"/uploads/cards/card{card_id}.jpg",
        "extracted_data": card_update.extracted_data or {},
        "reviewed": card_update.reviewed or False
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
