"""Billing router."""

from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.subscription import PlanType
from app.services.subscription_service import SubscriptionService
from app.schemas.billing import SubscriptionResponse, InvoiceResponse

router = APIRouter()


class BillingInfo(BaseModel):
    """Checkout billing details provided by the customer."""

    fullName: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    vatNumber: Optional[str] = None
    address: str
    city: str
    country: str


class CheckoutRequest(BaseModel):
    """Payload for creating a checkout session."""

    plan_id: Literal["starter", "business"]
    payment_method: Literal["mada", "visa", "applepay"]
    billing_info: BillingInfo


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user subscription details.
    """
    stats = await SubscriptionService.get_usage_stats(db, current_user.id)
    return stats


@router.get("/usage")
async def get_usage_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed usage statistics.
    """
    return await SubscriptionService.get_usage_stats(db, current_user.id)


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
    request: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create checkout session for payment.
    Integrates with Moyasar (Saudi payment gateway) or Stripe.
    """
    # Plan pricing
    plan_prices = {
        'starter': 79.00,
        'business': 199.00
    }
    
    plan_id = request.plan_id
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
        "billing_info": request.billing_info.model_dump(),
        "payment_method": request.payment_method,
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
    try:
        plan_type = PlanType(plan)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan type"
        )
    
    subscription = await SubscriptionService.upgrade_subscription(
        db, current_user.id, plan_type
    )
    
    return {
        "success": True,
        "message": f"Upgraded to {plan} plan",
        "checkout_url": f"/checkout?plan={plan}",
        "subscription": await SubscriptionService.get_usage_stats(db, current_user.id)
    }


@router.post("/purchase-cards")
async def purchase_extra_cards(
    cards_count: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Purchase extra OCR cards.
    """
    if cards_count < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cards count must be at least 1"
        )
    
    try:
        cost, subscription = await SubscriptionService.purchase_extra_cards(
            db, current_user.id, cards_count
        )
        
        return {
            "success": True,
            "cards_purchased": cards_count,
            "cost": cost,
            "cost_with_vat": cost * 1.15,
            "total_cards_available": subscription.ocr_cards_limit + subscription.extra_cards_purchased,
            "checkout_url": f"/checkout?type=cards&count={cards_count}"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel subscription.
    """
    try:
        subscription = await SubscriptionService.cancel_subscription(db, current_user.id)
        return {
            "success": True,
            "message": "تم إلغاء الاشتراك بنجاح",
            "cancelled_at": subscription.cancelled_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/features/{plan_type}")
async def get_plan_features(plan_type: str):
    """
    Get features for a specific plan.
    """
    try:
        plan = PlanType(plan_type)
        features = SubscriptionService.get_plan_features(plan)
        return features
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan type"
        )


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
