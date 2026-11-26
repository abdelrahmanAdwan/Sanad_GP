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
- Read Drive file 13 (my tasks), 12 (pilot sheet), 11, 09 and 07. Abdullah filled and downloaded rows 1–14 (PR #2); rows 15–20 are mine and empty.
- Task 1: YouTube blocks this container (bot check), so candidates came from a web search on youtube.com plus YouTube oEmbed (title and channel verified). Drive file 14 (id 1GnK82lzG4FVDUHo6C8t70HczmKCMp934z-6qowdBjpk) lists 6 primary picks + 10 reserves, in sheet-12 column order. Copy: `sessions/abdulrahman/pilot6_candidates.csv`. Rule used: first result in search order with the right format, from a channel not already in the pilot, adding publisher or dialect variety. Never by whether the content looks right or wrong.
- Task 2: `src/collect/sheet_to_jsonl.py` converts sheet 12 to `data/videos/pilot.jsonl` and checks the pilot design. Ran on the 14 rows: 0 errors. Message and daily checklist in `docs/updates/2026-11-26-pilot-schedule.md`.
- Task 5 prep: `--rules topic` checks the 80-video rule; templates `data/templates/topic_screen_{accepted,rejected}.csv`.
- New open record D019: the schema lacks caption fields, an accepted/rejected field and a reliable channel key.

## Next step
Open the 6 primary videos in Drive file 14 (about 5 min each). Check duration, date (2020 or later) and that the speech is Arabic and audible. Fill publisher type and dialect by listening; for long videos pick a 2–3 minute part and note start and end seconds. Copy the rows to file 12 rows 15–20 and tell Abdullah.

## Blocked on
- Claude cannot open YouTube from the cloud container, so duration, date, dialect and publisher type need a person.
- No GitHub issue exists for my tasks (only #1, Abdullah's), so there is nowhere to post the handoff comment.
- Send the schedule message (docs/updates/2026-11-26-pilot-schedule.md) to the team myself; Claude has no team chat.

## Files touched
- src/collect/sheet_to_jsonl.py, src/collect/README.md
- data/templates/topic_screen_accepted.csv, topic_screen_rejected.csv, README.md
- docs/decisions/D019-video-record-gaps.md, docs/updates/2026-11-26-pilot-schedule.md, docs/ai-use-log.md
- sessions/abdulrahman/ (this file, log/2026-11-10.md, pilot6_candidates.csv)

## Notes for next session
- When file 12 is complete: export CSV, run `python src/collect/sheet_to_jsonl.py <csv> --collected-at <date> --rules pilot --out data/videos/pilot.jsonl --extras-out data/reports/pilot_sheet_extras.csv`, then `python scripts/validate_data.py`.
- Hints for Abdullah (unverified, a person decides): row 4 channel "طبيبك اليوم" and the titles of rows 7 and 14 name a doctor, but publisher is "unknown"; row 7 has no search query.
- File 07's video (T6qEGgUKS4M) is not among rows 1–14. Same channel as row 5, different video.
- Tasks 3, 4 and 6 are human-only by project rule: write reference transcripts from scratch and annotate alone, without Claude.
- Earlier notes still open: re-verify Almogbel 2021 and Baqain 2023; first deadline (D001); written confirmation of D003 and D005.
