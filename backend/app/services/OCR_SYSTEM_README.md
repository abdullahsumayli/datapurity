# Business Card OCR System - DataPurity

## Overview

نظام OCR احترافي لمعالجة كروت الأعمال (Business Cards) باستخدام Tesseract OCR. يدعم معالجة دفعات كبيرة من الصور واستخراج البيانات المنظمة بجودة عالية.

## Features

### Core Capabilities

- ✅ **Batch Processing**: معالجة عدة كروت دفعة واحدة
- ✅ **Multi-language**: دعم اللغتين الإنجليزية والعربية (eng+ara)
- ✅ **Field Extraction**: استخراج تلقائي للحقول:
  - الاسم (Name)
  - الشركة (Company)
  - المسمى الوظيفي (Job Title)
  - أرقام الجوال (Phones)
  - البريد الإلكتروني (Emails)
  - الموقع الإلكتروني (Website)

### Advanced Features

- 🎯 **Quality Scoring**: تقييم جودة البيانات المستخرجة (0-100)
- 🔍 **Deduplication**: كشف وإزالة التكرارات تلقائيًا
- 🖼️ **Image Preprocessing**: تحسين الصور قبل OCR:
  - Grayscale conversion
  - Auto-contrast
  - Noise reduction (Median Filter)
  - Binarization (Threshold)
  - Standardized resizing

### Data Cleaning

- 📞 **Phone Normalization**: توحيد تنسيق أرقام الجوال
- 📧 **Email Validation**: تنظيف وتوحيد الإيميلات
- 🌐 **URL Standardization**: تنسيق الروابط بشكل موحد

## Architecture

```
app/services/business_card_ocr.py  # Core OCR engine
app/routers/cards.py                # FastAPI endpoints
```

### Main Components

#### 1. BusinessCardProcessor Class

```python
processor = BusinessCardProcessor(image_paths, logger=None)
df = processor.run(dedupe=True)
```

**Methods:**

- `process_all()`: معالجة جميع الصور
- `run(dedupe=True)`: تشغيل كامل البايبلاين
- `save_to_csv(df, path)`: حفظ النتائج كـ CSV

#### 2. CardRecord Data Model

```python
@dataclass
class CardRecord:
    source_file: str
    name: str
    company: str
    title: str
    phones: str
    emails: str
    website: str
    raw_text: str
    quality_score: float
    duplicate_of: Optional[str]
```

## API Endpoints

### POST /api/v1/ocr/card

معالجة كروت الأعمال باستخدام OCR.

**Request:**

```http
POST /api/v1/ocr/card
Content-Type: multipart/form-data

file: card.jpg
```

**Response:**

```json
{
  "success": true,
  "count": 3,
  "message": "Successfully processed 3 business cards",
  "records": [
    {
      "source_file": "card1.jpg",
      "name": "أحمد محمد",
      "company": "شركة التقنية المتقدمة",
      "title": "مدير تطوير الأعمال",
      "phones": "+966501234567",
      "emails": "ahmed@tech.sa",
      "website": "https://www.tech.sa",
      "quality_score": 90.0,
      "duplicate_of": null,
      "raw_text": "..."
    }
  ]
}
```

**Error Response:**

```json
{
  "detail": "OCR processing failed: ..."
}
```

## Installation

### 1. Install Tesseract OCR

#### Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-ara  # Arabic language pack
```

#### Windows:

1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location
3. Add to PATH or configure in code:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

#### macOS:

```bash
brew install tesseract
brew install tesseract-lang  # For Arabic support
```

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Required packages:

- `pytesseract==0.3.10`
- `Pillow==10.2.0`
- `pandas==2.2.0`

### 3. Verify Installation

```bash
tesseract --version
tesseract --list-langs  # Should show 'ara' and 'eng'
```

## Usage

### CLI Usage (Standalone Testing)

```bash
cd backend/app/services

# Process all cards in a folder
python business_card_ocr.py /path/to/cards --output results.csv

# Disable deduplication
python business_card_ocr.py /path/to/cards --no-dedupe
```

### API Usage

```python
import httpx

files = [
    ('files', open('card1.jpg', 'rb')),
    ('files', open('card2.jpg', 'rb'))
]

