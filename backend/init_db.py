"""
Initialize database and create test user
Run this script to set up the database for development
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.settings import get_settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.models.user import User

settings = get_settings()


async def init_db():
    """Initialize database and create tables"""
    print("🔧 Initializing database...")
    
    # Create async engine
    engine = create_async_engine(settings.DB_URL, echo=False, connect_args={"check_same_thread": False} if "sqlite" in settings.DB_URL else {})
    
    # Create all tables
    async with engine.begin() as conn:
        print("📋 Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("✅ Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully!")
    
    # Create session for adding test data
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Create test user
        print("\n👤 Creating test user...")
        test_user = User(
            email="sumayliabdullah@gmail.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User",
            is_active=True,
            is_superuser=False,
        )
        
        session.add(test_user)
        await session.commit()
        
        print(f"✅ Test user created:")
        print(f"   Email: {test_user.email}")
        print(f"   Password: password123")
        print(f"   ID: {test_user.id}")
    
    await engine.dispose()
    print("\n🎉 Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(init_db())
