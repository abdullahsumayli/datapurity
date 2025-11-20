"""Application configuration and constants."""

# API version
API_V1_STR = "/api/v1"

# JWT token settings
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Database
DATABASE_POOL_SIZE = 5
DATABASE_MAX_OVERFLOW = 10

# File upload limits
MAX_UPLOAD_SIZE_MB = 100
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

# OCR settings
OCR_SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".pdf"}

# Celery task timeouts
TASK_TIMEOUT_SECONDS = 3600  # 1 hour

# Data cleaning thresholds
MIN_CONFIDENCE_SCORE = 0.7
DEFAULT_BATCH_SIZE = 1000
