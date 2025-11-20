"""Celery application configuration."""

from celery import Celery
from app.core.settings import get_settings

settings = get_settings()

# Create Celery instance
celery_app = Celery(
    "datapurity",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3300,  # 55 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Import tasks to register them
from app.workers import tasks_datasets  # noqa: F401, E402
from app.workers import tasks_cards  # noqa: F401, E402
from app.workers import tasks_exports  # noqa: F401, E402
