---
name: start
description: Start a Sanad work session. Loads team state, the user's memory file and what changed since their last session, then reports before any work begins.
disable-model-invocation: true
argument-hint: "[your-name]"
---

Start a Sanad session for $ARGUMENTS (if empty, take the name from CLAUDE.local.md or ask).

1. Read `CLAUDE.md` if it is not already in context.
2. Run `git fetch origin`, then `python scripts/gen_state.py --ref origin/main`. Read `STATE.md`. If there is no remote yet, run `python scripts/gen_state.py`.
3. Read `sessions/<name>/CURRENT.md` and the GitHub issue it names (`gh issue view <n>` if `gh` works; otherwise ask the user).
4. Read `docs/ARCHITECTURE.md` and the `README.md` of the module named in the session file. Do not read other files yet.
5. Find what changed since the user's last session, using `main_seen` from their session file:
   - `git log --oneline <main_seen>..origin/main`
   - `git diff --stat <main_seen> origin/main -- docs/decisions data/schema guidelines docs/ARCHITECTURE.md`
   Read any changed decision record or schema in full.
6. Check that the current branch matches the session file. If the user is on `main`, say so and suggest the branch.
7. Report in at most five lines: where the user stopped, what changed that affects them (with decision IDs), blockers, and the exact next step. Then wait for the user to confirm before doing any work.
