"""
Production-grade OCR pipeline for business cards (Arabic + English).
Uses EasyOCR + OpenCV for high-quality extraction.
"""

import re
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, Any
from io import BytesIO

import cv2
import numpy as np
import easyocr
from PIL import Image

# Initialize logger
logger = logging.getLogger(__name__)

# Global EasyOCR reader (initialized once for performance)
_reader: Optional[easyocr.Reader] = None


def get_reader() -> easyocr.Reader:
    """Get or initialize EasyOCR reader (singleton pattern)."""
    global _reader
    if _reader is None:
        logger.info("Initializing EasyOCR reader for Arabic and English...")
        _reader = easyocr.Reader(['ar', 'en'], gpu=False)
        logger.info("EasyOCR reader initialized successfully")
    return _reader


@dataclass
class BusinessCardData:
    """Structured business card data."""
    
    full_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    mobile: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    other_lines: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None and empty values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                if isinstance(value, list):
                    if value:  # Only include non-empty lists
                        result[key] = value
                elif isinstance(value, str):
                    if value.strip():  # Only include non-empty strings
                        result[key] = value.strip()
                else:
                    result[key] = value
        return result


# =====================================================================
# IMAGE PROCESSING
# =====================================================================

def _load_image_from_bytes(content: bytes) -> np.ndarray:
    """Load image from bytes and convert to OpenCV format."""
    try:
        # Load via Pillow
        pil_image = Image.open(BytesIO(content)).convert("RGB")
        # Convert to numpy array (RGB)
        np_image = np.array(pil_image)
        # Convert RGB to BGR for OpenCV
        bgr_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        return bgr_image
    except Exception as e:
        logger.error(f"Failed to load image: {e}")
        raise ValueError(f"Invalid image data: {e}")


