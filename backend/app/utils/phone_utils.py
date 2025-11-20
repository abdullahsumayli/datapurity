"""Phone number utilities."""

import re
from typing import Optional, Tuple


def validate_phone(phone: str, country_code: str = "US") -> bool:
    """
    Validate phone number for a specific country.

    TODO: Implement the following:
    - Use phonenumbers library
    - Parse and validate
    - Return True/False
    """
    raise NotImplementedError("Phone validation not yet implemented")


def format_phone(phone: str, country_code: str = "US", format_type: str = "E164") -> Optional[str]:
    """
    Format phone number to standard format.

    TODO: Implement the following:
    - Parse phone number
    - Format to E164, INTERNATIONAL, or NATIONAL
    - Return formatted string or None if invalid
    """
    raise NotImplementedError("Phone formatting not yet implemented")


def normalize_phone(phone: str) -> str:
    """
    Normalize phone number (remove non-numeric characters).

    TODO: Implement the following:
    - Remove spaces, dashes, parentheses
    - Keep only digits and + sign
    - Return normalized string
    """
    return re.sub(r"[^\d+]", "", phone)


def extract_phone_numbers(text: str) -> list[str]:
    """
    Extract phone numbers from text.

    TODO: Implement the following:
    - Use regex patterns for common phone formats
    - Extract all matches
    - Return list of potential phone numbers
    """
    raise NotImplementedError("Phone extraction not yet implemented")
