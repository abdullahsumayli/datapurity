"""
اختبار OCR مع صورة بطاقة حقيقية
"""
import requests
import json
import sys
from pathlib import Path

def test_real_card(image_path: str, api_url: str = "http://localhost:8000"):
    """
    اختبار OCR مع صورة بطاقة حقيقية
    
    Args:
        image_path: مسار الصورة
        api_url: عنوان API (local أو production)
    """
    print("=" * 60)
    print("🧪 اختبار OCR مع بطاقة حقيقية")
    print("=" * 60)
    print()
    
    # التحقق من وجود الملف
    image_file = Path(image_path)
    if not image_file.exists():
        print(f"❌ الملف غير موجود: {image_path}")
        print()
        print("📁 الاستخدام:")
        print("   python test_real_card.py <مسار_الصورة>")
        print()
        print("📝 مثال:")
        print("   python test_real_card.py card.jpg")
        print("   python test_real_card.py D:\\Downloads\\business_card.png")
        return
    
    print(f"📸 الصورة: {image_file.name}")
    print(f"📊 الحجم: {image_file.stat().st_size / 1024:.1f} KB")
    print(f"🌐 API: {api_url}")
    print()
    
    # إرسال الطلب
    try:
        print("⏳ جاري المعالجة...")
        
        with open(image_file, 'rb') as f:
            files = {'file': (image_file.name, f, 'image/jpeg')}
            response = requests.post(
                f"{api_url}/api/v1/cards/ocr",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ نجحت المعالجة!")
            print()
            print("=" * 60)
            print("📋 البيانات المستخرجة:")
            print("=" * 60)
            print()
            
            cards = result.get('cards', [])
            if cards:
                card = cards[0]
                
                # الحقول المطلوبة
                print(f"👤 الاسم:          {card.get('name', '❌ لم يُستخرج')}")
                print(f"💼 المسمى الوظيفي: {card.get('title', '❌ لم يُستخرج')}")
                print(f"🏢 اسم الشركة:     {card.get('company', '❌ لم يُستخرج')}")
                print(f"📞 رقم الهاتف:     {card.get('phone', '❌ لم يُستخرج')}")
                print(f"📧 الإيميل:        {card.get('email', '❌ لم يُستخرج')}")
                print(f"🌐 الموقع:         {card.get('website', '❌ لم يُستخرج')}")
                print()
                print(f"⭐ جودة الاستخراج: {card.get('extraction_quality', 0)}/100")
                print()
                
                # النص الكامل المستخرج
                if card.get('ocr_text'):
                    print("=" * 60)
                    print("📝 النص الكامل المستخرج:")
                    print("=" * 60)
                    print(card['ocr_text'])
                    print()
                
                # تقييم النتيجة
                print("=" * 60)
                print("📊 تقييم النتيجة:")
                print("=" * 60)
                
                fields = ['name', 'title', 'company', 'phone', 'email']
                extracted = sum(1 for f in fields if card.get(f))
                total = len(fields)
                
                print(f"✅ تم استخراج {extracted}/{total} من الحقول المطلوبة")
                
                if extracted == total:
                    print("🎉 ممتاز! جميع الحقول استُخرجت بنجاح")
                elif extracted >= 3:
                    print("⚠️  جيد، لكن بعض الحقول ناقصة")
                else:
                    print("❌ ضعيف، معظم الحقول لم تُستخرج")
                
            else:
                print("⚠️  لم يتم العثور على بيانات")
        
        else:
            print(f"❌ فشل الطلب: {response.status_code}")
            print(f"📄 الرد: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print(f"❌ فشل الاتصال بـ {api_url}")
        print("   تأكد من أن السيرفر يعمل:")
        print("   uvicorn app.main:app --reload")
    
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print()
        print("=" * 60)
        print("📸 اختبار OCR مع صورة بطاقة حقيقية")
        print("=" * 60)
        print()
        print("📁 الاستخدام:")
        print("   python test_real_card.py <مسار_الصورة> [api_url]")
        print()
        print("📝 أمثلة:")
        print("   python test_real_card.py card.jpg")
        print("   python test_real_card.py D:\\Downloads\\business_card.png")
        print("   python test_real_card.py card.jpg http://46.62.239.119:8000")
        print()
        print("💡 ملاحظة:")
        print("   - يمكنك استخدام صور بصيغة: JPG, PNG, JPEG")
        print("   - ضع الصورة في مجلد المشروع أو اكتب المسار الكامل")
        print("   - الـ API الافتراضي: http://localhost:8000")
        print()
        print("=" * 60)
        print()
        sys.exit(1)
    
    image_path = sys.argv[1]
    api_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"
    
    test_real_card(image_path, api_url)
