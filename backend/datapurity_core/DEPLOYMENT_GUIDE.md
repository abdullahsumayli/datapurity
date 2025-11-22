# DataPurity Core - Deployment Guide

Complete guide for deploying DataPurity Core cleaning engine in production environments.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [CLI Deployment](#cli-deployment)
4. [API Deployment](#api-deployment)
5. [Integration with Existing System](#integration-with-existing-system)
6. [Performance Tuning](#performance-tuning)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Python Version

- Python 3.11 or higher
- pip 23.0+

### Dependencies

```
pandas>=2.2.0
phonenumbers>=8.13.0
rapidfuzz>=3.6.0
pydantic>=2.6.0
pydantic-settings>=2.1.0
openpyxl>=3.1.0
```

### Optional (for API)

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.9
```

### Hardware (Recommended)

- **CPU**: 2+ cores
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for dependencies + data files

---

## Installation

### 1. Clone/Copy Files

Copy the DataPurity Core module to your project:

```bash
# Structure:
backend/
├── datapurity_core/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── io_utils.py
│   ├── cleaning.py
│   ├── deduplication.py
│   ├── scoring.py
│   └── stats.py
├── scripts/
│   └── datapurity_clean_cli.py
└── api/
    └── main.py
```

### 2. Install Dependencies

```bash
cd backend
pip install -r datapurity_core/requirements.txt
```

### 3. Verify Installation

```bash
python -c "from datapurity_core import get_settings; print('✓ Installation successful')"
```

---

## CLI Deployment

### Basic Usage

```bash
# Clean a file
python -m scripts.datapurity_clean_cli input.xlsx output.xlsx

# With custom options
python -m scripts.datapurity_clean_cli \
  contacts.csv cleaned.csv \
  --country SA \
  --fuzzy-threshold 90 \
  --verbose
```

### Create Standalone Script

Create `clean_contacts.sh` (Linux/Mac):

```bash
#!/bin/bash
cd /path/to/backend
python -m scripts.datapurity_clean_cli "$@"
```

Make executable:

```bash
chmod +x clean_contacts.sh
```

### Windows Batch Script

Create `clean_contacts.bat`:

```batch
@echo off
cd C:\path\to\backend
python -m scripts.datapurity_clean_cli %*
```

### Scheduled Batch Processing

Create cron job (Linux):

```bash
# Edit crontab
crontab -e

# Add job (run daily at 2 AM)
0 2 * * * cd /path/to/backend && python -m scripts.datapurity_clean_cli /data/contacts.xlsx /data/cleaned.xlsx
```

Windows Task Scheduler:

- Create new task
- Trigger: Daily at 2:00 AM
- Action: Run `clean_contacts.bat`

---

## API Deployment

### 1. Development Server

```bash
cd backend/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access at: `http://localhost:8000`

### 2. Production Deployment (Linux/Ubuntu)

#### Install System Dependencies

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

#### Create Virtual Environment

```bash
cd /opt/datapurity
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Create Systemd Service

Create `/etc/systemd/system/datapurity-api.service`:

```ini
[Unit]
Description=DataPurity Contact Cleaning API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/datapurity/backend/api
Environment="PATH=/opt/datapurity/venv/bin"
ExecStart=/opt/datapurity/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable datapurity-api
sudo systemctl start datapurity-api
sudo systemctl status datapurity-api
```

#### Check Logs

```bash
sudo journalctl -u datapurity-api -f
```

### 3. Nginx Reverse Proxy

Install Nginx:

```bash
sudo apt install nginx
```

Create `/etc/nginx/sites-available/datapurity`:

```nginx
server {
    listen 80;
    server_name api.datapurity.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeout for large files
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Increase upload size limit
    client_max_body_size 100M;
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/datapurity /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.datapurity.com
sudo systemctl restart nginx
```

### 5. Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/datapurity_core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/datapurity_core ./datapurity_core
COPY backend/api ./api

# Expose port
EXPOSE 8000

# Run API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t datapurity-api .
docker run -d -p 8000:8000 --name datapurity datapurity-api
```

Docker Compose (`docker-compose.yml`):

```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./temp_cleaned_files:/app/temp_cleaned_files
    environment:
      - DEFAULT_COUNTRY_CODE=SA
      - FUZZY_NAME_THRESHOLD=90
    restart: unless-stopped
```

Run:

```bash
docker-compose up -d
```

---

## Integration with Existing System

### Method 1: Direct Python Import

```python
from datapurity_core.config import get_settings
from datapurity_core.cleaning import clean_contacts_df
from datapurity_core.io_utils import load_contacts_file, save_contacts_file

# In your existing FastAPI app
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/clean-contacts")
async def clean_uploaded_contacts(file: UploadFile):
    # Save uploaded file
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Clean using DataPurity Core
    settings = get_settings()
    df = load_contacts_file(temp_path)
    df_cleaned, stats = clean_contacts_df(df, settings)

    # Save results
    output_path = f"/tmp/cleaned_{file.filename}"
    save_contacts_file(df_cleaned, output_path)

    return {
        "original_rows": stats.rows_original,
        "final_rows": stats.rows_final,
        "output_file": output_path
    }
```

### Method 2: API Integration

```python
import requests

# Upload file for cleaning
files = {"file": open("contacts.xlsx", "rb")}
data = {
    "country_code": "SA",
    "enable_fuzzy": True,
    "fuzzy_threshold": 90
}

response = requests.post("http://api.datapurity.com/clean", files=files, data=data)
result = response.json()

# Download cleaned file
task_id = result["task_id"]
cleaned_file = requests.get(f"http://api.datapurity.com/clean/download/{task_id}")

with open("cleaned_contacts.xlsx", "wb") as f:
    f.write(cleaned_file.content)
```

### Method 3: Add to Existing FastAPI App

```python
# In your main.py
from backend.api.main import app as datapurity_app
from fastapi import FastAPI

# Your existing app
app = FastAPI()

# Mount DataPurity API
app.mount("/datapurity", datapurity_app)

# Now available at:
# POST /datapurity/clean
# GET /datapurity/clean/download/{task_id}
```

---

## Performance Tuning

### 1. Disable Fuzzy Deduplication for Large Files

```python
settings = get_settings()

# For files > 50,000 rows
if len(df) > 50000:
    settings.ENABLE_FUZZY_DEDUP = False
```

### 2. Batch Processing

```python
# Process in chunks
CHUNK_SIZE = 10000

for i in range(0, len(df), CHUNK_SIZE):
    chunk = df.iloc[i:i+CHUNK_SIZE]
    cleaned_chunk, stats = clean_contacts_df(chunk, settings)
    # Append to results
```

### 3. Parallel Processing

```python
from multiprocessing import Pool

def clean_file(file_path):
    df = load_contacts_file(file_path)
    df_cleaned, stats = clean_contacts_df(df, get_settings())
    return df_cleaned, stats

# Process multiple files in parallel
with Pool(4) as pool:
    results = pool.map(clean_file, file_paths)
```

### 4. Database Integration

```python
import sqlalchemy as sa

# Load from database
engine = sa.create_engine("postgresql://user:pass@localhost/db")
df = pd.read_sql("SELECT * FROM contacts", engine)

# Clean
df_cleaned, stats = clean_contacts_df(df, get_settings())

# Save back to database
df_cleaned.to_sql("contacts_cleaned", engine, if_exists="replace", index=False)
```

---

## Monitoring

### 1. API Health Check

```bash
curl http://localhost:8000/
```

Expected response:

```json
{
  "service": "DataPurity API",
  "version": "1.0.0",
  "status": "running"
}
```

### 2. Logging

Enable verbose logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('datapurity.log'),
        logging.StreamHandler()
    ]
)
```

### 3. Prometheus Metrics (Optional)

```python
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
requests_total = Counter('datapurity_requests_total', 'Total requests')
processing_time = Histogram('datapurity_processing_seconds', 'Processing time')

# In your endpoint
@processing_time.time()
def clean_contacts_endpoint(...):
    requests_total.inc()
    # ... existing code

# Start metrics server
start_http_server(9090)
```

---

## Troubleshooting

### Issue: ImportError: No module named 'datapurity_core'

**Solution:**

```bash
# Add parent directory to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"

# Or in Python:
import sys
sys.path.append('/path/to/backend')
```

### Issue: Phone numbers not normalizing correctly

**Check country code:**

```python
settings = get_settings()
print(settings.DEFAULT_COUNTRY_CODE)  # Should be "SA" for Saudi Arabia
```

### Issue: API returning 500 errors

**Check logs:**

```bash
# Systemd
sudo journalctl -u datapurity-api -n 100

# Docker
docker logs datapurity

# Manual
tail -f datapurity.log
```

### Issue: Out of memory for large files

**Solution: Process in chunks**

```python
# Increase chunk size gradually
CHUNK_SIZE = 5000  # Start with smaller chunks
```

### Issue: Slow fuzzy deduplication

**Solutions:**

1. Increase threshold (more strict = faster)
2. Disable fuzzy dedup for large files
3. Pre-filter data before deduplication

```python
settings.FUZZY_NAME_THRESHOLD = 95  # Higher = faster
settings.ENABLE_FUZZY_DEDUP = False  # For large files
```

---

## Production Checklist

- [ ] Python 3.11+ installed
- [ ] All dependencies installed
- [ ] Configuration file (.env) created
- [ ] Logs directory created with write permissions
- [ ] Temp directory created for file storage
- [ ] Firewall rules configured (port 8000)
- [ ] SSL certificate installed (for HTTPS)
- [ ] Systemd service created and enabled
- [ ] Nginx reverse proxy configured
- [ ] Monitoring/alerting set up
- [ ] Backup strategy implemented
- [ ] Load tested with production data volume
- [ ] Error handling verified
- [ ] Documentation reviewed by team

---

## Support

For deployment assistance:

- Check logs first
- Review configuration settings
- Test with sample data
- Contact development team

---

**DataPurity Core** - Enterprise-Grade Contact Data Cleaning
