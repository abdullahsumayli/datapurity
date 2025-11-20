"""Email utilities."""

import re
from typing import Optional


# Basic email regex pattern
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


def validate_email_format(email: str) -> bool:
    """
    Validate email format using regex.

    TODO: Improve with more sophisticated validation
    """
    return bool(EMAIL_REGEX.match(email))


def validate_email_domain(email: str) -> bool:
    """
    Validate email domain (DNS check).

    TODO: Implement the following:
    - Extract domain from email
    - Perform DNS MX record lookup
    - Return True if domain has MX records
    """
    raise NotImplementedError("Email domain validation not yet implemented")


def is_disposable_email(email: str) -> bool:
    """
    Check if email is from a disposable email service.

    TODO: Implement the following:
    - Maintain list of disposable domains
    - Check against list
    - Return True if disposable
    """
    raise NotImplementedError("Disposable email check not yet implemented")


def normalize_email(email: str) -> str:
    """
    Normalize email address.

    TODO: Implement the following:
    - Convert to lowercase
    - Remove dots from Gmail addresses (except before @)
    - Handle + aliases
    - Return normalized email
    """
    return email.lower().strip()


def extract_emails(text: str) -> list[str]:
    """
    Extract email addresses from text.

    TODO: Implement the following:
    - Use regex to find email patterns
    - Validate each match
    - Return list of valid emails
    """
    raise NotImplementedError("Email extraction not yet implemented")
