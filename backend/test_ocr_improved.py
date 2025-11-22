"""
اختبار محسّن لـ OCR مع صور أفضل
================================
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from app.services.business_card_ocr import BusinessCardProcessor

print("=" * 60)
print("اختبار OCR المحسّن")
print("=" * 60)
print()

temp_dir = Path("tmp/ocr_improved_test")
temp_dir.mkdir(parents=True, exist_ok=True)

# Create a more realistic business card with better spacing
def create_realistic_card(filename: str):
    """Create a realistic business card image."""
    img = Image.new('RGB', (1200, 700), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_name = ImageFont.truetype("arial.ttf", 60)
        font_company = ImageFont.truetype("arial.ttf", 42)
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_contact = ImageFont.truetype("arial.ttf", 28)
    except:
        font_name = ImageFont.load_default()
        font_company = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_contact = ImageFont.load_default()
    
    y = 100
    
    # Name - clearly separated
    draw.text((100, y), "Ahmed Mohammed", fill='#000000', font=font_name)
    y += 100
    
    # Company - clearly separated
    draw.text((100, y), "Tech Solutions Inc", fill='#1a1a1a', font=font_company)
    y += 80
    
    # Title - clearly separated
    draw.text((100, y), "Marketing Director", fill='#555555', font=font_title)
    y += 100
    
    # Separator
    draw.line([(100, y), (1100, y)], fill='#cccccc', width=3)
    y += 60
    
    # Contact info - each on its own line
    draw.text((100, y), "+966 50 123 4567", fill='#000000', font=font_contact)
    y += 60
    
    draw.text((100, y), "ahmed@techsolutions.com", fill='#000000', font=font_contact)
    y += 60
    
    draw.text((100, y), "www.techsolutions.com", fill='#000000', font=font_contact)
    
    # Border
    draw.rectangle([(20, 20), (1180, 680)], outline='#333333', width=5)
    
    filepath = temp_dir / filename
    img.save(filepath, quality=95, dpi=(300, 300))
    return filepath


# Create test cards
print("📝 إنشاء بطاقات اختبار محسّنة...")
cards = []

card1 = create_realistic_card("card_realistic.jpg")
cards.append(card1)
print(f"  ✅ {card1.name}")

print()
print("🔍 معالجة البطاقات...")
print()

try:
    processor = BusinessCardProcessor(cards)
    df = processor.run(dedupe=False)
    
    print("=" * 60)
    print("📊 النتائج")
    print("=" * 60)
    print()
    
    for idx, row in df.iterrows():
        print(f"🎴 البطاقة: {row['source_file']}")
        print(f"   ✓ الاسم:   '{row['name']}'")
        print(f"   ✓ الشركة:  '{row['company']}'")
        print(f"   ✓ المسمى:  '{row['title']}'")
        print(f"   ✓ الهاتف:  '{row['phones']}'")
        print(f"   ✓ البريد:  '{row['emails']}'")
        print(f"   ✓ الموقع:  '{row['website']}'")
        print(f"   ✓ الجودة:  {row['quality_score']}/100")
        print()
        
        # Show full raw text for debugging
        print("📝 النص الكامل المستخرج:")
        print("   " + "\n   ".join(row['raw_text'].split('\n')[:10]))
        print()
    
    # Check quality
    if len(df) > 0:
        avg_quality = df['quality_score'].mean()
        print(f"متوسط الجودة: {avg_quality:.1f}/100")
        
        # Detailed check
        row = df.iloc[0]
        checks = {
            'الاسم': row['name'] != '',
            'الشركة': row['company'] != '',
            'المسمى': row['title'] != '',
            'الهاتف': row['phones'] != '',
            'البريد': row['emails'] != '',
            'الموقع': row['website'] != ''
        }
        
        print()
        print("=" * 60)
        print("✓ فحص الحقول:")
        print("=" * 60)
        for field, found in checks.items():
            status = "✅" if found else "❌"
            print(f"  {status} {field}")
        
        success_rate = sum(checks.values()) / len(checks) * 100
        print()
        print(f"معدل النجاح: {success_rate:.0f}%")
        
        if success_rate >= 80:
            print("🎉 ممتاز!")
        elif success_rate >= 60:
            print("👍 جيد")
        else:
            print("⚠️ يحتاج تحسين")

except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Cleanup
    print()
    print("🧹 تنظيف...")
    for card in cards:
        try:
            if card.exists():
                card.unlink()
        except:
            pass
    
    print()
    print("=" * 60)
    print("انتهى!")
    print("=" * 60)
