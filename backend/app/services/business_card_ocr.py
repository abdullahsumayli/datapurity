"""
Advanced Business Card OCR Pipeline for DataPurity SaaS Platform
-----------------------------------------------------------------
Production-grade OCR service for processing business cards using Tesseract.
Supports batch processing, field extraction, deduplication, and quality scoring.

Dependencies:
- pytesseract (Tesseract OCR wrapper)
- Pillow (PIL) for image preprocessing
- pandas for data manipulation
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Iterable, Dict, Any, Tuple
import re
import logging
import unicodedata
from collections import defaultdict

from PIL import Image, ImageFilter, ImageOps
import pytesseract
import pandas as pd

# =====================================================================
# CONFIGURATION
# =====================================================================

# OCR Language configuration - English + Arabic
# Note: If Arabic not installed, will fallback to English only
OCR_LANG = "eng+ara"

# Try English only if Arabic fails
OCR_LANG_FALLBACK = "eng"

# Windows configuration - auto-detect tesseract path
import platform
import os

if platform.system() == "Windows":
    tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for path in tesseract_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

# =====================================================================
# REGEX PATTERNS
# =====================================================================

# Phone pattern - matches various formats including +966, 05xx, etc.
PHONE_PATTERN = re.compile(
    r'''(?:
        \+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}|
        \(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|
        \d{10,}
    )''',
    re.VERBOSE
)

# Email pattern
EMAIL_PATTERN = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
)

# URL pattern
URL_PATTERN = re.compile(
    r'(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
)

# =====================================================================
# HINT LISTS FOR FIELD DETECTION
# =====================================================================

# Common company-related keywords
COMPANY_HINTS = [
    'company', 'corporation', 'corp', 'inc', 'llc', 'ltd', 'group',
    'شركة', 'مؤسسة', 'مجموعة', 'شركه', 'موسسه'
]

# Common job title keywords
TITLE_HINTS = [
    'ceo', 'manager', 'director', 'president', 'officer', 'engineer',
    'developer', 'designer', 'consultant', 'specialist', 'analyst',
    'مدير', 'رئيس', 'نائب', 'مهندس', 'مطور', 'مستشار', 'أخصائي'
]


# =====================================================================
# DATA MODEL
# =====================================================================

@dataclass
class CardRecord:
    """
    Data model for a single business card record.
    
    Attributes:
        source_file: Original filename of the card image
        name: Person's name
        company: Company name
        title: Job title/position
        phones: Comma-separated phone numbers
        emails: Comma-separated email addresses
        website: Website URL
        raw_text: Full OCR extracted text
        quality_score: Quality score (0-100) based on field completeness
        duplicate_of: Source file of the master record if this is a duplicate
    """
    source_file: str
    name: str = ""
    company: str = ""
    title: str = ""
    phones: str = ""
    emails: str = ""
    website: str = ""
    raw_text: str = ""
    quality_score: float = 0.0
    duplicate_of: Optional[str] = None


# =====================================================================
# UTILITY FUNCTIONS
# =====================================================================

def normalize_text(text: str) -> str:
    """
    Normalize text by standardizing Unicode characters and whitespace.
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized text string
    """
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKC', text)
    
    # Replace multiple whitespaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def clean_phone(phone: str) -> str:
    """
    Clean and standardize phone number format.
    Keeps only digits and + sign.
    
    Args:
        phone: Raw phone number string
        
    Returns:
        Cleaned phone number
    """
    # Keep only digits and + sign
    cleaned = re.sub(r'[^\d+]', '', phone)
    return cleaned


def clean_email(email: str) -> str:
    """
    Clean and standardize email address.
    
    Args:
        email: Raw email string
        
    Returns:
        Cleaned email in lowercase
    """
    return email.strip().lower()


def clean_url(url: str) -> str:
    """
    Clean and standardize URL.
    Adds https:// prefix if missing.
    
    Args:
        url: Raw URL string
        
    Returns:
        Standardized URL
    """
    url = url.strip()
    if url.startswith('www.') and not url.startswith('http'):
        url = 'https://' + url
    return url


def is_potential_company(line: str) -> bool:
    """
    Check if a line likely contains a company name.
    
    Args:
        line: Text line to check
        
    Returns:
        True if line contains company-related keywords
    """
    line_lower = line.lower()
    return any(hint in line_lower for hint in COMPANY_HINTS)


def is_potential_title(line: str) -> bool:
    """
    Check if a line likely contains a job title.
    
    Args:
        line: Text line to check
        
    Returns:
        True if line contains title-related keywords
    """
    line_lower = line.lower()
    return any(hint in line_lower for hint in TITLE_HINTS)


# =====================================================================
# IMAGE PREPROCESSING
# =====================================================================

def preprocess_image(path: Path) -> Image.Image:
    """
    Preprocess image for better OCR results.
    
    Steps:
    1. Convert to grayscale
    2. Auto-contrast for better contrast
    3. Apply median filter to reduce noise
    4. Apply threshold for binarization
    5. Resize to standard width for consistency
    
    Args:
        path: Path to image file
        
    Returns:
        Preprocessed PIL Image object
    """
    # Open image
    img = Image.open(path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Apply auto-contrast
    img = ImageOps.autocontrast(img)
    
    # Apply median filter to reduce noise
    img = img.filter(ImageFilter.MedianFilter(size=3))
    
    # Apply simple threshold for binarization
    img = img.point(lambda x: 0 if x < 140 else 255, '1')
    
    # Resize to standard width (1000px) while maintaining aspect ratio
    target_width = 1000
    if img.width > target_width:
        ratio = target_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
    
    return img


# =====================================================================
# OCR FUNCTION
# =====================================================================

def ocr_image(img: Image.Image) -> str:
    """
    Perform OCR on preprocessed image.
    
    Args:
        img: Preprocessed PIL Image
        
    Returns:
        Extracted text string
    """
    try:
        # Try with Arabic + English
        text = pytesseract.image_to_string(img, lang=OCR_LANG)
        return text
    except pytesseract.TesseractError as e:
        # Fallback to English only if Arabic not available
        if "ara" in str(e).lower() or "language" in str(e).lower():
            logging.warning(f"Arabic language not available, falling back to English only")
            try:
                text = pytesseract.image_to_string(img, lang=OCR_LANG_FALLBACK)
                return text
            except Exception as fallback_error:
                logging.error(f"OCR failed even with English: {fallback_error}")
                return ""
        else:
            logging.error(f"OCR failed: {e}")
            return ""
    except Exception as e:
        logging.error(f"OCR failed: {e}")
        return ""


# =====================================================================
# FIELD EXTRACTION
# =====================================================================

def extract_fields_from_text(text: str) -> Dict[str, Any]:
    """
    Extract structured fields from OCR text.
    
    Uses regex patterns and heuristics to identify:
    - Name (typically first or second line)
    - Company name (lines with company keywords)
    - Job title (lines with title keywords)
    - Phone numbers (regex pattern matching)
    - Emails (regex pattern matching)
    - Website (URL pattern matching)
    
    Args:
        text: Raw OCR text
        
    Returns:
        Dictionary with extracted fields
    """
    # Normalize text
    normalized = normalize_text(text)
    
    # Split into lines
    lines = [line.strip() for line in normalized.split('\n') if line.strip()]
    
    # Initialize result
    result = {
        'name': '',
        'company': '',
        'title': '',
        'phones': '',
        'emails': '',
        'website': '',
        'raw_text': normalized
    }
    
    # Extract phones
    phone_matches = PHONE_PATTERN.findall(normalized)
    cleaned_phones = []
    for phone in phone_matches:
        cleaned = clean_phone(phone)
        # Filter out very short numbers (likely not phone numbers)
        if len(re.sub(r'\D', '', cleaned)) >= 7:
            cleaned_phones.append(cleaned)
    result['phones'] = ', '.join(cleaned_phones) if cleaned_phones else ''
    
    # Extract emails
    email_matches = EMAIL_PATTERN.findall(normalized)
    cleaned_emails = [clean_email(email) for email in email_matches]
    result['emails'] = ', '.join(cleaned_emails) if cleaned_emails else ''
    
    # Extract URLs
    url_matches = URL_PATTERN.findall(normalized)
    cleaned_urls = [clean_url(url) for url in url_matches]
    result['website'] = cleaned_urls[0] if cleaned_urls else ''
    
    # Extract name (heuristic: first or second non-empty line that doesn't look like contact info)
    for i, line in enumerate(lines[:3]):
        if (not '@' in line and 
            not 'www' in line.lower() and 
            not re.search(r'\d{7,}', line) and
            len(line.split()) <= 4 and
            len(line) > 3):
            result['name'] = line
            break
    
    # Extract company (look for company hints)
    for line in lines:
        if is_potential_company(line):
            result['company'] = line
            break
    
    # If no company found by hints, try to use a longer line from top lines
    if not result['company']:
        for line in lines[1:5]:
            if (len(line) > 10 and 
                not '@' in line and 
                not 'www' in line.lower() and
                line != result['name']):
                result['company'] = line
                break
    
    # Extract title (look for title hints)
    for line in lines:
        if is_potential_title(line) and line != result['name']:
            result['title'] = line
            break
    
    return result


# =====================================================================
# QUALITY SCORING
# =====================================================================

def compute_quality_score(record: Dict[str, Any]) -> float:
    """
    Calculate quality score based on field completeness.
    
    Scoring:
    - Name: +20 points
    - Company: +20 points
    - Title: +10 points
    - Phones: +20 points
    - Emails: +20 points
    - Website: +10 points
    
    Maximum: 100 points
    
    Args:
        record: Dictionary with extracted fields
        
    Returns:
        Quality score (0-100)
    """
    score = 0.0
    
    if record.get('name'):
        score += 20
    if record.get('company'):
        score += 20
    if record.get('title'):
        score += 10
    if record.get('phones'):
        score += 20
    if record.get('emails'):
        score += 20
    if record.get('website'):
        score += 10
    
    return score


# =====================================================================
# BUSINESS CARD PROCESSOR CLASS
# =====================================================================

class BusinessCardProcessor:
    """
    Main processor class for batch processing business card images.
    
    Handles:
    - Image preprocessing
    - OCR extraction
    - Field parsing
    - Quality scoring
    - Deduplication
    - Export to DataFrame/CSV
    """
    
    def __init__(
        self, 
        image_paths: Iterable[Path], 
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize processor with image paths.
        
        Args:
            image_paths: Iterable of Path objects pointing to card images
            logger: Optional logger instance (creates basic logger if None)
        """
        self.image_paths = list(image_paths)
        
        # Setup logger
        if logger is None:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
    
    def process_all(self) -> List[CardRecord]:
        """
        Process all images and extract card records.
        
        Returns:
            List of CardRecord objects
        """
        records = []
        
        for path in self.image_paths:
            try:
                self.logger.info(f"Processing {path.name}...")
                
                # Preprocess image
                img = preprocess_image(path)
                
                # Perform OCR
                text = ocr_image(img)
                
                # Extract fields
                fields = extract_fields_from_text(text)
                
                # Compute quality score
                quality_score = compute_quality_score(fields)
                
                # Create record
                record = CardRecord(
                    source_file=path.name,
                    name=fields.get('name', ''),
                    company=fields.get('company', ''),
                    title=fields.get('title', ''),
                    phones=fields.get('phones', ''),
                    emails=fields.get('emails', ''),
                    website=fields.get('website', ''),
                    raw_text=fields.get('raw_text', ''),
                    quality_score=quality_score
                )
                
                records.append(record)
                
            except Exception as e:
                self.logger.error(f"Error processing {path.name}: {e}")
                # Create empty record for failed processing
                records.append(CardRecord(
                    source_file=path.name,
                    raw_text=f"ERROR: {str(e)}"
                ))
        
        return records
    
    @staticmethod
    def _dedupe_records(records: List[CardRecord]) -> List[CardRecord]:
        """
        Deduplicate records based on email and phone.
        
        For duplicate groups:
        - Selects record with highest quality_score as master
        - Marks other records with duplicate_of field
        
        Args:
            records: List of CardRecord objects
            
        Returns:
            Updated list with duplicate markers
        """
        # Group by (first_email, first_phone) as key
        groups = defaultdict(list)
        
        for record in records:
            # Extract first email and first phone
            first_email = record.emails.split(',')[0].strip() if record.emails else ''
            first_phone = record.phones.split(',')[0].strip() if record.phones else ''
            
            key = (first_email, first_phone)
            groups[key].append(record)
        
        # Process groups
        for key, group in groups.items():
            # Skip if key is empty or group has only one record
            if key == ('', '') or len(group) == 1:
                continue
            
            # Sort by quality_score (descending)
            group.sort(key=lambda r: r.quality_score, reverse=True)
            
            # First record is master
            master = group[0]
            
            # Mark others as duplicates
            for duplicate in group[1:]:
                duplicate.duplicate_of = master.source_file
        
        return records
    
    def run(self, dedupe: bool = True) -> pd.DataFrame:
        """
        Run full processing pipeline.
        
        Args:
            dedupe: Whether to perform deduplication
            
        Returns:
            pandas DataFrame with all records
        """
        # Process all images
        records = self.process_all()
        
        # Deduplicate if requested
        if dedupe:
            records = self._dedupe_records(records)
        
        # Convert to DataFrame
        data = [asdict(record) for record in records]
        df = pd.DataFrame(data)
        
        # Reorder columns
        column_order = [
            'source_file', 'name', 'company', 'title', 
            'phones', 'emails', 'website', 
            'quality_score', 'duplicate_of', 'raw_text'
        ]
        
        # Ensure all columns exist
        for col in column_order:
            if col not in df.columns:
                df[col] = ''
        
        df = df[column_order]
        
        return df
    
    @staticmethod
    def save_to_csv(df: pd.DataFrame, path: Path) -> None:
        """
        Save DataFrame to CSV file.
        
        Args:
            df: DataFrame to save
            path: Output file path
        """
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save with UTF-8 BOM for Excel compatibility
        df.to_csv(path, index=False, encoding='utf-8-sig')


