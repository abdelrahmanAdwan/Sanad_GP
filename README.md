# Sanad · سند

Detecting and verifying health claims in Arabic YouTube videos. Graduation project, Department of Computer Engineering, Islamic University of Gaza, 2026–2027.

- **Semester 1:** an Arabic dataset for claim detection in health video transcripts, claim-detection benchmarks, and a dataset paper.
- **Semester 2:** an evidence base, a verification model, and a web platform with a timeline and a chatbot.

The official proposal is the primary reference for scope. Changes to it are recorded in `docs/decisions/`.

## Start here

| If you want to… | Read |
| --- | --- |
| Know where the project is | Run `python scripts/gen_state.py` and read `STATE.md` |
| Understand the system | `docs/ARCHITECTURE.md` |
| See what was decided and what is open | `docs/decisions/` |
| Annotate | `guidelines/` (latest version) |
| Contribute without conflicts | `CONTRIBUTING.md` |
| Work with Claude | `CLAUDE.md` and `docs/session-protocol.md` |

## Layout

```
CLAUDE.md                project rules for Claude (loaded automatically by Claude Code)
.claude/skills/          /start and /handoff session commands
docs/ARCHITECTURE.md     pipeline, data model, module map
docs/decisions/          one file per decision (D001…)
docs/meetings/           one file per meeting
docs/updates/            weekly update, one file per person per week
docs/milestones.yaml     milestones read by the state generator
sessions/<name>/         each person's Claude memory file (CURRENT.md) and log
guidelines/              annotation guidelines, versioned
data/schema/             JSON schemas: the contract between tracks
data/templates/          annotation sheet templates
data/videos/             video metadata (no audio or video files)
data/segments/           fixed time segments with transcript text
data/annotations/<name>/ each annotator's labels
src/collect/             search, screening, metadata          (Data & access)
src/transcribe/          audio, ASR, segmentation, WER         (Transcripts)
src/agreement/           merging labels, agreement, adjudication (Guidelines & quality)
src/models/              baselines, Arabic BERTs, LLMs          (Experiments)
experiments/             configs and results
paper/sections/          one file per paper section
scripts/                 project tooling (state generator)
```

Audio and video files are never committed. See `.gitignore`.
