# تحسين دقة OCR بإضافة تلميحات اللغة العربية/الإنجليزية + سكربتات فحص لويندوز

- نبذة:

  - تحسين التعرف البصري على النصوص في البطاقات ثنائية اللغة (عربي/إنجليزي) عبر تفعيل تلميحات اللغة في Google Vision.
  - إضافة سكربتات فحص وتشغيل سريعة لمستخدمي ويندوز.

- التغييرات:

  - `backend/app/routers/ocr.py`: استخدام `ImageContext(language_hints=["ar","en"])` مع `text_detection`.
  - `backend/app/services/ocr_google.py`: تمرير `language_hints=["ar","en"]` مع `document_text_detection`.
  - `scripts/windows/health-check.ps1`: فحص صحة الخدمة + خيار اختبار رفع صورة.
  - `scripts/windows/test-ocr.ps1`: اختبار سريع لرفع صورة إلى `/api/v1/ocr/card`.

- السبب:

  - بطاقات الأعمال العربية/الإنجليزية كانت قد تتأثر بدقة أقل بدون تلميحات لغة.
  - تسهيل الفحص على ويندوز بدون الاعتماد على WSL/bash.

- كيف تختبر:

  - تغيير ترميز الكونسول لعرض العربية:
    ```powershell
    chcp 65001
    ```
  - فحص الصحة:
    ```powershell
    powershell -ExecutionPolicy Bypass -File scripts/windows/health-check.ps1 -BaseUrl "https://aidotoo.com"
    ```
  - اختبار رفع صورة:
    ```powershell
    powershell -ExecutionPolicy Bypass -File scripts/windows/test-ocr.ps1 -BaseUrl "https://aidotoo.com" -ImagePath "C:\\path\\to\\card.jpg"
    ```

- ملاحظات:
  - نقطة النهاية المعتمدة: `/api/v1/ocr/card` فقط.
  - لا تغييرات على الواجهة العامة بخلاف تحسين الدقة.
  - يُفضّل دمج هذا الفرع ثم نشر التغييرات وإعادة تشغيل الخدمة.
