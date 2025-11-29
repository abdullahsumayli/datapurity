#!/usr/bin/env bash
# OCR Health Check Script for DataPurity
# Usage: bash scripts/health-check.sh [--verbose]

set -e

VERBOSE=false
for arg in "$@"; do
  case "$arg" in
    --verbose|-v) VERBOSE=true ;;
  esac
done

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

error() {
  echo "[ERROR] $*" >&2
}

check_service() {
  local service=$1
  log "Checking $service..."
  if systemctl is-active --quiet "$service"; then
    log "✓ $service is running"
    return 0
  else
    error "✗ $service is NOT running"
    return 1
  fi
}

check_endpoint() {
  local url=$1
  local name=$2
  log "Testing $name: $url"
  
  if curl -s -f -o /dev/null "$url"; then
    log "✓ $name is accessible"
    return 0
  else
    error "✗ $name is NOT accessible"
    return 1
  fi
}

check_ocr_endpoint() {
  local endpoint=$1
  local test_image=${2:-/root/test-card.jpg}
  
  if [ ! -f "$test_image" ]; then
    log "⚠ Test image not found: $test_image (skipping OCR test)"
    return 0
  fi
  
  log "Testing OCR endpoint: $endpoint"
  
  response=$(curl -s -w "\n%{http_code}" -F "file=@$test_image" "$endpoint" 2>&1)
  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | head -n-1)
  
  if [ "$http_code" = "200" ]; then
    log "✓ OCR endpoint returned 200 OK"
    if [ "$VERBOSE" = true ]; then
      log "Response preview: $(echo "$body" | head -c 200)..."
    fi
    # Check if response contains expected fields
    if echo "$body" | grep -q '"raw_text"' && echo "$body" | grep -q '"fields"'; then
      log "✓ Response contains expected fields (raw_text, fields)"
      return 0
    else
      error "✗ Response missing expected fields"
      return 1
    fi
  else
    error "✗ OCR endpoint returned HTTP $http_code"
    if [ "$VERBOSE" = true ]; then
      error "Response: $body"
    fi
    return 1
  fi
}

check_env_var() {
  local var_name=$1
  log "Checking environment variable: $var_name"
  
  if [ -n "${!var_name}" ]; then
    log "✓ $var_name is set: ${!var_name}"
    
    # Special check for credentials file
    if [ "$var_name" = "GOOGLE_APPLICATION_CREDENTIALS" ]; then
      if [ -f "${!var_name}" ]; then
        log "✓ Credentials file exists"
      else
        error "✗ Credentials file NOT found: ${!var_name}"
        return 1
      fi
    fi
    return 0
  else
    error "✗ $var_name is NOT set"
    return 1
  fi
}

main() {
  log "=== DataPurity Health Check ==="
  log ""
  
  # Service checks
  log "--- Service Status ---"
  check_service "datapurity-backend.service" || true
  check_service "datapurity-frontend.service" || true
  log ""
  
  # Environment checks
  log "--- Environment Variables ---"
  check_env_var "GOOGLE_APPLICATION_CREDENTIALS" || true
  log ""
  
  # Endpoint checks
  log "--- HTTP Endpoints ---"
  check_endpoint "https://aidotoo.com/api/v1/health" "Backend Health" || true
  check_endpoint "https://aidotoo.com/" "Frontend" || true
  log ""
  
  # OCR endpoint checks
  log "--- OCR Endpoints ---"
  check_ocr_endpoint "https://aidotoo.com/api/v1/ocr/card" "/root/test-card.jpg" || true
  log ""
  
  # Log file checks
  log "--- Recent Backend Logs ---"
  if command -v journalctl &> /dev/null; then
    log "Last 10 backend log entries:"
    journalctl -u datapurity-backend.service -n 10 --no-pager || true
  else
    log "⚠ journalctl not available"
  fi
  log ""
  
  log "=== Health Check Complete ==="
}

main
