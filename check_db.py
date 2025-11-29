import sqlite3
conn = sqlite3.connect('backend/datapurity.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", cursor.fetchall())

# Check contacts table exists
cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='contacts'")
print("Contacts table exists:", cursor.fetchone()[0])

# Check jobs table exists  
cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='jobs'")
print("Jobs table exists:", cursor.fetchone()[0])

conn.close()
