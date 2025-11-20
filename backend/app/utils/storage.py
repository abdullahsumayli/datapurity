"""Storage utilities for S3 file operations."""

from typing import BinaryIO, Optional
import boto3
from botocore.exceptions import ClientError

from app.core.settings import get_settings

settings = get_settings()


class StorageClient:
    """S3 storage client wrapper."""

    def __init__(self):
        """Initialize S3 client."""
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self.bucket = settings.S3_BUCKET

    def upload_file(
        self, file_obj: BinaryIO, key: str, content_type: Optional[str] = None
    ) -> str:
        """
        Upload file to S3.

        TODO: Implement the following:
        - Upload file object to S3
        - Set content type if provided
        - Return S3 key
        """
        raise NotImplementedError("File upload not yet implemented")

    def download_file(self, key: str, local_path: str) -> None:
        """
        Download file from S3.

        TODO: Implement the following:
        - Download file from S3 to local path
        - Handle errors
        """
        raise NotImplementedError("File download not yet implemented")

    def delete_file(self, key: str) -> None:
        """
        Delete file from S3.

        TODO: Implement the following:
        - Delete file from S3
        - Handle errors
        """
        raise NotImplementedError("File deletion not yet implemented")

    def generate_presigned_url(
        self, key: str, expires_in: int = 3600, download: bool = True
    ) -> str:
        """
        Generate presigned URL for downloading.

        TODO: Implement the following:
        - Generate presigned URL with expiration
        - Set Content-Disposition for downloads
        - Return URL
        """
        raise NotImplementedError("Presigned URL generation not yet implemented")

    def file_exists(self, key: str) -> bool:
        """
        Check if file exists in S3.

        TODO: Implement the following:
        - Check if object exists
        - Return True/False
        """
        raise NotImplementedError("File existence check not yet implemented")
