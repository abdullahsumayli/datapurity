#!/usr/bin/env python3
import sqlite3
from passlib.context import CryptContext

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# New password
new_password = "Admin@123"  # Change this to whatever you want
hashed = pwd_context.hash(new_password)

# Update in database
conn = sqlite3.connect('backend/datapurity.db')
cursor = conn.cursor()

cursor.execute("UPDATE users SET hashed_password = ? WHERE email = ?", 
               (hashed, "sumayliabdullah@gmail.com"))
conn.commit()

print(f"✅ Password updated for sumayliabdullah@gmail.com")
print(f"New password: {new_password}")

conn.close()
