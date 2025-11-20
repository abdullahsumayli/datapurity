"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.settings import get_settings

settings = get_settings()

# تحويل URL من postgresql إلى sqlite إذا كان الإعداد الافتراضي
if settings.DB_URL.startswith("postgresql"):
    # استخدام SQLite بدلاً من PostgreSQL للتطوير
    DATABASE_URL = "sqlite+aiosqlite:///./datapurity.db"
else:
    DATABASE_URL = settings.DB_URL

# إنشاء async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# إنشاء session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class للـ models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency للحصول على database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
