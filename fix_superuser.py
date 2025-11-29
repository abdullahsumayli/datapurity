#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')
from app.db.session import get_sync_db
from sqlalchemy import text

db = next(get_sync_db())
result = db.execute(text("SELECT email, is_superuser FROM users LIMIT 1"))
user = result.fetchone()
print(f"Before: {user}")

db.execute(text("UPDATE users SET is_superuser = 1"))
db.commit()

result2 = db.execute(text("SELECT email, is_superuser FROM users LIMIT 1"))
user2 = result2.fetchone()
print(f"After: {user2}")
print("✅ All users are now superusers!")
