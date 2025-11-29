# 📚 دليل نشر DataPurity على Production Server

## 📋 معلومات السيرفر

- **عنوان IP**: `46.62.239.119`
- **نظام التشغيل**: Ubuntu 24.04 LTS
- **المستخدم**: `root`
- **مسار المشروع**: `/opt/datapurity`
- **البورت الخلفي (Backend)**: `8000`
- **البورت الأمامي (Frontend)**: `80` (HTTP)

---

## 🚀 خطوات النشر السريع

### الطريقة 1️⃣: باستخدام السكربت الجاهز (موصى به)

```bash
# 1. اتصل بالسيرفر
ssh root@46.62.239.119

# 2. شغّل سكربت الإصلاح
bash /root/fix-server.sh
```

### الطريقة 2️⃣: خطوة بخطوة يدوياً

```bash
# اتصل بالسيرفر
ssh root@46.62.239.119

# انتقل لمجلد المشروع
cd /opt/datapurity

# احدث الكود من GitHub
git pull origin main

# بناء Frontend
cd frontend
npm install
npm run build

# إعداد Backend
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# إنشاء خدمة systemd
sudo tee /etc/systemd/system/datapurity.service > /dev/null << 'EOF'
[Unit]
Description=DataPurity FastAPI Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/datapurity
Environment="GOOGLE_APPLICATION_CREDENTIALS=/opt/datapurity/keys/datapurity-ocr-5dbb14e3432a.json"
ExecStart=/usr/bin/env uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# تفعيل وتشغيل الخدمة
sudo systemctl daemon-reload
sudo systemctl enable datapurity
sudo systemctl restart datapurity

# التحقق من الحالة
sudo systemctl status datapurity
```

---

## 🔍 التحقق من عمل السيرفر

### 1️⃣ فحص حالة الخدمات

```bash
# فحص FastAPI Backend
systemctl status datapurity

# فحص Nginx
systemctl status nginx

# فحص logs مباشرة
journalctl -u datapurity -f
```

### 2️⃣ اختبار API

```bash
# اختبار الصحة (Health Check)
curl http://localhost:8000/api/v1/health

# اختبار من الخارج
curl http://46.62.239.119/api/v1/health
```

### 3️⃣ فحص الملفات

```bash
# التحقق من بناء Frontend
ls -la /opt/datapurity/frontend/dist/

# التحقق من Backend
ls -la /opt/datapurity/backend/venv/

# فحص إعدادات Nginx
cat /etc/nginx/sites-available/datapurity
```

---

## 🌐 الوصول للتطبيق

بعد النشر الناجح، يمكن الوصول للتطبيق عبر:

- **الموقع الرئيسي**: http://46.62.239.119
- **API Documentation**: http://46.62.239.119/docs
- **ReDoc**: http://46.62.239.119/redoc
- **Health Check**: http://46.62.239.119/api/v1/health

---

## 🛠️ الأوامر المفيدة

### إعادة تشغيل الخدمات

```bash
# إعادة تشغيل Backend فقط
systemctl restart datapurity

# إعادة تشغيل Nginx
systemctl restart nginx

# إعادة تشغيل الاثنين
systemctl restart datapurity nginx
```

### عرض السجلات (Logs)

```bash
# آخر 50 سطر من logs
journalctl -u datapurity -n 50

# متابعة logs مباشرة
journalctl -u datapurity -f

# logs مع الأخطاء فقط
journalctl -u datapurity -p err

# nginx access logs
tail -f /var/log/nginx/access.log

# nginx error logs
tail -f /var/log/nginx/error.log
```

### تحديث الكود

```bash
cd /opt/datapurity
git pull origin main
cd frontend && npm install && npm run build
systemctl restart datapurity
```

---

## 🔧 حل المشاكل الشائعة

### ❌ المشكلة: Backend لا يعمل

```bash
# 1. افحص السجلات
journalctl -u datapurity -n 100

# 2. تحقق من المنفذ
netstat -tulpn | grep 8000

# 3. أعد تشغيل الخدمة
systemctl restart datapurity

# 4. تحقق من الحالة
systemctl status datapurity
```

### ❌ المشكلة: Nginx لا يعمل

```bash
# 1. افحص إعدادات Nginx
nginx -t

# 2. افحص السجلات
tail -n 50 /var/log/nginx/error.log

# 3. أعد تشغيل Nginx
systemctl restart nginx
```

### ❌ المشكلة: خطأ في قاعدة البيانات

