"""Card schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class CardBase(BaseModel):
    """Base card schema."""

    original_filename: str


class CardCreate(CardBase):
    """Card creation schema."""

    storage_path: str
    file_size: int


class CardUpdate(BaseModel):
    """Card update schema."""

    extracted_name: Optional[str] = None
    extracted_company: Optional[str] = None
    extracted_phone: Optional[str] = None
    extracted_email: Optional[EmailStr] = None
    extracted_address: Optional[str] = None
    is_reviewed: Optional[bool] = None


class CardResponse(CardBase):
    """Card response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    storage_path: str
    ocr_text: Optional[str] = None
    ocr_confidence: Optional[float] = None
    extracted_name: Optional[str] = None
    extracted_company: Optional[str] = None
    extracted_phone: Optional[str] = None
    extracted_email: Optional[str] = None
    extracted_address: Optional[str] = None
    is_processed: bool
    is_reviewed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
