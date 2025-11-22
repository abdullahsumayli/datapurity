"""
DataPurity Core - Usage Examples
================================

This file demonstrates how to use the DataPurity Core cleaning engine.
"""

import pandas as pd
from datapurity_core.config import get_settings
from datapurity_core.cleaning import clean_contacts_df
from datapurity_core.io_utils import load_contacts_file, save_contacts_file


# Example 1: Basic Usage
# =====================

def example_basic():
    """Basic cleaning example."""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)
    
    # Get default settings
    settings = get_settings()
    
    # Load data
    df = load_contacts_file("input_contacts.xlsx")
    
    # Clean data
    df_cleaned, stats = clean_contacts_df(df, settings)
    
    # Save results
    save_contacts_file(df_cleaned, "cleaned_contacts.xlsx")
    
    # Print statistics
    print(f"\nResults:")
    print(f"Original rows: {stats.rows_original}")
    print(f"Final rows: {stats.rows_final}")
    print(f"Duplicates removed: {stats.duplicates_removed}")
    print(f"Avg quality score: {stats.avg_quality_score:.1f}")


# Example 2: Saudi Arabia Contacts
# ================================

def example_saudi_contacts():
    """Clean Saudi contacts with specific settings."""
    print("\n" + "=" * 70)
    print("Example 2: Saudi Arabia Contacts")
    print("=" * 70)
    
    # Get settings and customize
    settings = get_settings()
    settings.DEFAULT_COUNTRY_CODE = "SA"
    
    # Load data
    df = load_contacts_file("saudi_contacts.xlsx")
    
    # Clean data
    df_cleaned, stats = clean_contacts_df(df, settings)
    
    # Save results
    save_contacts_file(df_cleaned, "cleaned_saudi_contacts.xlsx")
    
    print(f"\nSaudi Contacts Cleaned:")
    print(f"Invalid phones: {stats.invalid_phones}")


# Example 3: High Quality Contacts Only
# =====================================

def example_high_quality_only():
    """Filter and export only high-quality contacts."""
    print("\n" + "=" * 70)
    print("Example 3: High Quality Contacts Only")
    print("=" * 70)
    
    settings = get_settings()
    
    # Load and clean data
    df = load_contacts_file("all_contacts.xlsx")
    df_cleaned, stats = clean_contacts_df(df, settings)
    
    # Filter by quality score >= 80
    high_quality = df_cleaned[df_cleaned["quality_score"] >= 80]
    
    # Save high-quality contacts
    save_contacts_file(high_quality, "high_quality_contacts.xlsx")
    
    print(f"\nTotal contacts: {len(df_cleaned)}")
    print(f"High quality (≥80): {len(high_quality)}")
    print(f"Percentage: {len(high_quality) / len(df_cleaned) * 100:.1f}%")


# Example 4: Export Valid Phones to CSV
# =====================================

def example_export_valid_phones():
    """Export only contacts with valid phone numbers."""
    print("\n" + "=" * 70)
    print("Example 4: Export Valid Phones to CSV")
    print("=" * 70)
    
    settings = get_settings()
    settings.DEFAULT_COUNTRY_CODE = "SA"
    
    # Load and clean data
    df = load_contacts_file("contacts.xlsx")
    df_cleaned, stats = clean_contacts_df(df, settings)
    
    # Filter valid phones
    valid_phones = df_cleaned[df_cleaned["phone_valid"] == True]
    
    # Export name and phone only
    export_df = valid_phones[["name", "phone"]].copy()
    save_contacts_file(export_df, "valid_phones.csv")
    
    print(f"\nValid phones exported: {len(export_df)}")


# Example 5: Aggressive Deduplication
# ===================================

def example_aggressive_dedup():
    """Use aggressive fuzzy deduplication."""
    print("\n" + "=" * 70)
    print("Example 5: Aggressive Deduplication")
    print("=" * 70)
    
    settings = get_settings()
    
    # Enable aggressive fuzzy matching
    settings.ENABLE_FUZZY_DEDUP = True
    settings.FUZZY_NAME_THRESHOLD = 85  # Lower = more aggressive
    
    # Load and clean data
    df = load_contacts_file("duplicates.xlsx")
    df_cleaned, stats = clean_contacts_df(df, settings)
    
    # Save results
    save_contacts_file(df_cleaned, "deduped_contacts.xlsx")
    
    print(f"\nDeduplication Results:")
    print(f"Original: {stats.rows_original}")
    print(f"After dedup: {stats.rows_final}")
    print(f"Removed: {stats.duplicates_removed}")


