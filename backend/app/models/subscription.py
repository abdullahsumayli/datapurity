"""Subscription and billing models."""

from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PlanType(str, Enum):
    """Subscription plan types."""
    FREE = "free"
    STARTER = "starter"
    BUSINESS = "business"


class SubscriptionStatus(str, Enum):
    """Subscription status."""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TRIAL = "trial"
    SUSPENDED = "suspended"


class PaymentStatus(str, Enum):
    """Payment status."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Subscription(Base):
    """User subscription model."""

    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Plan details
    plan_type: Mapped[PlanType] = mapped_column(SQLEnum(PlanType), nullable=False, default=PlanType.FREE)
    status: Mapped[SubscriptionStatus] = mapped_column(
        SQLEnum(SubscriptionStatus), 
        nullable=False, 
        default=SubscriptionStatus.ACTIVE
    )
    
    # Billing period
    current_period_start: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    current_period_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Usage limits (reset monthly)
    cleaning_operations_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    cleaning_operations_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    ocr_cards_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    ocr_cards_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    records_per_file_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    users_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    # Extra usage (pay-as-you-go)
    extra_cards_purchased: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    extra_cards_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.50)
    
    # Payment integration
    moyasar_customer_id: Mapped[Optional[str]] = mapped_column(String(255))
    moyasar_subscription_id: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Auto renewal
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True)
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    # user: Mapped["User"] = relationship(back_populates="subscription")
    payments: Mapped[list["Payment"]] = relationship(back_populates="subscription", cascade="all, delete-orphan")


class Payment(Base):
    """Payment transaction model."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Payment details
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="SAR")
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    
    # Payment method
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)  # mada, visa, applepay
    
    # Moyasar integration
    moyasar_payment_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    moyasar_invoice_id: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Description
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Billing info
    billing_name: Mapped[Optional[str]] = mapped_column(String(255))
    billing_email: Mapped[Optional[str]] = mapped_column(String(255))
    billing_phone: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Timestamps
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    subscription: Mapped["Subscription"] = relationship(back_populates="payments")


class UsageLog(Base):
    """Track user usage for analytics and billing."""

    __tablename__ = "usage_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False)
    
    # Usage type
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)  # cleaning, ocr, export, etc.
    
    # Quantity
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    # Metadata
    metadata: Mapped[Optional[str]] = mapped_column(String(1000))  # JSON string with additional details
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class PlanFeature(Base):
    """Plan features and limits configuration."""

    __tablename__ = "plan_features"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    plan_type: Mapped[PlanType] = mapped_column(SQLEnum(PlanType), nullable=False, unique=True)
    
    # Pricing
    monthly_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # Limits
    cleaning_operations: Mapped[int] = mapped_column(Integer, nullable=False)
    ocr_cards: Mapped[int] = mapped_column(Integer, nullable=False)
    records_per_file: Mapped[int] = mapped_column(Integer, nullable=False)
    max_users: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    # Pay-as-you-go pricing
    extra_card_price: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Features
    has_advanced_reports: Mapped[bool] = mapped_column(Boolean, default=False)
    has_duplicate_detection: Mapped[bool] = mapped_column(Boolean, default=False)
    has_customer_classification: Mapped[bool] = mapped_column(Boolean, default=False)
    has_priority_support: Mapped[bool] = mapped_column(Boolean, default=False)
    has_whatsapp_support: Mapped[bool] = mapped_column(Boolean, default=False)
    has_api_access: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Display info
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    description_ar: Mapped[Optional[str]] = mapped_column(String(500))
    description_en: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
