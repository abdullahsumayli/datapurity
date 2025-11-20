# DataPurity Remote Deployment Script
# This script deploys the project to Ubuntu server via SSH

$SERVER_IP = "46.62.239.119"
$SERVER_USER = "root"
$DEPLOY_SCRIPT = "/root/deploy_datapurity.sh"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DataPurity Remote Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Make the script executable and run it
Write-Host "[1/2] Making deployment script executable..." -ForegroundColor Yellow
ssh ${SERVER_USER}@${SERVER_IP} "chmod +x $DEPLOY_SCRIPT"

Write-Host ""
Write-Host "[2/2] Running deployment script..." -ForegroundColor Yellow
Write-Host ""
ssh ${SERVER_USER}@${SERVER_IP} "$DEPLOY_SCRIPT"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Deployment script execution completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
