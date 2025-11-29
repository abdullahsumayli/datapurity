#!/usr/bin/env python3
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('backend/datapurity.db')
cursor = conn.cursor()

# Check current users
cursor.execute("SELECT email, is_superuser FROM users")
users = cursor.fetchall()
print("Current users:")
for user in users:
    print(f"  - {user[0]}: is_superuser={user[1]}")

# Make all users superuser
cursor.execute("UPDATE users SET is_superuser = 1")
conn.commit()

# Check after update
cursor.execute("SELECT email, is_superuser FROM users")
users = cursor.fetchall()
print("\nAfter update:")
for user in users:
    print(f"  - {user[0]}: is_superuser={user[1]}")

conn.close()
print("\n✅ All users are now superusers!")
