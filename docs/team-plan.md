# Team plan: five people, one pipeline (draft for team review)

Status: **proposed**, 2026-11-10. Owners are not assigned (D014). This document says what each track does week by week, how the five coordinate, and what Claude does and does not do in each track.

## 1. Tracks and workload

Everything in semester 1 is one pipeline run five times (once per topic, D008). Each track owns one stage and its code; everyone annotates.

| Track | Owns (folders) | Main deliverables, semester 1 | Rough effort |
| --- | --- | --- | --- |
| Coordination & paper | `docs/`, `paper/`, `scripts/`, `CLAUDE.md`, `.claude/` | Decision records, weekly status, datasheet, Zenodo release, paper draft, ICWSM checklist, AI-use log | 1 day/week + paper weeks in January |
| Data & access | `src/collect/`, `data/videos/` | Query lists, API script, screening, 80 videos per topic with `publisher_type` and `dialect` filled | 1–2 days per topic |
| Transcripts | `src/transcribe/`, `data/segments/` | yt-dlp runner, fixed Whisper version on the server, segmentation (D006), WER on corrected test transcripts | 2 days per topic + server time |
| Guidelines & quality | `guidelines/`, `src/agreement/` | Guidelines v0 → v1, pilot analysis, agreement (Krippendorff's α), adjudication log (D007), frozen per-topic splits | 2 days per topic, heavier in the pilot |
| Experiments | `src/models/`, `experiments/` | Baselines, AraBERT/CAMeLBERT/MARBERT fine-tuning, ASR-vs-corrected (RQ2), leave-one-topic-out, result tables | Starts on pilot data; 2–3 weeks in December–January |
| Everyone | own `data/annotations/<name>/`, own `sessions/<name>/` | Annotation of assigned videos; session memory | see below |

**Annotation load (estimate, to be replaced by pilot numbers).** 400 videos, each labeled by one person, 20% by two (proposal) → 480 video-annotations / 5 people = 96 per person. If a video takes about 10 minutes with the video playing (about 15 segments), that is about 16 hours per person over six weeks, or about 3 hours a week. If the pilot shows 20 minutes per video, double it. This is the number to watch; it decides whether 400 videos is realistic.

**Choosing owners.** Suggested matching, for the team to confirm: Data & access to whoever is most fluent across dialects (screening is a listening job); Transcripts to whoever administers the server; Experiments to whoever has trained transformers before; Guidelines & quality to the most careful reader, since the guidelines decide the dataset's value; Coordination to whoever already talks to the supervisor. Each track also has a **backup** who reviews its pull requests (CODEOWNERS), so no track has a single point of failure.

## 2. How the topics flow (pipelining)

Topics are sequential, but tracks overlap so nobody waits:

```
Week      1        2        3        4        5        6        7        8        9
Data      pilot20  T1       T2       T3       T4       T5       (reserve)
Transc.            pilot    T1       T2       T3       T4       T5
Guidel.   v0       pilot→v1 T1 agree T2 agree T3 agree T4 agree T5 agree  splits
Annot.             pilot    T1       T2       T3       T4       T5
Experim.  setup    pilot    baselines T1-T2   RQ2 ASR  LOTO     LLMs     final tables
Coord.    issues   datasheet start        weekly status     Zenodo   paper draft → submit
```

Dates are the milestones in `docs/milestones.yaml` (M1 pilot 23 Nov, M2 topic 1 7 Dec, …), all suggestions until the team confirms. If a topic slips, the next topic's collection still starts: collection is cheap, annotation is the bottleneck.

**Definition of done per topic:** 80 (or the agreed number) screened videos → audio and transcripts on the server → segments file validated → every segment labeled once, 20% twice → agreement computed and disagreements adjudicated → split frozen → `docs/updates/<date>-topic-<n>.md` written. Only then does the topic count toward the paper.

## 3. Weekly rhythm

| When | What | Who |
| --- | --- | --- |
| Monday, 30 min | Plan the week: each person names one issue to finish; STATE.md on screen | all five |
| Daily | Work in Claude on a branch; `/start` at the beginning, `/handoff` at the end (writes your memory file and a status comment on your issue) | each person |
| Thursday, 30 min | Blockers and decisions. New decision records proposed during the week are accepted or rejected here | all five |
| Weekly | Supervisor update: a 10-line email or meeting from the Coordinator, listing accepted decisions and open questions | Coordinator |
| Per topic | Annotation review: the Guidelines owner shows the agreement numbers and the worst disagreements; guideline changes go into the next version, never into the current one | all five |

Rules that keep this conflict-free are already in `CONTRIBUTING.md` and `docs/session-protocol.md`: one issue per task, one branch per issue, small pull requests reviewed by the folder owner, nobody edits another person's session or annotation files, STATE.md is generated.

## 4. What Claude does in each track, and what it must not do

Claude is a tool each member runs in their own session on the repository. It reads `CLAUDE.md`, `STATE.md` and the member's memory file, so it knows the project state without being told.

| Track | Good uses of Claude | Not allowed |
| --- | --- | --- |
| Data & access | Write and test the API search script and de-duplication; build the screening sheet; turn the screen log into `data/videos/<topic>.jsonl` and validate it; draft the query lists from Google Trends output | Deciding `publisher_type` or `dialect` for a video (a person listens and decides); selecting videos by content |
| Transcripts | yt-dlp and Whisper runners on the server; segmentation script; WER computation; detecting Whisper hallucinations on silence/music; comparing model sizes on the pilot | Choosing the Whisper version alone (that is D010, a team decision); "fixing" transcripts by generation instead of human correction |
| Guidelines & quality | Discuss edge cases against the guidelines; propose wording; compute α and κ; produce the adjudication log template; find systematic disagreements between two annotators | **Labeling segments.** Every label in the dataset must come from a person. Claude labels only appear in `experiments/` as an LLM baseline, clearly separated |
| Experiments | Training and evaluation code, experiment configs, result tables with seeds and confidence intervals, error analysis on dev data | Looking at test results while developing; tuning on test; reporting a number Claude did not actually run |
| Coordination & paper | Decision records, STATE generation, weekly update drafts, datasheet, checking every citation against its source, formatting the paper, ICWSM checklist | Writing claims about results that are not in `experiments/`; inventing or "completing" citations; marking a decision `accepted` |
| Everyone | `/start` and `/handoff`; explaining a script before running it; reviewing a pull request before asking the human reviewer | Running anything that deletes data or force-pushes; editing another member's files |

Every use of Claude for paper text, code, data processing or label-related work is logged in `docs/ai-use-log.md` (ICWSM requires an AI-use disclosure). One line per session is enough: date, person, what Claude produced, what the person checked.

## 5. What the team must decide before week 1

1. Owners and backups for the five tracks (D014) → fill `.github/CODEOWNERS` and `docs/ARCHITECTURE.md` §4.
2. Who owns the GitHub repository (GitHub Education for protected branches).
3. Topic order (D012) — evidence in `docs/collection-protocol.md` §1.
4. Pilot tool (D013) and whether annotators watch the video (D011).
5. Approve or change the selection rule (D017) and this plan (D018).
