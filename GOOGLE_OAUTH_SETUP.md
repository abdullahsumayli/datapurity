# إعداد Google OAuth للمشروع

## خطوات الحصول على Google Client ID و Secret

### 1. إنشاء مشروع في Google Cloud Console

1. اذهب إلى [Google Cloud Console](https://console.cloud.google.com/)
2. قم بإنشاء مشروع جديد أو اختر مشروع موجود
3. من القائمة الجانبية، اختر **APIs & Services** > **Credentials**

### 2. إنشاء OAuth 2.0 Client ID

1. اضغط على **Create Credentials** → **OAuth client ID**
2. اختر **Application type**: **Web application**
3. أضف **Authorized redirect URIs**:
   ```
   http://localhost:8000/api/v1/auth/google/callback
   http://localhost:5173/auth/callback
   ```
4. اضغط **Create**
5. انسخ **Client ID** و **Client Secret**

### 3. تفعيل Google+ API

1. من القائمة الجانبية، اختر **APIs & Services** > **Library**
2. ابحث عن **Google+ API**
3. اضغط **Enable**

### 4. تحديث ملف .env

في ملف `backend/.env`:

```env
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

### 5. إعادة تشغيل الـ Backend

```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## استخدام تسجيل الدخول بـ Google

1. افتح http://localhost:5173/login
2. اضغط على زر **تسجيل الدخول بحساب Google**
3. سيتم توجيهك لصفحة Google للمصادقة
4. بعد الموافقة، سيتم توجيهك للوحة التحكم تلقائياً

## ملاحظات مهمة

- ⚠️ تأكد من إضافة جميع الـ redirect URIs في Google Console
- ⚠️ للإنتاج، استخدم HTTPS فقط
- ⚠️ لا تشارك الـ Client Secret علناً
- ⚠️ أضف domain الإنتاج في Authorized domains

## للإنتاج (Production)

### على السيرفر 46.62.239.119

1. **إضافة URIs في Google Console:**
   ```
   http://46.62.239.119/api/v1/auth/google/callback
   http://46.62.239.119/auth/callback
   ```

2. **تعديل `.env` على السيرفر:**
   ```bash
   ssh root@46.62.239.119
   cd /opt/datapurity/backend
   nano .env
   ```
   
   أضف:
   ```env
   GOOGLE_CLIENT_ID=your-production-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-production-client-secret
   GOOGLE_REDIRECT_URI=http://46.62.239.119/api/v1/auth/google/callback
   ```

3. **إعادة تشغيل الخدمة:**
   ```bash
   systemctl restart datapurity
   ```

### للدومين (عند توفره):

في ملف `.env` للإنتاج:

```env
GOOGLE_CLIENT_ID=production-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=production-client-secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/api/v1/auth/google/callback
```

وأضف في Google Console:

```
https://yourdomain.com/api/v1/auth/google/callback
https://yourdomain.com/auth/callback
```

---

## 🔍 الحالة الحالية

**المشكلة:**
- ❌ `GOOGLE_CLIENT_ID` فارغ في `.env`
- ❌ `GOOGLE_CLIENT_SECRET` فارغ في `.env`
- ❌ الزر يعمل لكن لا يوجد OAuth مهيأ

**الحل:**
1. اتبع الخطوات أعلاه للحصول على Credentials
2. أضفها في `.env` محلياً وعلى السيرفر
3. أعد تشغيل الخدمات

---

## ✅ اختبار الإعداد

```bash
# افتح في المتصفح
http://46.62.239.119/api/v1/auth/google/login

# يجب أن تُحول لصفحة Google للدخول
# إذا ظهر خطأ "redirect_uri_mismatch"، تحقق من URIs في Google Console
```