def _preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for better OCR quality.
    
    Steps:
    1. Convert to grayscale
    2. Apply CLAHE for contrast enhancement
    3. Denoise with median blur
    """
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Denoise
        denoised = cv2.medianBlur(enhanced, 3)
        
        return denoised
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        return image


def _try_different_orientations(image: np.ndarray, reader: easyocr.Reader) -> tuple[list[str], list[tuple], float]:
    """
    Try different image orientations and return the best result.
    
    Returns:
        (lines, raw_results, avg_confidence)
    """
    orientations = [
        (0, image),
        (90, cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)),
        (180, cv2.rotate(image, cv2.ROTATE_180)),
        (270, cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)),
    ]
    
    best_result = ([], [], 0.0)
    best_confidence = 0.0
    
    for angle, rotated_img in orientations:
        try:
            results = reader.readtext(rotated_img, detail=1, paragraph=False)
            
            if not results:
                continue
            
            # Calculate average confidence
            confidences = [conf for (_, _, conf) in results]
            avg_conf = sum(confidences) / len(confidences) if confidences else 0
            
            # Extract lines
            lines = [text.strip() for (_, text, _) in results if text.strip()]
            
            if avg_conf > best_confidence:
                best_confidence = avg_conf
                best_result = (lines, results, avg_conf)
                logger.debug(f"Orientation {angle}°: confidence={avg_conf:.2f}, lines={len(lines)}")
        
        except Exception as e:
            logger.warning(f"OCR failed for orientation {angle}°: {e}")
            continue
    
    return best_result


# =====================================================================
# OCR EXTRACTION
# =====================================================================

def ocr_business_card_from_bytes(content: bytes) -> tuple[list[str], list[tuple]]:
    """
    Perform OCR on business card image.
    
    Args:
        content: Image bytes
    
    Returns:
        (lines, raw_results)
        - lines: List of cleaned text lines
        - raw_results: Raw EasyOCR results [(bbox, text, confidence), ...]
    """
    reader = get_reader()
    
    # Load and preprocess
    image = _load_image_from_bytes(content)
    preprocessed = _preprocess_image(image)
    
    # Try different orientations
    lines, raw_results, avg_conf = _try_different_orientations(preprocessed, reader)
    
    logger.info(f"OCR extracted {len(lines)} lines with avg confidence {avg_conf:.2f}")
    
    # Clean lines
    cleaned_lines = []
    for line in lines:
        # Remove bullet points and excessive punctuation
        cleaned = re.sub(r'^[•·∙◦▪▫-]+\s*', '', line)
        cleaned = cleaned.strip('.,;:!?-—')
        if cleaned:
            cleaned_lines.append(cleaned)
    
    return cleaned_lines, raw_results


# =====================================================================
# FIELD EXTRACTION & PARSING
# =====================================================================

# Regex patterns
EMAIL_PATTERN = re.compile(r'[A-Za-z0-9.+_-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', re.IGNORECASE)
URL_PATTERN = re.compile(
    r'(?:http[s]?://|www\.)[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[^\s]*)?|'
    r'[A-Za-z0-9.-]+\.(?:com|net|org|sa|ae|edu|gov|io|co)\b',
    re.IGNORECASE
)
PHONE_PATTERN = re.compile(r'(\+?\d[\d\s\-\(\)]{6,}\d)')

# Company keywords
COMPANY_KEYWORDS_AR = ['شركة', 'مؤسسة', 'المحدودة', 'القابضة', 'مجموعة', 'للتجارة', 'للصناعة']
COMPANY_KEYWORDS_EN = ['Company', 'Co.', 'Ltd', 'LLC', 'Inc', 'Group', 'Holding', 'Corp', 'Corporation', 'Limited', 'Enterprise']

# Job title keywords
JOB_KEYWORDS_EN = [
    'Manager', 'Director', 'Engineer', 'Developer', 'Designer', 'Analyst', 'Consultant',
    'CEO', 'CTO', 'CFO', 'COO', 'VP', 'President', 'Vice', 'Head', 'Lead', 'Senior', 'Junior',
    'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'Technical', 'IT', 'Executive',
    'Coordinator', 'Supervisor', 'Administrator', 'Assistant', 'Specialist', 'Officer',
    'Founder', 'Owner', 'Partner', 'Principal', 'Chief', 'Architect'
]
JOB_KEYWORDS_AR = [
    'مدير', 'مهندس', 'رئيس', 'مؤسس', 'مبيعات', 'تسويق', 'استشاري', 'مشرف', 'محلل',
    'مطور', 'مصمم', 'تنفيذي', 'منسق', 'أخصائي', 'مسؤول', 'مساعد', 'شريك', 'قائد'
]

# Address keywords
ADDRESS_KEYWORDS_AR = [
    'شارع', 'طريق', 'حي', 'ص.ب', 'صندوق', 'الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة',
    'الخبر', 'الظهران', 'ينبع', 'تبوك', 'أبها', 'جيزان', 'نجران', 'حائل', 'الطائف'
]
ADDRESS_KEYWORDS_EN = [
    'Street', 'St.', 'Road', 'Rd', 'Ave', 'Avenue', 'City', 'Box', 'P.O', 'PO Box',
    'Saudi', 'Arabia', 'UAE', 'Dubai', 'Abu Dhabi', 'Riyadh', 'Jeddah', 'Dammam'
]


def _normalize_phone(phone_str: str) -> str:
    """Normalize phone number."""
    # Remove all non-digits except leading +
    digits = re.sub(r'[^\d+]', '', phone_str)
    
    # Saudi mobile normalization
    if digits.startswith('05') and len(digits) == 10:
        # 05XXXXXXXX → +9665XXXXXXXX
        return '+966' + digits[1:]
    elif digits.startswith('5') and len(digits) == 9:
        # 5XXXXXXXX → +9665XXXXXXXX
        return '+966' + digits
    elif digits.startswith('+9665'):
        return digits
    elif digits.startswith('9665'):
        return '+' + digits
    
    # Keep as-is if doesn't match Saudi mobile pattern
    return digits


def _is_likely_name(line: str) -> bool:
    """Check if line is likely a person's name."""
    # Skip if contains email/URL/numbers
    if EMAIL_PATTERN.search(line) or URL_PATTERN.search(line):
        return False
    if any(char.isdigit() for char in line):
        return False
    
    # 1-4 words, mostly letters
    words = line.split()
    if not (1 <= len(words) <= 4):
        return False
    
    # Must contain letters (Arabic or English)
    if not re.search(r'[A-Za-zء-ي]', line):
        return False
    
    return True


def _is_likely_company(line: str) -> bool:
    """Check if line is likely a company name."""
    # Check for company keywords
    for keyword in COMPANY_KEYWORDS_AR + COMPANY_KEYWORDS_EN:
        if keyword.lower() in line.lower():
            return True
    return False


