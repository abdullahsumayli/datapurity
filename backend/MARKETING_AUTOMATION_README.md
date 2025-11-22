# DataPurity Marketing Automation & Free Trial System

## ✅ تم التنفيذ بنجاح!

تم إضافة نظام كامل للتسويق الآلي و التجربة المجانية إلى DataPurity.

---

## 🎯 الميزات المنفذة

### 1️⃣ Marketing Automation (التسويق الآلي)
- ✅ جدولة تلقائية لـ 4 رسائل بريد إلكتروني
- ✅ APScheduler لمعالجة المهام كل 60 ثانية
- ✅ تتبع الأحداث (Campaign Events)
- ✅ قوالب بريد إلكتروني عربية

**تسلسل الإيميلات:**
1. **فوري**: رسالة ترحيب + شرح التجربة المجانية
2. **بعد 24 ساعة**: تذكير بالتجربة المجانية
3. **بعد 3 أيام**: دراسة حالة عملية
4. **بعد 7 أيام**: عرض خصم محدود

### 2️⃣ Free Trial Upload (التجربة المجانية)
- ✅ رفع ملفات Excel/CSV
- ✅ تنظيف 150 سجل مجاناً
- ✅ استخدام محرك DataPurity الحالي
- ✅ تحديث حالة العميل المحتمل
- ✅ إرجاع إحصائيات + عينة من البيانات النظيفة

---

## 📊 قاعدة البيانات

### جداول جديدة:

#### `scheduled_tasks`
```sql
- id (PK)
- lead_id (FK → leads.id)
- task_type (send_email)
- payload (JSON: template, to, lead_name)
- run_at (TIMESTAMP)
- status (pending/done/failed)
- created_at, updated_at
```

#### `campaign_events`
```sql
- id (PK)
- lead_id (FK → leads.id)
- event_type (lead_created, email_sent, trial_started, trial_completed)
- meta (JSON)
- created_at
```

#### تحديث `leads`
```sql
+ status (new/trial_started/trial_completed/subscribed/lost)
```

---

## 🔗 API Endpoints

### Marketing
```bash
POST /api/v1/marketing/leads
GET  /api/v1/marketing/health
```

### Trial
```bash
POST /api/v1/trial/upload
GET  /api/v1/trial/health
```

---

## 🧪 الاختبار

### Local (جهازك)
```bash
cd d:\datapurity\backend
python test_marketing_automation.py
```

### Production (السيرفر)
```bash
http://46.62.239.119:8000/api/v1/docs
```

---

## ⚙️ الإعدادات المطلوبة

### 1. ملف `.env` (للبريد الإلكتروني الحقيقي)

```env
# Marketing Automation
MARKETING_SCHEDULER_ENABLED=true

# Email SMTP
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM=noreply@datapurity.com
```

### 2. Gmail App Password
إذا كنت تستخدم Gmail:
1. اذهب إلى https://myaccount.google.com/security
2. فعّل "2-Step Verification"
3. اذهب إلى "App passwords"
4. أنشئ password جديد للتطبيق
5. استخدمه في `EMAIL_PASSWORD`

---

## 📝 مثال استخدام

### إنشاء Lead جديد
```python
import requests

lead = {
    "full_name": "أحمد محمد",
    "email": "ahmed@example.com",
    "phone": "+966501234567",
    "company": "شركة الابتكار",
    "sector": "تقنية"
}

response = requests.post(
    "http://46.62.239.119:8000/api/v1/marketing/leads",
    json=lead
)

print(response.json())
```

**النتيجة:**
- ✅ Lead تم إنشاؤه
- ✅ 4 إيميلات تم جدولتها
- ✅ Campaign event مسجل

### رفع ملف للتجربة المجانية
```python
files = {'file': open('contacts.xlsx', 'rb')}
data = {'lead_id': 1}

response = requests.post(
    "http://46.62.239.119:8000/api/v1/trial/upload",
    files=files,
    data=data
)

result = response.json()
print(f"نظفنا {result['processed_rows']} سجل")
print(f"جودة البيانات: {result['stats']['avg_quality_score']}%")
```

---

## 📈 مراقبة النظام

### عرض المهام المجدولة
```bash
cd d:\datapurity\backend
python view_marketing_data.py
```

### فحص الجداول
```bash
python check_tables.py
```

---

## 🚀 الخطوات التالية

### المرحلة 1: اختبار البريد الإلكتروني
1. ✅ أضف SMTP credentials في `.env`
2. ✅ شغّل السيرفر محلياً
3. ✅ أنشئ lead جديد
4. ✅ انتظر 60 ثانية
5. ✅ افحص بريدك الإلكتروني

### المرحلة 2: النشر
1. ✅ أضف SMTP credentials على السيرفر
2. ✅ فعّل `MARKETING_SCHEDULER_ENABLED=true`
3. ✅ أعد تشغيل الخدمة

### المرحلة 3: التحسينات المستقبلية
- [ ] WhatsApp integration
- [ ] SMS notifications
- [ ] Dashboard for leads management
- [ ] A/B testing for emails
- [ ] Analytics & reporting

---

## 📚 الملفات الرئيسية

```
backend/
├── app/
│   ├── core/
│   │   └── scheduler.py          # APScheduler setup
│   ├── models/
│   │   ├── scheduled_task.py     # Task model
│   │   └── campaign_event.py     # Event model
│   ├── services/
│   │   ├── campaigns_service.py  # Campaign logic
│   │   └── email_service.py      # Email templates & SMTP
│   └── routers/
│       ├── marketing.py          # Lead endpoints
│       └── trial.py              # Trial upload endpoint
└── create_marketing_tables.py    # DB migration
```

---

## 🎉 النتيجة النهائية

**النظام الآن يعمل بالكامل على:**
- 🌐 Local: http://127.0.0.1:8000/
- 🌍 Production: http://46.62.239.119:8000/

**يمكنك:**
1. ✅ إنشاء leads من صفحة الهبوط
2. ✅ جدولة إيميلات تلقائياً
3. ✅ رفع ملفات للتجربة المجانية (150 سجل)
4. ✅ تتبع جميع الأحداث
5. ✅ مراقبة المهام المجدولة

---

## 🆘 المساعدة

إذا واجهت مشكلة:
```bash
# فحص logs السيرفر
ssh root@46.62.239.119 "journalctl -u datapurity -n 50"

# فحص الجداول
ssh root@46.62.239.119 "cd /opt/datapurity/backend && /opt/datapurity/backend/venv/bin/python3 check_tables.py"

# إعادة تشغيل الخدمة
ssh root@46.62.239.119 "systemctl restart datapurity"
```

---

تم بنجاح! 🚀