```bash
cd /opt/datapurity/backend
source venv/bin/activate
python init_db.py
deactivate
systemctl restart datapurity
```

### ❌ المشكلة: Frontend لا يظهر

```bash
# 1. تحقق من ملفات البناء
ls -la /opt/datapurity/frontend/dist/

# 2. أعد بناء Frontend
cd /opt/datapurity/frontend
npm install
npm run build

# 3. أعد تشغيل Nginx
systemctl restart nginx
```

---

## 📊 هيكل المشروع على السيرفر

```
/opt/datapurity/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   └── ...
│   ├── venv/                    # Python virtual environment
│   ├── requirements.txt
│   └── datapurity.db           # قاعدة البيانات
├── frontend/
│   ├── src/
│   ├── dist/                   # الملفات المبنية
│   ├── package.json
│   └── ...
└── README.md
```

---

## 🔐 الأمان والصيانة

### تحديثات النظام

```bash
# تحديث الحزم
apt update && apt upgrade -y

# إعادة تشغيل إن لزم
reboot
```

### النسخ الاحتياطي

```bash
# نسخ قاعدة البيانات
cp /opt/datapurity/backend/datapurity.db /root/backup-$(date +%Y%m%d).db

# نسخ المشروع كامل
tar -czf /root/datapurity-backup-$(date +%Y%m%d).tar.gz /opt/datapurity/
```

### مراقبة الموارد

```bash
# استخدام المعالج والذاكرة
htop

# مساحة القرص
df -h

# استخدام الذاكرة
free -h
```

---

## 📝 ملاحظات مهمة

1. **قاعدة البيانات**: تأكد من عمل نسخ احتياطية دورية
2. **SSL/HTTPS**: لم يتم إعداده بعد - استخدم Certbot لإضافة SSL
3. **Firewall**: تأكد من فتح المنافذ 80 و 443
4. **المراقبة**: استخدم أدوات مثل `htop` لمراقبة الأداء

---

## 🚨 جهات الاتصال

- **Repository**: https://github.com/abdullahsumayli/datapurity
- **Server IP**: 46.62.239.119
- **البريد الإلكتروني**: sumayliabdullah@gmail.com

---

## ✅ قائمة التحقق النهائية

- [ ] الكود محدث من GitHub
- [ ] Frontend مبني وموجود في `/opt/datapurity/frontend/dist/`
- [ ] Backend venv مُثبّت وجاهز
- [ ] خدمة `datapurity` تعمل: `systemctl status datapurity`
- [ ] Nginx يعمل: `systemctl status nginx`
- [ ] API يستجيب: `curl http://localhost:8000/api/v1/health`
- [ ] الموقع يعمل: http://46.62.239.119

---

**تم التحديث**: 21 نوفمبر 2025

## OCR Endpoint

- **URL:** `POST /api/v1/ocr/card`
- **Request:** `multipart/form-data` مع حقل واحد باسم `file` يحتوي صورة البطاقة (JPG/PNG/WebP).
- **استجابة نموذجية:**
  ```json
  {
    "raw_text": "Raw OCR text ...",
    "language": "ar",
    "fields": {
      "name": "Ahmad Ali",
      "company": "DataPurity",
      "title": "Sales Manager",
      "email": "ahmad@example.com",
      "phone": {
        "raw": "+966 50 123 4567",
        "normalized": "+966501234567"
      },
      "website": "https://datapurity.com",
      "address": "Riyadh, Saudi Arabia"
    }
  }
  ```
- **ملاحظة تشغيلية:** بعد تعديل الاعتمادات قم بتشغيل:
  ```bash
  pip install -r requirements.txt
  sudo systemctl restart datapurity
  ```

---

## استخدام OCR من واجهة المستخدم

1. انتقل إلى صفحة "معالجة البطاقات" من القائمة الرئيسية.
2. قم برفع صورة بطاقة العمل عبر زر رفع الصورة.
3. ستظهر رسالة "جاري المعالجة..." أثناء معالجة الصورة.
4. بعد انتهاء المعالجة، سيتم تعبئة الحقول تلقائياً بالبيانات المستخرجة (الاسم، الشركة، الهاتف، البريد الإلكتروني، العنوان، الوظيفة).
5. يمكنك تعديل أي حقل يدوياً عبر زر التعديل بجانب كل حقل.
6. لا حاجة لأي تعديل في الـ backend، فقط استخدم endpoint `/api/v1/ocr/card` الموجود مسبقاً.
