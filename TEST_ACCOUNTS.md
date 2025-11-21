# 🔑 حسابات الاختبار - DataPurity

## 🔐 حساب المدير (Admin)

**صفحة الدخول:** `/admin/login`

```
Username: admin
Password: DataPurity@2025
```

**الصلاحيات:**

- الوصول لجميع بيانات المستخدمين
- تغيير الباقات
- عرض الإحصائيات
- إدارة الاشتراكات

**ملاحظة:** هذا الحساب يستخدم sessionStorage ولا يتطلب قاعدة بيانات.

---

## 👤 حسابات العملاء (Customers)

**صفحة الدخول:** `/login`

### 1. حساب تجريبي - باقة مجانية

```
Email: demo.free@datapurity.com
Password: Demo123!
```

**الباقة:** Free

- 1 عملية تنظيف شهرياً
- 10 كروت OCR شهرياً
- جميع الميزات الأساسية

---

### 2. حساب تجريبي - باقة مبتدئ

```
Email: demo.starter@datapurity.com
Password: Demo123!
```

**الباقة:** Starter (79 ريال/شهر)

- 5 عمليات تنظيف شهرياً
- 100 كرت OCR شهرياً
- دعم فني ذو أولوية
- كروت إضافية: 0.40 ريال/كرت

---

### 3. حساب تجريبي - باقة أعمال

```
Email: demo.business@datapurity.com
Password: Demo123!
```

**الباقة:** Business (199 ريال/شهر)

- 20 عملية تنظيف شهرياً
- 500 كرت OCR شهرياً
- دعم فني مخصص
- API مخصص
- كروت إضافية: 0.30 ريال/كرت

---

## 🛠️ للمطورين - إنشاء الحسابات في قاعدة البيانات

### الطريقة 1: باستخدام FastAPI Docs

1. افتح `/docs` في المتصفح
2. اذهب إلى `POST /api/v1/auth/register`
3. استخدم البيانات التالية:

```json
{
  "email": "demo.free@datapurity.com",
  "password": "Demo123!",
  "full_name": "مستخدم تجريبي - مجاني"
}
```

كرر العملية للحسابات الأخرى.

---

### الطريقة 2: باستخدام SQL مباشرة

```sql
-- ملاحظة: يجب تشفير كلمات المرور باستخدام bcrypt في الكود الفعلي
-- هذا مثال توضيحي فقط

-- حساب باقة مجانية
INSERT INTO users (email, full_name, hashed_password, is_active)
VALUES ('demo.free@datapurity.com', 'مستخدم تجريبي - مجاني', '[hashed_password]', true);

-- إضافة اشتراك مجاني
INSERT INTO subscriptions (user_id, plan_type, status, monthly_cleaning_limit, monthly_ocr_limit)
VALUES (
  (SELECT id FROM users WHERE email = 'demo.free@datapurity.com'),
  'free',
  'active',
  1,
  10
);

-- حساب باقة مبتدئ
INSERT INTO users (email, full_name, hashed_password, is_active)
VALUES ('demo.starter@datapurity.com', 'مستخدم تجريبي - مبتدئ', '[hashed_password]', true);

INSERT INTO subscriptions (user_id, plan_type, status, monthly_cleaning_limit, monthly_ocr_limit)
VALUES (
  (SELECT id FROM users WHERE email = 'demo.starter@datapurity.com'),
  'starter',
  'active',
  5,
  100
);

-- حساب باقة أعمال
INSERT INTO users (email, full_name, hashed_password, is_active)
VALUES ('demo.business@datapurity.com', 'مستخدم تجريبي - أعمال', '[hashed_password]', true);

INSERT INTO subscriptions (user_id, plan_type, status, monthly_cleaning_limit, monthly_ocr_limit)
VALUES (
  (SELECT id FROM users WHERE email = 'demo.business@datapurity.com'),
  'business',
  'active',
  20,
  500
);
```

---

### الطريقة 3: سكريبت Python

احفظ هذا الملف كـ `backend/scripts/create_demo_accounts.py`:

