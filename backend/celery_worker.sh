#!/bin/bash
# Celery worker startup script

# Set environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start Celery worker
celery -A app.workers.celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --max-tasks-per-child=1000 \
    --time-limit=3600 \
    --soft-time-limit=3300
