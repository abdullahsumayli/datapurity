"""
Cleaning and Normalization Logic for DataPurity Core
===================================================

Functions for cleaning, normalizing, and validating contact data fields.
"""

import re
import logging
from typing import Any
import pandas as pd
import phonenumbers
from phonenumbers import NumberParseException

from datapurity_core.config import Settings
from datapurity_core.models import CleaningStats
from datapurity_core import deduplication, scoring, stats, io_utils

logger = logging.getLogger(__name__)


# Bad name patterns to reject
BAD_NAME_PATTERNS = [
    "na", "n/a", "test", "dummy", "unknown", "none", "null",
    "غير معروف", "بدون", "لا يوجد", "مجهول", "تست", "تجربة"
]


def clean_text(value: Any) -> str:
    """
    Clean and normalize text value.
    
    Handles:
    - None/NaN values
    - Whitespace trimming
    - Zero-width and control character removal
    - Multiple space collapsing
    
    Args:
        value: Input value (any type)
        
    Returns:
        Cleaned text string
        
    Example:
        >>> clean_text("  Ahmed   Mohamed  ")
        'Ahmed Mohamed'
        >>> clean_text(None)
        ''
    """
    if pd.isna(value) or value is None:
        return ""
    
    text = str(value).strip()
    
    # Remove zero-width characters and control characters
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e\ufeff]', '', text)
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def normalize_name(name: str) -> str:
    """
    Normalize person name.
    
    Args:
        name: Raw name string
        
    Returns:
        Normalized name
        
    Example:
        >>> normalize_name("  ahmed   mohamed  ")
        'Ahmed Mohamed'
    """
    name = clean_text(name)
    
    if not name:
        return ""
    
    # Title case for better formatting (works reasonably for Arabic and English)
    # Note: For Arabic, this won't capitalize but will preserve the text
    parts = name.split()
    normalized_parts = []
    
    for part in parts:
        # Only title-case if it looks like English (ASCII)
        if part.isascii():
            normalized_parts.append(part.title())
        else:
            normalized_parts.append(part)
    
    return " ".join(normalized_parts)


def extract_digits(value: str) -> str:
    """
    Extract only numeric digits from string.
    
    Args:
        value: Input string
        
    Returns:
        String containing only digits
        
    Example:
        >>> extract_digits("+966-50-123-4567")
        '966501234567'
    """
    if not value:
        return ""
    
    return re.sub(r'\D', '', str(value))


def normalize_phone(phone: str, default_country_code: str) -> tuple[str | None, bool]:
    """
    Normalize and validate phone number to E.164 format.
    
    Uses phonenumbers library with fallback logic for Saudi numbers.
    
    Args:
        phone: Raw phone number
        default_country_code: ISO country code (e.g., "SA")
        
    Returns:
        Tuple of (normalized_phone, is_valid)
        - normalized_phone: E.164 format (e.g., "+966501234567") or None
        - is_valid: Boolean indicating if phone is valid
        
    Example:
        >>> normalize_phone("0501234567", "SA")
        ('+966501234567', True)
        >>> normalize_phone("invalid", "SA")
        (None, False)
    """
    phone = clean_text(phone)
    
    if not phone:
        return (None, False)
    
    try:
        # Parse with phonenumbers library
        parsed = phonenumbers.parse(phone, default_country_code)
        
        # Validate
        is_valid = phonenumbers.is_valid_number(parsed)
        
        if is_valid:
            # Format to E.164
            e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            return (e164, True)
        else:
            return (None, False)
            
    except NumberParseException:
        # Fallback for Saudi numbers
        if default_country_code == "SA":
            digits = extract_digits(phone)
            
            # Saudi mobile: 9 digits starting with 5
            # Or 10 digits starting with 05
            if len(digits) == 9 and digits[0] == '5':
                normalized = f"+966{digits}"
                return (normalized, True)
            elif len(digits) == 10 and digits[:2] == '05':
                normalized = f"+966{digits[1:]}"
                return (normalized, True)
        
        return (None, False)


def normalize_email(email: str, bad_domains: list[str]) -> tuple[str | None, bool]:
    """
    Normalize and validate email address.
    
    Args:
        email: Raw email address
        bad_domains: List of domains to reject
        
    Returns:
        Tuple of (normalized_email, is_valid)
        
    Example:
        >>> normalize_email("Ahmed@Example.COM", ["test.com"])
        ('ahmed@example.com', True)
        >>> normalize_email("invalid-email", [])
        (None, False)
    """
    email = clean_text(email).lower()
    
    if not email:
        return (None, False)
    
    # Simple email regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return (None, False)
    
    # Check bad domains
    domain = email.split('@')[1] if '@' in email else ""
    
    if domain in bad_domains:
        return (None, False)
    
    return (email, True)


