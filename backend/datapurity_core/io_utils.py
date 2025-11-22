"""
I/O Utilities for DataPurity Core
=================================

Functions for loading and saving contact files (Excel, CSV) and normalizing column names.
"""

import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


# Column name mapping for normalization
COLUMN_MAPPINGS = {
    "name": [
        "name", "full_name", "fullname", "full name", "contact_name",
        "الاسم", "اسم العميل", "الاسم الكامل", "اسم"
    ],
    "phone": [
        "phone", "mobile", "mobile_phone", "tel", "telephone", "cell", "phone_number",
        "الجوال", "رقم الجوال", "رقم الهاتف", "جوال", "موبايل", "هاتف"
    ],
    "email": [
        "email", "e-mail", "mail", "email_address", "e_mail",
        "البريد", "البريد الإلكتروني", "الايميل", "ايميل", "بريد"
    ],
    "company": [
        "company", "company_name", "issuer", "organization", "org",
        "الشركة", "جهة العمل", "المؤسسة", "اسم الشركة", "شركة"
    ],
    "job_title": [
        "job_title", "position", "title", "job", "role",
        "المسمى الوظيفي", "الوظيفة", "المنصب", "الدور"
    ],
    "city": [
        "city", "location", "place", "region",
        "المدينة", "الموقع", "المنطقة"
    ],
    "notes": [
        "notes", "note", "comments", "remarks", "description",
        "ملاحظات", "تعليقات", "وصف"
    ]
}


def normalize_text_for_matching(text: str) -> str:
    """
    Normalize text for column name matching.
    
    Args:
        text: Raw column name
        
    Returns:
        Normalized text (lowercase, trimmed, special chars removed)
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower().strip()
    
    # Remove common separators and special characters
    text = text.replace("_", " ").replace("-", " ").replace(".", "")
    
    # Collapse multiple spaces
    text = " ".join(text.split())
    
    return text


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DataFrame column names to canonical names.
    
    Maps various column name variations (English/Arabic) to standard names:
    name, phone, email, company, job_title, city, notes.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with normalized column names
        
    Example:
        >>> df = pd.DataFrame({"الجوال": ["+966501234567"], "البريد": ["test@email.com"]})
        >>> normalized_df = normalize_column_names(df)
        >>> list(normalized_df.columns)
        ['phone', 'email']
    """
    logger.info(f"Normalizing column names from: {list(df.columns)}")
    
    # Create a copy
    df = df.copy()
    
    # Create mapping from current columns to canonical names
    rename_map = {}
    
    for col in df.columns:
        normalized_col = normalize_text_for_matching(str(col))
        
        # Find match in mappings
        for canonical_name, variants in COLUMN_MAPPINGS.items():
            normalized_variants = [normalize_text_for_matching(v) for v in variants]
            
            if normalized_col in normalized_variants:
                rename_map[col] = canonical_name
                break
    
    # Rename columns
    if rename_map:
        df = df.rename(columns=rename_map)
        logger.info(f"Renamed columns: {rename_map}")
    
    logger.info(f"Final columns: {list(df.columns)}")
    
    return df


def load_contacts_file(input_path: str) -> pd.DataFrame:
    """
    Load contacts from Excel or CSV file.
    
    Supports:
    - Excel files (.xlsx, .xls)
    - CSV files (.csv)
    
    Args:
        input_path: Path to input file
        
    Returns:
        DataFrame with loaded contacts
        
    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file does not exist
        
    Example:
        >>> df = load_contacts_file("contacts.xlsx")
        >>> print(len(df))
        150
    """
    path = Path(input_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    suffix = path.suffix.lower()
    
    logger.info(f"Loading file: {input_path} (format: {suffix})")
    
    try:
        if suffix in [".xlsx", ".xls"]:
            df = pd.read_excel(input_path)
            logger.info(f"Loaded {len(df)} rows from Excel file")
            
        elif suffix == ".csv":
            # Try UTF-8 first, fallback to UTF-8-SIG for BOM
            try:
                df = pd.read_csv(input_path, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(input_path, encoding="utf-8-sig")
            
            logger.info(f"Loaded {len(df)} rows from CSV file")
            
        else:
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                f"Supported formats: .xlsx, .xls, .csv"
            )
        
        return df
        
    except Exception as e:
        logger.error(f"Failed to load file {input_path}: {e}")
        raise


def save_contacts_file(df: pd.DataFrame, output_path: str) -> None:
    """
    Save contacts DataFrame to Excel or CSV file.
    
    Args:
        df: DataFrame to save
        output_path: Path to output file
        
    Example:
        >>> df = pd.DataFrame({"name": ["Ahmed"], "phone": ["+966501234567"]})
        >>> save_contacts_file(df, "cleaned_contacts.xlsx")
    """
    path = Path(output_path)
    suffix = path.suffix.lower()
    
    # Create parent directory if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving {len(df)} rows to: {output_path}")
    
    try:
        if suffix in [".xlsx", ".xls"]:
            df.to_excel(output_path, index=False, engine="openpyxl")
            logger.info("Saved as Excel file")
            
        else:  # Default to CSV
            df.to_csv(output_path, index=False, encoding="utf-8-sig")
            logger.info("Saved as CSV file")
            
    except Exception as e:
        logger.error(f"Failed to save file {output_path}: {e}")
        raise
