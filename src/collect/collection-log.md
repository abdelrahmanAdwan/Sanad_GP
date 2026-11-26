# Collection log

One entry per day of API use (docs/collection-protocol.md section 6): what was run, quota used, errors.

## 2026-11-26 · Abdulrahman Adwan (run by Claude)

Purpose: pick 6 non-diabetes pilot videos (Drive file 13, task 1).

- First attempt: web search on youtube.com plus YouTube oEmbed (title, channel). Dropped, because oEmbed gives no duration or date, and 3 of those 6 picks failed the rules once checked.
- `search.list` (key from the environment), all with `type=video`, `relevanceLanguage=ar`, `publishedAfter=2020-01-01`, `order=relevance`, `maxResults=25`:

| Query | videoDuration | Hits | Picked (rank) |
| --- | --- | --- | --- |
| خلطة طبيعية | short | 25 | Lpl_8P_bcuE (17) |
| خلطة طبيعية | medium | 25 | -l4KKQEaoHE (2) |
| علاج السرطان بالأعشاب | short | 25 | 5xbnkPueKiU (4) |
| علاج السرطان بالأعشاب | medium | 25 | none (reserves only) |
| رجيم سريع | short | 25 | lw0hr1PM7aw (1) |
| رجيم سريع | medium | 25 | bdfLAhrP8mk (1) |
| الكشف المبكر عن سرطان الثدي وزارة الصحة | short | 25 | MR1U8hidTJ0 (1) |

- `videos.list` for about 60 IDs (durations, dates, channel IDs), including the 14 diabetes pilot videos.
- Calls: 7 `search.list` + 11 `videos.list`. No errors.
- Rule used to pick: first result in rank order that is a Short of 15–60 s, or a 2–15 minute video; published 2020 or later; about health (title); from a channel not already in the pilot. One change for the pilot design: the cancer clip comes from a separate search for an official body (file 13 asks for one "if found"); its first result was eligible. The 15-second minimum is an assumption (shorter videos give at most one 15-second segment).
- Skipped results, with reasons, are visible by rerunning the queries; the picks and reserves are in Drive file 14.
