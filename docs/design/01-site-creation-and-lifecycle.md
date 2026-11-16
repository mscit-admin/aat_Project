# إنشاء الموقع والانتقال بين المراحل

ملحق بوثيقة «نظام إدارة مشروع GSDN — التصميم المقترح» · 16 نوفمبر 2026

يسد هذا القسم ثغرة في الوثيقة الأصلية: كيف يولد الموقع في النظام، ومن يملك ذلك، وكيف يسير عبر المراحل حتى الإغلاق.

**المصدر:** `GSDN_Site_Master_Template.xlsx`، وتحديداً شيتات Master وRF & Design وSetting، والملاحظات المكتوبة داخل الشيتات. كل قاعدة هنا مأخوذة من الملف ما لم يُذكر أنها اقتراح.

## 1. الخلاصة

| السؤال | الجواب من الملف |
| --- | --- |
| أين يولد الموقع؟ | في شيت **RF & Design**: «صف لكل موقع، وهو مصدر بيانات الموقع… Master وكل السجلات تقرأ منه». |
| من يُنشئه؟ | فريق التصميم والاستملاك: **RF Engineer** تحت **Team Lead (Design & Acquisition)**. |
| منسق المنطقة | **دور جديد** يُضاف إلى `StaffRole`، ولا يُنشئ مواقع (البند 3.4). |
| من يعتمده؟ | **Project Manager**، مقابل عدد المواقع المتعاقد عليه لكل مرحلة مشروع (`tblProjectScope`). |
| صيغة الرمز | بادئة المنطقة + 3 أرقام، مع لاحقة حرف اختيارية: `TR165` و`TR103 A`. |
| كم مرحلة؟ | **عشر مراحل وتسع بوابات**، ومسار جانبي للتفكيك. |
| متى تكون المرحلة «غير منطبقة»؟ | يحددها **نطاق العمل (SOW) للموقع** عند إنشائه، لا قرار يُتخذ عند كل مرحلة. |

> **قرار معتمد:** يبقى إنشاء الموقع عند فريق التصميم كما في الملف، ويُستحدث دور «منسق المنطقة» للمتابعة على مستوى المنطقة. هذا يلغي القرار الأسبق بأن «المنسق يُنشئ الموقع في منطقته».

## 2. إنشاء الموقع

### 2.1 المسار

```
مسودة (RF Engineer)
   └─► بانتظار المراجعة (Team Lead — Design & Acquisition)
          └─► بانتظار الاعتماد (Project Manager)
                 ├─► معتمد ──► يدخل المرحلة 1 ويُجمَّد خطها المرجعي
                 └─► مرفوض (مع السبب) ──► يعود مسودة
```

- **المسودة** لا تدخل أي تقرير أو عدّاد، ولا تحجز رمزاً.
- **منسق المنطقة يُبلَّغ** عند إرسال الموقع للاعتماد وعند اعتماده، ويرى الطلب للاطلاع. ملاحظته اختيارية ولا توقف المسار. بعد الاعتماد يدخل الموقع نطاقه تلقائياً.
- **عند الاعتماد** يتحقق النظام من عدد المواقع المعتمدة لمرحلة المشروع (PH1 / PH2) مقابل `Contract Sites` في `tblProjectScope`.
  - داخل العدد المتعاقد عليه: اعتماد عادي.
  - يتجاوزه: لا يُعتمد إلا كطلب تغيير من نوع `Scope Change`، وهو نوع موجود فعلاً في قائمة `ChangeType`.
- **الخط المرجعي** للمرحلة الأولى يُجمَّد من تاريخ الاعتماد لا من تاريخ المسودة.
- **الإلغاء والنقل** لموقع معتمد يمران عبر طلب تغيير من نوع `Cancellation` أو `Relocation` يعتمده مدير المشروع (`ApprStatus`). الموقع لا يُحذف أبداً.

### 2.2 صيغة رمز الموقع

الصيغة المستخرجة من الـ 469 موقعاً، بلا أي استثناء في البادئات:

```
^(BG|GM|MI|SB|TR|WM|ZW)[0-9]{3}( [A-Z])?$
```

| البادئة | المنطقة | عدد المواقع |
| --- | --- | --- |
| `TR` | Tripoli Area | 165 |
| `MI` | Middle Area | 80 |
| `SB` | Sebha Area | 63 |
| `GM` | GM Area | 49 |
| `WM` | WM Area | 44 |
| `BG` | Benghazi Area | 40 |
| `ZW` | Zawia Area | 28 |

