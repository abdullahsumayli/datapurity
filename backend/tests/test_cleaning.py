"""
Tests for datapurity_core.cleaning module
"""

import pytest
import pandas as pd
from datapurity_core.config import get_settings
from datapurity_core import cleaning


@pytest.fixture
def settings():
    """Get default settings for tests."""
    return get_settings()


class TestCleanText:
    """Tests for clean_text function."""
    
    def test_basic_cleaning(self):
        assert cleaning.clean_text("  Ahmed  ") == "Ahmed"
        assert cleaning.clean_text("Ahmed   Mohamed") == "Ahmed Mohamed"
    
    def test_none_and_nan(self):
        assert cleaning.clean_text(None) == ""
        assert cleaning.clean_text(pd.NA) == ""
        assert cleaning.clean_text(float('nan')) == ""
    
    def test_zero_width_characters(self):
        text_with_zwsp = "Ahmed\u200bMohamed"
        assert cleaning.clean_text(text_with_zwsp) == "AhmedMohamed"


class TestNormalizeName:
    """Tests for normalize_name function."""
    
    def test_basic_normalization(self):
        assert cleaning.normalize_name("ahmed mohamed") == "Ahmed Mohamed"
        assert cleaning.normalize_name("  JOHN  DOE  ") == "John Doe"
    
    def test_arabic_names(self):
        # Arabic names should be preserved as-is
        arabic_name = "أحمد محمد"
        assert cleaning.normalize_name(arabic_name) == arabic_name
    
    def test_empty_name(self):
        assert cleaning.normalize_name("") == ""
        assert cleaning.normalize_name("   ") == ""


class TestExtractDigits:
    """Tests for extract_digits function."""
    
    def test_phone_extraction(self):
        assert cleaning.extract_digits("+966-50-123-4567") == "966501234567"
        assert cleaning.extract_digits("(966) 501234567") == "966501234567"
    
    def test_empty_string(self):
        assert cleaning.extract_digits("") == ""
        assert cleaning.extract_digits(None) == ""


class TestNormalizePhone:
    """Tests for normalize_phone function."""
    
    def test_saudi_mobile_9_digits(self, settings):
        phone, valid = cleaning.normalize_phone("501234567", "SA")
        assert phone == "+966501234567"
        assert valid is True
    
    def test_saudi_mobile_10_digits(self, settings):
        phone, valid = cleaning.normalize_phone("0501234567", "SA")
        assert phone == "+966501234567"
        assert valid is True
    
    def test_saudi_mobile_with_code(self, settings):
        phone, valid = cleaning.normalize_phone("+966501234567", "SA")
        assert phone == "+966501234567"
        assert valid is True
    
    def test_invalid_phone(self, settings):
        phone, valid = cleaning.normalize_phone("123", "SA")
        assert phone is None
        assert valid is False
    
    def test_empty_phone(self, settings):
        phone, valid = cleaning.normalize_phone("", "SA")
        assert phone is None
        assert valid is False


class TestNormalizeEmail:
    """Tests for normalize_email function."""
    
    def test_basic_email(self, settings):
        email, valid = cleaning.normalize_email("Ahmed@Example.COM", [])
        assert email == "ahmed@example.com"
        assert valid is True
    
    def test_invalid_email(self, settings):
        email, valid = cleaning.normalize_email("not-an-email", [])
        assert email is None
        assert valid is False
    
    def test_bad_domain(self, settings):
        bad_domains = ["test.com", "example.com"]
        email, valid = cleaning.normalize_email("user@test.com", bad_domains)
        assert email is None
        assert valid is False
    
    def test_empty_email(self, settings):
        email, valid = cleaning.normalize_email("", [])
        assert email is None
        assert valid is False


class TestIsGoodName:
    """Tests for is_good_name function."""
    
    def test_good_names(self):
        assert cleaning.is_good_name("Ahmed Mohamed", 3) is True
        assert cleaning.is_good_name("أحمد محمد", 3) is True
    
    def test_too_short(self):
        assert cleaning.is_good_name("AB", 3) is False
    
    def test_bad_patterns(self):
        assert cleaning.is_good_name("test", 3) is False
        assert cleaning.is_good_name("Test User", 3) is False
        assert cleaning.is_good_name("n/a", 3) is False
        assert cleaning.is_good_name("غير معروف", 3) is False


class TestCleanContactsDF:
    """Tests for clean_contacts_df function."""
    
    def test_basic_cleaning(self, settings):
        # Create test data
        df = pd.DataFrame({
            "الاسم": ["أحمد محمد", "Ahmed Ali"],
            "الجوال": ["0501234567", "0509876543"],
            "البريد الإلكتروني": ["ahmed@example.com", "ali@test.com"]
        })
        
        # Clean
        df_cleaned, stats = cleaning.clean_contacts_df(df, settings)
        
        # Check results
        assert len(df_cleaned) == 2
        assert "name" in df_cleaned.columns
        assert "phone" in df_cleaned.columns
        assert "email" in df_cleaned.columns
        assert stats.rows_original == 2
        assert stats.rows_final == 2
    
    def test_duplicate_removal(self, settings):
        # Create test data with duplicates
        df = pd.DataFrame({
            "name": ["Ahmed", "Ahmed", "Ali"],
            "phone": ["+966501234567", "+966501234567", "+966509876543"],
            "email": ["ahmed@example.com", "ahmed@example.com", "ali@test.com"]
        })
        
        # Clean
        df_cleaned, stats = cleaning.clean_contacts_df(df, settings)
        
        # Should remove 1 duplicate
        assert len(df_cleaned) == 2
        assert stats.duplicates_removed == 1
    
    def test_empty_row_removal(self, settings):
        # Create test data with empty row
        df = pd.DataFrame({
            "name": ["Ahmed", "", "Ali"],
            "phone": ["+966501234567", "", "+966509876543"],
            "email": ["", "", ""]
        })
        
        # Clean
        df_cleaned, stats = cleaning.clean_contacts_df(df, settings)
        
        # Should remove empty row
        assert len(df_cleaned) == 2
        assert stats.empty_rows_removed == 1
