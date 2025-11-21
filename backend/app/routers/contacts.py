"""Contact management endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.db.session import get_db
from app.schemas.contact import ContactResponse, ContactUpdate
from app.models.contact import Contact

router = APIRouter()


@router.get("/", response_model=List[ContactResponse])
async def list_contacts(
    dataset_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """List contacts with optional filters."""
    query = select(Contact)
    
    # Filter by dataset if specified
    if dataset_id:
        query = query.where(Contact.dataset_id == dataset_id)
    
    # Search across name, email, company
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Contact.full_name.ilike(search_term),
                Contact.email.ilike(search_term),
                Contact.company.ilike(search_term),
            )
        )
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    contacts = result.scalars().all()
    
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Get contact details."""
    # TODO: Retrieve contact by ID
    # TODO: Verify access through dataset ownership
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get contact not yet implemented",
    )


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Update contact information."""
    # TODO: Update contact fields
    # TODO: Recalculate quality scores
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Update contact not yet implemented",
    )


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    # TODO: Add current_user dependency
):
    """Delete a contact."""
    # TODO: Delete contact record
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Delete contact not yet implemented",
    )
