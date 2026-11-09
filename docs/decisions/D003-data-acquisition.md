---
id: D003
title: Downloading YouTube audio and captions
status: accepted
date: 2026-11-09
decided_by: Supervisor meeting (reported by Abdulrahman)
owner: Data & access track
changes_proposal: true
follow_up:
  - Record who gave the approval and when, ideally as an email; the paper's ethics checklist will cite it
  - Test audio download on 2-3 videos from the team server and from Colab/Kaggle (cloud notebooks may be blocked; unverified)
---
## Question
May the team download audio and captions from YouTube for research?

## Decision
Yes, **by any method**. Where a video has no transcript, use speech-to-text (for example Whisper) or YouTube's automatic captions.

## Consequences
- Proposal §4 says collection follows YouTube's terms of service. YouTube's Terms (15 Dec 2023) restrict downloading without written permission; this approval is what the project relies on, so it must be documented.
- Audio and video files never go into the git repository (size and redistribution). See `.gitignore`.
- Enables Whisper on all videos and RQ2 as written. Transcription source: D010.
