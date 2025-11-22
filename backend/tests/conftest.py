"""
Pytest configuration and fixtures for DataPurity tests.
"""

import pytest


@pytest.fixture
async def client():
    """Create async test client."""
    # Lazy import to avoid loading app dependencies during collection
    try:
        from httpx import AsyncClient
        from app.main import app
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    except ImportError:
        # If dependencies not available, skip
        pytest.skip("HTTP client dependencies not available")


@pytest.fixture
async def auth_headers():
    """Create authentication headers for tests."""
    # TODO: Implement actual authentication
    # For now, return empty dict
    return {}
