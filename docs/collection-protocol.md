# Video collection protocol (draft for team review)

Status: **proposed**, 2026-11-10. Owner: Data & access track. Nothing here is decided; the choices that change the proposal are listed in D017.

What the proposal fixes (verified against the proposal via Drive file 01): the domain (health), the five topics, YouTube as the only source, two video formats (Shorts and 2–3 minute clips of longer videos; `data/schema/video.schema.json`), a target of about 400 videos and 6,000 sentences, and that collection follows YouTube's terms. The supervisor allowed downloading audio and captions by any method (D003) and topics one at a time with fewer videos (D008).

## 1. The five topics and what is known about each

The proposal fixes the topics. The question for the team is the **order** (D012). Two criteria were suggested on 9 Nov: how much Arabic content exists, and how common misinformation is. Below is what published studies say. I could only verify the studies I could open today; "none found" means my search found nothing, not that nothing exists.

| Topic (schema value) | Published evidence on Arabic YouTube content | What it suggests for us |
| --- | --- | --- |
| Diabetes (`diabetes`) | Gharbi et al. 2023 (ECE abstract, 50 most-viewed "diabetes treatment" videos, 17 Jan 2023): false information in 63%, 77% of publishers presented as doctors, 63% encouraged stopping medication; false information by sub-topic: alternative medicine 100%, dietetics 76%, treatment 72%. Dabbus et al. 2025 (53 Arabic carbohydrate-counting videos out of 108 screened, YouTube Data Tools): 85% educational, quality moderate to high, only 47.2% presented by dietitians. Almogbel et al. 2021 was confirmed in the audit on 2 Nov; I could not reopen it today. | Claim-rich, much of it checkable; both misleading and sound videos exist, so the label mix should be balanced. Strong candidate for topic 1. |
| Cancer (`cancer`) | Ayoub et al. 2021 (*Supportive Care in Cancer*, 60 most-viewed "breast cancer" videos): misleading information in 42%; 64% of blog/individual videos misleading vs 15% of institutional ones. Baqain et al. 2023 (prostate cancer, Arabic; cited in the proposal, page blocked today). Abu Daabes & Kharbat 2019 (*Int. J. Health Governance*, 120 "cancer treatment" videos found with the YouTube API v3 and Google Trends terms): 56% promoted herbal or natural products, 86% gave no risk information. | Plenty of content and a clear publisher-type effect. Overlaps heavily with herbal medicine (see next row). |
| Herbal and alternative medicine (`herbal_alternative`) | Kharbat & Abu Daabes 2023 (*Health Informatics Journal*, 110 Arabic videos on herbal cancer treatment, YouTube API v3 + Google Trends): about 95% uploaded by non-experts, more than 40 herbs, DISCERN 27/80, PEMAT 31/100. | Very claim-dense, mostly check-worthy and mostly implicit ("this herb cures…"). Risk: if collected after cancer, many videos will already have been taken by the cancer topic. Needs a rule for overlap (section 4). |
| Nutrition and diets (`nutrition_diets`) | No Arabic-specific YouTube study found except the diabetes-diet one above. Gharbi's "dietetics 76% false" sub-topic is the closest figure. | Likely the largest and most dialectal content (cooking, weight loss, intermittent fasting). Many segments will be advice and opinion rather than facts, which makes it good for testing the OPN/none boundary but slower to annotate. |
| Hypertension (`hypertension`) | No Arabic-specific YouTube study found. (The 2025 *Journal of Human Hypertension* study is not Arabic-specific; the 2026 *Frontiers* study is on Chinese platforms.) | Least documented. We would be measuring, not confirming. Reasonable as a later topic, or as the "unseen topic" held out for RQ2. |

**Suggestion (not a decision):** diabetes → herbal/alternative → cancer → nutrition/diets → hypertension. Reasons: diabetes has the strongest documented misinformation and overlaps the least with other topics; herbal before cancer so that the overlap rule assigns herbal-cancer videos to herbal (the denser label source); hypertension last because the leave-one-topic-out experiment (RQ2) wants a held-out topic that differs from the others, and hypertension content (measurement, medication, salt) differs most from the diet-and-cure cluster.

