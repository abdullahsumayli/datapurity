#!/usr/bin/env bash
set -e

# Usage: Run from local machine
# Ensure this file is executable: chmod +x deploy.sh
# Optional: bash deploy.sh --no-frontend --no-backend

SERVER_USER="root"
SERVER_HOST="aidotoo.com"
PROJECT_DIR="/opt/datapurity"

SKIP_FRONTEND=false
SKIP_BACKEND=false
for arg in "$@"; do
  case "$arg" in
    --no-frontend) SKIP_FRONTEND=true ;;
    --no-backend) SKIP_BACKEND=true ;;
  esac
done

echo ">>> Connecting to $SERVER_USER@$SERVER_HOST"
ssh "$SERVER_USER@$SERVER_HOST" << 'ENDSSH'
  set -e
  echo ">>> Navigate to project directory"
  cd "/opt/datapurity"

  echo ">>> Stash any local changes"
  git stash || true

  echo ">>> Pull latest code"
  git pull origin main

  echo ">>> Setup systemd services if not exists"
  if [ ! -f /etc/systemd/system/datapurity-backend.service ]; then
    echo "Installing backend service..."
    sudo cp infra/datapurity-backend.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable datapurity-backend.service
  fi
  
  if [ ! -f /etc/systemd/system/datapurity-frontend.service ]; then
    echo "Installing frontend service..."
    sudo cp infra/datapurity-frontend.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable datapurity-frontend.service
  fi

  # Backend: Python virtualenv handling (supports venv or .venv)
  if [ "$SKIP_BACKEND" = true ]; then
    echo ">>> Skipping backend per flag"
  else
    if [ -d venv ]; then
      VENV_DIR="venv"
    elif [ -d .venv ]; then
      VENV_DIR=".venv"
    else
      VENV_DIR=""
    fi

    if [ -n "$VENV_DIR" ]; then
      echo ">>> Backend: Activate $VENV_DIR and install requirements"
      source "$VENV_DIR/bin/activate"
      if [ -f requirements.txt ]; then
        pip install -r requirements.txt --quiet
      fi
      echo ">>> Restart backend service"
      sudo systemctl restart datapurity-backend.service || sudo systemctl start datapurity-backend.service
    else
      echo ">>> Backend: No virtualenv (venv/.venv) found; skipping dependencies and restart"
    fi
  fi

  # Frontend build & restart
  if [ "$SKIP_FRONTEND" = true ]; then
    echo ">>> Skipping frontend per flag"
  else
    if [ -d frontend ]; then
      echo ">>> Build frontend"
      cd frontend
      npm install --quiet
      npm run build
      echo ">>> Restart frontend service"
      sudo systemctl restart datapurity-frontend.service || sudo systemctl start datapurity-frontend.service
      cd ..
    else
      echo ">>> Frontend directory not found, skipping frontend build and restart"
    fi
  fi

  # Update Nginx configuration
  echo ">>> Update Nginx configuration"
  sudo cp infra/nginx.conf /etc/nginx/nginx.conf
  sudo nginx -t
  sudo systemctl reload nginx

  # Update systemd service files
  echo ">>> Update systemd service files"
  sudo cp infra/datapurity-backend.service /etc/systemd/system/
  sudo cp infra/datapurity-frontend.service /etc/systemd/system/
  sudo systemctl daemon-reload

  # Show service status
  echo ">>> Service status:"
  sudo systemctl status datapurity-backend --no-pager -l | head -n 10 || true
  sudo systemctl status datapurity-frontend --no-pager -l | head -n 10 || true

  echo ">>> Deployment completed successfully"
ENDSSH
