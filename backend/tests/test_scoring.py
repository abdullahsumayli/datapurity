"""
Tests for datapurity_core.scoring module
"""

import pytest
import pandas as pd
from datapurity_core.config import get_settings
from datapurity_core import scoring


@pytest.fixture
def settings():
    """Get default settings for tests."""
    return get_settings()


class TestComputeQualityScore:
    """Tests for compute_quality_score function."""
    
    def test_perfect_score(self, settings):
        row = pd.Series({
            "phone_valid": True,
            "email_valid": True,
            "name": "Ahmed Mohamed",
            "company": "Acme Corp",
            "job_title": "Manager",
            "city": "Riyadh"
        })
        
        score = scoring.compute_quality_score(row, settings)
        assert score == 100
    
    def test_phone_and_email_only(self, settings):
        row = pd.Series({
            "phone_valid": True,
            "email_valid": True,
            "name": "",
            "company": "",
            "job_title": "",
            "city": ""
        })
        
        score = scoring.compute_quality_score(row, settings)
        assert score == 60  # 30 + 30
    
    def test_no_valid_fields(self, settings):
        row = pd.Series({
            "phone_valid": False,
            "email_valid": False,
            "name": "",
            "company": "",
            "job_title": "",
            "city": ""
        })
        
        score = scoring.compute_quality_score(row, settings)
        assert score == 0
    
    def test_partial_score(self, settings):
        row = pd.Series({
            "phone_valid": True,
            "email_valid": False,
            "name": "Ahmed Mohamed",
            "company": "Acme Corp",
            "job_title": "",
            "city": ""
        })
        
        score = scoring.compute_quality_score(row, settings)
        assert score == 60  # 30 (phone) + 20 (name) + 10 (company)
    
    def test_name_too_short(self, settings):
        settings.MIN_VALID_NAME_LEN = 5
        
        row = pd.Series({
            "phone_valid": False,
            "email_valid": False,
            "name": "Ali",  # Too short
            "company": "",
            "job_title": "",
            "city": ""
        })
        
        score = scoring.compute_quality_score(row, settings)
        assert score == 0  # Name too short, no points
    
    def test_arabic_contact(self, settings):
        row = pd.Series({
            "phone_valid": True,
            "email_valid": True,
            "name": "أحمد محمد",
            "company": "شركة الاتصالات",
            "job_title": "مدير",
            "city": "الرياض"
        })
        
        score = scoring.compute_quality_score(row, settings)
        assert score == 100
