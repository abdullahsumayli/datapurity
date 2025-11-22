"""
Quality Scoring for DataPurity Core
===================================

Functions for computing contact quality scores.
"""

import logging
from typing import Any
import pandas as pd

from datapurity_core.config import Settings

logger = logging.getLogger(__name__)


def compute_quality_score(row: pd.Series, settings: Settings) -> int:
    """
    Compute quality score (0-100) for a contact record.
    
    Scoring breakdown:
    - Phone valid: 30 points
    - Email valid: 30 points
    - Name valid: 20 points
    - Company provided: 10 points
    - Job title provided: 5 points
    - City provided: 5 points
    
    Args:
        row: Contact row from DataFrame
        settings: Configuration settings
        
    Returns:
        Quality score (0-100)
        
    Example:
        >>> from datapurity_core.config import get_settings
        >>> settings = get_settings()
        >>> row = pd.Series({
        ...     "phone_valid": True,
        ...     "email_valid": True,
        ...     "name": "Ahmed Mohamed",
        ...     "company": "Acme Corp",
        ...     "job_title": "",
        ...     "city": "Riyadh"
        ... })
        >>> score = compute_quality_score(row, settings)
        >>> score
        85
    """
    score = 0
    
    # Phone (30 points)
    if row.get("phone_valid", False):
        score += 30
    
    # Email (30 points)
    if row.get("email_valid", False):
        score += 30
    
    # Name (20 points)
    name = row.get("name", "")
    if isinstance(name, str) and len(name.strip()) >= settings.MIN_VALID_NAME_LEN:
        score += 20
    
    # Company (10 points)
    company = row.get("company", "")
    if isinstance(company, str) and len(company.strip()) > 0:
        score += 10
    
    # Job title (5 points)
    job_title = row.get("job_title", "")
    if isinstance(job_title, str) and len(job_title.strip()) > 0:
        score += 5
    
    # City (5 points)
    city = row.get("city", "")
    if isinstance(city, str) and len(city.strip()) > 0:
        score += 5
    
    return score