القواعد:

- **البادئة تحددها المنطقة.** يُولّد النظام البادئة من المنطقة المختارة ولا يكتبها المستخدم. تطابُق البادئة والمنطقة 100% في الملف اليوم، فيصبح ذلك قيداً.
- **الرقم التسلسلي** يقترحه النظام (التالي في المنطقة)، ولا يُعاد استخدام رقم موقع ملغى.
- **اللاحقة الحرفية** (`A`) موجودة في 35 موقعاً. تُقبل فقط عبر مسار النقل أو الاستبدال، وتُربط بالموقع الأصلي (البند 2.4).
- **`Site Owner ID`** (رمز مالك البرج، مثل `BGZ008` و`MIS006`) حقل مرجعي منفصل وليس رمز الموقع. لا يُشترط تفرده، لأن موقعين قد يقعان على برج واحد لمالك واحد.

### 2.3 الحقول الإلزامية

**الهوية:** هي أعمدة C–P في RF & Design التي تقرأ منها بقية الشيتات.

| الحقل | القائمة المرجعية / الضابط |
| --- | --- |
| المنطقة | `Region` (7 مناطق)، وتولّد بادئة الرمز |
| المنطقة الفرعية | اقتراح: تصبح إلزامية، فهي ناقصة اليوم في 168 من 475 صفاً |
| اسم الموقع (عربي) | يُشذَّب آلياً |
| Site Owner ID | نص حر، اختياري للمواقع الجديدة كلياً |
| خط العرض / خط الطول | داخل حدود ليبيا، و`Earliest/Latest valid` لا تنطبق هنا |
| Site Type | `SiteType`: Core · MFN · FN · HUB · Terminal |
| Site Scenario | `Scenario`: Outdoor · Indoor |
| Uplink Site | رمز موقع قائم أو `N/A` |
| Tower Owner | `RefRFDesignTowerOwner` |
| Existing or New | `ExistNew` |
| RT or GF | `RTGF` |
| Tower Type | `TowerType` |
| Tower Height (m) | رقم موجب |

**نطاق العمل:** أعمدة X–AG في Master، وهي التي تحدد المراحل المنطبقة (القسم 4).

| الحقل | القيم |
| --- | --- |
| Project Phase | `ProjectPhases`: PH1 · PH2 |
| Delivery Batch | `DeliveryBatches` |
| Delivery Scenario | `DeliveryScenario`: New Build · Expansion · Hot Swap · Cold Swap · Relocation |
| CW SOW — Tower Erection | Yes · N/A |
| CW SOW — Site Adaption | Yes · N/A |
| CW SOW — GECOL Power | Yes · N/A |
| CW SOW — HLC Fiber | Yes · N/A |
| TE SOW — Full Scope / IP Router Only | أحدهما Yes |
| CW Delivery Model | `DeliveryModel`: In-House · Outsourced |

في الملف اليوم 87 موقعاً بلا قيمة في GECOL Power وHLC Fiber وDelivery Model. لهذا يكون النطاق إلزامياً قبل الاعتماد: الموقع بلا نطاق لا يُعرف أي مراحله منطبقة.

### 2.4 منع التكرار

| الفحص | النتيجة | الدليل من الملف |
| --- | --- | --- |
| الرمز مستخدم (بأي حالة، بما فيها ملغى) | **رفض** | — |
| رمز لا يطابق الصيغة | **رفض** | صف `New Site` في RF & Design |
| إحداثيات مطابقة تماماً لموقع قائم | **رفض**، إلا عبر مسار النقل أو الاستبدال | `TR103` في RF & Design و`TR103 A` في Master: الإحداثيات والاسم نفسهما برمزين مختلفين |
| موقع قائم ضمن 50 متراً | **تحذير** مع تبرير إلزامي | مواقع HUB المتجاورة حقيقية |
| اسم مطابق في المنطقة نفسها | **تحذير** | — |

**المواقع الستة الشاردة** موجودة في RF & Design وغائبة عن Master: `BG011` و`BG058` و`BG077` و`BG078` و`TR103` و`New Site`. في النظام لا يمكن أن يوجد موقع في سجل ويغيب عن آخر، لأن المتابعة تُحسب من سجل الموقع نفسه. هذه الستة تُحسم يدوياً قبل الترحيل.

