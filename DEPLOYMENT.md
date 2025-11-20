# 🚀 دليل النشر - DataPurity

## الهيكل الجديد

تم تبسيط المشروع ليعمل كتطبيق موحد:

- **Backend (FastAPI)** يخدم API + ملفات Frontend الثابتة
- لا حاجة لتشغيل خادمين منفصلين في الإنتاج

## 🔧 وضع التطوير (Development)

```powershell
# تشغيل Frontend و Backend في نوافذ منفصلة
.\dev.ps1
```

سيتم فتح:

- Frontend Dev Server على `http://localhost:5173` (مع Hot Reload)
- Backend API على `http://localhost:8000`

## 📦 بناء وتشغيل الإنتاج

```powershell
# بناء Frontend + تشغيل Backend الموحد
.\build-and-run.ps1
```

سيعمل التطبيق الكامل على `http://localhost:8000`

## 🌐 النشر على الخادم

### الخطوة 1: بناء Frontend

```bash
cd frontend
npm install
npm run build
```

### الخطوة 2: إعداد Backend

```bash
cd backend
pip install -r requirements.txt
```

### الخطوة 3: تشغيل الخادم

```bash
# باستخدام Gunicorn (Linux/Mac)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# أو باستخدام Uvicorn مباشرة
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔐 متغيرات البيئة

أنشئ ملف `.env` في `backend/`:

```env
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
DATABASE_URL=sqlite:///./datapurity.db
ENVIRONMENT=production
```

## 🐳 Docker (اختياري)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# تثبيت Node.js لبناء Frontend
RUN apt-get update && apt-get install -y nodejs npm

# نسخ وبناء Frontend
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install
COPY frontend ./frontend
RUN cd frontend && npm run build

# تثبيت Backend
COPY backend/requirements.txt ./backend/
RUN pip install -r backend/requirements.txt
COPY backend ./backend

# تشغيل التطبيق
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 المزايا الجديدة

✅ **خادم واحد فقط** في الإنتاج  
✅ **لا مشاكل CORS** - كل شيء من نفس الـorigin  
✅ **أسرع** - ملفات ثابتة تُخدم مباشرة  
✅ **أسهل في النشر** - لا حاجة لإعدادات معقدة  
✅ **وضع تطوير منفصل** - Hot Reload لكل من Frontend و Backend

## 🔄 كيف يعمل؟

1. **في التطوير**: Frontend (Vite) و Backend (FastAPI) يعملان بشكل منفصل
2. **في الإنتاج**:
   - Frontend يُبنى إلى ملفات ثابتة في `frontend/dist/`
   - FastAPI يخدم هذه الملفات تلقائياً
   - كل الطلبات إلى `/api/v1/*` تذهب للـ API
   - باقي الطلبات تُخدم من ملفات React

## 🛠️ استكشاف الأخطاء

### Frontend لا يظهر

```powershell
# تأكد من بناء Frontend
cd frontend
npm run build
```

### مشاكل في الـ API

```powershell
# تحقق من السجلات
cd backend
uvicorn app.main:app --reload --log-level debug
```

### منافذ مستخدمة

```powershell
# إيقاف جميع العمليات
Get-Process -Name python,node -ErrorAction SilentlyContinue | Stop-Process -Force
```
