"""
اختبار عملي لنظام OCR
====================

يقوم بـ:
1. إنشاء صورة بطاقة تجريبية
2. معالجتها بـ OCR
3. عرض النتائج
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.services.business_card_ocr import BusinessCardProcessor

print("=" * 60)
print("اختبار نظام OCR للبطاقات")
print("=" * 60)
print()

# Step 1: Create test card images
print("📝 الخطوة 1: إنشاء صورة بطاقة تجريبية")

temp_dir = Path("tmp/test_cards")
temp_dir.mkdir(parents=True, exist_ok=True)

# Create a simple business card image
def create_test_card(filename: str, name: str, company: str, phone: str, email: str):
    """إنشاء صورة بطاقة تجريبية."""
    # Create image
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font_large = ImageFont.truetype("arial.ttf", 40)
        font_medium = ImageFont.truetype("arial.ttf", 28)
        font_small = ImageFont.truetype("arial.ttf", 20)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw text
    y_offset = 50
    
    # Name
    draw.text((50, y_offset), name, fill='black', font=font_large)
    y_offset += 60
    
    # Company
    draw.text((50, y_offset), company, fill='navy', font=font_medium)
    y_offset += 50
    
    # Title
    draw.text((50, y_offset), "Marketing Director", fill='gray', font=font_small)
    y_offset += 50
    
    # Contact info
    draw.text((50, y_offset), f"📱 {phone}", fill='black', font=font_small)
    y_offset += 40
    
    draw.text((50, y_offset), f"📧 {email}", fill='black', font=font_small)
    y_offset += 40
    
    draw.text((50, y_offset), "🌐 www.company.com", fill='black', font=font_small)
    
    # Save
    filepath = temp_dir / filename
    img.save(filepath)
    print(f"  ✅ تم إنشاء: {filename}")
    return filepath


# Create test cards
card_paths = []

card1 = create_test_card(
    "card1.jpg",
    "Ahmed Mohammed",
    "Tech Solutions Inc.",
    "+966 50 123 4567",
    "ahmed@techsolutions.com"
)
card_paths.append(card1)

card2 = create_test_card(
    "card2.jpg",
    "Sarah Johnson",
    "Marketing Agency LLC",
    "+1-555-987-6543",
    "sarah@marketing.com"
)
card_paths.append(card2)

card3 = create_test_card(
    "card3.jpg",
    "خالد الرشيد",
    "شركة التقنية المتقدمة",
    "+966 11 234 5678",
    "khalid@advanced.sa"
)
card_paths.append(card3)

print()

# Step 2: Process with OCR
print("🔍 الخطوة 2: معالجة الصور بـ OCR")
print("  جاري المعالجة...")
print()

try:
    processor = BusinessCardProcessor(card_paths)
    df = processor.run(dedupe=True)
    
    print("✅ تمت المعالجة بنجاح!")
    print()
    
    # Step 3: Display results
    print("=" * 60)
    print("📊 النتائج")
    print("=" * 60)
    print()
    
    for idx, row in df.iterrows():
        print(f"🎴 البطاقة {idx + 1}: {row['source_file']}")
        print(f"   الاسم:       {row['name']}")
        print(f"   الشركة:      {row['company']}")
        print(f"   المسمى:      {row['title']}")
        print(f"   الهاتف:      {row['phones']}")
        print(f"   البريد:      {row['emails']}")
        print(f"   الموقع:      {row['website']}")
        print(f"   نقاط الجودة: {row['quality_score']:.0f}/100")
        
        if row['duplicate_of']:
            print(f"   ⚠️  مكرر من: {row['duplicate_of']}")
        
        print()
    
    # Statistics
    print("=" * 60)
    print("📈 الإحصائيات")
    print("=" * 60)
    print(f"  إجمالي البطاقات: {len(df)}")
    print(f"  متوسط الجودة:    {df['quality_score'].mean():.1f}/100")
    print(f"  أعلى جودة:       {df['quality_score'].max():.0f}/100")
    print(f"  أقل جودة:        {df['quality_score'].min():.0f}/100")
    
    duplicates = df['duplicate_of'].notna().sum()
    print(f"  المكررات:        {duplicates}")
    print()
    
    # Save results
    output_file = temp_dir / "ocr_results.csv"
    BusinessCardProcessor.save_to_csv(df, output_file)
    print(f"💾 تم حفظ النتائج في: {output_file}")
    print()
    
    # Display raw text sample
    print("=" * 60)
    print("📝 عينة من النص المستخرج")
    print("=" * 60)
    if len(df) > 0:
        sample_text = df.iloc[0]['raw_text'][:200]
        print(f"{sample_text}...")
    print()
    
    print("=" * 60)
    print("✅ الاختبار نجح بالكامل!")
    print("=" * 60)

except Exception as e:
    print(f"❌ خطأ في المعالجة: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Cleanup
    print()
    print("🧹 تنظيف الملفات المؤقتة...")
    for path in card_paths:
        try:
            if path.exists():
                path.unlink()
                print(f"  ✅ تم حذف: {path.name}")
        except Exception as e:
            print(f"  ⚠️  فشل حذف {path.name}: {e}")
    
    print()
    print("=" * 60)
    print("انتهى الاختبار!")
    print("=" * 60)
