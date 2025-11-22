"""
DataPurity API
==============

FastAPI application for contact cleaning service.

Endpoints:
- POST /clean - Upload and clean contact file
- GET /clean/download/{task_id} - Download cleaned file
"""

import logging
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
import pandas as pd

from datapurity_core.config import get_settings
from datapurity_core.cleaning import clean_contacts_df
from datapurity_core.io_utils import load_contacts_file, save_contacts_file
from datapurity_core.models import CleaningStats


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title="DataPurity API",
    description="Contact data cleaning and normalization service",
    version="1.0.0"
)


# Storage for processed files (in production, use Redis or database)
TEMP_DIR = Path("./temp_cleaned_files")
TEMP_DIR.mkdir(exist_ok=True)

processed_files = {}


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "DataPurity API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/clean")
async def clean_contacts_endpoint(
    file: UploadFile = File(...),
    country_code: Annotated[str, Form()] = "SA",
    enable_fuzzy: Annotated[bool, Form()] = True,
    fuzzy_threshold: Annotated[int, Form()] = 90
):
    """
    Clean and normalize contact data file.
    
    Args:
        file: Excel or CSV file with contact data
        country_code: Default country code for phone numbers (default: SA)
        enable_fuzzy: Enable fuzzy name deduplication (default: True)
        fuzzy_threshold: Fuzzy matching threshold 0-100 (default: 90)
        
    Returns:
        JSON response with:
        - task_id: Unique ID for this cleaning task
        - stats: Cleaning statistics
        - download_url: URL to download cleaned file
        
    Example:
        ```bash
        curl -X POST "http://localhost:8000/clean" \\
          -F "file=@contacts.xlsx" \\
          -F "country_code=SA" \\
          -F "enable_fuzzy=true"
        ```
    """
    logger.info(f"Received cleaning request for file: {file.filename}")
    
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ['.xlsx', '.xls', '.csv']:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Use .xlsx, .xls, or .csv"
        )
    
    # Generate task ID
    task_id = str(uuid.uuid4())
    
    # Save uploaded file temporarily
    input_path = TEMP_DIR / f"{task_id}_input{file_ext}"
    
    try:
        # Save uploaded file
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Saved uploaded file to {input_path}")
        
        # Load data
        df = load_contacts_file(str(input_path))
        logger.info(f"Loaded {len(df)} rows")
        
        # Get settings and override
        settings = get_settings()
        settings.DEFAULT_COUNTRY_CODE = country_code
        settings.ENABLE_FUZZY_DEDUP = enable_fuzzy
        settings.FUZZY_NAME_THRESHOLD = fuzzy_threshold
        
        # Clean contacts
        logger.info("Starting cleaning pipeline")
        df_cleaned, stats = clean_contacts_df(df, settings)
        
        # Save cleaned file
        output_path = TEMP_DIR / f"{task_id}_output.xlsx"
        save_contacts_file(df_cleaned, str(output_path))
        
        logger.info(f"Saved cleaned file to {output_path}")
        
        # Store result
        processed_files[task_id] = {
            "input_filename": file.filename,
            "output_path": str(output_path),
            "stats": stats
        }
        
        # Build response
        response = {
            "task_id": task_id,
            "original_filename": file.filename,
            "stats": {
                "rows_original": stats.rows_original,
                "rows_final": stats.rows_final,
                "duplicates_removed": stats.duplicates_removed,
                "empty_rows_removed": stats.empty_rows_removed,
                "invalid_phones": stats.invalid_phones,
                "invalid_emails": stats.invalid_emails,
                "avg_quality_score": round(stats.avg_quality_score, 1)
            },
            "download_url": f"/clean/download/{task_id}"
        }
        
        logger.info(f"Cleaning completed for task {task_id}")
        logger.info(f"Stats: {stats.rows_original} → {stats.rows_final} rows")
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing file: {e}", exc_info=True)
        
        # Cleanup
        if input_path.exists():
            input_path.unlink()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@app.get("/clean/download/{task_id}")
async def download_cleaned_file(task_id: str):
    """
    Download cleaned contact file.
    
    Args:
        task_id: Task ID from cleaning request
        
    Returns:
        Excel file with cleaned contacts
        
    Example:
        ```bash
        curl -O "http://localhost:8000/clean/download/{task_id}"
        ```
    """
    if task_id not in processed_files:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    result = processed_files[task_id]
    output_path = Path(result["output_path"])
    
    if not output_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Cleaned file not found"
        )
    
    # Generate filename
    original_name = Path(result["input_filename"]).stem
    download_filename = f"{original_name}_cleaned.xlsx"
    
    logger.info(f"Serving cleaned file for task {task_id}: {download_filename}")
    
    return FileResponse(
        path=output_path,
        filename=download_filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/stats/{task_id}")
async def get_cleaning_stats(task_id: str):
    """
    Get cleaning statistics for a task.
    
    Args:
        task_id: Task ID from cleaning request
        
    Returns:
        JSON with cleaning statistics
    """
    if task_id not in processed_files:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    result = processed_files[task_id]
    stats = result["stats"]
    
    return {
        "task_id": task_id,
        "original_filename": result["input_filename"],
        "stats": {
            "rows_original": stats.rows_original,
            "rows_final": stats.rows_final,
            "duplicates_removed": stats.duplicates_removed,
            "empty_rows_removed": stats.empty_rows_removed,
            "invalid_phones": stats.invalid_phones,
            "invalid_emails": stats.invalid_emails,
            "avg_quality_score": round(stats.avg_quality_score, 1)
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
