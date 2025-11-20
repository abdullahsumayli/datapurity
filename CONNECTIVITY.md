# 🔗 دليل الربط بين Frontend و Backend

## ✅ تم إصلاح جميع مشاكل الربط!

---

## 🏗️ الهيكلة الموحدة

### نظام الربط

```
التطبيق الموحد (Port 8000)
├── Backend API (/api/v1/*)
│   ├── /api/v1/auth/*
│   ├── /api/v1/users/*
│   ├── /api/v1/datasets/*
│   └── ...
│
└── Frontend SPA (/*)
    ├── / (index.html)
    ├── /login
    ├── /signup
    ├── /app/*
    └── /assets/* (CSS/JS)
```

---

## 📝 التعديلات المنفذة

### 1. apiClient.ts ✅

**الملف**: `frontend/src/config/apiClient.ts`

```typescript
// استخدام مسار نسبي
baseURL: "/api/v1"; // ✅ صحيح

// ❌ خطأ - لا تستخدم هذا
baseURL: "http://localhost:8000/api/v1";
```

**السبب**:

- في النسخة الموحدة، Frontend و Backend على نفس الdomain
- المسار النسبي يعمل في كل البيئات (development/production)
- لا توجد مشاكل CORS

---

### 2. LoginPage.tsx ✅

**التعديل**:

```typescript
// ❌ قبل
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";
window.location.href = `${API_BASE_URL}/auth/google/login`;

// ✅ بعد
window.location.href = "/api/v1/auth/google/login";
```

---

### 3. SignupPage.tsx ✅

**التعديل**:

```typescript
// ❌ قبل
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";
window.location.href = `${API_BASE_URL}/auth/google/login`;

// ✅ بعد
window.location.href = "/api/v1/auth/google/login";
```

---

### 4. حذف env.ts ✅

**الملف المحذوف**: `frontend/src/config/env.ts`

**السبب**: لا حاجة له في النسخة الموحدة

---

### 5. تحديث .env ✅

**الملف**: `frontend/.env`

```bash
# ❌ قبل
VITE_API_BASE_URL=http://localhost:8000/api/v1

# ✅ بعد (تم حذفه)
# لا حاجة لهذا المتغير
```

---

## 🔄 كيف يعمل الربط

### في Development Mode (dev.ps1)

```
Frontend (5173) → Backend (8000)
├── Frontend يستخدم proxy أو CORS
└── Requests تذهب لـ http://localhost:8000/api/v1
```

### في Production Mode (start.bat)

```
Unified Server (8000)
├── /api/v1/* → Backend API
└── /* → Frontend SPA
```

**المميزة**: نفس الorigin، لا CORS!

---

## 🧪 الاختبار

### 1. اختبار API

```bash
curl http://localhost:8000/api/v1/health
```

**النتيجة المتوقعة**:

```json
{
  "status": "healthy",
  "timestamp": "2025-11-20T...",
  "service": "datapurity-api"
}
```

### 2. اختبار Frontend

```bash
curl http://localhost:8000/
```

**النتيجة**: HTML content

### 3. اختبار Static Files

```bash
curl http://localhost:8000/assets/index-*.js
curl http://localhost:8000/assets/index-*.css
```

**النتيجة**: JS/CSS content

---

## 📱 Endpoints الرئيسية

### Authentication

- `POST /api/v1/auth/login` - تسجيل دخول
- `POST /api/v1/auth/signup` - إنشاء حساب
- `GET /api/v1/auth/google/login` - OAuth redirect
- `GET /api/v1/auth/google/callback` - OAuth callback
- `GET /api/v1/auth/me` - المستخدم الحالي

### Frontend Routes

- `/` - Landing page → index.html
- `/login` - صفحة تسجيل دخول → index.html
- `/signup` - صفحة تسجيل → index.html
- `/app/*` - التطبيق → index.html (React Router)

---

## 🐛 استكشاف الأخطاء

### خطأ: Cannot connect to API

**السبب**: السيرفر غير مشغل

**الحل**:

```bash
.\start.bat
```

### خطأ: CORS policy error

**السبب**: استخدام URL مطلق بدلاً من نسبي

**الحل**: استخدم `/api/v1` بدلاً من `http://localhost:8000/api/v1`

### خطأ: 404 on API calls

**السبب**: مسار خاطئ

**الحل**: تأكد من البادئة `/api/v1/`

---

## ✅ قائمة التحقق

- ✅ apiClient.ts يستخدم `/api/v1`
- ✅ LoginPage.tsx يستخدم مسار نسبي
- ✅ SignupPage.tsx يستخدم مسار نسبي
- ✅ لا توجد أي استدعاءات لـ `localhost:8000` في Frontend
- ✅ Frontend مبني (`npm run build`)
- ✅ Backend يخدم `/api/v1/*` و `/*`
- ✅ لا توجد مشاكل CORS

---

## 🎯 الخلاصة

**النسخة الموحدة**:

- ✅ سهولة في النشر (سيرفر واحد)
- ✅ لا مشاكل CORS (نفس الorigin)
- ✅ أسرع في التطوير (لا حاجة لإدارة خادمين)
- ✅ مسارات نسبية تعمل في كل البيئات

**كل شيء جاهز! 🚀**
