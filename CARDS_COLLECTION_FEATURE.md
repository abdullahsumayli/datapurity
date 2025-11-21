# 📇 نظام مجموعة الكروت المركزي

## نظرة عامة
صفحة مركزية لتجميع وإدارة جميع البيانات المستخرجة من الكروت من جميع مصادر الاستخراج.

## المسار
```
/app/cards/collection
```

## المزايا الرئيسية

### ✅ التجميع التلقائي
- تُحفظ البيانات المستخرجة من **رفع متعدد** و **مسح فردي** تلقائيًا
- كل كرت يُسجل مع معلومات المصدر وتاريخ الإضافة
- التخزين في `localStorage` باسم `cards_collection`

### 📊 الإحصائيات
- **إجمالي الكروت**: العدد الكلي
- **رفع متعدد**: الكروت من CardUploadPage
- **مسح فردي**: الكروت من BulkCardScanPage
- **يدوي**: كروت مضافة يدويًا (مستقبلاً)

### 🔍 البحث والفلترة
- **البحث**: بالاسم، الشركة، الهاتف، أو البريد
- **الفلاتر**: حسب المصدر (الكل، رفع متعدد، مسح فردي، يدوي)
- تحديث فوري للنتائج

### ⚙️ العمليات
1. **تحديد الكل**: تحديد/إلغاء تحديد جميع الكروت المعروضة
2. **تصدير Excel**: تصدير المحدد أو الكل إلى .xlsx
3. **تصدير CSV**: تصدير المحدد أو الكل إلى .csv
4. **حذف المحدد**: حذف الكروت المحددة
5. **حذف الكل**: مسح المجموعة بالكامل (مع تأكيد)

## التكامل مع الصفحات الأخرى

### CardProcessingPage
```typescript
const saveToContacts = async () => {
  const existingCollection = localStorage.getItem('cards_collection')
  const collection = existingCollection ? JSON.parse(existingCollection) : []
  
  const source = fromBulkScan ? 'single-scan' : 'bulk-upload'
  
  const newContacts = contacts.map(contact => ({
    ...contact,
    source,
    addedAt: new Date().toISOString()
  }))
  
  const updatedCollection = [...collection, ...newContacts]
  localStorage.setItem('cards_collection', JSON.stringify(updatedCollection))
  
  navigate('/app/cards/collection')
}
```

### BulkCardScanPage
```typescript
const processAllCards = async () => {
  const contacts = detectedCards.map((card, index) => ({
    // ... بيانات الكرت
  }))

  navigate('/app/cards/processing', { 
    state: { 
      contacts,
      fromBulkScan: true  // ← مهم لتحديد المصدر
    } 
  })
}
```

## بنية البيانات

### Contact Interface
```typescript
interface Contact {
  id: number
  name: string
  company: string
  phone: string
  email: string
  address: string
  position: string
  source: 'bulk-upload' | 'single-scan' | 'manual'
  addedAt: string  // ISO timestamp
}
```

### مثال على البيانات المخزنة
```json
[
  {
    "id": 1,
    "name": "أحمد محمد",
    "company": "شركة التقنية",
    "phone": "+966 50 123 1000",
    "email": "contact1@company.com",
    "address": "الرياض، المملكة العربية السعودية",
    "position": "مدير",
    "source": "bulk-upload",
    "addedAt": "2025-11-22T10:30:00.000Z"
  }
]
```

## الوصول السريع

### من CardUploadPage
```tsx
<button onClick={() => navigate('/app/cards/collection')}>
  📇 مجموعة الكروت
</button>
```

### من BulkCardScanPage
زر في الـ Header للوصول المباشر

## التصدير

### Excel (.xlsx)
- جداول منسقة بالعربي
- أعمدة: الاسم، الشركة، الهاتف، البريد، العنوان، المنصب، المصدر، التاريخ
- يستخدم مكتبة `xlsx`

### CSV
- UTF-8 with BOM (دعم العربية)
- نفس الأعمدة كـ Excel
- متوافق مع Excel وGoogle Sheets

## سيناريو الاستخدام

1. **المستخدم يرفع كروت متعددة**
   - CardUploadPage → CardProcessingPage
   - يضغط "💾 حفظ في جهات الاتصال"
   - البيانات تُحفظ مع `source: 'bulk-upload'`
   - ينتقل تلقائيًا لـ CardsCollectionPage

2. **المستخدم يرفع صورة بها عدة كروت**
   - BulkCardScanPage → CardProcessingPage
   - يضغط "💾 حفظ في جهات الاتصال"
   - البيانات تُحفظ مع `source: 'single-scan'`
   - ينتقل تلقائيًا لـ CardsCollectionPage

3. **في صفحة المجموعة**
   - يمكنه البحث والفلترة
   - تحديد كروت معينة
   - تصدير Excel أو CSV
   - حذف ما لا يحتاجه

## التحسينات المستقبلية

- [ ] مزامنة مع Backend API
- [ ] إضافة كروت يدويًا
- [ ] تعديل الكروت من صفحة المجموعة
- [ ] دمج الكروت المكررة
- [ ] مشاركة المجموعة
- [ ] استيراد من Excel/CSV
- [ ] الربط مع CRM

## الملفات المتأثرة

```
frontend/src/pages/cards/
├── CardsCollectionPage.tsx    (جديد - 340 سطر)
├── CardsCollectionPage.css    (جديد - 390 سطر)
├── CardProcessingPage.tsx     (محدث)
├── CardUploadPage.tsx         (محدث)
└── BulkCardScanPage.tsx       (جاهز للتكامل)

frontend/src/router.tsx         (محدث)
```

## API Routes
```typescript
<Route path="cards">
  <Route path="upload" element={<CardUploadPage />} />
  <Route path="bulk-scan" element={<BulkCardScanPage />} />
  <Route path="processing" element={<CardProcessingPage />} />
  <Route path="collection" element={<CardsCollectionPage />} />
</Route>
```

---

**تم التنفيذ**: 22 نوفمبر 2025  
**الحالة**: ✅ جاهز للاستخدام على السيرفر
