# ====================================================================
# DataPurity - Production Deployment Script with EasyOCR (PowerShell)
# ====================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🚀 DataPurity Production Deployment - EasyOCR System" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Server details
$SERVER = "root@46.62.239.119"
$REMOTE_DIR = "/root/datapurity"

# Step 1: Pull latest code
Write-Host "📦 Step 1: Pulling latest code from GitHub..." -ForegroundColor Yellow
ssh $SERVER "cd $REMOTE_DIR; git pull origin main"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to pull code from GitHub" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Code updated successfully" -ForegroundColor Green
Write-Host ""

# Step 2: Install EasyOCR dependencies
Write-Host "📚 Step 2: Installing EasyOCR dependencies..." -ForegroundColor Yellow
ssh $SERVER "cd $REMOTE_DIR/backend; pip install easyocr==1.7.1 opencv-python-headless==4.9.0.80 numpy==1.26.3"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

# Step 3: Restart backend service
Write-Host "🔄 Step 3: Restarting backend service..." -ForegroundColor Yellow
ssh $SERVER "systemctl restart datapurity"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to restart service" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Service restarted successfully" -ForegroundColor Green
Write-Host ""

# Step 4: Wait for service
Write-Host "⏳ Step 4: Waiting for service to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Write-Host ""

# Step 5: Health check
Write-Host "🏥 Step 5: Checking service health..." -ForegroundColor Yellow
ssh $SERVER "curl -s http://localhost:8000/api/v1/health"
Write-Host ""

# Step 6: Service status
Write-Host "📊 Step 6: Checking service status..." -ForegroundColor Yellow
ssh $SERVER "systemctl status datapurity --no-pager | head -20"
Write-Host ""

# Summary
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Deployment Summary:" -ForegroundColor White
Write-Host "   - EasyOCR system installed" -ForegroundColor Gray
Write-Host "   - Backend service restarted" -ForegroundColor Gray
Write-Host "   - Frontend already built and deployed" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 URLs:" -ForegroundColor White
Write-Host "   - Frontend: http://46.62.239.119" -ForegroundColor Cyan
Write-Host "   - API Docs: http://46.62.239.119/api/v1/docs" -ForegroundColor Cyan
Write-Host "   - OCR Endpoint: http://46.62.239.119/api/v1/ocr/business-card" -ForegroundColor Cyan
Write-Host ""
Write-Host "🧪 Test the system:" -ForegroundColor White
Write-Host "   1. Open: http://46.62.239.119/app/cards/upload" -ForegroundColor Gray
Write-Host "   2. Upload business card images" -ForegroundColor Gray
Write-Host "   3. View extracted data with EasyOCR!" -ForegroundColor Gray
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
