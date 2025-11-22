"""
Test OCR System - Business Card Extraction
"""

import requests
import os

# Test configuration
SERVER_URL = "http://46.62.239.119:8000"
OCR_ENDPOINT = f"{SERVER_URL}/api/v1/cards/ocr"

print("=" * 70)
print("Testing DataPurity OCR System")
print("=" * 70)

# Test 1: Check endpoint availability
print("\n1. Checking OCR endpoint...")
try:
    response = requests.post(OCR_ENDPOINT)
    if response.status_code == 422:  # Validation error - expected without files
        print("✓ OCR endpoint is available and responding")
        print(f"  Response: {response.json()}")
    else:
        print(f"✗ Unexpected response: {response.status_code}")
except Exception as e:
    print(f"✗ Error connecting to OCR endpoint: {e}")

# Test 2: Create a simple test image
print("\n2. Creating test image...")
try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a simple business card image
    img = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add text (simulating business card)
    try:
        # Try to use a font
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        # Use default font
        font = ImageFont.load_default()
    
    # Add business card text
    text_lines = [
        "Ahmed Mohamed",
        "Senior Manager",
        "Acme Corporation",
        "Phone: +966501234567",
        "Email: ahmed@acme.com"
    ]
    
    y_position = 50
    for line in text_lines:
        draw.text((50, y_position), line, fill='black', font=font)
        y_position += 60
    
    # Save test image
    test_image_path = "test_business_card.jpg"
    img.save(test_image_path, quality=95)
    print(f"✓ Test image created: {test_image_path}")
    
    # Test 3: Upload to OCR
    print("\n3. Testing OCR extraction...")
    with open(test_image_path, 'rb') as f:
        files = {'files': ('business_card.jpg', f, 'image/jpeg')}
        response = requests.post(OCR_ENDPOINT, files=files)
    
    if response.status_code == 200:
        print("✓ OCR processing successful!")
        result = response.json()
        
        print("\n" + "=" * 70)
        print("OCR RESULTS:")
        print("=" * 70)
        
        if isinstance(result, list) and len(result) > 0:
            card = result[0]
            print(f"\nExtracted Data:")
            print(f"  Name:    {card.get('name', 'N/A')}")
            print(f"  Company: {card.get('company', 'N/A')}")
            print(f"  Title:   {card.get('title', 'N/A')}")
            print(f"  Phone:   {card.get('phones', 'N/A')}")
            print(f"  Email:   {card.get('emails', 'N/A')}")
            print(f"  Quality: {card.get('quality_score', 0)}/100")
        else:
            print("Result:", result)
    else:
        print(f"✗ OCR failed with status {response.status_code}")
        print(f"  Response: {response.text}")
    
    # Cleanup
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
        print(f"\n✓ Cleaned up test file")

except ImportError:
    print("✗ PIL/Pillow not installed. Install with: pip install Pillow")
    print("\nManual test:")
    print("1. Create a business card image")
    print(f"2. Upload using: curl -F files=@card.jpg {OCR_ENDPOINT}")

except Exception as e:
    print(f"✗ Error during OCR test: {e}")

print("\n" + "=" * 70)
print("OCR System Test Complete")
print("=" * 70)
