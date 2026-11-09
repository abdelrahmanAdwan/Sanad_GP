# src/collect · Data & access track

Finds and screens candidate videos for one topic at a time (D008).

**Status:** not started.

- **Input:** topic name, search terms (MSA and dialects) in `src/collect/queries/<topic>.yaml`.
- **Output:** `data/videos/<topic>.jsonl`, one record per screened video, valid against `data/schema/video.schema.json`.
- **Steps:** YouTube Data API search → de-duplicate → rank by views → manual screening (about 30 s per video) → metadata (topic, publisher type, dialect).
- **Notes:** the API key lives in `.env` (never committed). The API's 30-day storage rule for API data applies to titles and statistics fetched through it (YouTube API Developer Policies III.E.4).
