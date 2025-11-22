"""
اختبار API endpoint لـ OCR
========================

اختبار عملي للـ endpoint على السيرفر
"""

import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

print("=" * 60)
print("اختبار OCR API Endpoint")
print("=" * 60)
print()

# Create a better quality test card
print("📝 إنشاء بطاقة اختبار بجودة أفضل...")

temp_dir = Path("tmp/api_test")
temp_dir.mkdir(parents=True, exist_ok=True)

# Create high-quality card
img = Image.new('RGB', (1000, 600), color='white')
draw = ImageDraw.Draw(img)

try:
    # Use larger, clearer fonts
    font_name = ImageFont.truetype("arial.ttf", 50)
    font_company = ImageFont.truetype("arial.ttf", 35)
    font_info = ImageFont.truetype("arial.ttf", 25)
except:
    font_name = ImageFont.load_default()
    font_company = ImageFont.load_default()
    font_info = ImageFont.load_default()

# Draw card content with good spacing
y = 80

# Name (bold, large)
draw.text((80, y), "AHMED MOHAMMED", fill='black', font=font_name)
y += 80

# Company
draw.text((80, y), "Tech Solutions Inc.", fill='#1a1a1a', font=font_company)
y += 60

# Title
draw.text((80, y), "Marketing Director", fill='#555555', font=font_info)
y += 70

# Divider line
draw.line([(80, y), (920, y)], fill='#cccccc', width=2)
y += 40

# Contact info
draw.text((80, y), "Phone: +966 50 123 4567", fill='black', font=font_info)
y += 50

draw.text((80, y), "Email: ahmed@techsolutions.com", fill='black', font=font_info)
y += 50

draw.text((80, y), "Web: www.techsolutions.com", fill='black', font=font_info)

# Add a simple border
draw.rectangle([(10, 10), (990, 590)], outline='#333333', width=3)

# Save
card_path = temp_dir / "test_card_hq.jpg"
img.save(card_path, quality=95, dpi=(300, 300))
print(f"✅ تم إنشاء: {card_path}")
print()

# Test 1: Local endpoint
print("🧪 الاختبار 1: Local API (http://localhost:8000)")
try:
    with open(card_path, 'rb') as f:
        files = {'files': (card_path.name, f, 'image/jpeg')}
        response = requests.post(
            'http://localhost:8000/api/v1/cards/ocr',
            files=files,
            timeout=30
        )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ نجح! تمت معالجة {result['count']} بطاقة")
        print()
        
        if result['records']:
            record = result['records'][0]
            print("📊 البيانات المستخرجة:")
            print(f"  الاسم:   {record.get('name', 'N/A')}")
            print(f"  الشركة:  {record.get('company', 'N/A')}")
            print(f"  المسمى:  {record.get('title', 'N/A')}")
            print(f"  الهاتف:  {record.get('phones', 'N/A')}")
            print(f"  البريد:  {record.get('emails', 'N/A')}")
            print(f"  الموقع:  {record.get('website', 'N/A')}")
            print(f"  الجودة:  {record.get('quality_score', 0)}/100")
    else:
        print(f"❌ فشل: {response.status_code}")
        print(f"   {response.text[:200]}")

except requests.exceptions.ConnectionError:
    print("⚠️  السيرفر المحلي غير مشغل")
    print("   شغّل السيرفر بـ: uvicorn app.main:app --reload")
except Exception as e:
    print(f"❌ خطأ: {e}")

print()

# Test 2: Production endpoint
print("🧪 الاختبار 2: Production API (http://46.62.239.119:8000)")
try:
    with open(card_path, 'rb') as f:
        files = {'files': (card_path.name, f, 'image/jpeg')}
        response = requests.post(
            'http://46.62.239.119:8000/api/v1/cards/ocr',
            files=files,
            timeout=30
        )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ نجح! تمت معالجة {result['count']} بطاقة")
        print()
        
        if result['records']:
            record = result['records'][0]
            print("📊 البيانات المستخرجة:")
            print(f"  الاسم:   {record.get('name', 'N/A')}")
            print(f"  الشركة:  {record.get('company', 'N/A')}")
            print(f"  المسمى:  {record.get('title', 'N/A')}")
            print(f"  الهاتف:  {record.get('phones', 'N/A')}")
            print(f"  البريد:  {record.get('emails', 'N/A')}")
            print(f"  الموقع:  {record.get('website', 'N/A')}")
            print(f"  الجودة:  {record.get('quality_score', 0)}/100")
            print()
            
            # Show sample of raw text
            raw_text = record.get('raw_text', '')
            if raw_text:
                print("📝 عينة من النص المستخرج:")
                print(f"  {raw_text[:150]}...")
    else:
        print(f"❌ فشل: {response.status_code}")
        print(f"   {response.text[:200]}")

except requests.exceptions.ConnectionError:
    print("⚠️  لا يمكن الاتصال بالسيرفر")
except Exception as e:
    print(f"❌ خطأ: {e}")

print()

# Cleanup
print("🧹 تنظيف...")
try:
    card_path.unlink()
    print(f"✅ تم حذف الملف المؤقت")
except:
    pass

print()
print("=" * 60)
print("انتهى الاختبار!")
print("=" * 60)
