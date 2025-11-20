# ============================================
# تشغيل DataPurity في وضع التطوير
# ============================================

Write-Host "🔧 تشغيل DataPurity في وضع التطوير..." -ForegroundColor Cyan

# إيقاف أي عمليات سابقة
Write-Host "`n🛑 إيقاف العمليات السابقة..." -ForegroundColor Yellow
Get-Process -Name python, uvicorn, node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# بدء Backend في نافذة منفصلة
Write-Host "`n🔧 تشغيل Backend..." -ForegroundColor Yellow
$backendCmd = "cd d:\datapurity\backend; Write-Host '🔧 Backend Server' -ForegroundColor Green; d:\datapurity\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

Start-Sleep -Seconds 3

# بدء Frontend في نافذة منفصلة
Write-Host "📦 تشغيل Frontend..." -ForegroundColor Yellow
$frontendCmd = "cd d:\datapurity\frontend; Write-Host '📦 Frontend Dev Server' -ForegroundColor Cyan; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Start-Sleep -Seconds 5

# فتح المتصفح
Write-Host "`n✨ جاري فتح المتصفح..." -ForegroundColor Green
Start-Process "http://localhost:5173"

Write-Host "`n✅ تم تشغيل الخوادم:" -ForegroundColor Green
Write-Host "   📦 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "   🔧 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   📚 API Docs: http://localhost:8000/api/v1/docs" -ForegroundColor Cyan
Write-Host "`nتم فتح نافذتين منفصلتين للخوادم" -ForegroundColor Yellow
