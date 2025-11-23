"""
Google Cloud Vision OCR Service for Business Cards.

This module provides OCR functionality using Google Cloud Vision API's
document_text_detection method for high-quality text extraction from
business card images.
"""

from typing import Dict, Any
from google.cloud import vision
import logging

logger = logging.getLogger(__name__)

# Initialize Google Vision client lazily to avoid import-time credential errors
_client = None


def _get_client() -> vision.ImageAnnotatorClient:
    """
    Get or create Vision API client (lazy initialization).
    
    Returns:
        Initialized Vision API client
        
    Raises:
        RuntimeError: If credentials are not configured
    """
    global _client
    if _client is None:
        try:
            _client = vision.ImageAnnotatorClient()
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Google Cloud Vision. "
                f"Set GOOGLE_APPLICATION_CREDENTIALS environment variable: {str(e)}"
            )
    return _client


def ocr_business_card(image_bytes: bytes) -> Dict[str, Any]:
    """
    Perform OCR on a business card image using Google Cloud Vision.
    
    Uses document_text_detection for better structured text extraction
    compared to basic text_detection.
    
    Args:
        image_bytes: Raw bytes of the business card image (JPEG, PNG, etc.)
        
    Returns:
        Dictionary containing:
        - raw_text: Full extracted text from the card
        - locale: Detected language/locale (e.g., 'ar', 'en')
        - pages: Raw page structure from Vision API (for advanced processing)
        
    Raises:
        RuntimeError: If Google Vision API call fails
        
    Example:
        >>> with open('card.jpg', 'rb') as f:
        ...     result = ocr_business_card(f.read())
        >>> print(result['raw_text'])
    """
    try:
        # Get client (lazy initialization)
        client = _get_client()
        # Create Vision API image object
        image = vision.Image(content=image_bytes)
        
        # Call document_text_detection for structured OCR
        response = client.document_text_detection(image=image)
        
        # Check for errors in the response
        if response.error.message:
            raise RuntimeError(
                f"Google Vision API error: {response.error.message}"
            )
        
        # Extract full text annotation
        if not response.full_text_annotation:
            logger.warning("No text detected in the image")
            return {
                "raw_text": "",
                "locale": None,
                "pages": []
            }
        
        # Get the full text
        raw_text = response.full_text_annotation.text
        
        # Detect language/locale (from first page if available)
        locale = None
        if response.full_text_annotation.pages:
            first_page = response.full_text_annotation.pages[0]
            if first_page.property and first_page.property.detected_languages:
                locale = first_page.property.detected_languages[0].language_code
        
        # Store page structure for advanced processing if needed
        pages = []
        for page in response.full_text_annotation.pages:
            page_data = {
                "width": page.width,
                "height": page.height,
                "blocks_count": len(page.blocks) if page.blocks else 0
            }
            pages.append(page_data)
        
        logger.info(
            f"OCR successful: {len(raw_text)} chars, "
            f"locale={locale}, pages={len(pages)}"
        )
        
        return {
            "raw_text": raw_text,
            "locale": locale,
            "pages": pages
        }
        
    except Exception as e:
        logger.error(f"Google Vision OCR failed: {str(e)}", exc_info=True)
        raise RuntimeError(f"Failed to perform OCR: {str(e)}") from e
