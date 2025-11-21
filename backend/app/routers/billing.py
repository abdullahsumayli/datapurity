"""Billing router."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
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


@router.post("/create-checkout")
async def create_checkout_session(
    plan_id: str,
    payment_method: str,
    billing_info: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create checkout session for payment.
    Integrates with Moyasar (Saudi payment gateway) or Stripe.
    """
    from pydantic import BaseModel
    
    # Validate plan
    valid_plans = ['starter', 'business']
    if plan_id not in valid_plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan selected"
        )
    
    # Plan pricing
    plan_prices = {
        'starter': 79.00,
        'business': 199.00
    }
    
    amount = plan_prices[plan_id]
    amount_with_vat = amount * 1.15  # Add 15% VAT
    
    # TODO: Integrate with Moyasar API
    # For now, return mock checkout URL
    # In production, create actual payment session with Moyasar:
    # https://docs.moyasar.com/ar/api/#create-payment
    
    checkout_session = {
        "id": f"checkout_{plan_id}_{current_user.id}",
        "amount": amount_with_vat,
        "currency": "SAR",
        "plan_id": plan_id,
        "customer_email": current_user.email,
        "billing_info": billing_info,
        "payment_method": payment_method,
        # In production, this will be Moyasar checkout URL
        "checkout_url": f"https://moyasar.com/checkout/mock_{plan_id}",
        "success_url": "http://localhost:5173/app/billing?status=success",
        "cancel_url": "http://localhost:5173/app/billing?status=cancelled"
    }
    
    # Save checkout session to database for tracking
    # TODO: Create CheckoutSession model and save
    
    return checkout_session


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
        "checkout_url": f"/checkout?plan={plan}"
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
