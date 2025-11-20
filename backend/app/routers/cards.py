"""Business card OCR endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.card import CardResponse, CardUpdate

router = APIRouter()


@router.post("/upload", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def upload_card(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Upload a business card image for OCR."""
    # TODO: Validate file type (JPG, PNG, PDF)
    # TODO: Upload to S3
    # TODO: Create card record
    # TODO: Queue OCR processing task
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Card upload not yet implemented",
    )


@router.get("/", response_model=List[CardResponse])
async def list_cards(
    skip: int = 0,
    limit: int = 100,
    reviewed: bool = None,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """List all business cards."""
    # TODO: Query cards with filters
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="List cards not yet implemented",
    )


@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: int,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Get card details."""
    # TODO: Retrieve card by ID
    # TODO: Verify ownership
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get card not yet implemented",
    )


@router.patch("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: int,
    card_update: CardUpdate,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Update extracted card data (manual correction)."""
    # TODO: Update card fields
    # TODO: Mark as reviewed
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Update card not yet implemented",
    )


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card_id: int,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Delete a card."""
    # TODO: Delete from S3
    # TODO: Delete card record
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Delete card not yet implemented",
    )