# Example 6: Custom Bad Email Domains
# ===================================

def example_custom_bad_domains():
    """Filter out specific email domains."""
    print("\n" + "=" * 70)
    print("Example 6: Custom Bad Email Domains")
    print("=" * 70)
    
    settings = get_settings()
    
    # Add custom bad domains
    settings.BAD_EMAIL_DOMAINS = [
        "test.com",
        "example.com",
        "spam.com",
        "tempmail.com"
    ]
    
    # Load and clean data
    df = load_contacts_file("contacts_with_spam.xlsx")
    df_cleaned, stats = clean_contacts_df(df, settings)
    
    # Save results
    save_contacts_file(df_cleaned, "cleaned_no_spam.xlsx")
    
    print(f"\nEmail Filtering Results:")
    print(f"Invalid emails: {stats.invalid_emails}")


# Example 7: Working with DataFrames Directly
# ===========================================

def example_dataframe_direct():
    """Create and clean DataFrame directly."""
    print("\n" + "=" * 70)
    print("Example 7: Working with DataFrames Directly")
    print("=" * 70)
    
    # Create sample data
    data = {
        "الاسم": ["أحمد محمد", "Ahmed Ali", "Sara Mohamed"],
        "الجوال": ["0501234567", "+966509876543", "0507777777"],
        "البريد الإلكتروني": ["ahmed@example.com", "ali@test.com", "sara@company.com"],
        "الشركة": ["شركة الاتصالات", "Acme Corp", "Tech Solutions"]
    }
    
    df = pd.DataFrame(data)
    
    # Clean data
    settings = get_settings()
    settings.DEFAULT_COUNTRY_CODE = "SA"
    
    df_cleaned, stats = clean_contacts_df(df, settings)
    
    # Display results
    print("\nCleaned Data:")
    print(df_cleaned[["name", "phone", "email", "company", "quality_score"]])
    
    print(f"\nStatistics:")
    print(f"Rows: {stats.rows_original} → {stats.rows_final}")
    print(f"Avg quality: {stats.avg_quality_score:.1f}")


# Example 8: Batch Processing Multiple Files
# ==========================================

def example_batch_processing():
    """Process multiple files in batch."""
    print("\n" + "=" * 70)
    print("Example 8: Batch Processing Multiple Files")
    print("=" * 70)
    
    settings = get_settings()
    settings.DEFAULT_COUNTRY_CODE = "SA"
    
    # List of files to process
    input_files = [
        "contacts_2023.xlsx",
        "contacts_2024.xlsx",
        "new_leads.csv"
    ]
    
    total_cleaned = 0
    total_duplicates = 0
    
    for input_file in input_files:
        print(f"\nProcessing: {input_file}")
        
        try:
            # Load and clean
            df = load_contacts_file(input_file)
            df_cleaned, stats = clean_contacts_df(df, settings)
            
            # Save with suffix
            output_file = input_file.replace(".", "_cleaned.")
            save_contacts_file(df_cleaned, output_file)
            
            # Update totals
            total_cleaned += stats.rows_final
            total_duplicates += stats.duplicates_removed
            
            print(f"✓ Cleaned: {stats.rows_original} → {stats.rows_final}")
            
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n" + "=" * 70)
    print(f"Batch Processing Complete")
    print(f"Total cleaned contacts: {total_cleaned}")
    print(f"Total duplicates removed: {total_duplicates}")
    print("=" * 70)


# Main: Run All Examples
# ======================

if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "DataPurity Core - Usage Examples" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Uncomment the examples you want to run:
    
    # example_basic()
    # example_saudi_contacts()
    # example_high_quality_only()
    # example_export_valid_phones()
    # example_aggressive_dedup()
    # example_custom_bad_domains()
    example_dataframe_direct()
    # example_batch_processing()
    
    print("\n✓ Examples completed!\n")
