---
id: D020
title: Claude as a separate, labelled system in the pilot (ASR correction; sixth annotator)
status: proposed
date: 2026-11-28
decided_by: ""
owner: Coordinator
changes_proposal: false
follow_up:
  - "Team approval at the 3 Dec meeting"
  - "ASR correction: Mohammad shares the Whisper large-v3 text of the reference clips; Claude corrects it without audio and without seeing the human references; Mahmoud adds one row to the comparison table"
  - "Sixth annotator: only after the five human files are handed in; stored under experiments/, never in data/annotations/"
---
## Proposal
Add Claude to the pilot as an extra system that is compared with the human work, never mixed into it. Suggested by Abdulrahman Adwan on 26–28 Nov.

1. **ASR + LLM correction.** Input: Whisper large-v3 output for each reference clip. Claude rewrites it using context only (no audio, no human reference, no YouTube captions). Output goes to `asr/whisper-large-v3+claude/`. Mahmoud scores it with the same CER/WER script as every other method. Question it answers: does LLM post-correction reduce errors on dialect speech, and does it invent words?
2. **Sixth annotator.** Claude labels the 20 pilot videos with guidelines v0 from the segment text, as annotator `claude`. Shaath computes agreement for the five humans first, then reports Claude-vs-human agreement separately. This is an early version of the LLM baseline in proposal §6.5.

## Rules
- Claude output is never used as a reference transcript, never edited into one, and never counted in human agreement.
- Every use is logged in `docs/ai-use-log.md`.
- Human annotators do not see Claude's labels before handing in their own (anchoring).

## Alternatives
- **No Claude in the pilot:** simpler; the LLM baseline waits for the experiments phase (M4).
- **Claude only as annotator:** skips the ASR question, which matters for D010.
