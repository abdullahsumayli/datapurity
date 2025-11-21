# 🎯 دليل سريع: إدارة الباقات وتصنيف العملاء

## ✅ ما تم إنجازه

تم إنشاء نظام متكامل لإدارة الباقات والاشتراكات يتضمن:

### 1️⃣ **قاعدة البيانات**

ملف: `backend/app/models/subscription.py`

**الجداول الجديدة**:

- `subscriptions` - معلومات اشتراك كل مستخدم
- `payments` - سجل المدفوعات والفواتير
- `usage_logs` - تتبع الاستخدام اليومي
- `plan_features` - تفاصيل وميزات كل باقة

### 2️⃣ **خدمة إدارة الاشتراكات**

ملف: `backend/app/services/subscription_service.py`

**الوظائف الرئيسية**:

```python
# إنشاء اشتراك جديد
await SubscriptionService.create_subscription(db, user_id, PlanType.FREE)

# فحص الحد قبل عملية التنظيف
can_clean, error = await SubscriptionService.check_cleaning_limit(db, user_id)

# فحص الحد قبل معالجة الكروت
can_process, error = await SubscriptionService.check_ocr_limit(db, user_id, cards_count=10)

# ترقية الباقة
await SubscriptionService.upgrade_subscription(db, user_id, PlanType.BUSINESS)

# شراء كروت إضافية
cost, subscription = await SubscriptionService.purchase_extra_cards(db, user_id, 50)

# الحصول على إحصائيات الاستخدام
stats = await SubscriptionService.get_usage_stats(db, user_id)
```

### 3️⃣ **API Endpoints المحدثة**

ملف: `backend/app/routers/billing.py`

```http
GET  /api/v1/billing/subscription      # معلومات الاشتراك
GET  /api/v1/billing/usage              # إحصائيات الاستخدام
POST /api/v1/billing/upgrade            # ترقية الباقة
POST /api/v1/billing/purchase-cards     # شراء كروت إضافية
POST /api/v1/billing/cancel             # إلغاء الاشتراك
GET  /api/v1/billing/features/{plan}    # ميزات باقة معينة
```

### 4️⃣ **لوحة الإدارة**

ملفات:

- `frontend/src/pages/admin/AdminDashboard.tsx`
- `frontend/src/pages/admin/admin.css`

**المميزات**:

- ✅ عرض جميع المستخدمين وباقاتهم
- ✅ تصفية حسب نوع الباقة
- ✅ تغيير باقة أي مستخدم بضغطة زر
- ✅ إحصائيات شاملة (عدد المستخدمين، الإيرادات، توزيع الباقات)
- ✅ عرض نسبة الاستخدام لكل مستخدم

---

## 🚀 كيفية الاستخدام

### للمطورين:

#### 1. إضافة جداول قاعدة البيانات

```bash
# في terminal backend
cd backend
alembic revision --autogenerate -m "Add subscription tables"
alembic upgrade head
```

#### 2. استخدام في الكود

```python
from app.services.subscription_service import SubscriptionService
from app.models.subscription import PlanType

# في أي endpoint تحتاج فحص الحد
@router.post("/datasets/upload")
async def upload_dataset(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # فحص الحد
    can_clean, error = await SubscriptionService.check_cleaning_limit(db, current_user.id)
    if not can_clean:
        raise HTTPException(status_code=403, detail=error)

    # العملية...
    result = process_dataset()

    # تحديث الاستخدام
    await SubscriptionService.increment_cleaning_usage(db, current_user.id)

    return result
```

### للمستخدمين:

#### 1. عرض الباقة الحالية

```
/app/billing
```

#### 2. ترقية الباقة

```
/checkout?plan=starter
/checkout?plan=business
```

#### 3. شراء كروت إضافية

من صفحة `/app/billing` عند الوصول للحد

### للإداريين:

#### 1. الوصول للوحة الإدارة

```
/app/admin
```

**ملاحظة**: تحتاج لصلاحيات Admin في قاعدة البيانات:

```sql
UPDATE users SET is_superuser = true WHERE email = 'admin@example.com';
```

#### 2. تغيير باقة مستخدم

- اختر المستخدم من الجدول
- اختر الباقة الجديدة من القائمة المنسدلة
- سيتم التحديث فورًا

---

## 📊 تصنيف العملاء

### تلقائيًا حسب:

1. **نوع الباقة**

   - Free (مجاني)
   - Starter (مبتدئ)
   - Business (أعمال)

2. **نسبة الاستخدام**

   - مستخدمين نشطين (0-70%)
   - قرب التجاوز (70-100%)
   - متجاوزين (100%+)

3. **حالة الاشتراك**
   - نشط (Active)
   - ملغي (Cancelled)
   - منتهي (Expired)
   - تجريبي (Trial)
   - موقوف (Suspended)

### يدويًا عبر Admin:

- تغيير الباقة
- تفعيل/إيقاف الحساب
- منح كروت إضافية مجانية

---

## 💡 أمثلة عملية

### مثال 1: مستخدم يريد تنظيف ملف

