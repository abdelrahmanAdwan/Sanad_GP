---
person: abdulrahman
track: "Coordination + help with collection (proposed in Drive file 09; D014 still open)"
updated: 2026-11-26
task: "Drive file 13: my data-collection tasks 1-6"
branch: ccr-35fdb68e-fbb5ju
last_commit: see git log
main_seen: 95b41d6
---

## Done this session
- Read Drive files 13 (my tasks), 12, 11, 09 and 07. Abdullah filled and downloaded rows 1–14 (PR #2).
- Task 1 done by Claude at my request, for me to verify: 6 videos picked with the YouTube Data API (key in the environment; calls logged in `src/collect/collection-log.md`). Paste-ready rows for file 12 rows 15–20, with 12 reserves, in Drive file 14 (id 1BufV7j4JOP8hrIyIAIfANvJScvOzS79FvxUvqNtgDiQ). Copy: `sessions/abdulrahman/pilot6_candidates.csv`. Duration, date and channel come from the API. Publisher type is from channel names. Dialect is from descriptions or a weak guess. Excerpts: chapters for -l4KKQEaoHE, whole video for MR1U8hidTJ0, default 60–210 s for bdfLAhrP8mk. Nobody has listened yet.
- The first round of picks (web search + oEmbed) was replaced: 3 of those 6 broke the duration or date rule once the API showed real values.
- With the 6 rows, the 20-video pilot passes the converter's design check (10 Shorts / 10 clips; 14 + 2 + 2 + 2; 1 official, 2 non-specialist).
- Task 2: converter `src/collect/sheet_to_jsonl.py` (+ `--channel-ids`), `data/reports/pilot_channel_ids.csv` (20 videos, 20 channels). Messages for the team and for Abdullah in `docs/updates/2026-11-26-pilot-schedule.md`. Scheduled task trig_01TNnGhGWi91f5TqWTfXpwaJ runs a daily check at 07:13 UTC until 3 Dec and builds `data/videos/pilot.jsonl` once file 12 is complete.
- Task 5 prep: draft `src/collect/queries/diabetes.yaml` to review with Abdullah; `--rules topic` check; screening templates in `data/templates/`.
- D019 (open): schema lacks caption fields, an accepted/rejected flag and (now partly solved by `--channel-ids`) a stable channel key.

## Next step
Listen to the 6 primary videos in Drive file 14 for 30 s each (Arabic and audible? dialect right? excerpt on topic?). Fix any value, paste columns A–O into file 12 columns C–Q, rows 15–20. Send Abdullah the message in docs/updates/2026-11-26-pilot-schedule.md.

## Blocked on
- Claude cannot hear audio or open YouTube pages from the cloud container: audibility, dialect and excerpt choice need a person.
- No GitHub issue exists for my tasks (only #1, Abdullah's), so there is nowhere to post the handoff comment.
- Tasks 3, 4 and 6 wait on others (audio clips from Mohammad on 28 Nov; segments and annotation files from Shaath) and are human work by design.

## Files touched
- src/collect/sheet_to_jsonl.py, src/collect/README.md, src/collect/collection-log.md, src/collect/queries/diabetes.yaml
- data/reports/pilot_channel_ids.csv; data/templates/topic_screen_{accepted,rejected}.csv, README.md
- docs/decisions/D019-video-record-gaps.md, docs/updates/2026-11-26-pilot-schedule.md, docs/ai-use-log.md
- sessions/abdulrahman/ (this file, log/2026-11-10.md, pilot6_candidates.csv)

## Notes for next session
- When file 12 is complete: export CSV and run `python src/collect/sheet_to_jsonl.py <csv> --collected-at 2026-11-26 --rules pilot --channel-ids data/reports/pilot_channel_ids.csv --out data/videos/pilot.jsonl --extras-out data/reports/pilot_sheet_extras.csv`, then `python scripts/validate_data.py`.
- The channel name changes: `_vTsmMjUyXg` is "ta3leem360" in sheet 12 but "Amr Samida" in the API today (evidence for D019 gap 3).
- File 07's video (T6qEGgUKS4M) is not among the 20; row 5 is the same channel, different video.
- YouTube API Developer Policies may limit how long API data (titles, counts) can be stored; only IDs are committed. Check the policy before the datasheet (unverified).
- Earlier notes still open: re-verify Almogbel 2021 and Baqain 2023; first deadline (D001); written confirmation of D003 and D005.
