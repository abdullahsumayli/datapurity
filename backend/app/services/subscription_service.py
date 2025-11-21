"""Subscription service for managing user plans and usage."""

from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.subscription import (
    Subscription, 
    PlanType, 
    SubscriptionStatus,
    PlanFeature,
    UsageLog
)
from app.models.user import User


class SubscriptionService:
    """Service for managing user subscriptions."""
    
    # Plan configurations
    PLAN_CONFIGS = {
        PlanType.FREE: {
            "cleaning_operations": 1,
            "ocr_cards": 10,
            "records_per_file": 100,
            "users_limit": 1,
            "extra_card_price": 0.50,
            "price": 0.0
        },
        PlanType.STARTER: {
            "cleaning_operations": 5,
            "ocr_cards": 100,
            "records_per_file": 500,
            "users_limit": 1,
            "extra_card_price": 0.40,
            "price": 79.0
        },
        PlanType.BUSINESS: {
            "cleaning_operations": 20,
            "ocr_cards": 500,
            "records_per_file": 2000,
            "users_limit": 5,
            "extra_card_price": 0.30,
            "price": 199.0
        }
    }
    
    @staticmethod
    async def create_subscription(
        db: AsyncSession,
        user_id: int,
        plan_type: PlanType = PlanType.FREE
    ) -> Subscription:
        """Create a new subscription for a user."""
        config = SubscriptionService.PLAN_CONFIGS[plan_type]
        
        now = datetime.utcnow()
        period_end = now + timedelta(days=30)
        
        subscription = Subscription(
            user_id=user_id,
            plan_type=plan_type,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=now,
            current_period_end=period_end,
            cleaning_operations_limit=config["cleaning_operations"],
            cleaning_operations_used=0,
            ocr_cards_limit=config["ocr_cards"],
            ocr_cards_used=0,
            records_per_file_limit=config["records_per_file"],
            users_limit=config["users_limit"],
            extra_cards_price=config["extra_card_price"],
            auto_renew=True
        )
        
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        
        return subscription
    
    @staticmethod
    async def get_user_subscription(
        db: AsyncSession,
        user_id: int
    ) -> Optional[Subscription]:
        """Get active subscription for a user."""
        result = await db.execute(
            select(Subscription).where(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.status == SubscriptionStatus.ACTIVE
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def upgrade_subscription(
        db: AsyncSession,
        user_id: int,
        new_plan: PlanType
    ) -> Subscription:
        """Upgrade user subscription to a new plan."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if not subscription:
            return await SubscriptionService.create_subscription(db, user_id, new_plan)
        
        config = SubscriptionService.PLAN_CONFIGS[new_plan]
        
        # Update plan
        subscription.plan_type = new_plan
        subscription.cleaning_operations_limit = config["cleaning_operations"]
        subscription.ocr_cards_limit = config["ocr_cards"]
        subscription.records_per_file_limit = config["records_per_file"]
        subscription.users_limit = config["users_limit"]
        subscription.extra_cards_price = config["extra_card_price"]
        
        # Reset usage on upgrade
        subscription.cleaning_operations_used = 0
        subscription.ocr_cards_used = 0
        subscription.extra_cards_purchased = 0
        
        # Extend period
        subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
        
        await db.commit()
        await db.refresh(subscription)
        
        return subscription
    
    @staticmethod
    async def check_cleaning_limit(
        db: AsyncSession,
        user_id: int
    ) -> tuple[bool, Optional[str]]:
        """Check if user can perform cleaning operation."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if not subscription:
            return False, "لا يوجد اشتراك نشط"
        
        if subscription.cleaning_operations_used >= subscription.cleaning_operations_limit:
            return False, f"تم استنفاد حد عمليات التنظيف ({subscription.cleaning_operations_limit} شهريًا)"
        
        return True, None
    
    @staticmethod
    async def check_ocr_limit(
        db: AsyncSession,
        user_id: int,
        cards_count: int = 1
    ) -> tuple[bool, Optional[str]]:
        """Check if user can process OCR cards."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if not subscription:
            return False, "لا يوجد اشتراك نشط"
        
        total_available = subscription.ocr_cards_limit + subscription.extra_cards_purchased
        
        if subscription.ocr_cards_used + cards_count > total_available:
            remaining = total_available - subscription.ocr_cards_used
            return False, f"تحتاج إلى {cards_count - remaining} كرت إضافي. السعر: {subscription.extra_cards_price} ريال/كرت"
        
        return True, None
    
    @staticmethod
    async def increment_cleaning_usage(
        db: AsyncSession,
        user_id: int
    ) -> None:
        """Increment cleaning operation usage."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if subscription:
            subscription.cleaning_operations_used += 1
            
            # Log usage
            log = UsageLog(
                user_id=user_id,
                subscription_id=subscription.id,
                action_type="cleaning",
                quantity=1
            )
            db.add(log)
            
            await db.commit()
    
    @staticmethod
    async def increment_ocr_usage(
        db: AsyncSession,
        user_id: int,
        cards_count: int = 1
    ) -> None:
        """Increment OCR cards usage."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if subscription:
            subscription.ocr_cards_used += cards_count
            
            # Log usage
            log = UsageLog(
                user_id=user_id,
                subscription_id=subscription.id,
                action_type="ocr",
                quantity=cards_count
            )
            db.add(log)
            
            await db.commit()
    
    @staticmethod
    async def purchase_extra_cards(
        db: AsyncSession,
        user_id: int,
        cards_count: int
    ) -> tuple[float, Subscription]:
        """Purchase extra OCR cards."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if not subscription:
            raise ValueError("لا يوجد اشتراك نشط")
        
        cost = cards_count * subscription.extra_cards_price
        subscription.extra_cards_purchased += cards_count
        
        await db.commit()
        await db.refresh(subscription)
        
        return cost, subscription
    
    @staticmethod
    async def get_usage_stats(
        db: AsyncSession,
        user_id: int
    ) -> dict:
        """Get user usage statistics."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if not subscription:
            return {
                "plan": "none",
                "status": "inactive",
                "usage": {}
            }
        
        total_cards_available = subscription.ocr_cards_limit + subscription.extra_cards_purchased
        
        return {
            "plan": subscription.plan_type.value,
            "status": subscription.status.value,
            "current_period_end": subscription.current_period_end.isoformat(),
            "usage": {
                "cleaning": {
                    "used": subscription.cleaning_operations_used,
                    "limit": subscription.cleaning_operations_limit,
                    "percentage": (subscription.cleaning_operations_used / subscription.cleaning_operations_limit * 100) if subscription.cleaning_operations_limit > 0 else 0
                },
                "ocr": {
                    "used": subscription.ocr_cards_used,
                    "limit": total_cards_available,
                    "base_limit": subscription.ocr_cards_limit,
                    "extra_purchased": subscription.extra_cards_purchased,
                    "percentage": (subscription.ocr_cards_used / total_cards_available * 100) if total_cards_available > 0 else 0
                },
                "records_per_file_limit": subscription.records_per_file_limit,
                "users_limit": subscription.users_limit
            },
            "pricing": {
                "extra_card_price": subscription.extra_cards_price
            },
            "auto_renew": subscription.auto_renew
        }
    
    @staticmethod
    async def reset_monthly_usage(
        db: AsyncSession,
        user_id: int
    ) -> None:
        """Reset monthly usage counters."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if subscription:
            subscription.cleaning_operations_used = 0
            subscription.ocr_cards_used = 0
            subscription.extra_cards_purchased = 0
            subscription.current_period_start = datetime.utcnow()
            subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
            
            await db.commit()
    
    @staticmethod
    async def cancel_subscription(
        db: AsyncSession,
        user_id: int
    ) -> Subscription:
        """Cancel user subscription."""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if not subscription:
            raise ValueError("لا يوجد اشتراك نشط")
        
        subscription.status = SubscriptionStatus.CANCELLED
        subscription.cancelled_at = datetime.utcnow()
        subscription.auto_renew = False
        
        await db.commit()
        await db.refresh(subscription)
        
        return subscription
    
    @staticmethod
    def get_plan_features(plan_type: PlanType) -> dict:
        """Get features for a specific plan."""
        config = SubscriptionService.PLAN_CONFIGS[plan_type]
        
        features = {
            PlanType.FREE: {
                "has_advanced_reports": False,
                "has_duplicate_detection": False,
                "has_customer_classification": False,
                "has_priority_support": False,
                "has_whatsapp_support": False,
                "has_api_access": False
            },
            PlanType.STARTER: {
                "has_advanced_reports": True,
                "has_duplicate_detection": True,
                "has_customer_classification": False,
                "has_priority_support": True,
                "has_whatsapp_support": False,
                "has_api_access": False
            },
            PlanType.BUSINESS: {
                "has_advanced_reports": True,
                "has_duplicate_detection": True,
                "has_customer_classification": True,
                "has_priority_support": True,
                "has_whatsapp_support": True,
                "has_api_access": False
            }
        }
        
        return {
            **config,
            **features[plan_type]
        }
