# src/transcribe · Transcripts track

Turns screened videos into fixed time segments with text.

**Status:** not started.

- **Input:** `data/videos/<topic>.jsonl`.
- **Output:** `data/segments/<topic>.jsonl`, valid against `data/schema/segment.schema.json`. Audio stays on the team server under `data/audio/` (gitignored).
- **Steps:** download audio (D003) → one fixed Whisper version (D010, proposed) → YouTube auto-captions as a second output where available → segmentation, frozen before annotation (D006) → manual correction of test-set text inside segment boundaries → WER per dialect.
