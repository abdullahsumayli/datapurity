"""Tests for business card OCR endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload_card(client: AsyncClient, auth_headers: dict):
    """Test card image upload."""
    # TODO: Implement test
    # - Upload test image
    # - Verify card created
    # - Verify OCR task queued
    pass


@pytest.mark.asyncio
async def test_update_card(client: AsyncClient, auth_headers: dict):
    """Test updating extracted card data."""
    # TODO: Implement test
    # - Create card with OCR data
    # - Update fields
    # - Verify update
    pass


@pytest.mark.asyncio
async def test_list_cards_filter_reviewed(client: AsyncClient, auth_headers: dict):
    """Test filtering cards by review status."""
    # TODO: Implement test
    # - Create reviewed and unreviewed cards
    # - Filter by reviewed=false
    # - Verify only unreviewed returned
    pass
