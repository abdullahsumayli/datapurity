"""
DataPurity Core - Contact Data Cleaning Engine
=============================================

A production-grade module for cleaning, normalizing, scoring, and deduplicating
contact data for Arabic + English markets.

Modules:
    - config: Configuration settings
    - models: Pydantic data models
    - io_utils: File I/O utilities
    - cleaning: Core cleaning and normalization logic
    - deduplication: Duplicate detection and removal
    - scoring: Contact quality scoring
    - stats: Statistics generation

Example:
    >>> from datapurity_core.config import get_settings
    >>> from datapurity_core.cleaning import clean_contacts_df
    >>> from datapurity_core.io_utils import load_contacts_file
    >>> 
    >>> settings = get_settings()
    >>> df = load_contacts_file("contacts.xlsx")
    >>> cleaned_df, stats = clean_contacts_df(df, settings)
"""

__version__ = "1.0.0"
__author__ = "DataPurity Team"

from datapurity_core.config import get_settings
from datapurity_core.models import ContactRaw, ContactCleaned, CleaningStats
from datapurity_core.cleaning import clean_contacts_df
from datapurity_core.io_utils import load_contacts_file, save_contacts_file

__all__ = [
    "get_settings",
    "ContactRaw",
    "ContactCleaned",
    "CleaningStats",
    "clean_contacts_df",
    "load_contacts_file",
    "save_contacts_file",
]
