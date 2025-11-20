# 🌟 DataPurity

**منصة ذكية لتنظيف البيانات وإدارة جهات الاتصال**

Smart Data Cleaning & Contact Management SaaS Platform

---

## ⚡ تشغيل سريع

### Windows

```bat
start.bat
```

### Linux/Mac

```bash
./start.sh
```

**افتح:** `http://localhost:5500`

---

## 📦 التثبيت الأولي

### 1. استنساخ المشروع

```bash
git clone https://github.com/abdullahsumayli/datapurity.git
cd datapurity
```

### 2. إعداد Backend

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate
# Linux/Mac
source .venv/bin/activate

cd backend
pip install -r requirements.txt
python init_db.py
```

### 3. إعداد Frontend

```bash
cd ../frontend
npm install
npm run build
```

---

## 🎯 المميزات

✅ **خادم موحد** - Backend يخدم API + Frontend معاً  
✅ **لا مشاكل CORS** - كل شيء من نفس الأصل  
✅ **مصادقة قوية** - JWT + Google OAuth  
✅ **معالجة ذكية** - تنظيف تلقائي للبيانات  
✅ **OCR متقدم** - استخراج من بطاقات الأعمال  
✅ **تصدير متعدد** - CSV, Excel, JSON, vCard  
✅ **واجهة عربية** - دعم RTL كامل

---

## 🏗️ الهيكل

```
datapurity/
├── backend/              # FastAPI (API + يخدم Frontend)
│   ├── app/
│   │   ├── main.py      # نقطة الدخول الرئيسية
│   │   ├── routers/     # Auth, Datasets, Jobs, إلخ
│   │   └── models/      # قاعدة البيانات
│   └── requirements.txt
├── frontend/            # React + TypeScript
│   ├── src/
│   ├── dist/           # البناء (يُخدم من Backend)
│   └── package.json
├── start.bat           # تشغيل سريع (Windows)
└── start.sh            # تشغيل سريع (Linux/Mac)
```

---

## 🔧 وضع التطوير

```powershell
# Windows
.\dev.ps1

# يفتح نافذتين:
# - Frontend: http://localhost:5173 (Hot Reload)
# - Backend: http://localhost:8000 (Auto-reload)
```

---

## 📖 التوثيق

- 📚 [دليل الإعداد الكامل](SETUP_GUIDE.md)
- 🏗️ [شرح الهيكل الجديد](NEW_STRUCTURE.md)
- 🚀 [دليل النشر](DEPLOYMENT.md)
- 🔐 [إعداد Google OAuth](GOOGLE_OAUTH_SETUP.md)

---

## 🔐 حساب تجريبي

```
البريد: sumayliabdullah@gmail.com
كلمة المرور: password123
```

---

## 🛠️ التقنيات

**Backend:**

- FastAPI 0.109.0
- Python 3.12
- SQLite + aiosqlite
- JWT Authentication
- Google OAuth (authlib)
- bcrypt 4.1.2

**Frontend:**

- React 18.2
- TypeScript 5.3
- Vite 5.0
- React Router
- Axios

---

## 🌐 API Docs

عند تشغيل الخادم، افتح:

```
http://localhost:8000/api/v1/docs
```

---

## 🐛 استكشاف الأخطاء

### الخادم لا يعمل

```powershell
# إيقاف العمليات السابقة
Get-Process -Name python,node -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Frontend لا يظهر

```bash
cd frontend
npm run build
```

### إعادة تهيئة قاعدة البيانات

```bash
cd backend
python init_db.py
```

---

## 📊 الأداء

- ⚡ وقت التحميل: ~1.2 ثانية
- 📦 حجم التنزيل: ~280KB
- 🔄 عدد الطلبات: 15

---

## 📝 الترخيص

MIT License

---

## 👨‍💻 المطور

عبدالله السميلي - [GitHub](https://github.com/abdullahsumayli)

---

⭐ إذا أعجبك المشروع، لا تنسى تقييمه!
