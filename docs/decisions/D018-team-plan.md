---
id: D018
title: Team plan (pipelining of topics, weekly rhythm, Claude use per track)
status: proposed
date: 2026-11-10
decided_by: ""
owner: Coordinator
changes_proposal: false
follow_up:
  - "Team approval of docs/team-plan.md"
  - "Assign owners and backups (D014), then fill .github/CODEOWNERS"
  - "Replace the annotation-load estimate with pilot measurements"
---
## Proposal
Run the dataset pipeline once per topic with the five tracks overlapping (collection of topic n+1 starts while topic n is annotated); a Monday plan and a Thursday decisions meeting; every member uses Claude in their own session with `/start` and `/handoff`; Claude never labels dataset segments, never decides a major question and never marks a decision accepted. Full text: `docs/team-plan.md`.

## Alternatives
- **Strict sequence (finish topic n fully before starting n+1):** simpler, but the Data and Transcripts tracks sit idle during annotation weeks; with about nine weeks to the first deadline this costs roughly two topics.
- **Everyone does everything per topic:** no idle time, but no ownership of code and schemas, which is where conflicts and silent format changes come from.
