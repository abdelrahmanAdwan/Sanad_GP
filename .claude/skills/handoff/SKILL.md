---
name: handoff
description: End a Sanad work session. Updates the user's memory file, records decisions as proposed, commits and pushes the branch, and drafts the issue status comment.
disable-model-invocation: true
argument-hint: "[your-name]"
---

End the Sanad session for $ARGUMENTS (if empty, take the name from CLAUDE.local.md or ask).

1. Copy `sessions/<name>/CURRENT.md` to `sessions/<name>/log/<YYYY-MM-DD>.md` (append `-2`, `-3` if that file exists).
2. Rewrite `sessions/<name>/CURRENT.md` from `sessions/_template/CURRENT.md`. Keep it to one page:
   - front matter: `updated`, `task`, `branch`, `last_commit` (after step 4, amend), `main_seen` (the `origin/main` commit read at /start, or the one merged into the branch)
   - Done this session, Next step (one concrete action), Blocked on, Files touched, Notes for next session.
3. For any decision made or proposed in this session, create a new file in `docs/decisions/` with `status: proposed` or `open`. Never set `accepted`.
4. If Claude wrote paper text, code, data or labels, add a line to `docs/ai-use-log.md`.
5. Run `git status`. Stage only files in the user's track, their session folder and new decision/meeting files. Commit with a clear message and push the branch. Never push to `main`; never force-push.
6. Post or print the issue comment: `Done: … | Next: … | Blocked: …` (`gh issue comment <n> --body "…"` if `gh` works; otherwise print it for the user to paste).
7. Do not edit `STATE.md`, other people's files, or `data/schema/`.
8. Tell the user in two lines what was saved and what the next session starts with.
