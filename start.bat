@echo off
echo Starting DataPurity Unified Server...
cd /d D:\datapurity\backend
D:\datapurity\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 5000
pause
