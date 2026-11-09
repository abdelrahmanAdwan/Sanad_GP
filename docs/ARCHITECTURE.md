# Architecture

Sanad has two parts. Semester 1 builds a **dataset pipeline** that turns YouTube videos into labeled transcript segments. Semester 2 builds the **verification system** that uses a claim detector trained on that dataset. Status as of 2026-11-09: nothing is implemented yet.

## 1. Verification system (proposal §6.1)

```
YouTube link
  │
  ▼
[1] Transcription ──► segments (start, end, text)            src/transcribe   reuse: Whisper
  │
  ▼
[2] Claim detection ──► labels per segment                    src/models       fine-tune on our dataset
  │   (check-worthy segments only continue)
  ▼
[3] Claim normalization ──► short, self-contained claim       platform         LLM, few-shot
  │
  ▼
[4] Claim matching ──► reuse verdict if a checked claim matches   platform     AraFacts (health subset)
  │
  ▼
[5] Evidence retrieval ──► top 20 passages ─► rerank to top 5  platform        BGE-M3 + pgvector + reranker
  │
  ▼
[6] Verification ──► supported / refuted / misleading / not enough evidence   fine-tune multilingual NLI
  │
  ▼
[7] Presentation ──► timeline beside the video + chatbot (RAG)  platform       Next.js + NestJS
```

The research contribution is stage 2. Stages 1 and 2 are built in semester 1 inside this repository; stages 3–7 are semester 2 (a `platform/` folder will be added then).

## 2. Dataset pipeline (semester 1)

Topics are processed **one at a time** (D008). For each topic:

| Step | What happens | Output | Module | Decided by |
| --- | --- | --- | --- | --- |
| 1. Search | YouTube Data API queries per topic in MSA and dialects | candidate list | `src/collect` | proposal Table 3 |
| 2. Screen | ~30 s manual check: spoken health content? | `data/videos/<topic>.jsonl` | `src/collect` | proposal Table 3 |
| 3. Audio | Download audio to the team server (never to git) | audio files on server | `src/transcribe` | D003 |
| 4. ASR | One fixed Whisper version on every video; YouTube auto-captions kept as a second output | raw transcripts | `src/transcribe` | D010 (proposed) |
| 5. Segment | Cut once into fixed time segments | `data/segments/<topic>.jsonl` | `src/transcribe` | D006 |
| 6. Correct | Manual correction of test-set transcripts **inside** segment boundaries | `text_corrected` field | `src/transcribe` | D006 |
| 7. Annotate | Each annotator labels segments with the guidelines | `data/annotations/<name>/` | annotators | D002 (open), guidelines |
| 8. Agree | Merge labels, compute agreement, adjudicate the double-annotated subset | merged labels + log | `src/agreement` | D007 (open) |
| 9. Split | Per-topic train/dev/test (70/15/15), grouped by video and channel; frozen when the topic is complete | `split` field | `src/agreement` | proposal Table 3, D008 |
| 10. Release | Zenodo with a DOI | dataset release | Coordination | D004 (open) |

Grouping splits by **video and channel** prevents near-duplicate segments from the same speaker landing in both training and test data.

## 3. Data model

Files, one JSON object per line (`.jsonl`). The schemas in `data/schema/` are the contract between tracks.

| Entity | Key | Schema | Written by |
| --- | --- | --- | --- |
| Video | `video_id` (YouTube ID) | `video.schema.json` | Data & access |
| Segment | `segment_id` = `<video_id>_<start_ms>` | `segment.schema.json` | Transcripts |
| Annotation | (`segment_id`, `annotator`) | `annotation.schema.json` | each annotator |

Segment IDs never change once annotation starts, because labels point to them.

The semester-2 database (PostgreSQL + pgvector, proposal Table 7) has the tables `sources`, `evidence_chunks`, `fact_checks`, `videos`, `segments`, `claims`, `claim_evidence`, `verdicts`. Only evidence passages, normalized claims and previously checked claims are embedded (BGE-M3, 1,024 dimensions, HNSW, cosine).

## 4. Ownership

| Track | Owns | Owner | Backup |
| --- | --- | --- | --- |
| Coordination & paper | `docs/`, `paper/`, `scripts/`, `CLAUDE.md`, `.claude/` | TBD (D014) | TBD |
| Data & access | `src/collect/`, `data/videos/` | TBD | TBD |
| Transcripts | `src/transcribe/`, `data/segments/` | TBD | TBD |
| Guidelines & quality | `guidelines/`, `src/agreement/` | TBD | TBD |
| Experiments | `src/models/`, `experiments/` | TBD | TBD |
| Everyone | `data/schema/` (joint review), own `sessions/<name>/` and `data/annotations/<name>/` | all | — |

## 5. Invariants

- No audio, video or model weights in git.
- Test splits are frozen per topic and never used for tuning.
- `STATE.md` is generated; decision records are append-only.
- Every experiment result in the paper is reproducible from a config in `experiments/` and a commit hash.

## 6. Open questions that affect this design

D002 label formulation · D004 transcript release · D007 adjudication · D011 watching while labeling · D012 topic order · D013 annotation tool · D014 owners. See `docs/decisions/`.