def is_good_name(name: str, min_len: int) -> bool:
    """
    Check if name is valid and meaningful.
    
    Rejects:
    - Too short names
    - Common placeholder names (test, dummy, etc.)
    - Arabic placeholder names
    
    Args:
        name: Name to check
        min_len: Minimum acceptable length
        
    Returns:
        True if name is good, False otherwise
        
    Example:
        >>> is_good_name("Ahmed Mohamed", 3)
        True
        >>> is_good_name("na", 3)
        False
    """
    name = name.strip().lower()
    
    if len(name) < min_len:
        return False
    
    # Check against bad patterns
    for bad_pattern in BAD_NAME_PATTERNS:
        if bad_pattern in name:
            return False
    
    return True


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure all required columns exist in DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with all required columns
    """
    required_columns = ["name", "phone", "email", "company", "job_title", "city", "notes"]
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""
    
    return df


def clean_contacts_df(df: pd.DataFrame, settings: Settings) -> tuple[pd.DataFrame, CleaningStats]:
    """
    Main cleaning pipeline for contact DataFrame.
    
    Steps:
    1. Normalize column names
    2. Ensure required columns exist
    3. Clean all text fields
    4. Normalize names
    5. Normalize phone numbers
    6. Normalize emails
    7. Mark duplicates
    8. Remove hard duplicates
    9. Compute quality scores
    10. Remove empty rows
    11. Generate statistics
    
    Args:
        df: Input DataFrame with raw contacts
        settings: Configuration settings
        
    Returns:
        Tuple of (cleaned_df, stats)
        
    Example:
        >>> from datapurity_core.config import get_settings
        >>> settings = get_settings()
        >>> df = pd.DataFrame({"الاسم": ["أحمد"], "الجوال": ["0501234567"]})
        >>> cleaned_df, stats = clean_contacts_df(df, settings)
    """
    logger.info("=" * 60)
    logger.info("Starting contact cleaning pipeline")
    logger.info(f"Input rows: {len(df)}")
    
    # Store original for stats
    df_original = df.copy()
    rows_original = len(df)
    
    # Step 1: Normalize column names
    logger.info("Step 1: Normalizing column names")
    df = io_utils.normalize_column_names(df)
    
    # Step 2: Ensure required columns
    logger.info("Step 2: Ensuring required columns")
    df = ensure_columns(df)
    
    # Step 3: Clean all text columns
    logger.info("Step 3: Cleaning text fields")
    text_columns = ["name", "phone", "email", "company", "job_title", "city", "notes"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    
    # Step 4: Normalize names
    logger.info("Step 4: Normalizing names")
    df["name"] = df["name"].apply(normalize_name)
    
    # Step 5: Normalize phone numbers
    logger.info("Step 5: Normalizing phone numbers")
    phone_results = df["phone"].apply(
        lambda x: normalize_phone(x, settings.DEFAULT_COUNTRY_CODE)
    )
    df["phone"] = phone_results.apply(lambda x: x[0])
    df["phone_valid"] = phone_results.apply(lambda x: x[1])
    
    invalid_phones = (~df["phone_valid"]).sum()
    logger.info(f"  - Invalid phones: {invalid_phones}")
    
    # Step 6: Normalize emails
    logger.info("Step 6: Normalizing emails")
    email_results = df["email"].apply(
        lambda x: normalize_email(x, settings.BAD_EMAIL_DOMAINS)
    )
    df["email"] = email_results.apply(lambda x: x[0])
    df["email_valid"] = email_results.apply(lambda x: x[1])
    
    invalid_emails = (~df["email_valid"]).sum()
    logger.info(f"  - Invalid emails: {invalid_emails}")
    
    # Step 7: Mark duplicates
    logger.info("Step 7: Marking duplicates")
    df = deduplication.mark_duplicates(df, settings)
    
    # Step 8: Remove hard duplicates
    logger.info("Step 8: Removing hard duplicates")
    df_after_drop = deduplication.drop_hard_duplicates(df)
    rows_after_drop = len(df_after_drop)
    duplicates_removed = len(df) - rows_after_drop
    logger.info(f"  - Removed {duplicates_removed} hard duplicates")
    
    df = df_after_drop
    
    # Step 9: Compute quality scores
    logger.info("Step 9: Computing quality scores")
    df["quality_score"] = df.apply(
        lambda row: scoring.compute_quality_score(row, settings),
        axis=1
    )
    
    avg_score = df["quality_score"].mean()
    logger.info(f"  - Average quality score: {avg_score:.1f}")
    
    # Step 10: Remove empty rows
    logger.info("Step 10: Removing empty/invalid rows")
    
    # A row is empty if:
    # - No phone
    # - No email
    # - AND name is not good
    rows_before_empty_removal = len(df)
    
    df = df[
        (df["phone"].notna()) | 
        (df["email"].notna()) | 
        (df["name"].apply(lambda n: is_good_name(n, settings.MIN_VALID_NAME_LEN)))
    ]
    
    empty_rows_removed = rows_before_empty_removal - len(df)
    logger.info(f"  - Removed {empty_rows_removed} empty rows")
    
    # Reset index
    df = df.reset_index(drop=True)
    df["id"] = df.index
    
    rows_final = len(df)
    
    # Step 11: Generate statistics
    logger.info("Step 11: Generating statistics")
    cleaning_stats = stats.build_stats(
        df_original=df_original,
        df_after_drop_duplicates=df_after_drop,
        df_final=df,
        phone_valid_flags=df["phone_valid"].tolist(),
        email_valid_flags=df["email_valid"].tolist()
    )
    
    logger.info("=" * 60)
    logger.info("Cleaning pipeline completed")
    logger.info(f"Final rows: {rows_final} (from {rows_original})")
    logger.info(f"Average quality score: {cleaning_stats.avg_quality_score:.1f}")
    logger.info("=" * 60)
    
    return df, cleaning_stats
