"""
Business Card Text Parser.

Parses raw OCR text to extract structured contact information
including name, company, job title, phone, email, and website.
"""

import re
from typing import Dict, Optional, List
import phonenumbers
from email_validator import validate_email, EmailNotValidError
import logging

logger = logging.getLogger(__name__)

# Regex patterns
EMAIL_REGEX = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
)

WEBSITE_REGEX = re.compile(
    r'(?:https?://)?(?:www\.)?([A-Za-z0-9-]+\.[A-Za-z]{2,}(?:\.[A-Za-z]{2,})?)',
    re.IGNORECASE
)

# Job title keywords (English and Arabic)
JOB_KEYWORDS_EN = [
    'manager', 'director', 'ceo', 'cto', 'cfo', 'coo', 'president',
    'vice', 'head', 'lead', 'senior', 'junior', 'engineer', 'developer',
    'designer', 'analyst', 'consultant', 'sales', 'marketing', 'hr',
    'finance', 'operations', 'executive', 'coordinator', 'supervisor',
    'administrator', 'specialist', 'officer', 'founder', 'owner',
    'partner', 'chief', 'architect'
]

JOB_KEYWORDS_AR = [
    'مدير', 'رئيس', 'نائب', 'مهندس', 'مطور', 'مصمم', 'محلل',
    'استشاري', 'مبيعات', 'تسويق', 'مالية', 'عمليات', 'تنفيذي',
    'منسق', 'مشرف', 'أخصائي', 'مسؤول', 'مؤسس', 'شريك', 'قائد'
]

# Company keywords
COMPANY_KEYWORDS_EN = [
    'company', 'corp', 'corporation', 'inc', 'incorporated', 'llc',
    'ltd', 'limited', 'group', 'holding', 'enterprise', 'co.'
]

COMPANY_KEYWORDS_AR = [
    'شركة', 'مؤسسة', 'مجموعة', 'القابضة', 'المحدودة'
]


def _extract_emails(text: str) -> List[str]:
    """Extract all valid email addresses from text."""
    emails = []
    matches = EMAIL_REGEX.findall(text)
    
    for match in matches:
        try:
            # Validate email
            valid = validate_email(match, check_deliverability=False)
            emails.append(valid.email)
        except EmailNotValidError:
            continue
    
    return emails


def _extract_phones(text: str, default_region: str = "SA") -> List[str]:
    """
    Extract and format phone numbers using phonenumbers library.
    
    Args:
        text: Raw text containing phone numbers
        default_region: Default country code (ISO 3166-1 alpha-2)
    """
    phones = []
    
    # Find potential phone numbers
    for match in phonenumbers.PhoneNumberMatcher(text, default_region):
        try:
            # Format in international format
            formatted = phonenumbers.format_number(
                match.number,
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            phones.append(formatted)
        except Exception as e:
            logger.warning(f"Failed to format phone number: {e}")
            continue
    
    return phones


def _extract_websites(text: str) -> List[str]:
    """Extract website URLs from text."""
    websites = []
    matches = WEBSITE_REGEX.findall(text)
    
    for match in matches:
        # Clean up and normalize
        website = match.lower().strip()
        if website and website not in websites:
            websites.append(website)
    
    return websites


def _is_likely_job_title(line: str) -> bool:
    """Check if a line likely contains a job title."""
    line_lower = line.lower()
    
    # Check English keywords
    for keyword in JOB_KEYWORDS_EN:
        if keyword in line_lower:
            return True
    
    # Check Arabic keywords
    for keyword in JOB_KEYWORDS_AR:
        if keyword in line:
            return True
    
    return False


def _is_likely_company(line: str) -> bool:
    """Check if a line likely contains a company name."""
    line_lower = line.lower()
    
    # Check English keywords
    for keyword in COMPANY_KEYWORDS_EN:
        if keyword in line_lower:
            return True
    
    # Check Arabic keywords
    for keyword in COMPANY_KEYWORDS_AR:
        if keyword in line:
            return True
    
    return False


def _clean_lines(text: str) -> List[str]:
    """Split text into clean, non-empty lines."""
    lines = []
    for line in text.split('\n'):
        clean = line.strip()
        if clean:
            lines.append(clean)
    return lines


def parse_business_card_text(
    raw_text: str,
    default_region: str = "SA"
) -> Dict[str, Optional[str]]:
    """
    Parse raw OCR text to extract business card fields.
    
    Uses heuristics and regex patterns to identify:
    - Name (typically first non-numeric line)
    - Company (lines with company keywords)
    - Job title (lines with job-related keywords)
    - Phone numbers (validated and formatted)
    - Email addresses (validated)
    - Website URLs
    
    Args:
        raw_text: Raw text from OCR
        default_region: Default country code for phone parsing (ISO 3166-1 alpha-2)
        
    Returns:
        Dictionary with extracted fields:
        {
            "name": "...",
            "company": "...",
            "job_title": "...",
            "phone": "...",        # First phone number found
            "email": "...",        # First email found
            "website": "...",      # First website found
            "raw_text": raw_text   # Original text preserved
        }
        
    Note:
        This is a simple heuristic-based parser. For production use,
        consider using machine learning models for better accuracy.
        
    Example:
        >>> text = '''John Smith
        ... Senior Manager
        ... ABC Corporation
        ... john@abc.com
        ... +966 50 123 4567'''
        >>> result = parse_business_card_text(text)
        >>> print(result['name'])
        John Smith
    """
    logger.debug(f"Parsing business card text: {len(raw_text)} chars")
    
    # Initialize result
    result = {
        "name": None,
        "company": None,
        "job_title": None,
        "phone": None,
        "email": None,
        "website": None,
        "raw_text": raw_text
    }
    
    if not raw_text.strip():
        return result
    
    # Extract structured data
    emails = _extract_emails(raw_text)
    phones = _extract_phones(raw_text, default_region)
    websites = _extract_websites(raw_text)
    
    # Assign first found items
    result["email"] = emails[0] if emails else None
    result["phone"] = phones[0] if phones else None
    result["website"] = websites[0] if websites else None
    
    # Parse lines for name, company, job title
    lines = _clean_lines(raw_text)
    
    if not lines:
        return result
    
    # Simple heuristics (TODO: Improve with ML model)
    # 1. First non-numeric, non-email, non-URL line is likely the name
    for i, line in enumerate(lines):
        # Skip if contains email, phone, or website
        if (
            any(email in line for email in emails) or
            any(phone in line for phone in phones) or
            any(website in line for website in websites)
        ):
            continue
        
        # Skip if mostly numbers
        if sum(c.isdigit() for c in line) > len(line) / 2:
            continue
        
        # This is likely the name
        if result["name"] is None and len(line.split()) <= 4:
            result["name"] = line
            break
    
    # 2. Find job title (line with job keywords)
    for line in lines:
        if _is_likely_job_title(line):
            result["job_title"] = line
            break
    
    # 3. Find company (line with company keywords or second line after name)
    for line in lines:
        if _is_likely_company(line):
            result["company"] = line
            break
    
    # Fallback: if no company found, use line after name
    if result["company"] is None and result["name"] and len(lines) > 1:
        name_index = lines.index(result["name"])
        if name_index + 1 < len(lines):
            potential_company = lines[name_index + 1]
            # Make sure it's not the job title
            if potential_company != result["job_title"]:
                result["company"] = potential_company
    
    logger.info(
        f"Parsed: name={bool(result['name'])}, "
        f"company={bool(result['company'])}, "
        f"job_title={bool(result['job_title'])}, "
        f"email={bool(result['email'])}, "
        f"phone={bool(result['phone'])}"
    )
    
    return result