## 3. المراحل والبوابات

### 3.1 المراحل العشر

هذا هو تسلسل `MilestoneOrder` في Setting، وأقسام شيت Master. كل مرحلة تنتهي بمَعلم (Milestone) له خط مرجعي (Baseline) وتاريخ فعلي.

| # | المرحلة | المَعلم الذي يُغلقها | المسؤول (من `StaffRole`) | المصدر في الملف |
| --- | --- | --- | --- | --- |
| 1 | RF & Design | Site Release | Team Lead (Design & Acquisition)، RF Engineer، Acquisition Team | RF & Design، Acquisition، Permission Log |
| 2 | PRE-CW | PRE-CW Completion | Team Lead (CW)، CW Engineer | Master: SOW، CW Procurement، CW Access، المسح والتحليل، CW DN |
| 3 | ACTUAL CW | CW Completion | Team Lead (CW)، Site Engineer | Master: CW MOS، Tower Erection، Site Adaption |
| 4 | RFI | Site RFI | Team Lead (CW)، Team Lead (GECOL)، Team Lead (Fiber) | Master: CW PAC، ‏GECOL، ‏HLC |
| 5 | TE INSTALLATION | TE Completion | Team Lead (TE) | Master: TE Access، Survey، DN، MOS، Items |
| 6 | ON-AIR | On-Air | Team Lead (TE)، MW Engineer | Master: Commissioning، Integration، Cutover |
| 7 | TE PAC | TE PAC | Team Lead (TE) | Master: SSV، HWID، EIR، PAT، As-Built، Snags |
| 8 | CLUSTER OPTIMIZATION | KPI Acceptance | RF Engineer | Master: Cluster ID، KPI Acceptance |
| 9 | LAUNCH & HOTO | HOTO | Project Manager، Inventory Supervisor | Master: Launch، Material Reconciliation، HOTO Package |
| 10 | FINAL CLOSURE | Final Closure | Project Manager | Master: CW DLP/FAC، TE DLP/FAC، الالتزامات التعاقدية |
| — | DISMANTLE (مسار جانبي) | CW RN · TE RN | Team Lead (CW)، Team Lead (TE) | Master: CW / TE Dismantle |

> هذا يصحح اقتراحي السابق (سبع مراحل وست بوابات). الملف فيه تسعة أعمدة `Phase Gate`، وهي «أعمدة البوابات التسعة» التي تذكرها الوثيقة الأصلية.

### 3.2 البوابات التسع

كل بوابة في الملف عمود `… Readiness` يسبق المرحلة التي يفتحها، وكلها فارغة اليوم. الشروط أدناه مأخوذة من أعمدة المرحلة السابقة في Master.

| البوابة (اسمها في الملف) | تفتح | الشرط: يكتمل أو يكون «غير منطبق» | الصلاحية |
| --- | --- | --- | --- |
| G1 · Pre-CW Readiness | PRE-CW | RF Survey Date، Acquisition Date (عقد موقّع + تصاريح معتمدة)، Site Release Date | `gate.approve.G1` |
| G2 · CW Readiness | ACTUAL CW | CW SOW محدد · PR · PO/WO · مقاول مُسند · CW Access · تقرير المسح والتحليل معتمد بنتيجة Pass أو Reinforce · CW DN معتمد | `gate.approve.G2` |
| G3 · RFI Readiness | RFI | CW MOS · بنود Tower Erection وSite Adaption كلها Done أو N/A · تاريخ انتهاء التركيب الفعلي | `gate.approve.G3` |
| G4 · TE Installation Readiness | TE INSTALLATION | CW PAC (الملاحظات مُغلقة، As-Built مُسلّم، تاريخ PAC) **و** GECOL منجز أو N/A **و** HLC منجز أو N/A | `gate.approve.G4` |
| G5 · On-Air Readiness | ON-AIR | TE Access · TE Survey · TE DN · TE MOS · بنود التركيب · تاريخ انتهاء التركيب الفعلي | `gate.approve.G5` |
| G6 · TE PAC Readiness | TE PAC | Commissioning · Integration · Cutover بنتيجة Success (للاستبدال فقط) · On-Air Actual Date | `gate.approve.G6` |
| G7 · Cluster Optimization Readiness | CLUSTER OPT. | SSV بنتيجة Pass · EIR (PWR/WL/MW/IP) · PAT · As-Built · الملاحظات مُغلقة · TE PAC | `gate.approve.G7` |
| G8 · HOTO Readiness | LAUNCH & HOTO | Cluster Optimization Date · KPI Acceptance بنتيجة Pass | `gate.approve.G8` |
| G9 · Final Closure Readiness | FINAL CLOSURE | Launch Date · Material Reconciliation · HOTO Package | `gate.approve.G9` |

