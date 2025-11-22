#!/usr/bin/env python3
"""
DataPurity CLI Tool
===================

Command-line interface for cleaning contact data files.

Usage:
    python -m scripts.datapurity_clean_cli input.xlsx output.xlsx
    python -m scripts.datapurity_clean_cli data.csv cleaned.csv --country SA
    python -m scripts.datapurity_clean_cli contacts.xlsx clean.xlsx --no-fuzzy
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from datapurity_core.config import get_settings, Settings
from datapurity_core.cleaning import clean_contacts_df
from datapurity_core.io_utils import load_contacts_file, save_contacts_file


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="DataPurity Contact Cleaning Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clean Excel file with default settings
  python -m scripts.datapurity_clean_cli input.xlsx output.xlsx
  
  # Clean CSV file with custom country code
  python -m scripts.datapurity_clean_cli data.csv cleaned.csv --country SA
  
  # Disable fuzzy deduplication
  python -m scripts.datapurity_clean_cli contacts.xlsx clean.xlsx --no-fuzzy
  
  # Use custom thresholds
  python -m scripts.datapurity_clean_cli data.xlsx out.xlsx --fuzzy-threshold 95
        """
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Input file path (Excel or CSV)"
    )
    
    parser.add_argument(
        "output_file",
        type=str,
        help="Output file path (Excel or CSV)"
    )
    
    parser.add_argument(
        "--country",
        type=str,
        default="SA",
        help="Default country code for phone numbers (default: SA)"
    )
    
    parser.add_argument(
        "--no-fuzzy",
        action="store_true",
        help="Disable fuzzy name deduplication"
    )
    
    parser.add_argument(
        "--fuzzy-threshold",
        type=int,
        default=90,
        help="Fuzzy name matching threshold 0-100 (default: 90)"
    )
    
    parser.add_argument(
        "--min-name-len",
        type=int,
        default=3,
        help="Minimum valid name length (default: 3)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def main():
    """Main CLI entry point."""
    args = parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)
    
    # Get settings with overrides
    settings = get_settings()
    
    # Override settings from CLI args
    settings.DEFAULT_COUNTRY_CODE = args.country
    settings.ENABLE_FUZZY_DEDUP = not args.no_fuzzy
    settings.FUZZY_NAME_THRESHOLD = args.fuzzy_threshold
    settings.MIN_VALID_NAME_LEN = args.min_name_len
    
    logger.info("=" * 70)
    logger.info("DataPurity Contact Cleaning Tool")
    logger.info("=" * 70)
    logger.info(f"Input file:       {args.input_file}")
    logger.info(f"Output file:      {args.output_file}")
    logger.info(f"Country code:     {settings.DEFAULT_COUNTRY_CODE}")
    logger.info(f"Fuzzy dedup:      {'Enabled' if settings.ENABLE_FUZZY_DEDUP else 'Disabled'}")
    logger.info(f"Fuzzy threshold:  {settings.FUZZY_NAME_THRESHOLD}")
    logger.info(f"Min name length:  {settings.MIN_VALID_NAME_LEN}")
    logger.info("=" * 70)
    
    try:
        # Load input file
        logger.info("Loading input file...")
        df = load_contacts_file(args.input_file)
        logger.info(f"Loaded {len(df)} rows")
        
        # Clean contacts
        logger.info("Starting cleaning pipeline...")
        df_cleaned, stats = clean_contacts_df(df, settings)
        
        # Save output file
        logger.info(f"Saving cleaned data to {args.output_file}...")
        save_contacts_file(df_cleaned, args.output_file)
        
        # Print summary
        logger.info("=" * 70)
        logger.info("CLEANING SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Original rows:        {stats.rows_original}")
        logger.info(f"Final rows:           {stats.rows_final}")
        logger.info(f"Duplicates removed:   {stats.duplicates_removed}")
        logger.info(f"Empty rows removed:   {stats.empty_rows_removed}")
        logger.info(f"Invalid phones:       {stats.invalid_phones}")
        logger.info(f"Invalid emails:       {stats.invalid_emails}")
        logger.info(f"Avg quality score:    {stats.avg_quality_score:.1f}/100")
        logger.info("=" * 70)
        logger.info("✓ Cleaning completed successfully!")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Error during cleaning: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
