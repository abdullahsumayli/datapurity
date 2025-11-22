"""View scheduled tasks and campaign events"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('datapurity.db')
cursor = conn.cursor()

print('=' * 80)
print('📅 SCHEDULED TASKS')
print('=' * 80)

try:
    cursor.execute('SELECT id, lead_id, task_type, run_at, status, created_at FROM scheduled_tasks ORDER BY run_at')
    tasks = cursor.fetchall()
    
    if tasks:
        for task in tasks:
            print(f'\n✉️ Task ID: {task[0]}')
            print(f'   Lead ID: {task[1]}')
            print(f'   Type: {task[2]}')
            print(f'   Run At: {task[3]}')
            print(f'   Status: {task[4]}')
            print(f'   Created: {task[5]}')
            print('-' * 80)
        print(f'\n✓ Total scheduled tasks: {len(tasks)}')
    else:
        print('\n⚠️  No scheduled tasks found')
except Exception as e:
    print(f'\n❌ Error reading scheduled_tasks: {e}')

print('\n' + '=' * 80)
print('📊 CAMPAIGN EVENTS')
print('=' * 80)

try:
    cursor.execute('SELECT id, lead_id, event_type, created_at FROM campaign_events ORDER BY created_at DESC LIMIT 10')
    events = cursor.fetchall()
    
    if events:
        for event in events:
            print(f'\n📌 Event ID: {event[0]}')
            print(f'   Lead ID: {event[1]}')
            print(f'   Type: {event[2]}')
            print(f'   Created: {event[3]}')
            print('-' * 80)
        print(f'\n✓ Total events shown: {len(events)}')
    else:
        print('\n⚠️  No campaign events found')
except Exception as e:
    print(f'\n❌ Error reading campaign_events: {e}')

print('\n' + '=' * 80)
print('👥 LEADS')
print('=' * 80)

try:
    cursor.execute('SELECT id, full_name, email, status, created_at FROM leads ORDER BY created_at DESC LIMIT 5')
    leads = cursor.fetchall()
    
    if leads:
        for lead in leads:
            print(f'\n👤 Lead ID: {lead[0]}')
            print(f'   Name: {lead[1]}')
            print(f'   Email: {lead[2]}')
            print(f'   Status: {lead[3]}')
            print(f'   Created: {lead[4]}')
            print('-' * 80)
        print(f'\n✓ Total leads shown: {len(leads)}')
    else:
        print('\n⚠️  No leads found')
except Exception as e:
    print(f'\n❌ Error reading leads: {e}')

conn.close()
print('\n✅ Done!\n')
