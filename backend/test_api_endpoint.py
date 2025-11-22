"""Test the marketing API endpoint."""

import requests
import json

# Test data
lead_data = {
    "full_name": "محمد أحمد السعيد",
    "email": "mohammed.ahmed@example.com",
    "phone": "+966505551234",
    "company": "شركة الابتكار التقني",
    "sector": "تقنية"
}

print("=== Testing Marketing Lead Capture API ===\n")
print(f"Submitting lead: {lead_data['full_name']} ({lead_data['email']})")

try:
    # Submit lead
    response = requests.post(
        "http://localhost:8000/api/v1/marketing/leads",
        json=lead_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("\n✓ Lead captured successfully!")
        print(f"  Lead ID: {result['id']}")
        print(f"  Full Name: {result['full_name']}")
        print(f"  Email: {result['email']}")
        print(f"  Phone: {result['phone']}")
        print(f"  Company: {result['company']}")
        print(f"  Sector: {result['sector']}")
        print(f"  Source: {result['source']}")
        print(f"  IP Address: {result['ip_address']}")
        print(f"  Created: {result['created_at']}")
        print("\n=== Test Passed ✓ ===")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n✗ Error: {str(e)}")

print("\n\nNext: Open http://localhost:8000/ in your browser to see the landing page!")
