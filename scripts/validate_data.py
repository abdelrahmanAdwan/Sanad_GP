#!/usr/bin/env python3
"""Validate data files against the schemas in data/schema/.

  data/videos/*.jsonl        -> video.schema.json
  data/segments/*.jsonl      -> segment.schema.json
  data/annotations/*/*.jsonl -> annotation.schema.json

Usage: python scripts/validate_data.py [paths...]   (default: all data files)
Exit code 1 if any record is invalid.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover
    sys.exit("jsonschema is required: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
RULES = [
    ("data/videos/*.jsonl", "video"),
    ("data/segments/*.jsonl", "segment"),
    ("data/annotations/*/*.jsonl", "annotation"),
]


def validator(name: str) -> Draft202012Validator:
    path = ROOT / "data" / "schema" / f"{name}.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    return Draft202012Validator(schema, format_checker=FormatChecker())


def schema_for(path: Path) -> str | None:
    rel = path.resolve().relative_to(ROOT)
    for pattern, name in RULES:
        if rel.match(pattern):
            return name
    return None


def main(argv: list[str]) -> int:
    default = [p for pattern, _ in RULES for p in sorted(ROOT.glob(pattern))]
    files = [Path(a) for a in argv] or default
    validators: dict[str, Draft202012Validator] = {}
    errors = 0
    for path in files:
        name = schema_for(path)
        if name is None:
            print(f"skip {path}: no schema for this location")
            continue
        v = validators.setdefault(name, validator(name))
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"{path}:{n}: invalid JSON ({e.msg})")
                errors += 1
                continue
            for err in v.iter_errors(record):
                where = "/".join(map(str, err.path)) or "(record)"
                print(f"{path}:{n}: {where}: {err.message}")
                errors += 1
    print(f"{len(files)} file(s) checked, {errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