### 3.3 من يعتمد البوابة: صاحب الصلاحية

**القرار:** يعتمد البوابة من يملك صلاحية اعتمادها. لا يرتبط الاعتماد في النظام باسم دور ثابت.

- **لكل بوابة صلاحية مستقلة** (`gate.approve.G1` … `gate.approve.G9`). تُمنح من شاشة الإعدادات لدور أو لشخص، ولا تُكتب في الكود. تغيير من يعتمد بوابةً قرار إداري لا يحتاج برمجة.
- **الصلاحية تخضع للنطاق كبقية الصلاحيات** (الدور × النطاق × المرحلة). من يملك `gate.approve.G4` على منطقة طرابلس لا يعتمد G4 لموقع في سبها.
- **النيابة المؤقتة تشمل الاعتماد.** يمكن تفويض صلاحية بوابة بتاريخ انتهاء أثناء الإجازات، كما في الوثيقة الأصلية، فلا يتوقف الموقع لغياب شخص.
- **الصلاحية لا تتجاوز الشرط.** حتى صاحب الصلاحية لا يعتمد بوابة لم تكتمل شروطها. زر الاعتماد لا يظهر قبل أن يصبح الشرط محققاً.
- **إن لم يملك أحد الصلاحية** على نطاق موقع ما، يظهر ذلك في تقرير جودة البيانات بوصفه «بوابة بلا معتمِد»، قبل أن يعلق موقع فعلاً.
- **كل اعتماد يُسجَّل** باسم المعتمِد ووقته والصلاحية التي اعتمد بها (أصلية أو نيابة) في سجل التدقيق.
- **البوابات المعبورة بالتجاوز** («غير منطبق» بحكم النطاق) لا تحتاج معتمِداً، وتُسجَّل باسم النظام.

**توزيع ابتدائي** يُحمَّل مع قالب GSDN ويُعدَّل من الإعدادات:

| الصلاحية | تُمنح افتراضياً لـ |
| --- | --- |
| G1 | Team Lead (Design & Acquisition) |
| G2، G3 | Team Lead (CW) |
| G4 | Project Manager |
| G5، G6 | Team Lead (TE) |
| G7 | Project Manager |
| G8 | RF Engineer |
| G9 | Project Manager |
| الكل | Project Manager (احتياطي) |

ملاحظات:

- **G4 هي نقطة التقاء المسارات.** RFI تجمع CW PAC وGECOL وHLC، وهذا ما يفسّر الخطر الحالي: الموقع ينتظر الكهرباء أو الألياف بعد اكتمال الأعمال المدنية.
- **المرحلة 10 تُغلق بالزمن.** فترة DLP محسوبة من الإعدادات: 90 يوماً بعد CW PAC، و12 شهراً بعد TE PAC. لذلك يُحسب تاريخ FAC المتوقع آلياً ويولّد تنبيه «نهاية DLP».
- **البيانات الحالية تعبر البوابات دون اعتماد.** مثال: 282 موقعاً لها On-Air Actual Date، و205 فقط لها TE PAC Actual Date، وأعمدة البوابات فارغة كلها. عند الترحيل تُعتمد البوابات المجتازة فعلاً بأثر رجعي باسم «ترحيل»، ولا تُختلق تواريخ اعتماد.

### 3.4 دور منسق المنطقة

دور جديد يُضاف إلى قائمة `StaffRole` باسم **Region Coordinator / منسق منطقة**. وظيفته المتابعة على مستوى المنطقة، أما إدخال بيانات المراحل فيبقى عند فرق التخصص. السبب قاعدة «الحقل له مالك واحد»: لو أدخل المنسق وقائد فريق التخصص الحقل نفسه، عاد التضارب الذي يعالجه النظام.

