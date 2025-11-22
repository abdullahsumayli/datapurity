"""
Data Models for DataPurity Core
===============================

Pydantic models representing raw contacts, cleaned contacts, and statistics.
"""

from typing import Any
from pydantic import BaseModel, Field, ConfigDict


class ContactRaw(BaseModel):
    """
    Raw contact data model accepting any fields from uploaded files.
    
    Attributes:
        name: Contact's full name
        phone: Phone number (any format)
        email: Email address
        company: Company name
        job_title: Job title/position
        city: City/location
        notes: Additional notes
    """
    
    model_config = ConfigDict(extra="allow")
    
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    company: str | None = None
    job_title: str | None = None
    city: str | None = None
    notes: str | None = None


class ContactCleaned(BaseModel):
    """
    Cleaned and validated contact data model.
    
    Attributes:
        id: Internal row index
        name: Normalized contact name
        phone: Normalized phone number (E.164 format)
        phone_valid: Whether phone number is valid
        email: Normalized email address
        email_valid: Whether email is valid
        company: Normalized company name
        job_title: Job title
        city: City name
        notes: Additional notes
        quality_score: Contact quality score (0-100)
        dup_phone: Duplicate phone flag
        dup_email: Duplicate email flag
        dup_name_company: Duplicate name+company flag (fuzzy)
        duplicate_group_id: Cluster ID for fuzzy duplicates
    """
    
    id: int | None = None
    name: str
    phone: str | None = None
    phone_valid: bool = False
    email: str | None = None
    email_valid: bool = False
    company: str | None = None
    job_title: str | None = None
    city: str | None = None
    notes: str | None = None
    quality_score: int = 0
    dup_phone: bool = False
    dup_email: bool = False
    dup_name_company: bool = False
    duplicate_group_id: str | None = None


class CleaningStats(BaseModel):
    """
    Statistics from the cleaning process.
    
    Attributes:
        rows_original: Number of rows in original file
        rows_after_drop_duplicates: Rows after hard duplicate removal
        rows_final: Final number of clean rows
        duplicates_removed: Number of duplicate rows removed
        empty_rows_removed: Number of empty/invalid rows removed
        invalid_phones: Count of invalid phone numbers
        invalid_emails: Count of invalid emails
        avg_quality_score: Average quality score of final dataset
        fuzzy_duplicate_clusters: Number of fuzzy duplicate groups found
    """
    
    rows_original: int = 0
    rows_after_drop_duplicates: int = 0
    rows_final: int = 0
    duplicates_removed: int = 0
    empty_rows_removed: int = 0
    invalid_phones: int = 0
    invalid_emails: int = 0
    avg_quality_score: float = 0.0
    fuzzy_duplicate_clusters: int = 0