```python
# 1. فحص الحد
can_clean, error = await SubscriptionService.check_cleaning_limit(db, user.id)

# 2. إذا لا يستطيع
if not can_clean:
    # عرض رسالة: "تم استنفاد حد عمليات التنظيف (5 شهريًا)"
    # عرض زر: "ترقية إلى Business للحصول على 20 عملية"
    return {"error": error, "upgrade_url": "/checkout?plan=business"}

# 3. إذا يستطيع
result = clean_dataset()
await SubscriptionService.increment_cleaning_usage(db, user.id)
return result
```

### مثال 2: مستخدم يريد معالجة 50 كرت

```python
# 1. فحص الحد
can_process, error = await SubscriptionService.check_ocr_limit(db, user.id, cards_count=50)

# 2. إذا لا يستطيع
if not can_process:
    # الرسالة: "تحتاج إلى 20 كرت إضافي. السعر: 0.40 ريال/كرت"
    extra_needed = 20
    price_per_card = 0.40
    total_cost = extra_needed * price_per_card

    return {
        "error": error,
        "extra_needed": extra_needed,
        "cost": total_cost,
        "purchase_url": f"/checkout?type=cards&count={extra_needed}"
    }

# 3. إذا يستطيع
result = process_cards()
await SubscriptionService.increment_ocr_usage(db, user.id, cards_count=50)
return result
```

### مثال 3: Admin يريد منح باقة مجانية

```python
# من لوحة الإدارة أو API
await SubscriptionService.upgrade_subscription(
    db=db,
    user_id=special_user_id,
    new_plan=PlanType.BUSINESS
)

# يمكن أيضًا منح كروت مجانية
cost, sub = await SubscriptionService.purchase_extra_cards(
    db=db,
    user_id=special_user_id,
    cards_count=1000
)
# ثم إلغاء الدفع في جدول payments
```

---

## 📈 الإحصائيات المتاحة

### 1. لكل مستخدم

```python
stats = await SubscriptionService.get_usage_stats(db, user_id)

# الناتج:
{
  "plan": "starter",
  "status": "active",
  "usage": {
    "cleaning": {"used": 2, "limit": 5, "percentage": 40},
    "ocr": {"used": 45, "limit": 100, "percentage": 45}
  },
  "pricing": {
    "extra_card_price": 0.40
  }
}
```

### 2. لكل النظام (Admin)

```python
# عدد المستخدمين في كل باقة
free_users = count(plan_type='free')
starter_users = count(plan_type='starter')
business_users = count(plan_type='business')

# الإيرادات الشهرية
monthly_revenue = (starter_users * 79) + (business_users * 199)

# معدل التحويل
conversion_rate = (paid_users / total_users) * 100
```

---

## 🔄 العمليات التلقائية المطلوبة

### 1. إعادة تعيين الحدود شهريًا

```python
# Cron job - أول كل شهر
@scheduler.scheduled_job('cron', day=1, hour=0)
async def reset_monthly_limits():
    users = await get_all_active_users()
    for user in users:
        await SubscriptionService.reset_monthly_usage(db, user.id)
```

### 2. التحقق من الاشتراكات المنتهية

```python
# Cron job - يوميًا
@scheduler.scheduled_job('cron', hour=0)
async def check_expired():
    expired = await get_expired_subscriptions()
    for sub in expired:
        if sub.auto_renew:
            await renew_subscription(sub)
        else:
            sub.status = SubscriptionStatus.EXPIRED
```

### 3. إرسال تنبيهات قبل انتهاء الحد

```python
# عند وصول 80% من الحد
if usage_percentage >= 80:
    await send_notification(
        user_id=user.id,
        message="اقتربت من انتهاء حد الاستخدام",
        cta="ترقية الباقة"
    )
```

---

## ⚙️ الخطوات التالية

### إنتاج (Production):

1. ✅ تشغيل migrations لإضافة الجداول
2. ✅ إضافة Middleware لفحص الحدود تلقائيًا
3. ✅ ربط بوابة الدفع Moyasar
4. ✅ إضافة Webhooks للتجديد التلقائي
5. ✅ إضافة نظام الإشعارات
6. ✅ إنشاء Cron jobs للعمليات الدورية

### تطوير (Development):

1. اختبار جميع السيناريوهات
2. إضافة Unit Tests
3. توثيق جميع الـ APIs
4. إنشاء دليل المستخدم

---

## 📞 الملفات المهمة

### Backend:

- `backend/app/models/subscription.py` - نماذج قاعدة البيانات
- `backend/app/services/subscription_service.py` - منطق العمل
- `backend/app/routers/billing.py` - API endpoints

### Frontend:

- `frontend/src/pages/admin/AdminDashboard.tsx` - لوحة الإدارة
- `frontend/src/pages/billing/BillingPage.tsx` - صفحة الفوترة
- `frontend/src/pages/checkout/CheckoutPage.tsx` - صفحة الدفع

### Documentation:

- `SUBSCRIPTION_MANAGEMENT.md` - الدليل الشامل

---

## ✨ الخلاصة

الآن لديك:

- ✅ نظام كامل لإدارة الباقات
- ✅ تتبع تلقائي للاستخدام
- ✅ لوحة إدارية للتحكم
- ✅ API endpoints جاهزة
- ✅ تصنيف تلقائي للعملاء
- ✅ نظام دفع حسب الاستخدام

كل ما عليك هو:

1. تشغيل migrations
2. اختبار النظام
3. ربط بوابة الدفع الفعلية
4. إطلاق النظام! 🚀
