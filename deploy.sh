#!/usr/bin/env bash
set -e

# Usage: Run from local machine
# Ensure this file is executable: chmod +x deploy.sh

SERVER_USER="root"
SERVER_HOST="aidotoo.com"
PROJECT_DIR="/opt/datapurity"

echo ">>> Connecting to $SERVER_USER@$SERVER_HOST"
ssh "$SERVER_USER@$SERVER_HOST" << 'ENDSSH'
  set -e
  echo ">>> Navigate to project directory"
  cd "/opt/datapurity"

  echo ">>> Stash any local changes"
  git stash

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

  # Backend: Python virtualenv handling
  if [ -d venv ]; then
    echo ">>> Backend: Activate venv and install requirements"
    source venv/bin/activate
    if [ -f requirements.txt ]; then
      pip install -r requirements.txt
    fi
    echo ">>> Restart backend service"
    sudo systemctl restart datapurity-backend.service
  else
    echo ">>> Backend: venv not found, skipping Python dependencies and backend restart"
  fi

  # Frontend build & restart
  if [ -d frontend ]; then
    echo ">>> Build frontend"
    cd frontend
    npm install
    npm run build
    echo ">>> Restart frontend service"
    sudo systemctl restart datapurity-frontend.service
  else
    echo ">>> Frontend directory not found, skipping frontend build and restart"
  fi

  echo ">>> Deployment completed successfully"
ENDSSH