| البند | منسق المنطقة |
| --- | --- |
| النطاق | منطقة أو أكثر، تُسند له فيرث كل مواقعها تلقائياً، بما فيها المواقع الجديدة عند اعتمادها |
| يُنشئ مواقع | **لا**. الإنشاء عند فريق التصميم (البند 2.1) |
| يرى | كل مراحل مواقع منطقته وكل حقولها، للقراءة |
| يُدخل | ما يُسند له صراحةً فقط: حقول **مشكلة الموقع** (Pending Issue وIssue Owner وIssue Status وRemark)، وهي اليوم بلا مالك واضح في Master |
| يعتمد | لا شيء افتراضياً. يمكن منحه صلاحية بوابة محصورة في منطقته (`gate.approve.Gx` على نطاق المنطقة) عبر البند 3.3 |
| يتلقى | تنبيهات مواقع منطقته كلها: تجاوز الخط المرجعي، تقادم المرحلة، بوابة بلا معتمِد، تصريح أو إيجار ينتهي، ملاحظة جودة مفتوحة |
| لوحته | تقادم مواقع منطقته، المواقع العالقة عند كل بوابة وسبب التعليق، الحقول الناقصة ومالكها |

بهذا يصبح المنسق «عين المنطقة»: يعرف الموقع العالق ومن المسؤول عنه لحظة حدوث التعليق، دون أن يملك بيانات غيره.

## 4. «غير منطبق» يحدده نطاق العمل

### 4.1 القاعدة

الملف يجيب عن هذا بوضوح: المرحلة أو البند لا يكون «غير منطبق» بقرار لحظي من الموظف، بل **يُستنتج من نطاق عمل الموقع** المحدد عند الإنشاء. الموظف لا يكتب `N/A` في أي حقل مرحلة.

| حقل النطاق | قيمته | ما يصبح «غير منطبق» تلقائياً |
| --- | --- | --- |
| Tower Erection | N/A | بنود Tower Foundation وSteel Erection وLightning & Grounding |
| Site Adaption | N/A | بنود Cabinet Foundation وMounting Pole وCable Tray وIndoor Rack وOptical Fiber وAC/DC Box وSite GND |
| Tower Erection **و** Site Adaption | كلاهما N/A | المرحلتان 2 و3 كاملتين (PRE-CW وACTUAL CW) و CW PAC وCW DLP/FAC |
| GECOL Power | N/A | مسار GECOL في RFI |
| HLC Fiber | N/A | مسار HLC في RFI |
| TE SOW | IP Router Only | بنود MTS Cabinet وRF Antenna وMW Antenna، وEIR/PAT لـ WL وMW |
| Delivery Scenario | New Build أو Expansion | Cutover كاملاً، والمسار الجانبي DISMANTLE |
| Delivery Scenario | Hot Swap أو Cold Swap | لا شيء، فيدخل Cutover وDismantle |
| CW Delivery Model | In-House | PR وPO/WO للأعمال المدنية |

مثال من الملف: الموقع `BG001` نطاقه IP Router Only وIn-House، وكل بنود CW فيه `N/A`. في النظام لا يمر بالمرحلتين 2 و3 إطلاقاً، ويعبر G2 وG3 تلقائياً بحالة «غير منطبق».

### 4.2 النتائج

- البوابة تعامل «غير منطبق» معاملة «منجز».
- المراحل غير المنطبقة لا يُجمَّد لها خط مرجعي، ولا تدخل حسابات التأخير أو التقادم.
- في قمع الإنجاز تُعرض منفصلة («عبر بالتجاوز») حتى لا تُضخّم النسب.

### 4.3 تغيير النطاق

تغيير أي حقل نطاق بعد الاعتماد يمر **بطلب تغيير** من نوع `Scope Change` بدرجة `Site` أو `Part` أو `Field`، يعتمده مدير المشروع. عند الاعتماد:

- البند الذي **أصبح منطبقاً**: إن كان الموقع لم يتجاوز بوابته بعد، يُضاف للمرحلة بخط مرجعي من تاريخ الاعتماد. وإن كان قد تجاوزها، يُفتح بنداً معلقاً تشترطه أول بوابة لم تُعتمد بعد، ولا يعود الموقع إلى الخلف.
- البند الذي **أصبح غير منطبق**: يُغلق بحالة «غير منطبق»، وتبقى بياناته السابقة في سجل التدقيق.

## 5. انعكاس ذلك على نموذج البيانات

