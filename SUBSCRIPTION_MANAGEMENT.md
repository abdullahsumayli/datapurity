# دليل إدارة الباقات والاشتراكات

## 📋 نظرة عامة

نظام DataPurity يحتوي على نظام متكامل لإدارة باقات الاشتراك وتصنيف العملاء حسب استخدامهم.

---

## 🎯 أنواع الباقات

### 1. الباقة المجانية (Free)
- **السعر**: 0 ريال
- **الحدود**:
  - عملية تنظيف واحدة شهريًا
  - 100 سجل لكل ملف
  - 10 كروت OCR شهريًا
  - مستخدم واحد
- **سعر الكروت الإضافية**: 0.50 ريال/كرت

### 2. باقة المبتدئ (Starter)
- **السعر**: 79 ريال/شهر
- **الحدود**:
  - 5 عمليات تنظيف شهريًا
  - 500 سجل لكل ملف
  - 100 كرت OCR شهريًا
  - مستخدم واحد
- **سعر الكروت الإضافية**: 0.40 ريال/كرت
- **الميزات**: تقارير متقدمة، كشف التكرار، دعم ذو أولوية

### 3. باقة الأعمال (Business)
- **السعر**: 199 ريال/شهر
- **الحدود**:
  - 20 عملية تنظيف شهريًا
  - 2000 سجل لكل ملف
  - 500 كرت OCR شهريًا
  - 5 مستخدمين
- **سعر الكروت الإضافية**: 0.30 ريال/كرت
- **الميزات**: كل ميزات Starter + تصنيف العملاء، دعم WhatsApp

---

## 🔧 كيفية التحكم في الباقات

### 1. عبر لوحة الإدارة (Admin Dashboard)

```
/app/admin
```

**الوصول**: المستخدمين الإداريين فقط

**الوظائف**:
- عرض جميع المستخدمين وباقاتهم
- تصفية حسب نوع الباقة
- تغيير باقة أي مستخدم
- عرض إحصائيات الاستخدام
- عرض الإيرادات الشهرية

### 2. عبر API

#### الحصول على معلومات الاشتراك
```http
GET /api/v1/billing/subscription
Authorization: Bearer {token}
```

**الرد**:
```json
{
  "plan": "starter",
  "status": "active",
  "current_period_end": "2025-12-20T00:00:00",
  "usage": {
    "cleaning": {
      "used": 2,
      "limit": 5,
      "percentage": 40
    },
    "ocr": {
      "used": 45,
      "limit": 100,
      "base_limit": 100,
      "extra_purchased": 0,
      "percentage": 45
    }
  }
}
```

#### ترقية الباقة
```http
POST /api/v1/billing/upgrade
Content-Type: application/json

{
  "plan": "business"
}
```

#### شراء كروت إضافية
```http
POST /api/v1/billing/purchase-cards
Content-Type: application/json

{
  "cards_count": 50
}
```

**الرد**:
```json
{
  "success": true,
  "cards_purchased": 50,
  "cost": 15.00,
  "cost_with_vat": 17.25,
  "total_cards_available": 150
}
```

#### إلغاء الاشتراك
```http
POST /api/v1/billing/cancel
```

---

## 📊 تصنيف العملاء

### حسب الاستخدام

يتم تصنيف العملاء تلقائيًا بناءً على:

1. **مستخدمين نشطين** (Active Users)
   - يستخدمون النظام بانتظام
   - لم يتجاوزوا حدودهم

2. **مستخدمين على وشك التجاوز** (Near Limit)
   - استخدموا أكثر من 80% من الحد
   - مرشحون للترقية

3. **مستخدمين متجاوزين** (Exceeded Limit)
   - تجاوزوا الحد المسموح
   - يحتاجون لترقية أو شراء إضافي

### حسب الباقة

```sql
-- عدد المستخدمين في كل باقة
SELECT 
  plan_type,
  COUNT(*) as user_count,
  SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_count
FROM subscriptions
GROUP BY plan_type;
```

### حسب الإيرادات

```python
# حساب الإيرادات الشهرية
async def calculate_monthly_revenue(db: AsyncSession) -> float:
    result = await db.execute(
        select(
            func.sum(PlanFeature.monthly_price)
        ).select_from(Subscription).join(
            PlanFeature,
            Subscription.plan_type == PlanFeature.plan_type
        ).where(
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    )
    return result.scalar() or 0.0
```

---

## 🛠️ استخدام SubscriptionService

### إنشاء اشتراك جديد
```python
from app.services.subscription_service import SubscriptionService
from app.models.subscription import PlanType

# إنشاء اشتراك مجاني للمستخدم الجديد
subscription = await SubscriptionService.create_subscription(
    db=db,
    user_id=user.id,
    plan_type=PlanType.FREE
)
```

### فحص الحدود قبل العملية
```python
# قبل عملية التنظيف
can_clean, error = await SubscriptionService.check_cleaning_limit(db, user.id)
if not can_clean:
    raise HTTPException(status_code=403, detail=error)

# قبل معالجة الكروت
can_process, error = await SubscriptionService.check_ocr_limit(db, user.id, cards_count=10)
if not can_process:
    raise HTTPException(status_code=403, detail=error)
```

