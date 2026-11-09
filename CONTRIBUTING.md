# Working together without conflicts

Conflicts happen when two people edit the same file at the same time. The rules below make that rare instead of making us good at resolving it.

## The flow (GitHub Flow)
1. **Issue first.** Every task is a GitHub issue with one assignee and a milestone.
2. **Branch.** Create a branch from the latest `main`, named `<issue>-<short-name>`, for example `12-guidelines-v0`.
3. **Small commits.** Pull `main` into your branch at least once a day: `git pull origin main`.
4. **Pull request.** Open a small PR (aim for under ~300 changed lines; data files excepted). Link the issue: `Closes #12`.
5. **Review.** The owner of each touched folder reviews (`.github/CODEOWNERS`). Checks must pass.
6. **Merge.** Squash merge, delete the branch. The issue closes automatically.

A branch should live 1–3 days. Long branches drift from `main` and conflict.

## Rules that prevent conflicts
- **Add a new file instead of editing a shared one.** One file per decision, per meeting, per weekly update, per annotator.
- **`STATE.md` is generated, never edited.** It is gitignored; run `python scripts/gen_state.py`.
- **Your session file is yours only:** `sessions/<name>/CURRENT.md`.
- **Annotations:** each annotator writes only in `data/annotations/<name>/`. A script merges them.
- **Schemas are a contract.** A change to `data/schema/` is a PR reviewed by every track owner.
- **One person updates dependencies** (`requirements*.txt`, `package.json`).
- **Notebooks are personal.** Keep them under `experiments/<name>/notebooks/`; shared code goes in `src/` as `.py` files. Outputs are stripped on commit.
- **Formatting is automatic.** Install the hooks once: `pip install pre-commit && pre-commit install`. Run `pre-commit autoupdate` to move the hook versions forward.

## Never commit
Audio, video, model weights, API keys or tokens. `.gitignore` blocks common formats. Store audio on the team server.

## Test sets
Each topic's test split is frozen when the topic is complete. Whoever tunes models does not look at test results until the final run.

## Repository settings (owner does this once)
- Make the repository **private**.
- Branch protection on `main`: require a pull request, 1 approving review, review from code owners, passing checks; block force pushes and deletion.
- On a private repository these settings need GitHub Pro or higher. Verified students get GitHub Pro free through GitHub Education, so the owner should verify their student status first. (Source: docs.github.com, "About GitHub's plans" and "About protected branches".)
- Fill in real GitHub usernames in `.github/CODEOWNERS`.

## Working offline
Git works without internet. Commit locally and push when the connection returns. Small PRs make interrupted sessions cheap.