**Alternative order:** diabetes → hypertension → nutrition → herbal → cancer, if the team prefers two "clinical" topics first so that the guidelines are stable before the opinion-heavy topics. Trade-off: hypertension early means collecting with no published baseline to compare against.

## 2. Finding candidate videos (YouTube Data API v3)

Verified on 10 Nov 2026 from developers.google.com:

- `search.list`: `q` (supports `|` for OR and `-` for NOT), `type=video`, `relevanceLanguage=ar`, `regionCode` (ISO 3166-1, default US), `videoDuration` (`short` < 4 min, `medium` 4–20 min, `long` > 20 min), `videoCaption` (`closedCaption` / `none` / `any`), `publishedAfter`, `order` (`relevance` default, `date`, `rating`, `title`, `viewCount`), `maxResults` ≤ 50. Cost: 1 unit, but **search.list is limited to 100 calls per day** per project (quota page, read today). So at most 100 × 50 = 5,000 candidate hits per project per day.
- `videos.list`: 1 unit per call, comma-separated IDs; gives `contentDetails.duration` (ISO 8601), `contentDetails.caption` (captions available or not), `snippet.defaultAudioLanguage`, `statistics.viewCount`, `snippet.liveBroadcastContent`, `status.madeForKids`, `topicDetails.topicCategories` (Wikipedia URLs).
- `captions.download` requires permission to edit the video (200 units), so captions and audio come from yt-dlp instead (D003).
- Default daily quota 10,000 units; the 100-search limit is the real constraint. Two or three Cloud projects (one per Data-track member) multiply it, but one project is enough for one topic per week.

Precedent: Abu Daabes & Kharbat (2019, 2023) used exactly this route (Python + YouTube API v3) and took their Arabic search terms from Google Trends. We can do the same, and we should also add dialect terms that Trends under-reports.

### Query design per topic

`src/collect/queries/<topic>.yaml` holds, for each topic:

- **MSA terms**, for example diabetes: `السكري`, `مرض السكري`, `علاج السكري`, `داء السكري`, `السكري النوع الثاني`, `الأنسولين`.
- **Dialect and colloquial terms**, for example `السكر` (Egyptian/Levantine use "sugar" for diabetes), `مريض سكر`, `علاج السكر بالأعشاب`, `وصفة للسكر`, `السكري نهائيا`.
- **Claim-prone phrasings** such as `علاج نهائي`, `بدون أدوية`, `وصفة طبيعية`, `خلطة`, `في أسبوع`, because misinformation studies found these in misleading titles (Gharbi: 75% misleading titles).
- **Institutional phrasings** such as `نصائح طبيب`, `وزارة الصحة`, `توعية`, so that sound content is also sampled.

Run each query with `relevanceLanguage=ar` and with a rotation of `regionCode` values to pull dialect regions: `EG`, `SA`, `JO`, `PS`, `IQ`, `MA`, `DZ`, `SD`, `AE`, `LB` (suggestion; the region filter restricts to videos viewable there, which is weak, so dialect terms matter more). Use `order=relevance` for most queries and `order=viewCount` for a few, then de-duplicate by `video_id`. Budget: about 60–80 search calls per topic, one day of quota.

Before writing any query list, the team should spend 30 minutes in YouTube's search box and Google Trends (Arabic, past 12 months) per topic and write down the terms real users type. The term list goes into the paper's datasheet.

## 3. Selection criteria (what we take and what we leave)

Apply after `videos.list` enrichment, automatically where possible, then by a 30-second manual screen.

**Automatic filters**
- `snippet.liveBroadcastContent` must be `none`; `status.madeForKids` false.
- Duration: Shorts ≤ 60 s go in as `format: short`; videos 2–15 min are clip candidates; videos > 15 min only if a clear 2–3 minute segment on the topic can be chosen at screening (store `clip_start_s`, `clip_end_s`). Suggested cap: 15 min, because screening and Whisper time grow with length.
- Published after 2020-01-01 (suggestion: recent language and current claims; also keeps the dataset describable as "2020–2026").
- De-duplicate by `video_id`; flag likely re-uploads (same title, same duration ± 2 s).
- Per-channel cap: at most 3 videos per channel per topic. Reason: splits are grouped by channel (ARCHITECTURE §2), so one channel with 20 videos either dominates a split or forces an unbalanced split.

