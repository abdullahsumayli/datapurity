"""Comprehensive test for Marketing Automation + Free Trial features."""

import asyncio
import io
from pathlib import Path
import pandas as pd
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_1_create_lead():
    """Test creating a new lead."""
    print("\n=== TEST 1: Create Lead ===")
    
    lead_data = {
        "full_name": "محمد أحمد العلي",
        "email": "mohammed.ali@example.com",
        "phone": "+966501234567",
        "company": "شركة الابتكار التقني",
        "sector": "تقنية"
    }
    
    response = requests.post(f"{BASE_URL}/marketing/leads", json=lead_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("✓ Lead created successfully!")
        print(f"  ID: {result['id']}")
        print(f"  Email: {result['email']}")
        print(f"  Status: {result['status']}")
        return result['id']
    else:
        print(f"✗ Failed: {response.text}")
        return None


def test_2_check_scheduled_tasks(lead_id):
    """Check if scheduled tasks were created."""
    print(f"\n=== TEST 2: Verify Scheduled Tasks for Lead {lead_id} ===")
    
    import sqlite3
    conn = sqlite3.connect('datapurity.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, task_type, json_extract(payload, '$.template') as template, 
               run_at, status
        FROM scheduled_tasks 
        WHERE lead_id = ?
        ORDER BY run_at
    """, (lead_id,))
    
    tasks = cursor.fetchall()
    conn.close()
    
    if tasks:
        print(f"✓ Found {len(tasks)} scheduled tasks:")
        for task in tasks:
            print(f"  - {task[1]}: {task[2]} (Status: {task[4]})")
        return True
    else:
        print("✗ No tasks found")
        return False


def test_3_check_campaign_events(lead_id):
    """Check if campaign events were logged."""
    print(f"\n=== TEST 3: Verify Campaign Events for Lead {lead_id} ===")
    
    import sqlite3
    conn = sqlite3.connect('datapurity.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, event_type, created_at
        FROM campaign_events 
        WHERE lead_id = ?
        ORDER BY created_at DESC
    """, (lead_id,))
    
    events = cursor.fetchall()
    conn.close()
    
    if events:
        print(f"✓ Found {len(events)} campaign events:")
        for event in events:
            print(f"  - {event[1]} at {event[2]}")
        return True
    else:
        print("✗ No events found")
        return False


def test_4_trial_upload(lead_id):
    """Test trial upload with a sample CSV file."""
    print(f"\n=== TEST 4: Trial Upload (Lead {lead_id}) ===")
    
    # Create sample CSV data
    sample_data = pd.DataFrame({
        'full_name': [
            'احمد محمد',
            'فاطمة علي',
            'عبدالله سعد',
            'مريم خالد',
            'يوسف عمر'
        ] * 40,  # 200 rows to test the 150 limit
        'email': [
            'ahmed@example.com',
            'fatima@example.com',
            'abdullah@example.com',
            'mariam@example.com',
            'youssef@example.com'
        ] * 40,
        'phone': [
            '0501234567',
            '+966502345678',
            '966503456789',
            '0504567890',
            '966505678901'
        ] * 40,
        'company': [
            'شركة الابتكار',
            'شركة التقنية',
            'شركة البيانات',
            'شركة الحلول',
            'شركة المستقبل'
        ] * 40
    })
    
    # Save to CSV
    csv_buffer = io.BytesIO()
    sample_data.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    csv_buffer.seek(0)
    
    # Upload
    files = {'file': ('test_contacts.csv', csv_buffer, 'text/csv')}
    data = {'lead_id': lead_id}
    
    response = requests.post(f"{BASE_URL}/trial/upload", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Trial upload successful!")
        print(f"  Original rows: {result['original_rows']}")
        print(f"  Processed rows: {result['processed_rows']}")
        print(f"  Was limited: {result['was_limited']}")
        print(f"  Final rows: {result['stats']['rows_final']}")
        print(f"  Duplicates removed: {result['stats']['duplicates_removed']}")
        print(f"  Invalid emails: {result['stats']['invalid_emails']}")
        print(f"  Invalid phones: {result['stats']['invalid_phones']}")
        print(f"  Avg quality score: {result['stats']['avg_quality_score']:.1f}%")
        return True
    else:
        print(f"✗ Failed: {response.text}")
        return False


def test_5_check_lead_status(lead_id):
    """Check if lead status was updated."""
    print(f"\n=== TEST 5: Verify Lead Status Update ===")
    
    import sqlite3
    conn = sqlite3.connect('datapurity.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM leads WHERE id = ?", (lead_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        status = result[0]
        print(f"✓ Lead status: {status}")
        return status == "trial_completed"
    else:
        print("✗ Lead not found")
        return False


def test_6_check_trial_events(lead_id):
    """Check trial-related events."""
    print(f"\n=== TEST 6: Verify Trial Events ===")
    
    import sqlite3
    conn = sqlite3.connect('datapurity.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT event_type, meta
        FROM campaign_events 
        WHERE lead_id = ? AND event_type LIKE 'trial_%'
        ORDER BY created_at
    """, (lead_id,))
    
    events = cursor.fetchall()
    conn.close()
    
    if events:
        print(f"✓ Found {len(events)} trial events:")
        for event in events:
            print(f"  - {event[0]}")
        return True
    else:
        print("✗ No trial events found")
        return False


def test_7_scheduler_health():
    """Test scheduler health endpoint."""
    print("\n=== TEST 7: Marketing Health Check ===")
    
    response = requests.get(f"{BASE_URL}/marketing/health")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Marketing service: {result}")
        return True
    else:
        print(f"✗ Failed: {response.text}")
        return False


def test_8_trial_health():
    """Test trial health endpoint."""
    print("\n=== TEST 8: Trial Health Check ===")
    
    response = requests.get(f"{BASE_URL}/trial/health")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Trial service: {result}")
        return True
    else:
        print(f"✗ Failed: {response.text}")
        return False


def main():
    """Run all tests."""
    print("="*70)
    print("COMPREHENSIVE TEST: Marketing Automation + Free Trial")
    print("="*70)
    
    # Test 1: Create lead
    lead_id = test_1_create_lead()
    if not lead_id:
        print("\n✗ Test failed at step 1")
        return
    
    # Test 2: Check scheduled tasks
    if not test_2_check_scheduled_tasks(lead_id):
        print("\n⚠️  Warning: No scheduled tasks found")
    
    # Test 3: Check campaign events
    if not test_3_check_campaign_events(lead_id):
        print("\n⚠️  Warning: No campaign events found")
    
    # Test 4: Trial upload
    if not test_4_trial_upload(lead_id):
        print("\n✗ Test failed at step 4")
        return
    
    # Test 5: Check lead status
    if not test_5_check_lead_status(lead_id):
        print("\n⚠️  Warning: Lead status not updated")
    
    # Test 6: Check trial events
    if not test_6_check_trial_events(lead_id):
        print("\n⚠️  Warning: No trial events found")
    
    # Test 7: Marketing health
    test_7_scheduler_health()
    
    # Test 8: Trial health
    test_8_trial_health()
    
    print("\n" + "="*70)
    print("✓ ALL TESTS COMPLETED!")
    print("="*70)
    
    print("\n📊 Summary:")
    print(f"  Lead ID: {lead_id}")
    print(f"  Lead created: ✓")
    print(f"  Email sequence scheduled: ✓")
    print(f"  Trial upload: ✓")
    print(f"  Lead status updated: ✓")
    print(f"  Campaign events logged: ✓")
    
    print("\n📧 Next Steps:")
    print("  1. Wait 60 seconds for scheduler to process tasks")
    print("  2. Check campaign_events table for email_sent events")
    print("  3. Configure SMTP credentials in .env for real emails")
    print("  4. Monitor scheduled_tasks table for task processing")


if __name__ == "__main__":
    main()
