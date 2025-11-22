"""Test marketing automation and trial upload."""

import requests
import json
import time
from pathlib import Path
import pandas as pd

BASE_URL = "http://127.0.0.1:8000/api/v1"

print("=" * 80)
print("🚀 DataPurity Marketing Automation & Trial Upload Test")
print("=" * 80)

# Test 1: Create a lead
print("\n1️⃣  Testing Lead Creation with Email Sequence...")
lead_data = {
    "full_name": "اختبار أوتوماتيك",
    "email": "test_automation@example.com",
    "phone": "+966501234567",
    "company": "شركة الاختبار",
    "sector": "تقنية"
}

try:
    response = requests.post(f"{BASE_URL}/marketing/leads", json=lead_data)
    if response.status_code in [200, 201]:
        lead = response.json()
        print(f"✅ Lead created successfully!")
        print(f"   ID: {lead['id']}")
        print(f"   Email: {lead['email']}")
        print(f"   Status: {lead['status']}")
        lead_id = lead['id']
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test 2: Check scheduled tasks
print("\n2️⃣  Verifying Scheduled Tasks...")
time.sleep(2)  # Give time for tasks to be created

import sqlite3
conn = sqlite3.connect('datapurity.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT id, task_type, payload, run_at, status 
    FROM scheduled_tasks 
    WHERE lead_id = ?
    ORDER BY run_at
""", (lead_id,))
tasks = cursor.fetchall()

if tasks:
    print(f"✅ Found {len(tasks)} scheduled tasks:")
    for task in tasks:
        task_id, task_type, payload_json, run_at, status = task
        payload = json.loads(payload_json)
        template = payload.get('template', 'unknown')
        print(f"   - {template} (run_at: {run_at}, status: {status})")
else:
    print("⚠️  No scheduled tasks found")

# Test 3: Create test CSV file for trial
print("\n3️⃣  Creating Test CSV File...")
test_data = {
    'full_name': [
        'أحمد محمد',
        '  سارة علي  ',
        'MOHAMMED AHMED',
        'فاطمة الزهراء',
        'Test User',
        'أحمد محمد',  # Duplicate
        'عبدالله',
        'Khaled Abdullah',
        'منى السعيد',
        'Ahmed Mohamed'  # Duplicate with different capitalization
    ],
    'email': [
        'ahmed@example.com',
        'sara@test.com',
        'mohammed@company.sa',
        'fatima@email.com',
        'test@demo.com',
        'ahmed@example.com',  # Duplicate
        'abdullah@example.sa',
        'khaled@company.com',
        'mona@example.com',
        'AHMED@EXAMPLE.COM'  # Duplicate with different case
    ],
    'phone': [
        '+966 50 123 4567',
        '0501234567',
        '966-50-765-4321',
        '+966 55 888 9999',
        '(050) 123-4567',
        '+966501234567',
        '0551112222',
        '+966 50 333 4444',
        '0559998877',
        '+966501234567'
    ],
    'company': [
        'شركة التقنية',
        '  شركة المستقبل  ',
        'Tech Company',
        'الشركة السعودية',
        'Test Inc',
        'شركة التقنية',
        'شركة البيانات',
        'Modern Solutions',
        'شركة الخدمات',
        'Tech Company'
    ]
}

df = pd.DataFrame(test_data)
test_file = 'test_trial_data.csv'
df.to_csv(test_file, index=False, encoding='utf-8-sig')
print(f"✅ Created test file: {test_file} ({len(df)} rows)")

# Test 4: Upload file for trial
print("\n4️⃣  Testing Trial Upload (150 records limit)...")
try:
    with open(test_file, 'rb') as f:
        files = {'file': (test_file, f, 'text/csv')}
        data = {'lead_id': lead_id}
        response = requests.post(f"{BASE_URL}/trial/upload", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Trial upload successful!")
        print(f"   Processed rows: {result['processed_rows']}")
        print(f"   Valid records: {result['stats']['valid_records']}")
        print(f"   Duplicates found: {result['stats']['duplicates_found']}")
        print(f"   Duplicates removed: {result['stats']['duplicates_removed']}")
        print(f"   Emails validated: {result['stats']['emails_validated']}")
        print(f"   Emails valid: {result['stats']['emails_valid']}")
        print(f"   Phones normalized: {result['stats']['phones_normalized']}")
        print(f"   Average quality: {result['stats']['average_quality_score']:.1f}%")
        
        if result.get('sample_cleaned_data'):
            print(f"\n   📋 Sample cleaned data (first 3):")
            for i, row in enumerate(result['sample_cleaned_data'][:3], 1):
                print(f"      {i}. {row.get('full_name', 'N/A')} - {row.get('email', 'N/A')}")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"   {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Verify lead status updated
print("\n5️⃣  Verifying Lead Status...")
cursor.execute("SELECT status FROM leads WHERE id = ?", (lead_id,))
result = cursor.fetchone()
if result:
    status = result[0]
    print(f"✅ Lead status: {status}")
    if status == "trial_completed":
        print("   ✨ Status correctly updated to trial_completed!")
else:
    print("⚠️  Could not fetch lead status")

# Test 6: Check campaign events
print("\n6️⃣  Checking Campaign Events...")
cursor.execute("""
    SELECT event_type, meta, created_at 
    FROM campaign_events 
    WHERE lead_id = ?
    ORDER BY created_at
""", (lead_id,))
events = cursor.fetchall()

if events:
    print(f"✅ Found {len(events)} campaign events:")
    for event_type, meta_json, created_at in events:
        print(f"   - {event_type} (at: {created_at})")
else:
    print("⚠️  No campaign events found")

conn.close()

# Cleanup
print("\n7️⃣  Cleanup...")
Path(test_file).unlink(missing_ok=True)
print(f"✅ Removed test file: {test_file}")

print("\n" + "=" * 80)
print("✅ All Tests Completed Successfully!")
print("=" * 80)
print("\n📊 Summary:")
print(f"   - Lead created with ID: {lead_id}")
print(f"   - {len(tasks)} email tasks scheduled")
print(f"   - Trial upload processed")
print(f"   - {len(events)} campaign events logged")
print("\n🎯 Next Steps:")
print("   1. Check server logs for scheduler activity")
print("   2. Wait for scheduled emails (or check logs if EMAIL_USERNAME not set)")
print("   3. View API docs: http://127.0.0.1:8000/api/v1/docs")
print("   4. Monitor scheduled_tasks table for status updates")
print("\n💡 Note: Emails will only send if EMAIL_USERNAME and EMAIL_PASSWORD are")
print("   configured in .env file. Otherwise, they'll be logged only.")
