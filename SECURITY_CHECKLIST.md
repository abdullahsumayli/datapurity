# قائمة الفحص الأمني 🔐

## ✅ تم الإصلاح

1. **CORS محدود**
   - تم تقييد `allow_origins` للدومينات المسموح بها فقط
   - حذف `allow_origins=["*"]`

## 🔴 يجب إصلاحه فوراً

### 1. JWT Secret (حرج جداً!)
```bash
# على السيرفر:
ssh root@46.62.239.119
cd /opt/datapurity/backend

# إنشاء ملف .env
cat > .env << 'EOF'
JWT_SECRET=CPwfvL9Yq91BMyT2KKGtMEyY1vvIQbNcwnDm5-HTQXg
DB_URL=sqlite+aiosqlite:///./datapurity.db
ENVIRONMENT=production
DEBUG=False
EOF

# إعادة تشغيل Backend
pkill -9 uvicorn
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
```

### 2. تفعيل Authentication
**المشكلة:** جميع API endpoints بدون حماية!

الملفات التي تحتاج تعديل:
- `backend/app/routers/contacts.py` - TODO: Add current_user
- `backend/app/routers/datasets.py` - TODO: Add current_user
- `backend/app/routers/cards.py` - TODO: Add current_user
- `backend/app/routers/exports.py` - TODO: Add current_user
- `backend/app/routers/jobs.py` - TODO: Add current_user

### 3. حذف كلمات المرور من الكود
ملفات تحتوي كلمات مرور:
- `backend/scripts/create_demo_accounts.py` - "Demo123!"
- `backend/scripts/activate_user.py` - "Abdullah@2025"
- `backend/reset_user.py` - "password123"

**الحل:** استخدام متغيرات بيئية

### 4. Database URL
- حالياً: `user:password@localhost` في الكود
- يجب: نقله لـ `.env` على السيرفر

### 5. HTTPS
- حالياً: HTTP فقط
- يجب: تثبيت SSL certificate (Let's Encrypt)

```bash
# تثبيت Certbot
apt install certbot python3-certbot-nginx
certbot --nginx -d yourdomain.com
```

## ⚠️ توصيات إضافية

1. **Rate Limiting**
   - تحديد عدد الطلبات لكل IP
   - منع Brute Force attacks

2. **Input Validation**
   - التحقق من جميع المدخلات
   - منع SQL Injection

3. **Logging**
   - تسجيل جميع محاولات الدخول
   - مراقبة الأنشطة المشبوهة

4. **Backup**
   - نسخ احتياطي للـ Database
   - خطة استرجاع البيانات

## 📋 أولويات التنفيذ

### فوري (خلال 24 ساعة):
1. ✅ تغيير JWT_SECRET
2. ⚠️ إنشاء ملف .env على السيرفر
3. ⚠️ تفعيل Authentication على Contacts endpoint

### قريب (خلال أسبوع):
4. حذف كلمات المرور من Scripts
5. تثبيت HTTPS
6. تفعيل Authentication على جميع Endpoints

### متوسط الأهمية:
7. Rate Limiting
8. Logging System
9. Backup Strategy
