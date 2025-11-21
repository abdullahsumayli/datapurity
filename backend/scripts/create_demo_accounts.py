"""
سكريبت لإنشاء حسابات تجريبية في قاعدة البيانات

الاستخدام:
    cd backend
    python -m scripts.create_demo_accounts
"""

import asyncio
import sys
from pathlib import Path

# إضافة مسار backend للـ path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.subscription import Subscription, PlanType, SubscriptionStatus
from app.core.security import get_password_hash
from datetime import datetime, timedelta


async def create_demo_accounts():
    """إنشاء حسابات تجريبية للتطوير والاختبار"""
    
    print("🚀 بدء إنشاء الحسابات التجريبية...\n")
    
    async with AsyncSessionLocal() as session:
        # كلمة المرور الموحدة: Demo123!
        hashed_password = get_password_hash("Demo123!")
        
        # تعريف الحسابات التجريبية
        demo_accounts = [
            {
                "email": "demo.free@datapurity.com",
                "full_name": "مستخدم تجريبي - مجاني",
                "plan": PlanType.FREE,
                "cleaning_limit": 1,
                "ocr_limit": 10,
                "price": 0
            },
            {
                "email": "demo.starter@datapurity.com",
                "full_name": "مستخدم تجريبي - مبتدئ",
                "plan": PlanType.STARTER,
                "cleaning_limit": 5,
                "ocr_limit": 100,
                "price": 79
            },
            {
                "email": "demo.business@datapurity.com",
                "full_name": "مستخدم تجريبي - أعمال",
                "plan": PlanType.BUSINESS,
                "cleaning_limit": 20,
                "ocr_limit": 500,
                "price": 199
            }
        ]
        
        created_count = 0
        
        for account_data in demo_accounts:
            try:
                # التحقق من وجود المستخدم
                from sqlalchemy import select
                result = await session.execute(
                    select(User).where(User.email == account_data["email"])
                )
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    print(f"⚠️  الحساب موجود مسبقاً: {account_data['email']}")
                    continue
                
                # إنشاء المستخدم
                user = User(
                    email=account_data["email"],
                    full_name=account_data["full_name"],
                    hashed_password=hashed_password,
                    is_active=True,
                    is_verified=True,  # تفعيل الحساب مباشرة
                    created_at=datetime.utcnow()
                )
                session.add(user)
                await session.flush()  # للحصول على user.id
                
                # إنشاء الاشتراك
                subscription = Subscription(
                    user_id=user.id,
                    plan_type=account_data["plan"],
                    status=SubscriptionStatus.ACTIVE,
                    monthly_cleaning_limit=account_data["cleaning_limit"],
                    monthly_ocr_limit=account_data["ocr_limit"],
                    current_cleaning_usage=0,
                    current_ocr_usage=0,
                    extra_ocr_cards=0,
                    current_period_start=datetime.utcnow(),
                    current_period_end=datetime.utcnow() + timedelta(days=30),
                    auto_renew=True
                )
                session.add(subscription)
                
                print(f"✅ تم إنشاء الحساب: {account_data['email']}")
                print(f"   - الاسم: {account_data['full_name']}")
                print(f"   - الباقة: {account_data['plan'].value}")
                print(f"   - السعر: {account_data['price']} ريال/شهر")
                print(f"   - حد التنظيف: {account_data['cleaning_limit']}")
                print(f"   - حد OCR: {account_data['ocr_limit']}")
                print()
                
                created_count += 1
                
            except Exception as e:
                print(f"❌ خطأ في إنشاء الحساب {account_data['email']}: {str(e)}")
                continue
        
        # حفظ التغييرات
        if created_count > 0:
            await session.commit()
            print(f"\n🎉 تم إنشاء {created_count} حساب/حسابات بنجاح!")
        else:
            print("\n⚠️  لم يتم إنشاء حسابات جديدة (جميع الحسابات موجودة مسبقاً)")
        
        # عرض معلومات تسجيل الدخول
        print("\n" + "="*60)
        print("📋 معلومات تسجيل الدخول:")
        print("="*60)
        print("\n🔐 حساب المدير:")
        print("   URL: /admin/login")
        print("   Username: admin")
        print("   Password: DataPurity@2025")
        print("\n👤 حسابات العملاء:")
        print("   URL: /login")
        print("   Password لجميع الحسابات: Demo123!")
        print()
        for account_data in demo_accounts:
            print(f"   • {account_data['email']} - {account_data['full_name']}")
        print("\n" + "="*60)


async def reset_demo_accounts():
    """إعادة تعيين استخدام الحسابات التجريبية"""
    
    print("🔄 إعادة تعيين الحسابات التجريبية...\n")
    
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select, update
        
        # الحصول على المستخدمين التجريبيين
        result = await session.execute(
            select(User).where(User.email.like("demo.%@datapurity.com"))
        )
        demo_users = result.scalars().all()
        
        if not demo_users:
            print("⚠️  لا توجد حسابات تجريبية")
            return
        
        user_ids = [user.id for user in demo_users]
        
        # إعادة تعيين الاستخدام
        await session.execute(
            update(Subscription)
            .where(Subscription.user_id.in_(user_ids))
            .values(
                current_cleaning_usage=0,
                current_ocr_usage=0,
                current_period_start=datetime.utcnow(),
                current_period_end=datetime.utcnow() + timedelta(days=30),
                status=SubscriptionStatus.ACTIVE
            )
        )
        
        await session.commit()
        
        print(f"✅ تم إعادة تعيين {len(demo_users)} حساب/حسابات")
        print("   - تم تصفير الاستخدام الحالي")
        print("   - تم تحديث فترة الاشتراك")
        print("   - تم تفعيل الحسابات")


async def delete_demo_accounts():
    """حذف جميع الحسابات التجريبية (للاستخدام قبل الإطلاق)"""
    
    print("⚠️  حذف الحسابات التجريبية...\n")
    
    confirm = input("هل أنت متأكد من حذف جميع الحسابات التجريبية؟ (yes/no): ")
    if confirm.lower() != "yes":
        print("تم الإلغاء")
        return
    
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select, delete
        from app.models.subscription import UsageLog, Payment
        
        # الحصول على المستخدمين التجريبيين
        result = await session.execute(
            select(User).where(User.email.like("demo.%@datapurity.com"))
        )
        demo_users = result.scalars().all()
        
        if not demo_users:
            print("⚠️  لا توجد حسابات تجريبية")
            return
        
        user_ids = [user.id for user in demo_users]
        
        # حذف السجلات المرتبطة
        await session.execute(delete(UsageLog).where(UsageLog.user_id.in_(user_ids)))
        await session.execute(delete(Payment).where(Payment.user_id.in_(user_ids)))
        await session.execute(delete(Subscription).where(Subscription.user_id.in_(user_ids)))
        await session.execute(delete(User).where(User.id.in_(user_ids)))
        
        await session.commit()
        
        print(f"✅ تم حذف {len(demo_users)} حساب/حسابات تجريبية")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="إدارة الحسابات التجريبية")
    parser.add_argument(
        "action",
        choices=["create", "reset", "delete"],
        help="create: إنشاء الحسابات | reset: إعادة تعيين الاستخدام | delete: حذف الحسابات"
    )
    
    args = parser.parse_args()
    
    if args.action == "create":
        asyncio.run(create_demo_accounts())
    elif args.action == "reset":
        asyncio.run(reset_demo_accounts())
    elif args.action == "delete":
        asyncio.run(delete_demo_accounts())
