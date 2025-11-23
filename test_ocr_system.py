"""
Quick test script for the new EasyOCR business card system.
Run this to verify the OCR endpoints are working correctly.
"""

import requests
import sys
from pathlib import Path


def test_ocr_endpoint():
    """Test the /ocr/business-card endpoint."""
    
    print("=" * 60)
    print("🧪 Testing EasyOCR Business Card System")
    print("=" * 60)
    
    # API endpoint
    base_url = "http://localhost:8000/api/v1"
    ocr_url = f"{base_url}/ocr/business-card"
    save_url = f"{base_url}/ocr/business-card/save"
    
    # Check if test image exists
    test_images = [
        Path("test_card.jpg"),
        Path("sample_card.jpg"),
        Path("card.jpg"),
    ]
    
    test_image = None
    for img in test_images:
        if img.exists():
            test_image = img
            break
    
    if not test_image:
        print("⚠️  No test image found!")
        print("📁 Please provide a business card image:")
        print("   - test_card.jpg")
        print("   - sample_card.jpg")
        print("   - card.jpg")
        return False
    
    print(f"\n📸 Using test image: {test_image}")
    
    # Test 1: OCR only (no save)
    print("\n" + "-" * 60)
    print("Test 1: OCR Extraction (no save)")
    print("-" * 60)
    
    try:
        with open(test_image, "rb") as f:
            files = {"file": (test_image.name, f, "image/jpeg")}
            response = requests.post(ocr_url, files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(f"\n📊 Metadata:")
            if data.get("metadata"):
                print(f"   - Total lines: {data['metadata'].get('total_lines', 'N/A')}")
                print(f"   - Avg confidence: {data['metadata'].get('avg_confidence', 'N/A')}")
            
            print(f"\n📋 Extracted Data:")
            fields = [
                ("full_name", "👤 Name"),
                ("company", "🏢 Company"),
                ("job_title", "💼 Job Title"),
                ("email", "📧 Email"),
                ("mobile", "📱 Mobile"),
                ("phone", "☎️  Phone"),
                ("website", "🌐 Website"),
                ("address", "📍 Address"),
            ]
            
            for field, label in fields:
                value = data.get(field)
                if value:
                    print(f"   {label}: {value}")
            
            if data.get("other_lines"):
                print(f"\n📝 Other lines ({len(data['other_lines'])}):")
                for line in data['other_lines'][:3]:  # Show first 3
                    print(f"   - {line}")
                if len(data['other_lines']) > 3:
                    print(f"   ... and {len(data['other_lines']) - 3} more")
            
            print(f"\n📄 All extracted lines ({len(data.get('all_lines', []))}):")
            for i, line in enumerate(data.get('all_lines', [])[:5], 1):
                print(f"   {i}. {line}")
            if len(data.get('all_lines', [])) > 5:
                print(f"   ... and {len(data['all_lines']) - 5} more")
        
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    # Test 2: OCR + Save
    print("\n" + "-" * 60)
    print("Test 2: OCR + Save to Database")
    print("-" * 60)
    
    try:
        with open(test_image, "rb") as f:
            files = {"file": (test_image.name, f, "image/jpeg")}
            response = requests.post(save_url, files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(f"\n💾 Save Result:")
            print(f"   - Success: {data.get('success')}")
            print(f"   - Contact ID: {data.get('contact_id')}")
            print(f"   - Message: {data.get('message')}")
            
            extracted = data.get('extracted_data', {})
            print(f"\n📋 Saved Contact:")
            print(f"   - Name: {extracted.get('full_name', 'N/A')}")
            print(f"   - Company: {extracted.get('company', 'N/A')}")
            print(f"   - Email: {extracted.get('email', 'N/A')}")
            print(f"   - Mobile: {extracted.get('mobile', 'N/A')}")
        
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    return True


def check_server():
    """Check if FastAPI server is running."""
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        return response.status_code == 200
    except:
        return False


if __name__ == "__main__":
    print("\n🔍 Checking FastAPI server...")
    
    if not check_server():
        print("❌ FastAPI server is not running!")
        print("\n💡 Start the server first:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --reload")
        sys.exit(1)
    
    print("✅ Server is running!\n")
    
    # Run tests
    success = test_ocr_endpoint()
    
    if success:
        print("\n🎉 EasyOCR system is working perfectly!")
        print("\n📚 Next steps:")
        print("   1. Open Swagger UI: http://localhost:8000/api/v1/docs")
        print("   2. Try the /ocr/business-card endpoint")
        print("   3. Check OCR_SYSTEM_GUIDE.md for full documentation")
    else:
        print("\n😞 Some tests failed. Check the errors above.")
        sys.exit(1)
