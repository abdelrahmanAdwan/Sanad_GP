---
id: D010
title: Transcription source for the dataset
status: proposed
date: 2026-11-09
decided_by: ""
owner: Transcripts track
changes_proposal: true
follow_up:
  - Compare Whisper model sizes on pilot videos (WER per dialect, hallucination on music/silence) and fix one version
---
## Proposal
Run **one fixed Whisper version on every dataset video**, so all videos share one kind of ASR error and RQ2 measures one system. Keep YouTube's automatic captions as a **second ASR output** where they exist, for comparison.

## Why
Proposal §6.1 uses captions when available and Whisper otherwise. That mixes two error types across videos and confuses RQ2. D003 now allows downloading audio, so a single source is possible.
