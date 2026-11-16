# GSDN · النموذج الأولي

نموذج قابل للنقر لمراجعة التصميم قبل التنفيذ. ملف HTML واحد يعمل دون إنترنت ودون خادم.

- **التشغيل:** افتح `gsdn-prototype.html` في المتصفح.
- **إعادة البناء من ملف Excel محدَّث:**

  ```bash
  python3 -I prototype/build.py path/to/GSDN_Site_Master_Template.xlsx
  ```

- **المصدر:** `src/app.html` (الواجهة والمنطق)، و`build.py` (يستخرج المواقع من Master وRF & Design ويضمّنها في الملف).
- **الحفظ:** التعديلات التجريبية تُحفظ في `localStorage` للمتصفح فقط. زر «إعادة ضبط» يمسحها.

التصميم الذي يجسّده: `docs/design/01-site-creation-and-lifecycle.md`.
