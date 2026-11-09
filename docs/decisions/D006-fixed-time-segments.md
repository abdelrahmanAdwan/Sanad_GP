---
id: D006
title: Labels attach to fixed time segments
status: accepted
date: 2026-11-09
decided_by: Supervisor meeting (reported by Abdulrahman)
owner: Transcripts track
changes_proposal: false
follow_up:
  - Choose the segmentation method on pilot videos and freeze it before main annotation
---
## Decision
Each video is cut once into fixed time segments (start, end). Labels belong to segments. Corrected transcripts are edited **inside** the same segment boundaries, so one label applies to both the automatic and the corrected text.

## Consequences
- RQ2 becomes a clean paired comparison (same segments, same labels, two texts) with no label transfer.
- The segment is the annotation unit; see `data/schema/segment.schema.json`.
- Whether annotators watch the video while labeling is still open: D011.