```python
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.models.user import User
from app.models.subscription import Subscription, PlanType, SubscriptionStatus
from app.core.security import get_password_hash

async def create_demo_accounts():
    async with async_session_maker() as session:
        # كلمة المرور: Demo123!
        hashed_password = get_password_hash("Demo123!")

        accounts = [
            {
                "email": "demo.free@datapurity.com",
                "full_name": "مستخدم تجريبي - مجاني",
                "plan": PlanType.FREE,
                "cleaning_limit": 1,
                "ocr_limit": 10
            },
            {
                "email": "demo.starter@datapurity.com",
                "full_name": "مستخدم تجريبي - مبتدئ",
                "plan": PlanType.STARTER,
                "cleaning_limit": 5,
                "ocr_limit": 100
            },
            {
                "email": "demo.business@datapurity.com",
                "full_name": "مستخدم تجريبي - أعمال",
                "plan": PlanType.BUSINESS,
                "cleaning_limit": 20,
                "ocr_limit": 500
            }
        ]

        for account in accounts:
            # إنشاء المستخدم
            user = User(
                email=account["email"],
                full_name=account["full_name"],
                hashed_password=hashed_password,
                is_active=True
            )
            session.add(user)
            await session.flush()

            # إنشاء الاشتراك
            subscription = Subscription(
                user_id=user.id,
                plan_type=account["plan"],
                status=SubscriptionStatus.ACTIVE,
                monthly_cleaning_limit=account["cleaning_limit"],
                monthly_ocr_limit=account["ocr_limit"],
                current_cleaning_usage=0,
                current_ocr_usage=0
            )
            session.add(subscription)

        await session.commit()
        print("✅ تم إنشاء الحسابات التجريبية بنجاح!")

if __name__ == "__main__":
    asyncio.run(create_demo_accounts())
```

**لتشغيل السكريبت:**

```bash
cd backend
python scripts/create_demo_accounts.py
```

---

## 🧪 اختبار الحسابات

### 1. اختبار حساب المدير

```bash
# افتح المتصفح
http://46.62.239.119/admin/login

# أدخل البيانات:
Username: admin
Password: DataPurity@2025

# يجب أن تنتقل إلى:
http://46.62.239.119/app/admin
```

### 2. اختبار حسابات العملاء

```bash
# افتح المتصفح
http://46.62.239.119/login

# جرب كل حساب:
Email: demo.free@datapurity.com
Password: Demo123!

# يجب أن تنتقل إلى:
http://46.62.239.119/app/dashboard
```

---

## 🔒 ملاحظات أمنية

### للتطوير (Development):

- ✅ استخدم هذه الحسابات بحرية
- ✅ كلمات المرور بسيطة للاختبار
- ✅ يمكن مشاركتها مع فريق التطوير

### للإنتاج (Production):

- ❌ **لا تستخدم هذه الحسابات**
- ❌ **احذف هذه الحسابات قبل الإطلاق**
- ✅ استخدم كلمات مرور قوية
- ✅ فعّل Two-Factor Authentication
- ✅ راقب محاولات الدخول الفاشلة

---

## 📊 سيناريوهات الاختبار

### السيناريو 1: تجاوز الحد الشهري

1. سجل دخول بـ `demo.free@datapurity.com`
2. حاول تنظيف ملفين
3. يجب أن تظهر رسالة: "تم استنفاد حد التنظيف الشهري"
4. يجب أن يظهر زر "ترقية الباقة"

### السيناريو 2: شراء كروت إضافية

1. سجل دخول بـ `demo.starter@datapurity.com`
2. اذهب لـ `/app/billing`
3. جرب معالجة 150 كرت
4. يجب أن تظهر خيار شراء 50 كرت إضافي بـ 20 ريال

### السيناريو 3: إدارة المستخدمين

1. سجل دخول كـ admin
2. اذهب لـ `/app/admin`
3. يجب أن ترى جميع المستخدمين التجريبيين
4. جرب تغيير باقة أحد المستخدمين

---

## 🔄 إعادة تعيين الحسابات

لإعادة تعيين استخدام الحسابات التجريبية:

```sql
-- إعادة تعيين الاستخدام لجميع الحسابات
UPDATE subscriptions
SET
  current_cleaning_usage = 0,
  current_ocr_usage = 0
WHERE user_id IN (
  SELECT id FROM users
  WHERE email LIKE 'demo.%@datapurity.com'
);

-- حذف سجلات الاستخدام
DELETE FROM usage_logs
WHERE user_id IN (
  SELECT id FROM users
  WHERE email LIKE 'demo.%@datapurity.com'
);
```

---

## 📝 تتبع المشاكل

إذا واجهت مشاكل:

1. **لا يمكن تسجيل الدخول:**

   - تحقق من أن الحسابات موجودة في قاعدة البيانات
   - تأكد من تشفير كلمة المرور صحيح

2. **الحساب غير نشط:**

   ```sql
   UPDATE users SET is_active = true
   WHERE email = 'demo.free@datapurity.com';
   ```

3. **الاشتراك منتهي:**
   ```sql
   UPDATE subscriptions
   SET status = 'active', current_period_end = NOW() + INTERVAL '30 days'
   WHERE user_id IN (
     SELECT id FROM users WHERE email LIKE 'demo.%@datapurity.com'
   );
   ```

---

## ✅ Checklist قبل الإطلاق

- [ ] حذف جميع الحسابات التجريبية
- [ ] حذف هذا الملف من repository العام
- [ ] تغيير كلمة مرور المدير
- [ ] تفعيل rate limiting
- [ ] مراجعة logs للتأكد من عدم وجود محاولات اختراق
- [ ] تفعيل SSL/HTTPS
- [ ] نقل بيانات الدخول للـ environment variables
