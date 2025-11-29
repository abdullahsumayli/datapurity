#!/usr/bin/env bash
# Quick OCR Test Script
# Usage: bash scripts/test-ocr.sh <image-path> [endpoint]
# Example: bash scripts/test-ocr.sh card.jpg
# Example: bash scripts/test-ocr.sh card.jpg https://aidotoo.com/api/v1/ocr/card

IMAGE_PATH=${1:-}
ENDPOINT=${2:-https://aidotoo.com/api/v1/ocr/card}

if [ -z "$IMAGE_PATH" ]; then
  echo "Usage: $0 <image-path> [endpoint]"
  echo "Example: $0 /root/business-card.jpg"
  exit 1
fi

if [ ! -f "$IMAGE_PATH" ]; then
  echo "Error: Image file not found: $IMAGE_PATH"
  exit 1
fi

echo "Testing OCR endpoint..."
echo "Image: $IMAGE_PATH"
echo "Endpoint: $ENDPOINT"
echo "---"

# Get file info
FILE_TYPE=$(file --mime-type -b "$IMAGE_PATH")
FILE_SIZE=$(stat -f%z "$IMAGE_PATH" 2>/dev/null || stat -c%s "$IMAGE_PATH" 2>/dev/null)

echo "File type: $FILE_TYPE"
echo "File size: $FILE_SIZE bytes"
echo ""

# Test endpoint
echo "Sending request..."
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -F "file=@$IMAGE_PATH" "$ENDPOINT")

http_code=$(echo "$response" | grep "HTTP_CODE:" | cut -d: -f2)
body=$(echo "$response" | grep -v "HTTP_CODE:")

echo "HTTP Status: $http_code"
echo ""

if [ "$http_code" = "200" ]; then
  echo "✓ SUCCESS"
  echo ""
  echo "Response:"
  echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
  echo "✗ FAILED"
  echo ""
  echo "Response:"
  echo "$body"
fi