# =====================================================================
# CLI USAGE (for standalone testing)
# =====================================================================

if __name__ == "__main__":
    import argparse
    from glob import glob
    
    parser = argparse.ArgumentParser(
        description="Process business card images with OCR"
    )
    parser.add_argument(
        'input',
        help='Directory containing card images'
    )
    parser.add_argument(
        '--output',
        default='business_cards_output.csv',
        help='Output CSV filename (default: business_cards_output.csv)'
    )
    parser.add_argument(
        '--no-dedupe',
        action='store_true',
        help='Disable deduplication'
    )
    
    args = parser.parse_args()
    
    # Find all image files
    input_dir = Path(args.input)
    image_patterns = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    image_paths = []
    
    for pattern in image_patterns:
        image_paths.extend(input_dir.glob(pattern))
    
    if not image_paths:
        print(f"No images found in {input_dir}")
        exit(1)
    
    print(f"Found {len(image_paths)} images")
    
    # Process
    processor = BusinessCardProcessor(image_paths)
    df = processor.run(dedupe=not args.no_dedupe)
    
    # Save
    output_path = Path(args.output)
    BusinessCardProcessor.save_to_csv(df, output_path)
    
    print(f"\nProcessed {len(df)} records")
    print(f"Output saved to: {output_path}")
    
    # Print summary
    print(f"\nQuality Score Distribution:")
    print(df['quality_score'].describe())
    
    if not args.no_dedupe:
        duplicates = df['duplicate_of'].notna().sum()
        print(f"\nDuplicates found: {duplicates}")
