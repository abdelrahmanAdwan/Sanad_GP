#!/usr/bin/env python3
"""Generate STATE.md: a one-page view of the project built from repository files.

Nobody edits STATE.md by hand, so it never causes merge conflicts. Sources:
  docs/milestones.yaml          milestones
  docs/decisions/D*.md          decision records (YAML front matter)
  sessions/<name>/CURRENT.md    each person's session memory (front matter + sections)
  GitHub issues (optional)      with --issues, if the gh CLI is installed and logged in

Usage:
  python scripts/gen_state.py                    # from the working tree
  python scripts/gen_state.py --ref origin/main  # from a git ref (the team's merged state)
  python scripts/gen_state.py --issues           # also list open GitHub issues
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.S)
STATUS_ORDER = {"open": 0, "proposed": 1, "accepted": 2, "superseded": 3}


class Source:
    """Reads files from the working tree or from a git ref."""

    def __init__(self, ref: str | None):
        self.ref = ref

    def _git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True
        ).stdout

    def describe(self) -> str:
        try:
            commit = self._git("rev-parse", "--short", self.ref or "HEAD").strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "working tree (no git commit)"
        return f"{self.ref} @ {commit}" if self.ref else f"working tree (HEAD @ {commit})"

    def list(self, pattern: str) -> list[str]:
        if self.ref is None:
            return sorted(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
        names = self._git("ls-tree", "-r", "--name-only", self.ref).splitlines()
        return sorted(n for n in names if Path(n).match(pattern))

    def read(self, path: str) -> str | None:
        if self.ref is None:
            p = ROOT / path
            return p.read_text(encoding="utf-8") if p.exists() else None
        try:
            return self._git("show", f"{self.ref}:{path}")
        except subprocess.CalledProcessError:
            return None


def split_front_matter(text: str) -> tuple[dict, str]:
    m = FRONT_MATTER.match(text)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    return (meta if isinstance(meta, dict) else {}), m.group(2)


def section(body: str, heading: str) -> str:
    """Return the text under '## <heading>' up to the next '## ' heading."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)", body, re.S | re.M)
    if not m:
        return ""
    lines = [ln.strip().lstrip("-").strip() for ln in m.group(1).splitlines()]
    return "; ".join(ln for ln in lines if ln)


def as_text(value: object) -> str:
    """Flatten a YAML value that was meant as text (an unquoted 'a: b' becomes a dict)."""
    if isinstance(value, dict):
        return "; ".join(f"{k}: {v}" for k, v in value.items())
    return "" if value is None else str(value)


def cell(value: object) -> str:
    text = as_text(value)
    return text.replace("|", "\\|").replace("\n", " ").strip() or "—"


def load_decisions(src: Source) -> list[dict]:
    out = []
    for path in src.list("docs/decisions/D*.md"):
        meta, _ = split_front_matter(src.read(path) or "")
        if meta.get("id"):
            meta["_path"] = path
            out.append(meta)
    return sorted(out, key=lambda d: (STATUS_ORDER.get(d.get("status"), 9), str(d["id"])))


def load_sessions(src: Source) -> list[dict]:
    out = []
    for path in src.list("sessions/*/CURRENT.md"):
        if "/_template/" in path:
            continue
        meta, body = split_front_matter(src.read(path) or "")
        meta.setdefault("person", Path(path).parent.name)
        meta["_next"] = section(body, "Next step")
        meta["_blocked"] = section(body, "Blocked on")
        out.append(meta)
    return sorted(out, key=lambda s: str(s.get("person")))


def load_milestones(src: Source) -> list[dict]:
    text = src.read("docs/milestones.yaml")
    data = yaml.safe_load(text) if text else None
    return data if isinstance(data, list) else []


def load_issues() -> tuple[list[dict], str | None]:
    if not shutil.which("gh"):
        return [], "gh CLI not installed"
    fields = "number,title,assignees,milestone,labels,updatedAt"
    proc = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--limit", "100", "--json", fields],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return [], (proc.stderr.strip().splitlines() or ["gh failed"])[0]
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError:
        return [], "could not parse gh output"


def render(src: Source, with_issues: bool) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    decisions = load_decisions(src)
    sessions = load_sessions(src)
    milestones = load_milestones(src)
    lines = [
        "# Sanad: project state",
        "",
        f"Generated {now} from {src.describe()} by `scripts/gen_state.py`. Do not edit by hand.",
        "",
    ]

    lines += ["## Milestones", "", "| ID | Milestone | Status | Target | Note |"]
    lines += ["| --- | --- | --- | --- | --- |"]
    for m in milestones:
        lines.append(
            f"| {cell(m.get('id'))} | {cell(m.get('name'))} | {cell(m.get('status'))} "
            f"| {cell(m.get('target'))} | {cell(m.get('note'))} |"
        )
    if not milestones:
        lines.append("| — | No milestones file | — | — | — |")

    pending = [d for d in decisions if d.get("status") in ("open", "proposed")]
    lines += ["", f"## Decisions needing action ({len(pending)})", ""]
    lines += ["| ID | Title | Status | Owner | Next |", "| --- | --- | --- | --- | --- |"]
    for d in pending:
        follow = d.get("follow_up") or []
        lines.append(
            f"| {cell(d['id'])} | {cell(d.get('title'))} | {cell(d.get('status'))} "
            f"| {cell(d.get('owner'))} | {cell(follow[0] if follow else '')} |"
        )

    accepted = [d for d in decisions if d.get("status") == "accepted"]
    lines += ["", f"## Accepted decisions ({len(accepted)})", ""]
    for d in accepted:
        flag = " · changes the proposal" if d.get("changes_proposal") else ""
        lines.append(f"- **{d['id']}** {d.get('title')} ({d.get('date')}){flag}")
    followups = [(d["id"], f) for d in accepted for f in (d.get("follow_up") or [])]
    if followups:
        lines += ["", "Follow-ups on accepted decisions:", ""]
        lines += [f"- [ ] {did}: {as_text(text)}" for did, text in followups]

    lines += ["", "## People", ""]
    lines += ["| Person | Task | Branch | Updated | Next step | Blocked on |"]
    lines += ["| --- | --- | --- | --- | --- | --- |"]
    for s in sessions:
        lines.append(
            f"| {cell(s.get('person'))} | {cell(s.get('task'))} | {cell(s.get('branch'))} "
            f"| {cell(s.get('updated'))} | {cell(s.get('_next'))} | {cell(s.get('_blocked'))} |"
        )
    if src.ref:
        lines += ["", "Session files show merged work only. Live status is in the issue comments."]

    if with_issues:
        issues, err = load_issues()
        lines += ["", "## Open issues", ""]
        if err:
            lines.append(f"Not available: {err}.")
        else:
            lines += ["| # | Title | Assignee | Milestone |", "| --- | --- | --- | --- |"]
            for i in issues:
                logins = [a.get("login", "") for a in i.get("assignees") or []]
                who = ", ".join(logins) or "unassigned"
                ms = (i.get("milestone") or {}).get("title")
                title = cell(i.get("title"))
                lines.append(f"| {i.get('number')} | {title} | {cell(who)} | {cell(ms)} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--ref", help="read files from this git ref, e.g. origin/main")
    ap.add_argument("--issues", action="store_true", help="include open GitHub issues (needs gh)")
    ap.add_argument("--out", default=str(ROOT / "STATE.md"), help="output path (default: STATE.md)")
    args = ap.parse_args()
    text = render(Source(args.ref), args.issues)
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
