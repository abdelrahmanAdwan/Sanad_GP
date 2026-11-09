---
paths:
  - "data/**"
  - "experiments/**"
  - "src/models/**"
  - "src/agreement/**"
---

# Data and test-set rules

- Never write audio, video or model weights into the repository.
- Each topic's test split is frozen when the topic is complete. Never change `split` values of a frozen topic, never tune thresholds or hyperparameters on test data, and do not print test metrics during development runs.
- Splits are grouped by video and by channel: all segments of one video, and all videos of one channel, go to the same split.
- `segment_id` values never change after annotation starts.
- Each annotator writes only in `data/annotations/<name>/`. Do not edit another annotator's files, even to fix an obvious error: open an issue instead.
- Records must validate against `data/schema/*.schema.json`.
