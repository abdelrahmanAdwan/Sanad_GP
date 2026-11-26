# Annotation templates

`pilot_annotation.csv` is one sheet per annotator for the pilot (if the team picks a spreadsheet, D013). Columns match `data/schema/annotation.schema.json`; booleans are 1/0; `flags` is a `;`-separated list. Each annotator works in their own copy and exports to `data/annotations/<name>/`. The example row is illustrative; delete it before use.

Also record, per video, the minutes spent (needed to re-plan the dataset size after the pilot).

## Screening sheets for one topic (phase 2, about 80 videos)

Two sheets, one row per screened candidate (Drive file 13, task 5; rule in `docs/collection-protocol.md` §3, D017 proposed). Make them as Google Sheets with drop-downs, export as CSV, then run `src/collect/sheet_to_jsonl.py <accepted.csv> --rules topic`.

- `topic_screen_accepted.csv`: same columns as Drive file 12, plus `مين فحصه` (screener) and `شريحة المشاهدات` (view band: `أعلى 50` for the 50 most-viewed candidates of the topic, `الباقي` for the rest). The band is needed to check "a third from the most viewed".
- `topic_screen_rejected.csv`: every rejected candidate with its reason. Suggested drop-down for `سبب الرفض`: `مش عربي أو مش مسموع` · `مش عن الموضوع` · `موسيقى أو نص على الشاشة بس` · `مكرر أو إعادة رفع` · `أطول من 15 دقيقة بدون جزء واضح` · `قبل 2020` · `القناة وصلت 3 فيديوهات` · `غير ذلك (اكتب بالملاحظات)`. The counts go into the datasheet ("how many were excluded and why").

Drop-down values the converter understands: topic `السكري` / `الأعشاب والطب البديل` / `السرطان` / `التغذية والحميات` / `ضغط الدم`; format `Short` / `مقطع من فيديو أطول`; publisher `طبيب (حسب ما يقدّم نفسه)` / `جهة رسمية` / `غير مختص` / `غير معروف`; dialect `فصحى` / `شامي` / `مصري` / `خليجي` / `عراقي` / `مغاربي` / `سوداني` / `مختلطة` / `أخرى` / `غير معروف`. How rejected rows enter `data/videos/` is open (D019).