**Manual screen (30 s, by the Data track, logged in `screen_note`)**
- Spoken Arabic is the main audio (any dialect; MSA counts). Reject music-only, text-only, mostly English or French, dubbed cartoons.
- The topic is actually discussed (not only in the title).
- Record `publisher_type` (doctor as self-described in the channel or title / official body / non-specialist / unknown) and `dialect` (schema values). These two fields are what the paper's descriptive analysis will use, so they must be filled for every accepted video.

**Stratification (suggestion; D017)**
Per topic of 80 videos: about half Shorts and half clips (the proposal names both formats); and a target spread over publisher types, for example at least 15 official/doctor videos and at least 25 non-specialist videos, so the dataset is not only misinformation. Published studies show misleading content concentrates in individual/blog channels (Ayoub: 64% vs 15%), so a dataset drawn only from "most viewed" would over-represent one publisher type. Do not select by whether a video "looks wrong": that would bias the claim-detection labels. Select by format, publisher type, dialect spread and popularity band (for example: a third from the top 50 by views, two thirds from the rest of the candidate pool), then label whatever is said.

**Overlap between topics**
A video is assigned to the topic whose query found it first in the collection order, unless the manual screen shows it is mainly about another topic. Herbal-cancer videos count as `herbal_alternative` if that topic is collected before cancer; this is why the order matters.

## 4. Getting audio and captions (yt-dlp, D003)

- `yt-dlp -x --audio-format m4a --write-auto-subs --sub-langs "ar.*" --write-info-json --sleep-interval 5 --max-sleep-interval 15 -a ids.txt` (flags verified in the yt-dlp README today). Audio goes to the team server, never to git.
- Keep the `.info.json` (title, channel, upload date, duration, view count at download time): it is the metadata snapshot the datasheet will cite.
- The automatic Arabic captions, when present, are the "second ASR output" of D010.
- The YouTube API Developer Policies 30-day storage rule applies to data fetched through the API; metadata we keep long-term comes from yt-dlp and from the public page, which is a different route. This is a legal reading, not verified with a lawyer; it should be stated honestly in the paper's ethics section together with the supervisor's approval (D003 follow-up).

## 5. Pilot first

Before collecting 80 videos of topic 1, collect **20 pilot videos**: 14 from topic 1 and 2 each from three other topics (D008 consequence), half Shorts and half clips, all dialect groups represented if possible. The pilot measures: candidate yield per query (how many of 50 hits survive the screen), screening time, segments per video, and agreement. Those numbers then set the real per-topic budget.

## 6. Records to keep from day one

- `src/collect/queries/<topic>.yaml`: every query, region code, order, date run, hits returned.
- `data/videos/<topic>.jsonl`: one record per screened video, accepted or rejected (`screened: true`, `screen_note` says why if rejected). Rejections are needed for the datasheet's "how many were excluded and why".
- A `collection-log.md` in `src/collect/` with the day, the quota used and any API errors.

## Sources checked on 10 Nov 2026

- YouTube Data API: search.list reference; videos resource; captions.download; quota cost page (developers.google.com/youtube/v3).
- yt-dlp README (github.com/yt-dlp/yt-dlp).
- Gharbi et al. 2023, Endocrine Abstracts 90 EP539. Ayoub et al. 2021, Supportive Care in Cancer 29:8009–8017. Abu Daabes & Kharbat 2019, Int. J. Health Governance 24(4):267–273. Kharbat & Abu Daabes 2023, Health Informatics Journal 29(3), doi 10.1177/14604582231198022. Dabbus et al. 2025, J. Egypt. Public Health Assoc. 100(1), doi 10.1186/s42506-025-00201-2.
- Not reopened today (blocked pages): Almogbel et al. 2021; Baqain et al. 2023 (PMC10393303).
