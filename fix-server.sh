#!/bin/bash
set -e

echo "🔧 إصلاح إعدادات DataPurity..."

# تحديث الكود من GitHub
echo "[1/5] تحديث الكود..."
cd /opt/datapurity
git pull origin main

# بناء Frontend
echo "[2/5] بناء Frontend..."
cd /opt/datapurity/frontend
npm install
npm run build

# إعداد Backend
echo "[3/5] إعداد Backend..."
cd /opt/datapurity/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# إنشاء خدمة systemd
echo "[4/5] إنشاء خدمة systemd..."
cat > /etc/systemd/system/datapurity.service << 'EOF'
[Unit]
Description=DataPurity FastAPI Service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/datapurity/backend
ExecStart=/opt/datapurity/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3
Environment="PYTHONPATH=/opt/datapurity/backend"

[Install]
WantedBy=multi-user.target
EOF

# تفعيل وتشغيل الخدمة
echo "[5/5] تشغيل الخدمة..."
systemctl daemon-reload
systemctl enable datapurity
systemctl restart datapurity

# الانتظار قليلاً
sleep 5

# عرض الحالة
echo ""
echo "=========================================="
echo "✅ تم الإصلاح!"
echo "=========================================="
systemctl status datapurity --no-pager | head -n 15
echo ""
echo "اختبار الاتصال..."
curl -s http://localhost:8000/api/v1/health && echo "✅ Backend يعمل!" || echo "⚠️ Backend لا يستجيب - تحقق من الأخطاء"
echo ""
echo "جاري عرض آخر سطور من log..."
journalctl -u datapurity -n 20 --no-pager
