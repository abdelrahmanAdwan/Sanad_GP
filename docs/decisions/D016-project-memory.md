---
id: D016
title: Project state and Claude session memory
status: proposed
date: 2026-11-09
decided_by: ""
owner: Coordinator
changes_proposal: false
follow_up:
  - Team approval; mechanism described in docs/session-protocol.md
---
## Proposal
- `STATE.md` is **generated** by `scripts/gen_state.py` from decision records, session files and milestones. Nobody edits it by hand, so it never conflicts.
- Each person has one memory file, `sessions/<name>/CURRENT.md`, written only by that person and their Claude.
- Every session starts with `/start` and ends with `/handoff` (project skills in `.claude/skills/`), and ends with a short status comment on the person's GitHub issue.
