"""
اختبار OCR مع الصورة المرفقة
"""
import sys
sys.path.insert(0, 'D:\\datapurity\\backend')

from app.services.business_card_ocr import BusinessCardProcessor, ocr_image, extract_fields_from_text
from PIL import Image
import json

def test_attached_image():
    print("=" * 80)
    print("🧪 اختبار OCR مع الصورة المرفقة")
    print("=" * 80)
    print()
    
    # تحميل الصورة
    image_path = input("أدخل مسار الصورة: ").strip().strip('"')
    
    try:
        image = Image.open(image_path)
        print(f"✅ تم تحميل الصورة: {image.size}")
        print()
        
        # معالجة الصورة
        print("⏳ جاري معالجة الصورة...")
        ocr_text = ocr_image(image)
        result = extract_fields_from_text(ocr_text)
        
        print()
        print("=" * 80)
        print("📝 النص الكامل المستخرج من OCR:")
        print("=" * 80)
        print(ocr_text)
        print()
        
        print("=" * 80)
        print("📊 الحقول المستخرجة:")
        print("=" * 80)
        print()
        print(f"👤 الاسم:          '{result.get('name', '')}'")
        print(f"💼 المسمى الوظيفي: '{result.get('title', '')}'")
        print(f"🏢 الشركة:         '{result.get('company', '')}'")
        print(f"📞 الهاتف:         '{result.get('phone', '')}'")
        print(f"📧 الإيميل:        '{result.get('email', '')}'")
        print(f"🌐 الموقع:         '{result.get('website', '')}'")
        print(f"📍 العنوان:        '{result.get('address', '')}'")
        print()
        
        # حساب الجودة
        fields = ['name', 'title', 'company', 'phone', 'email']
        extracted = sum(1 for f in fields if result.get(f))
        quality = (extracted / len(fields)) * 100
        print(f"⭐ جودة الاستخراج: {quality:.0f}/100")
        print()
        
        # تحليل المشكلة
        print("=" * 80)
        print("🔍 تحليل المشكلة:")
        print("=" * 80)
        
        issues = []
        if not result.get('name') or result.get('name', '').strip() == "":
            issues.append("❌ الاسم فارغ")
        if not result.get('title') or result.get('title', '').strip() == "":
            issues.append("❌ المسمى الوظيفي فارغ")
        if not result.get('company') or result.get('company', '').strip() == "":
            issues.append("❌ اسم الشركة فارغ")
        if not result.get('phone') or result.get('phone', '').strip() == "":
            issues.append("❌ رقم الهاتف فارغ")
        if not result.get('email') or result.get('email', '').strip() == "":
            issues.append("❌ الإيميل فارغ")
        
        if issues:
            print("⚠️  المشاكل المكتشفة:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("✅ جميع الحقول المطلوبة تم استخراجها")
        
        print()
        
        # عرض البيانات الصحيحة المتوقعة من الصورة
        print("=" * 80)
        print("✅ البيانات الصحيحة المتوقعة (من الصورة):")
        print("=" * 80)
        print("الاسم:   براء اليد")
        print("المسمى:  مدير التسويق")
        print("الشركة:  شركة 1")
        print("الهاتف:  +966 50 123 1000")
        print("الإيميل: contact1@company.com")
        print("العنوان: الرياض، المملكة العربية السعودية")
        print()
        
    except FileNotFoundError:
        print(f"❌ الملف غير موجود: {image_path}")
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_attached_image()
