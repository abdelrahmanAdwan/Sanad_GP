# Annotation templates

`pilot_annotation.csv` is one sheet per annotator for the pilot (if the team picks a spreadsheet, D013). Columns match `data/schema/annotation.schema.json`; booleans are 1/0; `flags` is a `;`-separated list. Each annotator works in their own copy and exports to `data/annotations/<name>/`. The example row is illustrative; delete it before use.

Also record, per video, the minutes spent (needed to re-plan the dataset size after the pilot).
