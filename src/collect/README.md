# src/collect · Data & access track

Finds and screens candidate videos for one topic at a time (D008).

**Status:** pilot in progress (14 of 20 videos downloaded, PR #2). Protocol draft: `docs/collection-protocol.md` (D017).

- **Input:** topic name, search terms (MSA and dialects) in `src/collect/queries/<topic>.yaml`.
- **Output:** `data/videos/<topic>.jsonl`, one record per screened video, valid against `data/schema/video.schema.json`.
- **Steps:** YouTube Data API search → de-duplicate → rank by views → manual screening (about 30 s per video) → metadata (topic, publisher type, dialect).
- **Notes:** the API key lives in `.env` (never committed). The API's 30-day storage rule for API data applies to titles and statistics fetched through it (YouTube API Developer Policies III.E.4).

## Sheet to JSONL

`sheet_to_jsonl.py` turns a video sheet (Drive file 12 format, exported as CSV) into `data/videos/<name>.jsonl`. It maps the Arabic drop-down values to the schema enums, validates every record, and prints warnings for the selection rule (`--rules pilot` for the 20-video pilot, `--rules topic` for one topic of about 80). Sheet columns the schema lacks go to `--extras-out` (open question D019).

```
python src/collect/sheet_to_jsonl.py sheet12.csv --collected-at 2026-11-26 --rules pilot \
    --out data/videos/pilot.jsonl --extras-out data/reports/pilot_sheet_extras.csv
```

Tested on 26 Nov on the 14 filled rows of file 12: 14 converted, 0 errors.