```sql
-- عدد المواقع المتعاقد عليه لكل مرحلة مشروع (tblProjectScope)
CREATE TABLE project_scope (
  project_id     bigint NOT NULL REFERENCES project(id),
  project_phase  text   NOT NULL,             -- PH1 / PH2
  contract_sites integer NOT NULL CHECK (contract_sites >= 0),
  reference      text,
  approved_date  date,
  PRIMARY KEY (project_id, project_phase)
);

-- بادئة الرمز جزء من تعريف المنطقة
ALTER TABLE region ADD COLUMN site_code_prefix text UNIQUE
  CHECK (site_code_prefix ~ '^[A-Z]{2}$');      -- TR, MI, SB, GM, WM, BG, ZW

-- الموقع: الهوية + النطاق، بلا أي بيانات مراحل
CREATE TABLE site (
  id               bigserial PRIMARY KEY,
  project_id       bigint  NOT NULL REFERENCES project(id),
  region_id        bigint  NOT NULL REFERENCES region(id),
  serial_no        integer NOT NULL CHECK (serial_no BETWEEN 1 AND 999),
  suffix           char(1) CHECK (suffix ~ '^[A-Z]$'),
  code             text    NOT NULL,          -- يُولّد: prefix || lpad(serial) || coalesce(' ' || suffix, '')
  replaces_site_id bigint  REFERENCES site(id),   -- إلزامي إذا وُجدت لاحقة
  owner_site_id    text,                      -- Site Owner ID
  name_ar          text    NOT NULL,
  sub_region_id    bigint  NOT NULL REFERENCES sub_region(id),
  latitude         numeric(10,7) NOT NULL CHECK (latitude  BETWEEN 19.5 AND 33.5),
  longitude        numeric(10,7) NOT NULL CHECK (longitude BETWEEN  9.3 AND 25.2),
  site_type_id     bigint  NOT NULL REFERENCES site_type(id),
  site_scenario_id bigint  NOT NULL REFERENCES site_scenario(id),
  uplink_site_id   bigint  REFERENCES site(id),
  tower_owner_id   bigint  NOT NULL REFERENCES tower_owner(id),
  existing_or_new  text    NOT NULL CHECK (existing_or_new IN ('existing','new','na')),
  rt_or_gf         text    NOT NULL CHECK (rt_or_gf IN ('rt','gf','na')),
  tower_type_id    bigint  NOT NULL REFERENCES tower_type(id),
  tower_height_m   numeric(5,1) CHECK (tower_height_m > 0),
  -- نطاق العمل: يحدد ما هو «غير منطبق»
  project_phase    text    NOT NULL,
  delivery_batch   text,
  delivery_scenario text   NOT NULL CHECK (delivery_scenario IN
                     ('new_build','expansion','hot_swap','cold_swap','relocation')),
  sow_tower_erection boolean NOT NULL,
  sow_site_adaption  boolean NOT NULL,
  sow_gecol_power    boolean NOT NULL,
  sow_hlc_fiber      boolean NOT NULL,
  sow_te             text    NOT NULL CHECK (sow_te IN ('full_scope','ip_router_only')),
  cw_delivery_model  text    NOT NULL CHECK (cw_delivery_model IN ('in_house','outsourced')),
  -- الحالة والاعتماد
  status           text NOT NULL DEFAULT 'draft' CHECK (status IN
                     ('draft','pending_review','pending_approval','approved','rejected','cancelled')),
  justification    text NOT NULL,
  created_by       bigint NOT NULL REFERENCES app_user(id),
  reviewed_by      bigint REFERENCES app_user(id),
  approved_by      bigint REFERENCES app_user(id),
  approved_at      timestamptz,
  UNIQUE (project_id, code),
  UNIQUE (project_id, region_id, serial_no, suffix),
  CHECK ((suffix IS NULL) = (replaces_site_id IS NULL)),
  FOREIGN KEY (project_id, project_phase) REFERENCES project_scope(project_id, project_phase)
);
-- تطابق الإحداثيات يُرفض إلا للموقع البديل
CREATE UNIQUE INDEX site_coords_uq ON site (project_id, latitude, longitude)
  WHERE replaces_site_id IS NULL AND status <> 'cancelled';

-- حالة كل مرحلة / بند لكل موقع
CREATE TABLE site_stage (
  site_id          bigint NOT NULL REFERENCES site(id),
  stage_id         bigint NOT NULL REFERENCES stage_definition(id),   -- العشر + DISMANTLE، من قالب المشروع
  track            text   NOT NULL DEFAULT 'main',                    -- 'gecol' / 'hlc' في RFI، 'cw' / 'te' في DISMANTLE
  status           text   NOT NULL DEFAULT 'required' CHECK (status IN
                     ('required','in_progress','done','not_applicable','cancelled')),
  na_source        text   CHECK (na_source IN ('scope','scope_change')), -- «غير منطبق» يأتي من النطاق فقط
  baseline_date    date,
  actual_date      date,
  gate_approved_by bigint REFERENCES app_user(id),
  gate_approved_at timestamptz,
  gate_approval_kind text CHECK (gate_approval_kind IN ('normal','auto_na','migration')),
  PRIMARY KEY (site_id, stage_id, track),
  CHECK (status <> 'done'           OR actual_date IS NOT NULL),
  CHECK ((status = 'not_applicable') = (na_source IS NOT NULL)),
  CHECK (status <> 'not_applicable' OR baseline_date IS NULL)
);

-- صلاحية اعتماد البوابة: تُمنح لدور أو لشخص، على نطاق، وقد تكون نيابة مؤقتة
CREATE TABLE permission_grant (
  id            bigserial PRIMARY KEY,
  project_id    bigint NOT NULL REFERENCES project(id),
  permission    text   NOT NULL,                 -- 'gate.approve.G1' … 'gate.approve.G9'
  role_id       bigint REFERENCES role(id),
  user_id       bigint REFERENCES app_user(id),
  region_id     bigint REFERENCES region(id),    -- NULL = المشروع كاملاً
  site_id       bigint REFERENCES site(id),      -- إسناد بموقع بعينه
  delegated_from bigint REFERENCES app_user(id), -- نيابة مؤقتة
  valid_from    date   NOT NULL DEFAULT current_date,
  valid_to      date,                            -- إلزامي للنيابة
  CHECK ((role_id IS NULL) <> (user_id IS NULL)),
  CHECK (delegated_from IS NULL OR (user_id IS NOT NULL AND valid_to IS NOT NULL))
);

ALTER TABLE site_stage
  ADD COLUMN gate_grant_id bigint REFERENCES permission_grant(id),  -- الصلاحية التي اعتُمد بها
  ADD CONSTRAINT gate_grant_required
    CHECK (gate_approval_kind IS DISTINCT FROM 'normal' OR gate_grant_id IS NOT NULL);
```

