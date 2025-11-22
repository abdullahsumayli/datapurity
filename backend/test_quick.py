"""
Quick Test for DataPurity Core
"""

import pandas as pd
from datapurity_core.config import get_settings
from datapurity_core.cleaning import clean_contacts_df

# Create test data
print("Creating test data...")
test_data = {
    "الاسم": ["أحمد محمد", "Ahmed Ali", "Sara Mohamed", "Ahmed Ali"],  # Duplicate Ahmed Ali
    "الجوال": ["0501234567", "0509876543", "0507777777", "0509876543"],  # Duplicate phone
    "البريد الإلكتروني": ["ahmed@example.com", "ali@test.com", "sara@company.com", "ali@test.com"],
    "الشركة": ["شركة الاتصالات", "Acme Corp", "Tech Solutions", "Acme Corp"]
}

df = pd.DataFrame(test_data)

print(f"\nOriginal data ({len(df)} rows):")
print(df)

# Clean data
print("\nCleaning data...")
settings = get_settings()
settings.DEFAULT_COUNTRY_CODE = "SA"

df_cleaned, stats = clean_contacts_df(df, settings)

print(f"\nCleaned data ({len(df_cleaned)} rows):")
print(df_cleaned[["name", "phone", "email", "company", "phone_valid", "email_valid", "quality_score"]])

print("\n" + "=" * 70)
print("STATISTICS:")
print("=" * 70)
print(f"Original rows:        {stats.rows_original}")
print(f"Final rows:           {stats.rows_final}")
print(f"Duplicates removed:   {stats.duplicates_removed}")
print(f"Empty rows removed:   {stats.empty_rows_removed}")
print(f"Invalid phones:       {stats.invalid_phones}")
print(f"Invalid emails:       {stats.invalid_emails}")
print(f"Avg quality score:    {stats.avg_quality_score:.1f}/100")
print("=" * 70)

print("\n✓ Test completed successfully!")
