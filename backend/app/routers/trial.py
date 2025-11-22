"""Free trial upload endpoint for cleaning 150 records."""

import logging
import io
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from app.db.session import get_db
from app.services.lead_service import get_lead, update_lead_status
from app.services.campaigns_service import log_campaign_event, schedule_trial_followup_sequence

# Import the existing DataPurity cleaning engine
from datapurity_core.cleaning import clean_contacts_df
from datapurity_core.config import Settings as CleaningSettings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload")
async def trial_upload(
    file: UploadFile = File(..., description="Excel or CSV file to clean"),
    lead_id: Optional[int] = Form(None, description="Lead ID (optional)"),
    db: AsyncSession = Depends(get_db),
):
    """
    Free trial: Clean up to 150 contact records.
    
    This endpoint:
    1. Accepts Excel or CSV file
    2. Limits processing to first 150 rows
    3. Cleans data using DataPurity engine
    4. Returns stats + sample of cleaned data
    5. Updates lead status to trial_completed
    """
    try:
        # Validate file type
        filename = file.filename or ""
        if not (filename.endswith('.xlsx') or filename.endswith('.xls') or filename.endswith('.csv')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be Excel (.xlsx, .xls) or CSV (.csv)"
            )
        
        # Read file content
        content = await file.read()
        
        # Parse file into DataFrame
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
            else:
                df = pd.read_excel(io.BytesIO(content))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to parse file: {str(e)}"
            )
        
        # Validate DataFrame
        if df.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty or contains no data"
            )
        
        original_count = len(df)
        
        # Limit to 150 rows for free trial
        FREE_TRIAL_LIMIT = 150
        df_limited = df.head(FREE_TRIAL_LIMIT).copy()
        limited_count = len(df_limited)
        
        logger.info(f"Processing {limited_count} rows (original: {original_count})")
        
        # Update lead status to trial_started (if lead_id provided)
        if lead_id:
            lead = await get_lead(db, lead_id)
            if lead and lead.status == "new":
                await update_lead_status(db, lead_id, "trial_started")
                await log_campaign_event(
                    db,
                    lead_id=lead_id,
                    event_type="trial_started",
                    meta={"file_name": filename, "rows": limited_count}
                )
        
        # Get default cleaning config
        config = CleaningSettings()
        
        # Clean the data using the existing engine
        try:
            cleaned_df, stats = clean_contacts_df(df_limited, config)
        except Exception as e:
            logger.error(f"Cleaning failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Cleaning failed: {str(e)}"
            )
        
        # Update lead status to trial_completed
        if lead_id:
            lead = await get_lead(db, lead_id)
            if lead:
                await update_lead_status(db, lead_id, "trial_completed")
                await log_campaign_event(
                    db,
                    lead_id=lead_id,
                    event_type="trial_completed",
                    meta={
                        "file_name": filename,
                        "rows_processed": limited_count,
                        "stats": stats.model_dump()
                    }
                )
                
                # Schedule follow-up sequence
                await schedule_trial_followup_sequence(db, lead)
        
        await db.commit()
        
        # Prepare response
        response = {
            "success": True,
            "message": f"Successfully cleaned {limited_count} records",
            "original_rows": original_count,
            "processed_rows": limited_count,
            "was_limited": original_count > FREE_TRIAL_LIMIT,
            "free_trial_limit": FREE_TRIAL_LIMIT,
            "stats": {
                "rows_original": stats.rows_original,
                "rows_final": stats.rows_final,
                "duplicates_removed": stats.duplicates_removed,
                "empty_rows_removed": stats.empty_rows_removed,
                "invalid_phones": stats.invalid_phones,
                "invalid_emails": stats.invalid_emails,
                "avg_quality_score": stats.avg_quality_score,
                "fuzzy_duplicate_clusters": stats.fuzzy_duplicate_clusters,
            },
            "sample_cleaned_data": cleaned_df.head(10).to_dict(orient="records"),
            "note": "This is a free trial limited to 150 records. Upgrade for unlimited cleaning!"
        }
        
        logger.info(f"Trial completed successfully for lead {lead_id or 'unknown'}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in trial upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )


@router.get("/health")
async def trial_health():
    """Health check for trial endpoints."""
    return {"status": "ok", "service": "trial", "limit": 150}
