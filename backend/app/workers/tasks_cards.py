"""Celery tasks for business card OCR processing."""

from celery import Task
from app.workers.celery_app import celery_app


class DatabaseTask(Task):
    """Base task with database session management."""

    _db = None

    def after_return(self, *args, **kwargs):
        """Close database session after task completion."""
        if self._db is not None:
            # TODO: Close database session
            pass


@celery_app.task(base=DatabaseTask, bind=True)
def process_card_ocr(self, card_id: int):
    """
    Process OCR for a business card.

    TODO: Implement the following:
    - Load card from database
    - Download image from S3
    - Preprocess image
    - Run OCR (Tesseract, Google Vision, or AWS Textract)
    - Extract structured fields from OCR text
    - Save extracted data to card record
    - Update job progress
    """
    self.update_state(state="PROGRESS", meta={"current": 0, "total": 100})

    # TODO: Implement OCR processing logic
    raise NotImplementedError("Card OCR processing not yet implemented")


@celery_app.task(base=DatabaseTask)
def batch_process_cards(card_ids: list[int]):
    """
    Process multiple cards in batch.

    TODO: Implement the following:
    - Iterate through card IDs
    - Process each card
    - Update progress
    - Handle errors gracefully
    """
    raise NotImplementedError("Batch card processing not yet implemented")
