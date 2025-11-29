"""Make a user superuser."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from app.core.settings import get_settings

settings = get_settings()
engine = create_engine(settings.DB_URL.replace('+asyncpg', ''))

with engine.connect() as conn:
    # Get user by email or first user
    email = sys.argv[1] if len(sys.argv) > 1 else None
    
    if email:
        result = conn.execute(text("SELECT id, email, is_superuser FROM users WHERE email = :email"), {"email": email})
    else:
        result = conn.execute(text("SELECT id, email, is_superuser FROM users LIMIT 1"))
    
    user = result.fetchone()
    
    if not user:
        print("No user found")
        sys.exit(1)
    
    user_id, user_email, is_superuser = user
    print(f"Found user: {user_email}")
    
    if is_superuser:
        print("User is already a superuser")
    else:
        conn.execute(text("UPDATE users SET is_superuser = true WHERE id = :user_id"), {"user_id": user_id})
        conn.commit()
        print(f"✅ {user_email} is now a superuser!")

