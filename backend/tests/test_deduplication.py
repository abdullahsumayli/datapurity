"""
Tests for datapurity_core.deduplication module
"""

import pytest
import pandas as pd
from datapurity_core.config import get_settings
from datapurity_core import deduplication


@pytest.fixture
def settings():
    """Get default settings for tests."""
    return get_settings()


class TestMarkDuplicates:
    """Tests for mark_duplicates function."""
    
    def test_no_duplicates(self, settings):
        df = pd.DataFrame({
            "name": ["Ahmed", "Ali", "Sara"],
            "phone": ["+966501234567", "+966509876543", "+966507777777"],
            "email": ["ahmed@test.com", "ali@test.com", "sara@test.com"]
        })
        
        df_marked = deduplication.mark_duplicates(df, settings)
        
        # No duplicates should be marked
        assert df_marked["is_duplicate"].sum() == 0
    
    def test_phone_duplicates(self, settings):
        df = pd.DataFrame({
            "name": ["Ahmed", "Ahmed Ali", "Sara"],
            "phone": ["+966501234567", "+966501234567", "+966507777777"],
            "email": ["ahmed1@test.com", "ahmed2@test.com", "sara@test.com"]
        })
        
        df_marked = deduplication.mark_duplicates(df, settings)
        
        # One duplicate (second Ahmed)
        assert df_marked["is_duplicate"].sum() == 1
        assert df_marked.iloc[1]["is_duplicate"] == True
        assert "phone:" in df_marked.iloc[1]["duplicate_reason"]
    
    def test_email_duplicates(self, settings):
        df = pd.DataFrame({
            "name": ["Ahmed", "Ali", "Sara"],
            "phone": ["+966501234567", "+966509876543", "+966507777777"],
            "email": ["same@test.com", "same@test.com", "sara@test.com"]
        })
        
        df_marked = deduplication.mark_duplicates(df, settings)
        
        # One duplicate (Ali has same email as Ahmed)
        assert df_marked["is_duplicate"].sum() == 1
        assert df_marked.iloc[1]["is_duplicate"] == True
        assert "email:" in df_marked.iloc[1]["duplicate_reason"]
    
    def test_fuzzy_name_duplicates(self, settings):
        # Enable fuzzy dedup
        settings.ENABLE_FUZZY_DEDUP = True
        settings.FUZZY_NAME_THRESHOLD = 90
        
        df = pd.DataFrame({
            "name": ["Ahmed Mohamed", "Ahmed Mohammed", "Sara Ali"],
            "phone": ["+966501234567", "+966509876543", "+966507777777"],
            "email": ["ahmed1@test.com", "ahmed2@test.com", "sara@test.com"]
        })
        
        df_marked = deduplication.mark_duplicates(df, settings)
        
        # Should detect fuzzy match between "Ahmed Mohamed" and "Ahmed Mohammed"
        fuzzy_duplicates = df_marked[df_marked["duplicate_reason"].str.contains("fuzzy_name", na=False)]
        assert len(fuzzy_duplicates) >= 1
    
    def test_duplicate_group_ids(self, settings):
        df = pd.DataFrame({
            "name": ["Ahmed", "Ahmed", "Ahmed"],
            "phone": ["+966501234567", "+966501234567", "+966501234567"],
            "email": ["a@test.com", "b@test.com", "c@test.com"]
        })
        
        df_marked = deduplication.mark_duplicates(df, settings)
        
        # All should have same group ID
        group_ids = df_marked["duplicate_group_id"].dropna().unique()
        assert len(group_ids) == 1


class TestDropHardDuplicates:
    """Tests for drop_hard_duplicates function."""
    
    def test_drop_duplicates(self):
        df = pd.DataFrame({
            "name": ["Ahmed", "Ali", "Sara"],
            "is_duplicate": [False, True, False]
        })
        
        df_clean = deduplication.drop_hard_duplicates(df)
        
        assert len(df_clean) == 2
        assert "Ali" not in df_clean["name"].values
    
    def test_no_duplicates_to_drop(self):
        df = pd.DataFrame({
            "name": ["Ahmed", "Ali", "Sara"],
            "is_duplicate": [False, False, False]
        })
        
        df_clean = deduplication.drop_hard_duplicates(df)
        
        assert len(df_clean) == 3
