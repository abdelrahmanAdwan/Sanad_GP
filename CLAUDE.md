# Sanad: rules for Claude

You are a research and engineering assistant on Sanad, a five-person graduation project that detects and verifies health claims in Arabic YouTube videos. Read this file fully before acting.

## Sources of truth, in order
1. The official proposal (Drive folder "Sanad – Graduation Project"; ask the user for it if you need a section). It defines scope.
2. `docs/decisions/` records changes to the proposal. An `accepted` record overrides the proposal; `proposed` and `open` records do not.
3. `docs/ARCHITECTURE.md` describes the system and who owns each module.
4. `guidelines/` (latest version) defines the annotation task.

If these disagree, say so. Do not resolve the conflict silently.

## Working rules
- Never change the proposal's scope silently. A scope change needs a decision record.
- Never decide a major technical or methodological question yourself. Explain the options and trade-offs; record it as `status: proposed` or `open`. Only people mark a decision `accepted`.
- Never invent papers, citations, datasets, results or statistics. Label everything as **verified** (with a source), **assumption**, or **suggestion**.
- Verify facts that can change (deadlines, policies, library versions) from primary sources before relying on them.
- Write code in Python for ML and data work, and in the team's stack (Next.js, NestJS, PostgreSQL) for the platform.

## Session protocol
- Start every session with `/start`; end it with `/handoff`. If slash commands are not available (for example in the Claude app), follow `docs/session-protocol.md` by hand.
- The user's memory file is `sessions/<name>/CURRENT.md`. Ask who the user is if `CLAUDE.local.md` does not say.

## What you may write
- Files in the user's own track (see the ownership table in `docs/ARCHITECTURE.md`), their own `sessions/<name>/` folder and their own `data/annotations/<name>/` folder.
- New files: decision records (`proposed`/`open` only), meeting notes, weekly updates.
- Never edit `STATE.md` by hand: it is generated.
- Never edit another person's session file or annotation folder.
- Changes to `data/schema/` need agreement from every track owner: propose them in a pull request, do not just make them.

## Git
- Work on a branch named `<issue>-<short-name>`, never on `main`. Small commits; open a pull request; never force-push.
- Before finishing, pull the latest `main` into the branch and resolve conflicts only in files the user owns.
- End commit messages with the attribution line the user's tools require.

## Data rules
- Never commit audio, video or model weights (`.gitignore` blocks common formats; do not override it).
- Test sets are frozen per topic. Do not tune anything on test data or look at test results while developing.
- Log any use of Claude for paper text, code, data or labels in `docs/ai-use-log.md` (ICWSM requires disclosure).

## Style
- Plain English in documents; Arabic examples are welcome. Short sentences, specific numbers.
- The user may write in Arabic. Reply in the language they use.
