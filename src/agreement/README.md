# src/agreement · Guidelines & quality track

Merges annotations, measures agreement, records adjudication, and makes the splits.

**Status:** not started.

- **Input:** `data/annotations/<name>/*.jsonl`, valid against `data/schema/annotation.schema.json`.
- **Output:** merged labels, agreement report (Krippendorff's α per label as the primary figure; pairwise Cohen's κ and Jaccard set agreement for comparison with ViClaim), adjudication log (D007), per-topic splits grouped by video and channel.
