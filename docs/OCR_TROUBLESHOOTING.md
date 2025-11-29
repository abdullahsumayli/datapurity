# OCR Troubleshooting Guide

## Quick Diagnostics

### 1. Check Services Status

```bash
sudo systemctl status datapurity-backend.service
sudo systemctl status datapurity-frontend.service
```

### 2. View Recent Logs

```bash
# Backend logs (last 100 lines)
sudo journalctl -u datapurity-backend.service -n 100 --no-pager

# Follow live logs
sudo journalctl -u datapurity-backend.service -f
```

### 3. Test OCR Endpoint Manually

```bash
# Using curl with a test image
curl -v -F "file=@/path/to/card.jpg" https://aidotoo.com/api/v1/ocr/card

# Check response format
curl -s -F "file=@/path/to/card.jpg" https://aidotoo.com/api/v1/ocr/card | jq
```

### 4. Verify Google Cloud Credentials

```bash
# Check if environment variable is set
echo $GOOGLE_APPLICATION_CREDENTIALS

# Verify file exists
test -f "$GOOGLE_APPLICATION_CREDENTIALS" && echo "✓ File exists" || echo "✗ File missing"

# Check file permissions
ls -la "$GOOGLE_APPLICATION_CREDENTIALS"

# Test credentials manually
python3 -c "
from google.cloud import vision
client = vision.ImageAnnotatorClient()
print('✓ Google Vision client initialized successfully')
"
```

### 5. Run Automated Health Check

```bash
# Basic check
bash scripts/health-check.sh

# Verbose mode with detailed output
bash scripts/health-check.sh --verbose
```

### 6. Test with Sample Image

```bash
bash scripts/test-ocr.sh /path/to/business-card.jpg
```

## Common Issues and Solutions

### Issue: "Empty file" error

**Cause:** File not properly uploaded or corrupted
**Solution:**

1. Check file size: `ls -lh /path/to/image.jpg`
2. Verify file type: `file --mime-type /path/to/image.jpg`
3. Ensure file is valid: `identify /path/to/image.jpg` (requires ImageMagick)

### Issue: "Unsupported image type"

**Cause:** File MIME type not in allowed list (jpeg, png, webp)
**Solution:**

1. Convert image: `convert input.bmp output.jpg`
2. Check actual MIME type: `file --mime-type -b image.jpg`

### Issue: Vision API error

**Cause:** Google Cloud credentials missing or invalid
**Solution:**

1. Verify credentials file path in service file:
   ```bash
   cat /etc/systemd/system/datapurity-backend.service | grep GOOGLE
   ```
2. Regenerate credentials from Google Cloud Console
3. Update service file and reload:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart datapurity-backend.service
   ```

### Issue: 404 Not Found on /api/v1/ocr/card

**Cause:** Router not properly mounted or service not restarted
**Solution:**

1. Check router is included in main app:
   ```bash
   grep -n "ocr" backend/app/main.py
   ```
2. Restart backend service:
   ```bash
   sudo systemctl restart datapurity-backend.service
   ```
3. Verify endpoint exists:
   ```bash
   curl -I https://aidotoo.com/api/v1/ocr/card
   ```

### Issue: Service won't start

**Cause:** Virtual environment path wrong or dependencies missing
**Solution:**

1. Check service file paths:
   ```bash
   cat /etc/systemd/system/datapurity-backend.service
   ```
2. Verify venv exists:
   ```bash
   ls -la /opt/datapurity/venv/bin/activate || ls -la /opt/datapurity/.venv/bin/activate
   ```
3. Reinstall dependencies:
   ```bash
   cd /opt/datapurity
   source .venv/bin/activate  # or venv/bin/activate
   pip install -r requirements.txt
   ```

### Issue: Frontend shows 0/0 or "فشل"

**Cause:** Frontend using old build or wrong endpoint
**Solution:**

1. Check built files contain correct endpoint:
   ```bash
   grep -r "/api/v1/ocr" /opt/datapurity/frontend/dist/assets/
   ```
2. Rebuild frontend:
   ```bash
   cd /opt/datapurity/frontend
   npm install
   npm run build
   sudo systemctl restart datapurity-frontend.service
   ```
3. Clear browser cache (Ctrl+Shift+R)

## Deployment Checklist

Before deploying, ensure:

- [ ] Backend changes committed and pushed to main
- [ ] Frontend changes committed and pushed to main
- [ ] Google credentials file exists on server
- [ ] Environment variables set in systemd service file
- [ ] Both services enabled: `systemctl is-enabled datapurity-{backend,frontend}`

Deploy command:

```bash
bash deploy.sh
```

Post-deployment verification:

```bash
bash scripts/health-check.sh --verbose
```

## Log Locations

- **Backend logs**: `sudo journalctl -u datapurity-backend.service`
- **Frontend logs**: `sudo journalctl -u datapurity-frontend.service`
- **Nginx logs** (if applicable):
  - Access: `/var/log/nginx/access.log`
  - Error: `/var/log/nginx/error.log`

## Testing Different Endpoints

```bash
# Main OCR endpoint
curl -F "file=@card.jpg" https://aidotoo.com/api/v1/ocr/card

# Legacy compatibility endpoint
curl -F "file=@card.jpg" https://aidotoo.com/api/v1/cards/ocr

# With verbose output
curl -v -F "file=@card.jpg" https://aidotoo.com/api/v1/ocr/card
```

## Performance Monitoring

```bash
# Check service resource usage
systemctl status datapurity-backend.service

# Monitor in real-time
top -p $(systemctl show -p MainPID datapurity-backend.service | cut -d= -f2)

# Check disk space
df -h

# Check memory
free -h
```

## Emergency Recovery

If services are completely broken:

```bash
# Stop services
sudo systemctl stop datapurity-backend.service
sudo systemctl stop datapurity-frontend.service

# Check for errors
sudo journalctl -xe

# Reset to last known good commit
cd /opt/datapurity
git stash
git reset --hard HEAD~1

# Reinstall dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Rebuild frontend
cd frontend
npm install
npm run build
cd ..

# Restart services
sudo systemctl start datapurity-backend.service
sudo systemctl start datapurity-frontend.service
```
