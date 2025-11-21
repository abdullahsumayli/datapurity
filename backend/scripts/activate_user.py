"""Script to activate or create a user account."""
import asyncio
import sys
import os

# Set the working directory to backend
backend_dir = '/opt/datapurity/backend'
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Define User model directly to avoid circular imports
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


async def activate_user(email: str, password: str = "Abdullah@2025", full_name: str = "Abdullah Sumayli"):
    """Activate or create a user account."""
    
    # Database URL
    DATABASE_URL = "postgresql+asyncpg://datapurity_user:DataPurity2024!@localhost/datapurity_db"
    
    # Create engine
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Check if user exists
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # Activate existing user
            user.is_active = True
            await session.commit()
            print("✅ تم تفعيل الحساب بنجاح")
            print(f"📧 البريد: {user.email}")
            print(f"👤 الاسم: {user.full_name}")
            print(f"🟢 الحالة: نشط")
            print(f"📅 تاريخ الإنشاء: {user.created_at}")
        else:
            # Create new user
            hashed_password = get_password_hash(password)
            new_user = User(
                email=email,
                hashed_password=hashed_password,
                full_name=full_name,
                is_active=True
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            
            print("✅ تم إنشاء وتفعيل الحساب بنجاح")
            print(f"📧 البريد: {new_user.email}")
            print(f"👤 الاسم: {new_user.full_name}")
            print(f"🔑 كلمة المرور: {password}")
            print(f"🟢 الحالة: نشط")
            print(f"🆔 ID: {new_user.id}")
    
    await engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python activate_user.py <email> [password] [full_name]")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else "Abdullah@2025"
    full_name = sys.argv[3] if len(sys.argv) > 3 else "User"
    
    asyncio.run(activate_user(email, password, full_name))
