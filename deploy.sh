#!/bin/bash

# ====================================================================
# DataPurity - Production Deployment Script with EasyOCR
# ====================================================================

echo "======================================================================"
echo "🚀 DataPurity Production Deployment - EasyOCR System"
echo "======================================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Server details
SERVER="root@46.62.239.119"
REMOTE_DIR="/root/datapurity"

echo ""
echo -e "${YELLOW}📦 Step 1: Pulling latest code from GitHub...${NC}"
ssh $SERVER "cd $REMOTE_DIR && git pull origin main"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to pull code from GitHub${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Code updated successfully${NC}"

echo ""
echo -e "${YELLOW}📚 Step 2: Installing EasyOCR dependencies...${NC}"
ssh $SERVER "cd $REMOTE_DIR/backend && pip install easyocr==1.7.1 opencv-python-headless==4.9.0.80 numpy==1.26.3"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencies installed successfully${NC}"

echo ""
echo -e "${YELLOW}🔄 Step 3: Restarting backend service...${NC}"
ssh $SERVER "systemctl restart datapurity"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to restart service${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Service restarted successfully${NC}"

echo ""
echo -e "${YELLOW}⏳ Step 4: Waiting for service to be ready...${NC}"
sleep 5

echo ""
echo -e "${YELLOW}🏥 Step 5: Checking service health...${NC}"
ssh $SERVER "curl -s http://localhost:8000/api/v1/health > /dev/null && echo 'Service is healthy' || echo 'Service health check failed'"

echo ""
echo -e "${YELLOW}📊 Step 6: Checking service status...${NC}"
ssh $SERVER "systemctl status datapurity --no-pager | head -20"

echo ""
echo "======================================================================"
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo "======================================================================"
echo ""
echo "📝 Deployment Summary:"
echo "   - EasyOCR system installed"
echo "   - Backend service restarted"
echo "   - Frontend already built and deployed"
echo ""
echo "🌐 URLs:"
echo "   - Frontend: http://46.62.239.119"
echo "   - API Docs: http://46.62.239.119/api/v1/docs"
echo "   - OCR Endpoint: http://46.62.239.119/api/v1/ocr/business-card"
echo ""
echo "🧪 Test the system:"
echo "   1. Open: http://46.62.239.119/app/cards/upload"
echo "   2. Upload business card images"
echo "   3. View extracted data with EasyOCR!"
echo ""
echo "======================================================================"
