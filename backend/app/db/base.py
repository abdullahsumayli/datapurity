"""SQLAlchemy base configuration."""

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all database models."""

    pass


# Import all models here for Alembic to detect them
from app.models.user import User  # noqa: F401, E402
from app.models.job import Job  # noqa: F401, E402
from app.models.dataset import Dataset  # noqa: F401, E402
from app.models.card import Card  # noqa: F401, E402
from app.models.contact import Contact  # noqa: F401, E402
from app.models.export import Export  # noqa: F401, E402
from app.models.lead import Lead  # noqa: F401, E402
