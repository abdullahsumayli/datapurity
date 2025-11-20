"""Reset test user with correct password."""
import asyncio
from sqlalchemy import select, delete
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash


async def reset_user():
    async with AsyncSessionLocal() as db:
        # Delete existing user
        await db.execute(delete(User).where(User.email == "sumayliabdullah@gmail.com"))
        await db.commit()
        
        # Create new user with correct password
        hashed_password = get_password_hash("password123")
        user = User(
            email="sumayliabdullah@gmail.com",
            hashed_password=hashed_password,
            full_name="Abdullah Sumayli",
            is_active=True,
        )
        
        db.add(user)
        await db.commit()
        print("✅ User created: sumayliabdullah@gmail.com / password123")


if __name__ == "__main__":
    asyncio.run(reset_user())
