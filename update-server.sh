#!/bin/bash
set -e

echo "🔄 تحديث DataPurity على السيرفر..."

# سحب آخر تحديثات
echo "[1/6] سحب التحديثات من GitHub..."
cd /opt/datapurity
git pull origin main

# تحديث Backend dependencies
echo "[2/6] تحديث مكتبات Backend..."
cd /opt/datapurity/backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# بناء Frontend
echo "[3/6] بناء Frontend..."
cd /opt/datapurity/frontend
npm install
npm run build

# التحقق من ملف .env
echo "[4/6] التحقق من إعدادات البيئة..."
if [ ! -f /opt/datapurity/backend/.env ]; then
    echo "⚠️  ملف .env غير موجود، سيتم إنشاؤه..."
    cat > /opt/datapurity/backend/.env << 'EOF'
# Database
DB_URL=sqlite+aiosqlite:///./datapurity.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Google OAuth
GOOGLE_CLIENT_ID=99438233604-tqsk1jpcdkcndkh8bncj1hildkfudn31.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=http://46.62.239.119/api/v1/auth/google/callback

# CORS
BACKEND_CORS_ORIGINS=["http://46.62.239.119","http://localhost:5173"]

# App Settings
DEBUG=False
EOF
fi

# إعادة تشغيل الخدمة
echo "[5/6] إعادة تشغيل Backend..."
systemctl restart datapurity

# الانتظار والتحقق
echo "[6/6] التحقق من الحالة..."
sleep 5

echo ""
echo "=========================================="
echo "✅ التحديث اكتمل!"
echo "=========================================="
systemctl status datapurity --no-pager | head -n 15

echo ""
echo "🧪 اختبار API..."
if curl -s http://localhost:8000/api/v1/health > /dev/null; then
    echo "✅ API يعمل بنجاح!"
else
    echo "⚠️  API لا يستجيب - تحقق من الأخطاء"
fi

echo ""
echo "📋 آخر سطور من log:"
journalctl -u datapurity -n 10 --no-pager
