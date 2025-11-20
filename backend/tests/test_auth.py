"""Tests for authentication endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup(client: AsyncClient):
    """Test user signup."""
    # TODO: Implement signup test
    # - Post to /api/v1/auth/signup
    # - Verify user created
    # - Verify response
    pass


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """Test user login."""
    # TODO: Implement login test
    # - Create test user
    # - Post to /api/v1/auth/login
    # - Verify token returned
    pass


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    # TODO: Implement test
    # - Post with wrong password
    # - Verify 401 response
    pass
