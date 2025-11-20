# 🎯 ابدأ من هنا - DataPurity

## 📋 نظرة عامة

DataPurity منصة SaaS حديثة لتنظيف البيانات وإدارة جهات الاتصال. تم بناؤها باستخدام:

- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript + Vite
- **Database**: SQLite
- **Authentication**: JWT + Google OAuth

---

## 🚀 التشغيل السريع (خطوة واحدة!)

### Windows

```bat
start.bat
```

### Linux/Mac

```bash
chmod +x start.sh
./start.sh
```

ثم افتح المتصفح على: **http://localhost:5500**

### بيانات الدخول

```
البريد: sumayliabdullah@gmail.com
كلمة المرور: password123
```

---

## 📦 التثبيت الكامل (للمرة الأولى)

### 1. المتطلبات

- Python 3.11 أو أحدث
- Node.js 18 أو أحدث
- Git

### 2. تثبيت Backend

```bash
# إنشاء virtual environment
python -m venv .venv

# تفعيل virtual environment
.venv\Scripts\activate    # Windows
source .venv/bin/activate  # Linux/Mac

# تثبيت المكتبات
cd backend
pip install -r requirements.txt

# إنشاء قاعدة البيانات
python init_db.py
```

### 3. تثبيت Frontend

```bash
cd frontend
npm install
npm run build
```

---

## 🎮 وضعيات التشغيل

### 1. وضع الإنتاج (Unified Server) ⭐ مُوصى به

خادم واحد يخدم Backend API + Frontend معاً على port 8000

```bash
# Windows
.\start.bat

# Linux/Mac
./start.sh
```

**المميزات:**

- ✅ لا توجد مشاكل CORS
- ✅ سهولة النشر
- ✅ أسرع في التحميل

**الرابط:** http://localhost:8000

---

### 2. وضع التطوير (Development Mode)

خادمين منفصلين - Frontend على 5173 و Backend على 8000

```bash
# Windows
.\dev.ps1
```

**المميزات:**

- ✅ Hot reload للفرونت إند
- ✅ تحديثات فورية

**الروابط:**

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

---

## 📁 هيكل المشروع

```
datapurity/
├── backend/           # FastAPI Backend
│   ├── app/
│   │   ├── routers/      # API Endpoints
│   │   ├── models/       # Database Models
│   │   ├── schemas/      # Pydantic Schemas
│   │   └── core/         # Settings & Security
│   └── datapurity.db     # SQLite Database
│
├── frontend/          # React Frontend
│   ├── src/
│   │   ├── pages/        # صفحات التطبيق
│   │   ├── components/   # مكونات
│   │   └── contexts/     # React Contexts
│   └── dist/             # Build Output
│
└── .venv/             # Python Virtual Environment
```

---

## 🎨 الصفحات والميزات

- 🔐 **Authentication** - تسجيل دخول بالبريد أو Google
- 📊 **Dashboard** - إحصائيات شاملة
- 📁 **Datasets** - رفع وإدارة البيانات
- ⚙️ **Jobs** - مهام التنظيف
- 🃏 **Cards** - مراجعة البطاقات
- 👥 **Contacts** - إدارة جهات الاتصال
- 📤 **Exports** - تصدير البيانات
- 💳 **Billing** - الاشتراكات والفواتير

---

## 🔧 الأوامر المفيدة

### Backend

```bash
cd backend
python -m uvicorn app.main:app --reload  # تشغيل
python init_db.py                        # قاعدة بيانات جديدة
```

### Frontend

```bash
cd frontend
npm run dev    # تطوير
npm run build  # بناء
```

---

## 🐛 استكشاف الأخطاء

### الخادم لا يعمل

```bash
# تفعيل virtual environment
.venv\Scripts\activate

# تثبيت المكتبات
cd backend
pip install -r requirements.txt
```

### Frontend لا يظهر

```bash
# بناء Frontend
cd frontend
npm run build
```

### مشاكل Port

```bash
# إيقاف Python
Get-Process -Name python | Stop-Process -Force
```

---

## 📚 مصادر إضافية

- **README.md** - معلومات عامة
- **DEPLOYMENT.md** - دليل النشر
- **GOOGLE_OAUTH_SETUP.md** - إعداد Google OAuth

---

**تم بناؤه بـ ❤️ بواسطة Abdullah Sumayli**
