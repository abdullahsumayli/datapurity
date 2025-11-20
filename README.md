# DataPurity - منصة ذكية لتنظيف البيانات

**Smart Data Cleaning & Contact Management SaaS Platform**

منصة احترافية لتنظيف البيانات وإدارة جهات الاتصال مع قدرات معالجة OCR وكشف التكرارات.

## 🚀 التشغيل السريع

### الطريقة الأولى: سكريبت تلقائي

```powershell
.\start-dev.ps1
```

### الطريقة الثانية: يدوياً

**Backend:**

```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**

```powershell
cd frontend
npm run dev
```

## 📍 الروابط

- **Frontend**: http://localhost:5173 أو http://localhost:5174
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **Interactive API**: http://localhost:8000/api/v1/redoc

## 🔑 بيانات تسجيل الدخول التجريبية

```
Email: sumayliabdullah@gmail.com
Password: password123
```

## ✨ المميزات

- **تنظيف وتحقق من البيانات**: تحقق تلقائي من البريد الإلكتروني وأرقام الهواتف
- **معالجة بطاقات العمل (OCR)**: استخراج معلومات الاتصال من صور بطاقات العمل
- **كشف التكرارات**: تحديد ودمج جهات الاتصال المكررة
- **تقييم الجودة**: حساب درجات جودة البيانات
- **تصدير متعدد**: تصدير إلى CSV, Excel, JSON, vCard
- **معالجة خلفية**: معالجة غير متزامنة مع Celery

## 📁 Project Structure

```
datapurity/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── core/        # Settings, security, logging
│   │   ├── db/          # Database configuration
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── routers/     # API endpoints
│   │   ├── services/    # Business logic
│   │   ├── workers/     # Celery tasks
│   │   └── utils/       # Utility functions
│   ├── tests/           # Backend tests
│   └── requirements.txt
│
├── frontend/            # React + TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── layouts/     # Layout components
│   │   ├── hooks/       # Custom React hooks
│   │   ├── types/       # TypeScript types
│   │   ├── config/      # API client config
│   │   └── styles/      # CSS files
│   └── package.json
│
└── infra/               # Infrastructure
    ├── docker-compose.yml
    ├── nginx.conf
    ├── env/             # Environment examples
    └── ci/              # CI/CD configs
```

## 🏗️ البنية التقنية

### Backend

- **Framework**: FastAPI 0.109.0
- **Database**: SQLite (للتطوير) / PostgreSQL (للإنتاج)
- **ORM**: SQLAlchemy 2.0 (Async)
- **Authentication**: JWT (python-jose + bcrypt)
- **Task Queue**: Celery + Redis
- **Storage**: AWS S3 (boto3)

### Frontend

- **Framework**: React 18.2 + TypeScript 5.3
- **Build Tool**: Vite 5.0
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: CSS Modules

## 🔧 التطوير

### تثبيت التبعيات

**Backend:**

```powershell
cd backend
pip install -r requirements.txt
```

**Frontend:**

```powershell
cd frontend
npm install
```

### إعداد قاعدة البيانات

```powershell
cd backend
python init_db.py
```

هذا السكريبت سيقوم بـ:

- ✅ حذف الجداول القديمة
- ✅ إنشاء جداول جديدة
- ✅ إنشاء مستخدم تجريبي (sumayliabdullah@gmail.com / password123)

### المتغيرات البيئية

**Backend (.env):**

```env
DB_URL=sqlite+aiosqlite:///./datapurity.db
JWT_SECRET=your-secret-key-here
API_PREFIX=/api/v1
DEBUG=True
```

**Frontend (.env):**

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 📊 قاعدة البيانات

### الجداول الرئيسية

- **users** - المستخدمين
- **datasets** - مجموعات البيانات المرفوعة
- **jobs** - المهام الخلفية
- **cards** - بطاقات العمل (OCR)
- **contacts** - جهات الاتصال المنظفة
- **exports** - ملفات التصدير

## 🔐 نظام المصادقة

النظام يستخدم JWT للمصادقة:

1. تسجيل الدخول → يحصل على `access_token`
2. يتم حفظ Token في `localStorage`
3. يتم إرسال Token مع كل طلب في Header: `Authorization: Bearer {token}`
4. مدة صلاحية Token: 7 أيام

## 🎨 الصفحات المتوفرة

### صفحات عامة

- `/login` - تسجيل الدخول
- `/signup` - حساب جديد

### صفحات محمية

- `/dashboard` - لوحة التحكم
- `/datasets/upload` - رفع البيانات
- `/jobs` - متابعة المهام
- `/cards/upload` - رفع بطاقات العمل
- `/contacts` - إدارة جهات الاتصال
- `/exports` - التصديرات
- `/billing` - الفواتير

## 📝 حالة التطوير

تم تنفيذ:

✅ البنية الكاملة للمشروع  
✅ نظام المصادقة (JWT) مع قاعدة البيانات  
✅ نماذج البيانات (Models) وSchemas  
✅ واجهة المستخدم الأمامية (Frontend)  
✅ التوجيه (Routing) والحماية  
✅ قاعدة بيانات SQLite مع مستخدم تجريبي

**TODO** (منطق الأعمال):

- خوارزميات تنظيف البيانات
- معالجة OCR للبطاقات
- كشف التكرارات
- حساب جودة البيانات
- توليد التصديرات (CSV, Excel, JSON, vCard)
- رفع الملفات إلى S3
- إشعارات فورية
- تقارير تفاعلية

## 🚧 الخطوات التالية

1. ✅ ~~تثبيت التبعيات~~
2. ✅ ~~إعداد قاعدة البيانات~~
3. ✅ ~~تنفيذ نظام المصادقة~~
4. ⏳ تنفيذ خدمات تنظيف البيانات
5. ⏳ دمج خدمة OCR
6. ⏳ بناء المكونات الأمامية
7. ⏳ إضافة الاختبارات
8. ⏳ النشر للإنتاج

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contributing

This is a SaaS starter project. Contributions are welcome!

## 📞 Support

For questions or issues, please open a GitHub issue.

---

**Built with ❤️ using FastAPI, React, and TypeScript**
