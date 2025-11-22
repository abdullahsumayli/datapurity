"""
Configuration Module for DataPurity Core
========================================

Provides centralized configuration management using Pydantic Settings.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Global configuration settings for DataPurity cleaning engine.
    
    Attributes:
        DEFAULT_COUNTRY_CODE: Default country code for phone normalization (ISO 3166-1 alpha-2)
        MIN_PHONE_DIGITS: Minimum number of digits required for a valid phone number
        MIN_VALID_NAME_LEN: Minimum character length for a valid name
        MIN_EMAIL_LEN: Minimum character length for a valid email
        BAD_EMAIL_DOMAINS: List of email domains to filter out
        ENABLE_FUZZY_DEDUP: Enable fuzzy deduplication using similarity matching
        FUZZY_NAME_THRESHOLD: Similarity threshold (0-100) for fuzzy name matching
        FUZZY_NAME_COMPANY_THRESHOLD: Similarity threshold for name+company matching
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    
    # Phone configuration
    DEFAULT_COUNTRY_CODE: str = "SA"
    MIN_PHONE_DIGITS: int = 8
    
    # Name configuration
    MIN_VALID_NAME_LEN: int = 3
    
    # Email configuration
    MIN_EMAIL_LEN: int = 5
    BAD_EMAIL_DOMAINS: list[str] = [
        "example.com",
        "test.com",
        "mail.com",
        "temp-mail.com",
        "tempmail.com",
        "10minutemail.com"
    ]
    
    # Deduplication configuration
    ENABLE_FUZZY_DEDUP: bool = True
    FUZZY_NAME_THRESHOLD: int = 90
    FUZZY_NAME_COMPANY_THRESHOLD: int = 85
    
    # Logging configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        """Pydantic configuration"""
        env_prefix = "DATAPURITY_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance (singleton pattern).
    
    Returns:
        Settings: Singleton settings object
    
    Example:
        >>> settings = get_settings()
        >>> print(settings.DEFAULT_COUNTRY_CODE)
        'SA'
    """
    return Settings()
