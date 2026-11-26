---
id: D019
title: Gaps between the video sheet and video.schema.json (captions, rejected videos, channel)
status: open
date: 2026-11-26
decided_by: ""
owner: Data & access
changes_proposal: false
follow_up:
  - "Choose an option for each of the three gaps before data/videos/diabetes.jsonl is written (8 Dec)"
  - "Any schema change goes in one pull request reviewed by every track owner (CLAUDE.md)"
---
## Context
Converting Drive file 12 (pilot sheet) with `src/collect/sheet_to_jsonl.py` on 26 Nov showed three things the sheet records that `data/schema/video.schema.json` cannot hold. The schema has `additionalProperties: false`, so the converter cannot add them without a schema change. Nothing is decided here.

## Gap 1: caption availability
The sheet records "audio downloaded", "YouTube automatic Arabic captions" and "captions uploaded by the channel". These numbers feed D010 (9 of the 14 downloaded pilot videos have automatic Arabic captions, from `data/reports/pilot_check.csv`).
- **A.** Add optional booleans to the schema: `has_ar_auto_captions`, `has_ar_manual_captions`. One place for everything; needs a schema pull request.
- **B.** Keep them in a side file, `data/reports/<name>_sheet_extras.csv` (what the converter does now with `--extras-out`). No schema change; two files to keep in sync.

## Gap 2: rejected videos
`docs/collection-protocol.md` §6 says rejected videos also go into `data/videos/<topic>.jsonl` with `screened: true` and a `screen_note`. But no field says accepted or rejected, so every reader must parse free text, and the schema still requires `format`, `publisher_type` and `dialect`, which a screener may not fill for a rejected video.
- **A.** Add `accepted` (boolean) and `reject_reason` (enum, same list as `data/templates/topic_screen_rejected.csv`) to the schema.
- **B.** Rejected videos stay in their own CSV (`data/reports/<topic>_rejected.csv`); `data/videos/` holds accepted videos only. Simpler; changes protocol §6 (proposed, D017).
- **C.** Keep protocol §6 and agree that `screen_note` starts with `rejected:` (what the converter writes today for "speech not clear Arabic"). No schema change; fragile.

## Gap 3: channel
Splits are grouped by channel (ARCHITECTURE §2), so every video needs a stable channel key. The schema has `channel_id`, but the sheet has only the channel name, and names change (in the pilot, sheet "Dr SMART team [ARABIC]" vs info.json "Dr SMART Arabic").
- **A.** Fill `channel_id` from each video's `.info.json` on the server (the download check script can print it).
- **B.** Store the channel name instead. Easier, but unstable.

## Suggestion (not a decision)
Gap 1: B now, A if the paper's datasheet needs caption numbers per video. Gap 2: A. Gap 3: A. Reason: one schema pull request before the diabetes collection fixes all three, and segment IDs are not affected.
