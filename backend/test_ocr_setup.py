"""
اختبار نظام استخراج المعلومات من صور الكروت (OCR)
====================================================

هذا السكربت يتحقق من:
1. تثبيت Tesseract OCR
2. عمل السيرفس business_card_ocr.py
3. الـ endpoint /api/v1/cards/ocr
"""

import sys
from pathlib import Path

print("=" * 60)
print("اختبار نظام OCR للكروت")
print("=" * 60)
print()

# Test 1: Import check
print("📦 الخطوة 1: التحقق من المكتبات")
try:
    from PIL import Image
    print("  ✅ PIL (Pillow) مثبت")
except ImportError:
    print("  ❌ PIL (Pillow) غير مثبت")
    sys.exit(1)

try:
    import pytesseract
    print("  ✅ pytesseract مثبت")
except ImportError:
    print("  ❌ pytesseract غير مثبت")
    sys.exit(1)

try:
    import pandas as pd
    print("  ✅ pandas مثبت")
except ImportError:
    print("  ❌ pandas غير مثبت")
    sys.exit(1)

print()

# Test 2: Tesseract binary check
print("🔍 الخطوة 2: التحقق من Tesseract OCR Engine")
import platform
import os

tesseract_found = False
tesseract_path = None

if platform.system() == "Windows":
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\ProgramData\chocolatey\bin\tesseract.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            tesseract_found = True
            tesseract_path = path
            pytesseract.pytesseract.tesseract_cmd = path
            print(f"  ✅ Tesseract موجود في: {path}")
            break
    
    if not tesseract_found:
        print("  ❌ Tesseract غير مثبت!")
        print()
        print("  📥 للتثبيت:")
        print("     1. حمّل من: https://github.com/UB-Mannheim/tesseract/wiki")
        print("     2. أو استخدم Chocolatey: choco install tesseract")
        print("     3. أعد تشغيل الاختبار")
        sys.exit(1)
else:
    # Linux/Mac
    import subprocess
    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            tesseract_found = True
            version = result.stdout.split('\n')[0]
            print(f"  ✅ Tesseract مثبت: {version}")
        else:
            print("  ❌ Tesseract غير مثبت")
            print("  📥 للتثبيت: sudo apt-get install tesseract-ocr")
            sys.exit(1)
    except FileNotFoundError:
        print("  ❌ Tesseract غير مثبت")
        print("  📥 للتثبيت: sudo apt-get install tesseract-ocr")
        sys.exit(1)

print()

# Test 3: Get Tesseract version
print("📊 الخطوة 3: معلومات Tesseract")
try:
    version = pytesseract.get_tesseract_version()
    print(f"  ✅ الإصدار: {version}")
except Exception as e:
    print(f"  ⚠️  تعذر الحصول على الإصدار: {e}")

print()

# Test 4: Check Arabic language support
print("🌐 الخطوة 4: التحقق من دعم اللغة العربية")
try:
    langs = pytesseract.get_languages()
    if 'ara' in langs:
        print("  ✅ اللغة العربية مدعومة")
    else:
        print("  ⚠️  اللغة العربية غير مثبتة")
        print("  📥 للتثبيت:")
        print("     Windows: أعد تشغيل تثبيت Tesseract واختر Arabic")
        print("     Linux: sudo apt-get install tesseract-ocr-ara")
    
    print(f"  📋 اللغات المثبتة: {', '.join(langs[:10])}")
    if len(langs) > 10:
        print(f"      ... و {len(langs) - 10} لغات أخرى")
except Exception as e:
    print(f"  ⚠️  تعذر فحص اللغات: {e}")

print()

# Test 5: Import business card service
print("📄 الخطوة 5: التحقق من business_card_ocr.py")
try:
    from app.services.business_card_ocr import BusinessCardProcessor
    print("  ✅ BusinessCardProcessor متاح")
except ImportError as e:
    print(f"  ❌ فشل استيراد BusinessCardProcessor: {e}")
    sys.exit(1)

print()

# Test 6: Check endpoint
print("🌐 الخطوة 6: التحقق من endpoint")
try:
    from app.routers.cards import router
    print("  ✅ Cards router متاح")
    print("  📍 Endpoint: POST /api/v1/cards/ocr")
except ImportError as e:
    print(f"  ❌ فشل استيراد router: {e}")

print()

# Summary
print("=" * 60)
print("📊 الملخص")
print("=" * 60)

if tesseract_found:
    print("✅ نظام OCR جاهز للعمل!")
    print()
    print("📝 كيفية الاستخدام:")
    print()
    print("1️⃣ عبر API:")
    print("   POST http://localhost:8000/api/v1/cards/ocr")
    print("   Body: multipart/form-data مع ملفات الصور")
    print()
    print("2️⃣ عبر السكربت مباشرة:")
    print("   cd backend")
    print("   python -m app.services.business_card_ocr path/to/images --output results.csv")
    print()
    print("📦 الميزات:")
    print("  • معالجة دفعات من الصور")
    print("  • استخراج: الاسم، الشركة، المسمى الوظيفي، الهاتف، البريد، الموقع")
    print("  • معالجة الصور (تحسين الجودة)")
    print("  • إزالة التكرار")
    print("  • تسجيل جودة (quality score)")
    print("  • دعم العربية والإنجليزية")
else:
    print("⚠️  يرجى تثبيت Tesseract OCR أولاً")

print("=" * 60)
