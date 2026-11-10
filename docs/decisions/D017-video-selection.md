---
id: D017
title: Video selection rule (formats, duration cap, per-channel cap, stratification)
status: proposed
date: 2026-11-10
decided_by: ""
owner: Data & access
changes_proposal: true
follow_up:
  - "Team approval of the rule in docs/collection-protocol.md §3"
  - "Replace the suggested numbers (duration cap, per-channel cap, publisher-type minimums) with pilot numbers"
  - "Confirm the start date filter (2020-01-01) or drop it"
---
## Proposal
Per topic: about half YouTube Shorts (≤ 60 s) and half 2–3 minute clips cut from videos of 2–15 minutes; at most 3 videos per channel; published 2020 or later; a target spread over publisher types (at least 15 doctor/official and at least 25 non-specialist videos per 80) and over dialect groups; popularity bands rather than "most viewed" only. Videos are never chosen because they look right or wrong; that would bias the claim labels. Full rule: `docs/collection-protocol.md` §3.

## Why it changes the proposal
The proposal names the two formats and the counts but no duration cap, channel cap or stratification. Table 3's "80 videos per topic" stays the target.

## Alternatives
- **Most-viewed only** (as in the published Arabic YouTube studies): easier to describe, but over-represents popular individual channels and misinformation; weak for a claim-detection dataset that must also contain ordinary informational speech.
- **No per-channel cap**: more videos faster, but channel-grouped splits become unbalanced and the model learns speakers.
- **Clips only, no Shorts**: more sentences per video (the audit estimates Shorts give fewer than 15), but it drops the format where the proposal and ViClaim expect most misinformation.
