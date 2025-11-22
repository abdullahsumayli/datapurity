"""
Statistics Calculation for DataPurity Core
==========================================

Functions for building cleaning statistics.
"""

import logging
from typing import Any
import pandas as pd

from datapurity_core.models import CleaningStats

logger = logging.getLogger(__name__)


def build_stats(
    df_original: pd.DataFrame,
    df_after_drop_duplicates: pd.DataFrame,
    df_final: pd.DataFrame,
    phone_valid_flags: list[bool],
    email_valid_flags: list[bool]
) -> CleaningStats:
    """
    Build comprehensive cleaning statistics.
    
    Args:
        df_original: Original DataFrame before cleaning
        df_after_drop_duplicates: DataFrame after dropping duplicates
        df_final: Final cleaned DataFrame
        phone_valid_flags: List of phone validation flags
        email_valid_flags: List of email validation flags
        
    Returns:
        CleaningStats object with all statistics
        
    Example:
        >>> df_orig = pd.DataFrame({"name": ["A", "A", "B"]})
        >>> df_after_drop = pd.DataFrame({"name": ["A", "B"]})
        >>> df_final = pd.DataFrame({
        ...     "name": ["A", "B"],
        ...     "quality_score": [80, 90]
        ... })
        >>> stats = build_stats(df_orig, df_after_drop, df_final, [True, False], [True, True])
    """
    # Basic counts
    rows_original = len(df_original)
    rows_after_drop = len(df_after_drop_duplicates)
    rows_final = len(df_final)
    duplicates_removed = rows_original - rows_after_drop
    empty_rows_removed = rows_after_drop - rows_final
    
    # Validation counts
    phone_valid_count = sum(phone_valid_flags) if phone_valid_flags else 0
    phone_invalid_count = len(phone_valid_flags) - phone_valid_count if phone_valid_flags else 0
    
    email_valid_count = sum(email_valid_flags) if email_valid_flags else 0
    email_invalid_count = len(email_valid_flags) - email_valid_count if email_valid_flags else 0
    
    # Quality scores
    avg_quality_score = 0.0
    if "quality_score" in df_final.columns and len(df_final) > 0:
        avg_quality_score = float(df_final["quality_score"].mean())
    
    stats = CleaningStats(
        rows_original=rows_original,
        rows_after_drop_duplicates=rows_after_drop,
        rows_final=rows_final,
        duplicates_removed=duplicates_removed,
        empty_rows_removed=empty_rows_removed,
        invalid_phones=phone_invalid_count,
        invalid_emails=email_invalid_count,
        avg_quality_score=avg_quality_score,
        fuzzy_duplicate_clusters=0  # Updated by deduplication module if needed
    )
    
    logger.info("Statistics computed:")
    logger.info(f"  - Original rows: {rows_original}")
    logger.info(f"  - Final rows: {rows_final}")
    logger.info(f"  - Duplicates removed: {duplicates_removed}")
    logger.info(f"  - Empty rows removed: {empty_rows_removed}")
    logger.info(f"  - Valid phones: {phone_valid_count}")
    logger.info(f"  - Invalid phones: {phone_invalid_count}")
    logger.info(f"  - Valid emails: {email_valid_count}")
    logger.info(f"  - Invalid emails: {email_invalid_count}")
    logger.info(f"  - Avg quality score: {avg_quality_score:.1f}")
    
    return stats