ملاحظات التنفيذ:

- **قواعد الانطباق** (الجدول 4.1) تُخزَّن كجدول `stage_applicability_rule` مرتبط بقالب المشروع، لا كشروط مكتوبة في الكود. مشروع رولآوت آخر يعرّف قواعده دون برمجة.
- **عند اعتماد الموقع** يُنشئ النظام صفوف `site_stage` كلها دفعة واحدة، ويضع «غير منطبق» حيث يقتضي النطاق.
- **فحص القرب (50 متراً)** في التطبيق، أو بامتداد PostGIS إن اعتُمد.
- **حدود الإحداثيات** تقريبية لحدود ليبيا الكاملة. حدود كل منطقة على حدة تُضاف لاحقاً إن توفرت.

## 6. ما زال مطلوباً

- [ ] **معنى اللاحقة `A`** في الـ 35 موقعاً: نقل (`Relocation`)؟ بديل مرشح؟ توسعة؟ التصميم أعلاه يفترض «موقع بديل مرتبط بموقع أصلي».
- [x] **من يعتمد كل بوابة**: من يملك صلاحية اعتمادها، وتُدار من الإعدادات (البند 3.3).
- [ ] **التوزيع الابتدائي للصلاحيات** في البند 3.3: هل يُعتمد كما هو؟
- [x] **دور منسق المنطقة**: يُستحدث للمتابعة، والإنشاء يبقى عند فريق التصميم (البند 3.4).
- [ ] **صلاحيات المنسق**: هل يُمنح افتراضياً صلاحية اعتماد بوابة على منطقته (G4 مثلاً)؟ أم يبقى للمتابعة فقط؟
- [ ] **عدد المنسقين**: منسق لكل منطقة من السبع، أم منسق لعدة مناطق؟
- [ ] **حسم المواقع الستة الشاردة** قبل الترحيل: `BG011` و`BG058` و`BG077` و`BG078` و`TR103` و`New Site` (`SRM008`، الزاوية).
- [ ] **قائمة `Project Staff` فارغة** في Setting، ويلزم ملؤها بالأسماء والأدوار قبل إسناد أي مرحلة.
