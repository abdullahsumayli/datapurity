# DataPurity Development Server Startup Script

Write-Host "🚀 Starting DataPurity Development Environment..." -ForegroundColor Cyan
Write-Host ""

# Start Backend
Write-Host "📦 Starting Backend (FastAPI)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\datapurity\backend; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
Start-Sleep -Seconds 2

# Start Frontend
Write-Host "🎨 Starting Frontend (Vite + React)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\datapurity\frontend; npm run dev"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "✅ DataPurity is now running!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend: http://localhost:5173 or http://localhost:5174" -ForegroundColor Yellow
Write-Host "📍 Backend API: http://localhost:8000" -ForegroundColor Yellow
Write-Host "📍 API Docs: http://localhost:8000/api/v1/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔑 Test Login:" -ForegroundColor Cyan
Write-Host "   Email: sumayliabdullah@gmail.com"
Write-Host "   Password: password123"
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
