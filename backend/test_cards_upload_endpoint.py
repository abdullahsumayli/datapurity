"""
اختبار endpoint /cards/upload مع authentication
"""
import requests
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json

# إنشاء بطاقة اختبار
def create_test_card():
    img = Image.new('RGB', (600, 350), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_medium = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # رسم البطاقة
    draw.text((50, 30), "AHMED MOHAMMED", fill='black', font=font_large)
    draw.text((50, 80), "Tech Solutions Inc.", fill='gray', font=font_medium)
    draw.text((50, 110), "Marketing Director", fill='gray', font=font_medium)
    draw.text((50, 160), "Phone: +966 50 123 4567", fill='black', font=font_small)
    draw.text((50, 190), "Email: ahmed@techsolutions.com", fill='black', font=font_small)
    draw.text((50, 220), "Web: www.techsolutions.com", fill='black', font=font_small)
    
    # حفظ
    output_dir = Path("tmp/upload_test")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "test_card.jpg"
    img.save(output_path, 'JPEG', quality=95)
    
    return output_path

def test_upload_endpoint(api_url: str, token: str = None):
    """
    اختبار endpoint /cards/upload
    """
    print("=" * 80)
    print(f"🧪 اختبار {api_url}/api/v1/cards/upload")
    print("=" * 80)
    print()
    
    # إنشاء بطاقة
    card_path = create_test_card()
    print(f"✅ تم إنشاء بطاقة اختبار: {card_path}")
    print()
    
    # إعداد الطلب
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # إرسال الطلب
    try:
        print("⏳ جاري إرسال الطلب...")
        with open(card_path, 'rb') as f:
            files = {'files': ('test_card.jpg', f, 'image/jpeg')}
            response = requests.post(
                f"{api_url}/api/v1/cards/upload",
                files=files,
                headers=headers,
                timeout=30
            )
        
        print(f"📊 Response Status: {response.status_code}")
        print()
        
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            print("✅ نجح!")
            print()
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print()
            
            # عرض البيانات المستخرجة
            if isinstance(data, list) and len(data) > 0:
                card = data[0]
                print("=" * 80)
                print("📋 البيانات المستخرجة:")
                print("=" * 80)
                print(f"الاسم:   {card.get('extracted_name', 'N/A')}")
                print(f"الشركة:  {card.get('extracted_company', 'N/A')}")
                print(f"الهاتف:  {card.get('extracted_phone', 'N/A')}")
                print(f"الإيميل: {card.get('extracted_email', 'N/A')}")
                print(f"الجودة:  {card.get('ocr_confidence', 'N/A')}")
                print()
        
        elif response.status_code == 401:
            print("❌ خطأ 401: Authentication مطلوب")
            print("   قم بتسجيل الدخول أولاً وأدخل الـ token")
            print()
        
        else:
            print(f"❌ فشل: {response.status_code}")
            print(response.text)
            print()
    
    except requests.exceptions.ConnectionError:
        print(f"❌ فشل الاتصال بـ {api_url}")
        print("   تأكد من أن السيرفر يعمل")
    
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
    
    print("=" * 80)

if __name__ == "__main__":
    print()
    print("🔐 هذا الـ endpoint يحتاج authentication")
    print()
    print("الخيارات:")
    print("1. اختبار بدون token (سيفشل مع 401)")
    print("2. اختبار مع token")
    print()
    
    choice = input("اختر (1/2): ").strip()
    
    if choice == "2":
        token = input("أدخل الـ access token: ").strip()
    else:
        token = None
    
    print()
    print("اختبار السيرفر المحلي...")
    test_upload_endpoint("http://localhost:8000", token)
    
    print()
    test_prod = input("اختبار السيرفر الإنتاجي أيضاً؟ (y/n): ").strip().lower()
    if test_prod == 'y':
        print()
        test_upload_endpoint("http://46.62.239.119:8000", token)