### تحديث الاستخدام
```python
# بعد عملية التنظيف
await SubscriptionService.increment_cleaning_usage(db, user.id)

# بعد معالجة الكروت
await SubscriptionService.increment_ocr_usage(db, user.id, cards_count=10)
```

### الحصول على إحصائيات الاستخدام
```python
stats = await SubscriptionService.get_usage_stats(db, user.id)
print(f"Plan: {stats['plan']}")
print(f"Cleaning used: {stats['usage']['cleaning']['used']}/{stats['usage']['cleaning']['limit']}")
```

---

## 📈 تقارير ولوحات تحليلية

### 1. تقرير الاستخدام الشهري
```python
from app.models.subscription import UsageLog

# احصل على سجل الاستخدام للشهر الحالي
logs = await db.execute(
    select(UsageLog).where(
        and_(
            UsageLog.user_id == user.id,
            UsageLog.created_at >= start_of_month
        )
    )
)
```

### 2. تحليل معدل التحويل (Conversion Rate)
```python
# نسبة المستخدمين الذين ترقوا من Free
conversion_rate = (paid_users / total_users) * 100
```

### 3. متوسط الإيرادات لكل مستخدم (ARPU)
```python
arpu = total_revenue / total_active_users
```

---

## 🔄 العمليات الدورية (Cron Jobs)

### إعادة تعيين الحدود الشهرية
```python
# يجب تشغيله في بداية كل شهر
from app.services.subscription_service import SubscriptionService

async def reset_all_subscriptions():
    users = await get_all_active_users(db)
    for user in users:
        await SubscriptionService.reset_monthly_usage(db, user.id)
```

### التحقق من الاشتراكات المنتهية
```python
from datetime import datetime

async def check_expired_subscriptions():
    now = datetime.utcnow()
    expired = await db.execute(
        select(Subscription).where(
            and_(
                Subscription.current_period_end < now,
                Subscription.status == SubscriptionStatus.ACTIVE
            )
        )
    )
    
    for sub in expired.scalars():
        if sub.auto_renew:
            # محاولة تجديد تلقائي
            await renew_subscription(sub)
        else:
            # إلغاء الاشتراك
            sub.status = SubscriptionStatus.EXPIRED
```

---

## 🎨 واجهة المستخدم

### صفحة الفوترة (`/app/billing`)
- عرض الباقة الحالية
- نسبة الاستخدام
- زر الترقية
- سجل الفواتير

### صفحة الدفع (`/checkout?plan=starter`)
- اختيار الباقة
- معلومات الفوترة
- طرق الدفع
- حساب الضريبة

### لوحة الإدارة (`/app/admin`)
- جدول المستخدمين
- إحصائيات الباقات
- تغيير الباقات
- عرض الإيرادات

---

## 🔐 الصلاحيات

### صلاحيات المستخدم العادي:
- عرض اشتراكه
- ترقية اشتراكه
- شراء كروت إضافية
- إلغاء اشتراكه

### صلاحيات المدير (Admin):
- عرض جميع الاشتراكات
- تغيير باقة أي مستخدم
- عرض الإحصائيات المالية
- إدارة الميزات

---

## 📝 أمثلة عملية

### سيناريو 1: مستخدم يريد الترقية
```python
# 1. المستخدم يختار الباقة من صفحة الهبوط
# 2. يتم توجيهه لـ /checkout?plan=business
# 3. يدخل معلومات الدفع
# 4. عند نجاح الدفع:

await SubscriptionService.upgrade_subscription(
    db=db,
    user_id=current_user.id,
    new_plan=PlanType.BUSINESS
)
```

### سيناريو 2: مستخدم يحتاج كروت إضافية
```python
# 1. المستخدم يصل للحد
# 2. يظهر له تنبيه بالسعر
# 3. عند الموافقة:

cost, subscription = await SubscriptionService.purchase_extra_cards(
    db=db,
    user_id=current_user.id,
    cards_count=50
)

# 4. إنشاء فاتورة دفع
# 5. بعد الدفع تضاف الكروت
```

### سيناريو 3: إدارة يريد تغيير باقة مستخدم
```python
# من لوحة الإدارة
await SubscriptionService.upgrade_subscription(
    db=db,
    user_id=target_user_id,
    new_plan=PlanType.BUSINESS
)
```

---

## 🚀 الخطوات التالية

1. ✅ إضافة جداول قاعدة البيانات
2. ✅ تنفيذ SubscriptionService
3. ✅ تحديث API endpoints
4. ✅ إنشاء لوحة الإدارة
5. ⏳ التكامل مع Moyasar للدفع الفعلي
6. ⏳ إضافة Webhooks للتجديد التلقائي
7. ⏳ إنشاء تقارير تحليلية متقدمة
8. ⏳ إضافة نظام الإشعارات (قرب انتهاء الحد)

---

## 📞 الدعم

للمساعدة في إدارة الباقات، راجع:
- `backend/app/services/subscription_service.py`
- `backend/app/models/subscription.py`
- `backend/app/routers/billing.py`
- `frontend/src/pages/admin/AdminDashboard.tsx`
