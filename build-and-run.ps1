# ============================================
# بناء وتشغيل DataPurity - نسخة موحدة
# ============================================

Write-Host "🚀 بناء وتشغيل DataPurity..." -ForegroundColor Cyan

# 1. بناء Frontend
Write-Host "`n📦 بناء Frontend..." -ForegroundColor Yellow
Push-Location "d:\datapurity\frontend"
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ فشل بناء Frontend" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host "✅ تم بناء Frontend بنجاح" -ForegroundColor Green
Pop-Location

# 2. تشغيل Backend (الذي سيخدم Frontend أيضاً)
Write-Host "`n🔧 تشغيل الخادم..." -ForegroundColor Yellow

# إيقاف أي عملية Python سابقة
Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# تشغيل الخادم
Write-Host "`n✨ الخادم يعمل الآن على:" -ForegroundColor Green
Write-Host "   📱 التطبيق: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   📚 API Docs: http://localhost:8000/api/v1/docs" -ForegroundColor Cyan
Write-Host "`nاضغط Ctrl+C للإيقاف`n" -ForegroundColor Yellow

Push-Location "d:\datapurity\backend"
d:\datapurity\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Pop-Location
