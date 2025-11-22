"""
Deduplication Logic for DataPurity Core
=======================================

Functions for detecting and removing duplicate contacts using:
- Hard deduplication (exact phone/email matches)
- Fuzzy deduplication (name similarity with RapidFuzz)
"""

import logging
from typing import Any
import pandas as pd
from rapidfuzz import fuzz

from datapurity_core.config import Settings

logger = logging.getLogger(__name__)


def mark_duplicates(df: pd.DataFrame, settings: Settings) -> pd.DataFrame:
    """
    Mark duplicates in DataFrame using both hard and fuzzy matching.
    
    Hard duplicates:
    - Same phone number
    - Same email address
    
    Fuzzy duplicates:
    - Similar names (using Levenshtein ratio)
    - Threshold controlled by settings
    
    Adds columns:
    - is_duplicate: Boolean flag
    - duplicate_group_id: Group ID for related duplicates
    - duplicate_reason: Reason for duplication
    
    Args:
        df: Input DataFrame
        settings: Configuration settings
        
    Returns:
        DataFrame with duplicate flags
        
    Example:
        >>> df = pd.DataFrame({
        ...     "name": ["Ahmed Ali", "Ahmed Ali"],
        ...     "phone": ["+966501234567", "+966501234567"]
        ... })
        >>> marked_df = mark_duplicates(df, settings)
        >>> marked_df["is_duplicate"].tolist()
        [False, True]
    """
    logger.info("Marking duplicates")
    
    # Initialize duplicate columns
    df["is_duplicate"] = False
    df["duplicate_group_id"] = None
    df["duplicate_reason"] = ""
    
    # Track which rows we've already marked
    marked = set()
    group_counter = 0
    
    # Hard deduplication by phone
    phone_groups = df[df["phone"].notna()].groupby("phone")
    
    for phone, group_df in phone_groups:
        if len(group_df) > 1:
            indices = group_df.index.tolist()
            
            # First occurrence is not duplicate
            first_idx = indices[0]
            
            # Mark rest as duplicates
            for idx in indices[1:]:
                if idx not in marked:
                    df.at[idx, "is_duplicate"] = True
                    df.at[idx, "duplicate_group_id"] = group_counter
                    df.at[idx, "duplicate_reason"] = f"phone:{phone}"
                    marked.add(idx)
            
            # Also assign group ID to first occurrence (even though not marked as duplicate)
            df.at[first_idx, "duplicate_group_id"] = group_counter
            
            group_counter += 1
    
    logger.info(f"  - Found {len(marked)} phone duplicates")
    
    # Hard deduplication by email
    email_marked_count = 0
    email_groups = df[df["email"].notna()].groupby("email")
    
    for email, group_df in email_groups:
        if len(group_df) > 1:
            indices = group_df.index.tolist()
            
            # First occurrence is not duplicate
            first_idx = indices[0]
            
            # Mark rest as duplicates
            for idx in indices[1:]:
                if idx not in marked:
                    df.at[idx, "is_duplicate"] = True
                    df.at[idx, "duplicate_group_id"] = group_counter
                    df.at[idx, "duplicate_reason"] = f"email:{email}"
                    marked.add(idx)
                    email_marked_count += 1
            
            # Also assign group ID to first occurrence
            if df.at[first_idx, "duplicate_group_id"] is None:
                df.at[first_idx, "duplicate_group_id"] = group_counter
            
            group_counter += 1
    
    logger.info(f"  - Found {email_marked_count} additional email duplicates")
    
    # Fuzzy deduplication by name (optional)
    if settings.ENABLE_FUZZY_DEDUP:
        logger.info("  - Running fuzzy name matching")
        fuzzy_marked_count = 0
        
        # Only check rows not already marked
        unmarked_df = df[~df.index.isin(marked)]
        
        # Filter to rows with valid names
        valid_names_df = unmarked_df[
            unmarked_df["name"].notna() & (unmarked_df["name"].str.len() >= settings.MIN_VALID_NAME_LEN)
        ]
        
        if len(valid_names_df) > 1:
            # Compare each pair
            names = valid_names_df["name"].tolist()
            indices = valid_names_df.index.tolist()
            
            for i in range(len(names)):
                if indices[i] in marked:
                    continue
                
                for j in range(i + 1, len(names)):
                    if indices[j] in marked:
                        continue
                    
                    # Calculate similarity
                    similarity = fuzz.ratio(names[i], names[j])
                    
                    if similarity >= settings.FUZZY_NAME_THRESHOLD:
                        # Mark second as duplicate
                        idx_j = indices[j]
                        df.at[idx_j, "is_duplicate"] = True
                        df.at[idx_j, "duplicate_group_id"] = group_counter
                        df.at[idx_j, "duplicate_reason"] = f"fuzzy_name:{similarity}%"
                        marked.add(idx_j)
                        fuzzy_marked_count += 1
                        
                        # Assign group to first if needed
                        idx_i = indices[i]
                        if df.at[idx_i, "duplicate_group_id"] is None:
                            df.at[idx_i, "duplicate_group_id"] = group_counter
                        
                        group_counter += 1
        
        logger.info(f"  - Found {fuzzy_marked_count} fuzzy name duplicates")
    
    total_duplicates = len(marked)
    logger.info(f"Total duplicates marked: {total_duplicates}")
    
    return df


def drop_hard_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows marked as duplicates.
    
    Args:
        df: DataFrame with duplicate flags
        
    Returns:
        DataFrame with duplicates removed
        
    Example:
        >>> df = pd.DataFrame({
        ...     "name": ["Ahmed", "Ahmed"],
        ...     "is_duplicate": [False, True]
        ... })
        >>> clean_df = drop_hard_duplicates(df)
        >>> len(clean_df)
        1
    """
    rows_before = len(df)
    
    # Remove rows marked as duplicate
    df_clean = df[~df["is_duplicate"]].copy()
    
    rows_after = len(df_clean)
    removed = rows_before - rows_after
    
    logger.info(f"Dropped {removed} duplicate rows ({rows_before} → {rows_after})")
    
    return df_clean
