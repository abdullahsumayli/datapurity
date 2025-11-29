#!/usr/bin/env bash
# upload_gcv_key.sh
# Script to upload Google Cloud Vision credentials to the DataPurity backend server.
#
# BEFORE RUNNING:
# 1. Edit LOCAL_KEY_PATH below to point to your actual JSON key file location.
# 2. Make this script executable: chmod +x upload_gcv_key.sh
# 3. Run from Git Bash: ./upload_gcv_key.sh
#
# This script will:
# - Upload your GCV credentials file to the server
# - Verify the file was uploaded
# - Restart the backend service to apply changes

set -e

# TODO: Edit this path to point to your actual Google Cloud Vision JSON key file
# Example for Windows Git Bash: /c/Users/amas2/Downloads/datapurity-ocr-5dbb14e3432a.json
LOCAL_KEY_PATH="/d/datapurity/keys/gcv.json/datapurity-ocr-5dbb14e3432a.json"

# Server configuration
SERVER_USER="root"
SERVER_HOST="aidotoo.com"
REMOTE_KEY_PATH="/opt/datapurity/backend/gcv-credentials.json"

# Check if local key file exists
if [ ! -f "$LOCAL_KEY_PATH" ]; then
  echo "ERROR: Local key file not found at: $LOCAL_KEY_PATH"
  echo "Please edit the LOCAL_KEY_PATH variable in this script to point to your actual JSON key file."
  exit 1
fi

echo "============================================"
echo "DataPurity GCV Key Upload Script"
echo "============================================"
echo ""
echo "Local key file: $LOCAL_KEY_PATH"
echo "Remote location: $SERVER_USER@$SERVER_HOST:$REMOTE_KEY_PATH"
echo ""

# Upload the key file to the server
echo ">>> Uploading GCV key to server..."
scp "$LOCAL_KEY_PATH" "$SERVER_USER@$SERVER_HOST:$REMOTE_KEY_PATH"

echo ""
echo ">>> Verifying upload and restarting service..."

# SSH into the server to verify and restart
ssh "$SERVER_USER@$SERVER_HOST" << 'ENDSSH'
  set -e
  
  # Verify the file exists and show details
  echo "Checking uploaded file..."
  ls -l /opt/datapurity/backend/gcv-credentials.json
  
  # Restart the backend service
  echo ""
  echo "Restarting datapurity-backend service..."
  sudo systemctl restart datapurity-backend.service
  
  # Check service status
  echo ""
  echo "Service status:"
  sudo systemctl status datapurity-backend.service --no-pager -l | head -n 10
ENDSSH

echo ""
echo "============================================"
echo "✓ GCV key uploaded and datapurity-backend.service restarted successfully."
echo "============================================"
echo ""
echo "You can now test the OCR endpoint:"
echo "  curl -F \"file=@/path/to/card.jpg\" https://aidotoo.com/api/v1/ocr/card"
echo ""
