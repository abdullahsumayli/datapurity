"""Check database tables"""
import sqlite3

conn = sqlite3.connect('datapurity.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print('✅ Tables in database:')
for table in tables:
    print(f'   - {table[0]}')
    
    # Count rows
    cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
    count = cursor.fetchone()[0]
    print(f'     ({count} rows)')

conn.close()