response = httpx.post(
  'http://localhost:8000/api/v1/ocr/card',
  files={'file': open('card1.jpg', 'rb')},
  headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

print(response.json())
```

### Programmatic Usage

```python
from pathlib import Path
from app.services.business_card_ocr import BusinessCardProcessor

# Prepare image paths
images = list(Path('/path/to/cards').glob('*.jpg'))

# Process
processor = BusinessCardProcessor(images)
df = processor.run(dedupe=True)

# Save results
BusinessCardProcessor.save_to_csv(df, Path('output.csv'))

# Access data
print(f"Processed {len(df)} cards")
print(f"Average quality: {df['quality_score'].mean():.1f}")
```

## Configuration

### OCR Language

Edit in `business_card_ocr.py`:

```python
OCR_LANG = "eng+ara"  # English + Arabic
# OCR_LANG = "eng"     # English only
# OCR_LANG = "ara"     # Arabic only
```

### Image Preprocessing Parameters

```python
# In preprocess_image() function:
target_width = 1000          # Resize width
threshold = 140              # Binarization threshold
median_filter_size = 3       # Noise reduction filter size
```

### Deduplication Logic

```python
# In _dedupe_records() method:
# Key = (first_email, first_phone)
# Master = highest quality_score
```

## Quality Score Calculation

| Field     | Points  |
| --------- | ------- |
| Name      | +20     |
| Company   | +20     |
| Title     | +10     |
| Phones    | +20     |
| Emails    | +20     |
| Website   | +10     |
| **Total** | **100** |

## Field Extraction Logic

### Name Detection

- أول أو ثاني سطر غير فارغ
- لا يحتوي على @ أو www
- لا يحتوي أرقام كثيرة
- طوله معقول (≤4 كلمات)

### Company Detection

1. **Keyword matching**: ابحث عن كلمات مثل "شركة", "company", "corp", "inc"
2. **Fallback**: اختر سطر طويل (>10 حرف) من السطور 1-4

### Title Detection

- ابحث عن كلمات مثل "مدير", "manager", "director", "engineer"

### Contact Info

- **Phones**: Regex pattern + تنظيف + فلترة (<7 أرقام)
- **Emails**: Regex pattern + lowercase
- **URLs**: Regex pattern + إضافة https://

## Performance Tips

### Image Quality

- ✅ استخدم صور بدقة عالية (≥300 DPI)
- ✅ تأكد من وضوح النص
- ✅ تجنب الصور المائلة أو المشوهة

### Batch Processing

- معالجة 100 كرت تستغرق ~1-2 دقيقة (حسب جودة الصور)
- كل صورة تُعالج بشكل مستقل
- الأخطاء في صورة لا تؤثر على باقي الدفعة

### Optimization

```python
# استخدم معالجة متوازية للدفعات الكبيرة
from concurrent.futures import ThreadPoolExecutor

def process_batch(paths):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_single_card, paths))
    return results
```

## Error Handling

### Common Issues

#### 1. Tesseract Not Found

```
pytesseract.TesseractNotFoundError
```

**Solution**: تأكد من تثبيت Tesseract وتحديد المسار

#### 2. Language Data Missing

```
Error opening data file ara.traineddata
```

**Solution**: ثبّت حزم اللغة:

```bash
sudo apt-get install tesseract-ocr-ara
```

#### 3. Poor OCR Results

- تحقق من جودة الصور
- جرب تعديل threshold في preprocessing
- تأكد من تثبيت حزم اللغة الصحيحة

## Future Enhancements

### Planned Features

- [ ] Database integration (save to contacts table)
- [ ] Advanced image rotation detection
- [ ] Support for QR codes on cards
- [ ] Machine learning-based field classification
- [ ] Confidence scores per field
- [ ] API for batch status tracking
- [ ] WebSocket support for real-time progress

### Integration Ideas

```python
# Save to database (future)
@router.post("/ocr/card")
async def ocr_cards(files, db: Session):
    processor = BusinessCardProcessor(paths)
    df = processor.run(dedupe=True)

    # Save to contacts table
    for _, row in df.iterrows():
        contact = Contact(
            name=row['name'],
            company=row['company'],
            phone=row['phones'],
            email=row['emails']
        )
        db.add(contact)

    db.commit()
    return {"count": len(df)}
```

## Testing

### Unit Tests

```bash
pytest tests/test_ocr.py -v
```

### Integration Tests

```bash
# Test endpoint
curl -X POST http://localhost:8000/api/v1/ocr/card \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@card1.jpg"
```

### Sample Test Cases

```python
def test_phone_extraction():
    text = "Mobile: +966 50 123 4567"
    fields = extract_fields_from_text(text)
    assert fields['phones'] == "+966501234567"

def test_deduplication():
    records = [
        CardRecord(source_file="c1.jpg", emails="test@email.com", quality_score=80),
        CardRecord(source_file="c2.jpg", emails="test@email.com", quality_score=90)
    ]
    result = BusinessCardProcessor._dedupe_records(records)
    assert result[0].duplicate_of == "c2.jpg"  # Lower score marked as duplicate
```

## License

MIT License - DataPurity SaaS Platform

## Support

For issues or questions:

- GitHub Issues: https://github.com/abdullahsumayli/datapurity
- Email: support@datapurity.sa

---

**Last Updated**: 2025-11-22
**Version**: 1.0.0