def _is_likely_job_title(line: str) -> bool:
    """Check if line is likely a job title."""
    for keyword in JOB_KEYWORDS_AR + JOB_KEYWORDS_EN:
        if keyword.lower() in line.lower():
            return True
    return False


def _is_likely_address(line: str) -> bool:
    """Check if line is likely an address."""
    if len(line) < 12:
        return False
    
    for keyword in ADDRESS_KEYWORDS_AR + ADDRESS_KEYWORDS_EN:
        if keyword.lower() in line.lower():
            return True
    
    # Long lines with digits could be addresses
    if len(line) > 20 and any(c.isdigit() for c in line):
        return True
    
    return False


def parse_business_card_lines(lines: list[str]) -> BusinessCardData:
    """
    Parse OCR lines into structured business card data.
    
    Args:
        lines: List of text lines from OCR
    
    Returns:
        BusinessCardData object
    """
    data = BusinessCardData()
    
    # Extract all instances first
    emails = []
    websites = []
    phones = []
    mobiles = []
    candidates_name = []
    candidates_company = []
    candidates_job = []
    address_parts = []
    used_lines = set()
    
    for i, line in enumerate(lines):
        # Extract emails
        email_match = EMAIL_PATTERN.search(line)
        if email_match:
            email = email_match.group(0).lower()
            if email not in emails:
                emails.append(email)
            used_lines.add(i)
            continue
        
        # Extract websites/URLs
        url_match = URL_PATTERN.search(line)
        if url_match:
            url = url_match.group(0).lower()
            url = re.sub(r'^https?://', '', url)  # Remove protocol
            url = re.sub(r'^www\.', '', url)  # Remove www
            if url not in websites:
                websites.append(url)
            used_lines.add(i)
            continue
        
        # Extract phones
        phone_matches = PHONE_PATTERN.findall(line)
        if phone_matches:
            for phone in phone_matches:
                normalized = _normalize_phone(phone)
                # Classify as mobile or phone
                if '+9665' in normalized or (normalized.startswith('05') and len(normalized) == 10):
                    if normalized not in mobiles:
                        mobiles.append(normalized)
                else:
                    if normalized not in phones:
                        phones.append(normalized)
            used_lines.add(i)
            continue
        
        # Candidate name (prefer early lines)
        if i < 3 and _is_likely_name(line):
            candidates_name.append(line)
            used_lines.add(i)
            continue
        
        # Company detection
        if _is_likely_company(line):
            candidates_company.append(line)
            used_lines.add(i)
            continue
        
        # Job title detection
        if _is_likely_job_title(line):
            candidates_job.append(line)
            used_lines.add(i)
            continue
        
        # Address detection
        if _is_likely_address(line):
            address_parts.append(line)
            used_lines.add(i)
            continue
    
    # Assign best candidates
    data.email = emails[0] if emails else None
    data.website = websites[0] if websites else None
    data.mobile = mobiles[0] if mobiles else None
    data.phone = phones[0] if phones else None
    
    data.full_name = candidates_name[0] if candidates_name else None
    data.company = candidates_company[0] if candidates_company else None
    data.job_title = candidates_job[0] if candidates_job else None
    
    # Combine address parts
    if address_parts:
        data.address = ' | '.join(address_parts)
    
    # Remaining lines go to other_lines
    data.other_lines = [lines[i] for i in range(len(lines)) if i not in used_lines]
    
    logger.info(f"Parsed card: name={data.full_name}, company={data.company}, job={data.job_title}")
    
    return data


# =====================================================================
# HIGH-LEVEL API
# =====================================================================

def extract_business_card_data_from_bytes(content: bytes) -> dict[str, Any]:
    """
    Extract structured data from business card image.
    
    Args:
        content: Image bytes (JPG/PNG)
    
    Returns:
        Dict with:
        - structured: Cleaned structured data
        - lines: All OCR lines
        - metadata: OCR metadata (optional)
    """
    try:
        # Perform OCR
        lines, raw_results = ocr_business_card_from_bytes(content)
        
        # Parse into structured data
        card_data = parse_business_card_lines(lines)
        
        # Calculate average confidence
        if raw_results:
            confidences = [conf for (_, _, conf) in raw_results]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        else:
            avg_confidence = 0
        
        return {
            "structured": card_data.to_dict(),
            "lines": lines,
            "metadata": {
                "total_lines": len(lines),
                "avg_confidence": round(avg_confidence, 2)
            }
        }
    
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        raise
