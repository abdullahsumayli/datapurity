# DataPurity Backend

FastAPI backend for the DataPurity SaaS platform.

## Quick Start

1. **Create virtual environment:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. **Install dependencies:**

```powershell
pip install -r requirements.txt
```

3. **Set up environment variables:**

```powershell
cp ..\infra\env\backend.env.example .env
# Edit .env with your configuration
```

4. **Run database migrations:**

```powershell
alembic upgrade head
```

5. **Start the server:**

```powershell
uvicorn app.main:app --reload
```

6. **Start Celery worker:**

```powershell
celery -A app.workers.celery_app worker --loglevel=info
```

## API Documentation

Once running, visit:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Testing

```powershell
pytest
pytest --cov=app tests/
```

## Project Structure

- `app/core/` - Core configuration and utilities
- `app/models/` - Database models
- `app/schemas/` - Pydantic schemas
- `app/routers/` - API endpoints
- `app/services/` - Business logic
- `app/workers/` - Celery tasks
- `app/utils/` - Helper functions
- `tests/` - Test suite
