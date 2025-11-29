# DataPurity SystemD Services Setup

## Prerequisites
- Ubuntu 24.04 LTS
- Node.js installed
- Python 3.11+ with venv
- Nginx (optional, for reverse proxy)

## Installation Steps

### 1. Copy Service Files
```bash
sudo cp /opt/datapurity/infra/datapurity-backend.service /etc/systemd/system/
sudo cp /opt/datapurity/infra/datapurity-frontend.service /etc/systemd/system/
```

### 2. Install Frontend Serve Package (if not installed)
```bash
cd /opt/datapurity/frontend
npm install -g serve
```

### 3. Reload SystemD
```bash
sudo systemctl daemon-reload
```

### 4. Enable Services (auto-start on boot)
```bash
sudo systemctl enable datapurity-backend.service
sudo systemctl enable datapurity-frontend.service
```

### 5. Start Services
```bash
sudo systemctl start datapurity-backend.service
sudo systemctl start datapurity-frontend.service
```

### 6. Check Status
```bash
sudo systemctl status datapurity-backend.service
sudo systemctl status datapurity-frontend.service
```

## Service Management Commands

### View Logs
```bash
# Backend logs
sudo journalctl -u datapurity-backend.service -f

# Frontend logs
sudo journalctl -u datapurity-frontend.service -f
```

### Restart Services
```bash
sudo systemctl restart datapurity-backend.service
sudo systemctl restart datapurity-frontend.service
```

### Stop Services
```bash
sudo systemctl stop datapurity-backend.service
sudo systemctl stop datapurity-frontend.service
```

## Nginx Configuration (Optional)

Create `/etc/nginx/sites-available/datapurity`:

```nginx
server {
    listen 80;
    server_name aidotoo.com www.aidotoo.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/datapurity /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Troubleshooting

### Service Won't Start
```bash
# Check logs
sudo journalctl -u datapurity-backend.service -n 50
sudo journalctl -u datapurity-frontend.service -n 50

# Check if ports are in use
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3000
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R www-data:www-data /opt/datapurity

# Fix venv permissions
sudo chown -R www-data:www-data /opt/datapurity/venv
```

### Update After Code Changes
The deploy.sh script automatically restarts services after pulling new code and rebuilding.
