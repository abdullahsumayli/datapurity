"""Billing router."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.billing import SubscriptionResponse, InvoiceResponse

router = APIRouter()


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user subscription details.
    """
    # Mock data for now - في الإنتاج سيتم جلبها من قاعدة البيانات
    subscription = {
        "plan": "free",  # free, starter, professional, enterprise
        "status": "active",
        "current_period_end": "2025-12-20T00:00:00",
        "usage": {
            "contacts": 150,
            "limit": 1000
        }
    }
    
    return subscription


@router.get("/invoices", response_model=List[InvoiceResponse])
async def get_invoices(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user billing invoices.
    """
    # Mock data for now - في الإنتاج سيتم جلبها من قاعدة البيانات
    invoices = [
        {
            "id": "inv_001",
            "amount": 99.00,
            "status": "paid",
            "date": "2025-11-01T00:00:00",
            "invoice_url": "/api/v1/billing/invoices/inv_001/download"
        },
        {
            "id": "inv_002",
            "amount": 99.00,
            "status": "paid",
            "date": "2025-10-01T00:00:00",
            "invoice_url": "/api/v1/billing/invoices/inv_002/download"
        }
    ]
    
    return invoices


@router.post("/upgrade")
async def upgrade_plan(
    plan: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upgrade subscription plan.
    """
    # Mock response - في الإنتاج سيتم التكامل مع بوابة الدفع
    return {
        "success": True,
        "message": f"Upgraded to {plan} plan",
        "checkout_url": f"/checkout/{plan}"
    }


@router.get("/invoices/{invoice_id}/download")
async def download_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Download invoice PDF.
    """
    # Mock response - في الإنتاج سيتم إرجاع ملف PDF
    return {
        "invoice_id": invoice_id,
        "download_url": f"/downloads/invoices/{invoice_id}.pdf"
    }
