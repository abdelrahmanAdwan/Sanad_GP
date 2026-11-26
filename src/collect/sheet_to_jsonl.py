#!/usr/bin/env python3
"""Convert a video sheet (Drive file 12 format, exported as CSV) to data/videos/<name>.jsonl.

The sheet uses Arabic column names and drop-down values. This script maps them to the
enums in data/schema/video.schema.json, validates every record, and checks the
selection rule for the sample:

  --rules pilot   the 20-video pilot (docs/collection-protocol.md section 5, Drive file 13)
  --rules topic   one topic of about 80 videos (collection protocol section 3, D017 proposed)

Columns that the video schema does not have (audio downloaded, Arabic captions, notes)
are written to a separate CSV with --extras-out, so nothing in the sheet is lost.

Examples:
  python src/collect/sheet_to_jsonl.py sheet12.csv --collected-at 2026-11-26 \
      --rules pilot --out data/videos/pilot.jsonl --extras-out data/reports/pilot_sheet_extras.csv
  # check only, write nothing:
  python src/collect/sheet_to_jsonl.py sheet12.csv --collected-at 2026-11-26 --rules pilot

Exit code 1 if any row cannot be converted or any record fails the schema.
Selection-rule problems are printed as warnings and do not change the exit code.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover
    sys.exit("jsonschema is required: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "data" / "schema" / "video.schema.json"

# Sheet column headers (Drive file 12, sheet "فيديوهات التجربة").
COL = {
    "row": "#",
    "picked_by": "من اختاره",
    "url": "رابط الفيديو",
    "topic": "المجال",
    "format": "الشكل",
    "start": "بداية المقطع (ثانية)",
    "end": "نهاية المقطع (ثانية)",
    "duration": "المدة الكاملة (ثانية)",
    "channel": "اسم القناة",
    "publisher": "نوع الناشر",
    "dialect": "اللهجة",
    "query": "كلمة البحث اللي لقيته فيها",
    "audible": "الكلام عربي ومسموع؟",
    "audio_ok": "تنزّل الصوت؟",
    "ar_auto": "ترجمة عربية آلية؟",
    "ar_manual": "ترجمة عربية من صاحب القناة؟",
    "notes": "ملاحظات",
    # Phase-2 screening sheet only (data/templates/topic_screen_accepted.csv):
    "band": "شريحة المشاهدات",
    "screener": "مين فحصه",
}

# Sheet value -> schema enum. Matching is on the start of the cell, after trimming.
TOPIC = [
    ("السكر", "diabetes"),
    ("الأعشاب", "herbal_alternative"),
    ("الاعشاب", "herbal_alternative"),
    ("الطب البديل", "herbal_alternative"),
    ("السرطان", "cancer"),
    ("التغذية", "nutrition_diets"),
    ("الحميات", "nutrition_diets"),
    ("الضغط", "hypertension"),
    ("ضغط الدم", "hypertension"),
]
FORMAT = [("short", "short"), ("شورت", "short"), ("مقطع", "clip"), ("clip", "clip")]
PUBLISHER = [
    ("طبيب", "doctor"),
    ("جهة رسمية", "official_body"),
    ("غير مختص", "non_specialist"),
    ("غير معروف", "unknown"),
]
DIALECT = [
    ("فصحى", "msa"),
    ("شامي", "levantine"),
    ("مصري", "egyptian"),
    ("خليجي", "gulf"),
    ("عراقي", "iraqi"),
    ("مغاربي", "maghrebi"),
    ("مغربي", "maghrebi"),
    ("سوداني", "sudanese"),
    ("مختلط", "mixed"),
    ("أخرى", "other"),
    ("غير ذلك", "other"),
    ("غير معروف", "unknown"),
]
YES = {"نعم", "yes", "1", "true"}

ID_RE = re.compile(r"(?:v=|/shorts/|youtu\.be/|/embed/|/live/)([A-Za-z0-9_-]{11})")
DOCTOR_HINT = re.compile(r"(\bد\.|\bدكتور|\bالدكتور|\bDr\b|\bDr\.|طبيب)", re.IGNORECASE)

# Drive file 07 video: annotators who saw Claude's labels on it must tell the
# guidelines owner if it is in the pilot (Drive file 13, task 4).
FILE07_VIDEO = "T6qEGgUKS4M"


def lookup(table: list[tuple[str, str]], value: str) -> str | None:
    v = value.strip().lower()
    for prefix, enum in table:
        if v.startswith(prefix.lower()):
            return enum
    return None


def video_id(url: str) -> str | None:
    m = ID_RE.search(url.strip())
    return m.group(1) if m else None


def number(value: str) -> float | int | None:
    v = value.strip()
    if not v:
        return None
    x = float(v)
    return int(x) if x.is_integer() else x


def convert(row: dict[str, str], collected_at: str) -> tuple[dict | None, list[str]]:
    """Return (record, errors) for one sheet row."""
    errors: list[str] = []
    get = lambda k: (row.get(COL[k]) or "").strip()  # noqa: E731

    vid = video_id(get("url"))
    if not vid:
        return None, [f"no YouTube ID in link {get('url')!r}"]

    rec: dict = {"video_id": vid}
    for key, table, field in (
        ("topic", TOPIC, "topic"),
        ("format", FORMAT, "format"),
        ("publisher", PUBLISHER, "publisher_type"),
        ("dialect", DIALECT, "dialect"),
    ):
        raw = get(key)
        enum = lookup(table, raw)
        if enum is None:
            errors.append(f"{COL[key]}: value {raw!r} is empty or unknown")
        else:
            rec[field] = enum

    try:
        start, end, duration = number(get("start")), number(get("end")), number(get("duration"))
    except ValueError as e:
        return None, [f"a number column is not a number ({e})"]
    if rec.get("format") == "clip":
        if start is None or end is None:
            errors.append("clip without start and end seconds")
        else:
            rec["clip_start_s"], rec["clip_end_s"] = start, end
    if duration is not None:
        rec["duration_s"] = duration
    if get("query"):
        rec["search_query"] = get("query")
    rec["collected_at"] = collected_at
    rec["screened"] = True
    if get("audible") and get("audible").lower() not in YES:
        rec["screen_note"] = "rejected: speech is not clear Arabic"
    return rec, errors


def extras(row: dict[str, str], vid: str) -> dict[str, str]:
    get = lambda k: (row.get(COL[k]) or "").strip()  # noqa: E731
    return {
        "video_id": vid,
        "sheet_row": get("row"),
        "picked_by": get("picked_by"),
        "channel_name": get("channel"),
        "audible_arabic": get("audible"),
        "audio_downloaded": get("audio_ok"),
        "ar_auto_captions": get("ar_auto"),
        "ar_manual_captions": get("ar_manual"),
        "notes": get("notes"),
        "view_band": get("band"),
        "screener": get("screener"),
    }


def check_rules(rows: list[tuple[dict, dict]], rules: str) -> list[str]:
    """Selection-rule warnings. rows = [(record, sheet_extras)]."""
    w: list[str] = []
    recs = [r for r, _ in rows]
    n = len(recs)
    fmt = Counter(r.get("format") for r in recs)
    pub = Counter(r.get("publisher_type") for r in recs)
    dia = Counter(r.get("dialect") for r in recs)
    top = Counter(r.get("topic") for r in recs)
    chan = Counter(x["channel_name"].strip().lower() for _, x in rows if x["channel_name"].strip())

    print(f"\n{n} videos | format {dict(fmt)} | topic {dict(top)}")
    print(f"publisher {dict(pub)} | dialect {dict(dia)}")

    ids = Counter(r["video_id"] for r in recs)
    w += [f"video {v} appears {c} times" for v, c in ids.items() if c > 1]
    if FILE07_VIDEO in ids:
        w.append(
            f"{FILE07_VIDEO} is the Drive file 07 video: annotators who saw Claude's "
            "labels on it must tell the guidelines owner"
        )

    for r, x in rows:
        tag = f"row {x['sheet_row'] or '?'} ({r['video_id']})"
        d = r.get("duration_s")
        if r.get("format") == "short" and d is not None and d > 60:
            w.append(f"{tag}: Short but {d} s long (Shorts are 60 s or less)")
        if r.get("format") == "clip":
            s, e = r.get("clip_start_s"), r.get("clip_end_s")
            if s is not None and e is not None:
                if not 120 <= e - s <= 180:
                    w.append(f"{tag}: excerpt is {e - s} s; the rule is 2-3 minutes (120-180 s)")
                if d is not None and e > d + 1:
                    w.append(f"{tag}: excerpt ends at {e} s, after the video ends ({d} s)")
            if d is not None and not 120 <= d <= 900:
                w.append(f"{tag}: source video is {d} s; the rule is 2-15 minutes")
        if "search_query" not in r:
            w.append(f"{tag}: search query is empty (needed to describe the collection)")
        if r.get("publisher_type") == "unknown" and DOCTOR_HINT.search(x["channel_name"]):
            w.append(
                f"{tag}: publisher is 'unknown' but the channel name suggests a doctor; "
                "a person should check"
            )

    over = {c: k for c, k in chan.items() if k > 3}
    if over:
        w.append(f"channels with more than 3 videos: {over}")

    if rules == "pilot":
        if n != 20:
            w.append(f"pilot has {n} videos, expected 20")
        if abs(fmt["short"] - fmt["clip"]) > 2:
            w.append(
                f"pilot should be about half Shorts: {fmt['short']} Shorts, {fmt['clip']} clips"
            )
        others = {t: k for t, k in top.items() if t != "diabetes"}
        if top["diabetes"] != 14 or len(others) != 3 or any(k != 2 for k in others.values()):
            w.append(
                f"pilot design is 14 diabetes + 2 from each of 3 other topics; got {dict(top)}"
            )
        if pub["non_specialist"] == 0:
            w.append("no non-specialist publisher in the pilot")
        if pub["official_body"] == 0:
            w.append("no official body in the pilot (the rule says 'if you find one')")
    elif rules == "topic":
        if abs(fmt["short"] - fmt["clip"]) > max(4, n // 10):
            w.append(
                f"topic should be about half Shorts: {fmt['short']} Shorts, {fmt['clip']} clips"
            )
        if pub["doctor"] + pub["official_body"] < 15:
            w.append(
                "needs at least 15 doctor or official videos, "
                f"has {pub['doctor'] + pub['official_body']}"
            )
        if pub["non_specialist"] < 25:
            w.append(f"needs at least 25 non-specialist videos, has {pub['non_specialist']}")
        if len(top) > 1:
            w.append(f"a topic file should hold one topic; got {dict(top)}")
        bands = Counter(x["view_band"] for _, x in rows if x["view_band"])
        if bands:
            top_band = sum(k for b, k in bands.items() if b.startswith("أعلى"))
            if abs(top_band - n / 3) > max(3, n // 10):
                w.append(f"about a third should come from the most-viewed band: {top_band} of {n}")
        else:
            w.append("no view band filled; cannot check the 'one third most viewed' rule")
    if dia["unknown"] > n // 4:
        w.append(f"{dia['unknown']} of {n} videos have dialect 'unknown'")
    return w


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("csv", type=Path, help="sheet exported as CSV (File > Download > CSV)")
    ap.add_argument(
        "--collected-at", required=True, help="date the videos were selected, YYYY-MM-DD"
    )
    ap.add_argument("--rules", choices=["pilot", "topic", "none"], default="none")
    ap.add_argument(
        "--channel-ids",
        type=Path,
        help="CSV with video_id,channel_id (for example data/reports/pilot_channel_ids.csv)",
    )
    ap.add_argument("--out", type=Path, help="write records here (.jsonl); omit to check only")
    ap.add_argument(
        "--extras-out", type=Path, help="write sheet columns the schema lacks here (.csv)"
    )
    args = ap.parse_args(argv)

    validator = Draft202012Validator(
        json.loads(SCHEMA.read_text(encoding="utf-8")), format_checker=FormatChecker()
    )
    with args.csv.open(encoding="utf-8-sig", newline="") as f:
        sheet = list(csv.DictReader(f))
    missing = [
        c for c in (COL["url"], COL["topic"], COL["format"]) if c not in (sheet[0] if sheet else {})
    ]
    if missing:
        sys.exit(f"columns not found in {args.csv}: {missing}")

    channel_ids: dict[str, str] = {}
    if args.channel_ids:
        with args.channel_ids.open(encoding="utf-8-sig", newline="") as f:
            channel_ids = {r["video_id"]: r["channel_id"] for r in csv.DictReader(f)}

    good: list[tuple[dict, dict]] = []
    errors = 0
    empty = []
    for i, row in enumerate(sheet, start=2):
        label = f"row {row.get(COL['row']) or i}"
        if not (row.get(COL["url"]) or "").strip():
            empty.append(row.get(COL["row"]) or str(i))
            continue
        rec, errs = convert(row, args.collected_at)
        if rec is not None and rec["video_id"] in channel_ids:
            rec["channel_id"] = channel_ids[rec["video_id"]]
        if rec is not None:
            errs += [
                f"schema: {'/'.join(map(str, e.path)) or '(record)'}: {e.message}"
                for e in validator.iter_errors(rec)
            ]
        for e in errs:
            print(f"ERROR {label}: {e}")
        errors += len(errs)
        if rec is not None and not errs:
            good.append((rec, extras(row, rec["video_id"])))

    if empty:
        print(f"skipped {len(empty)} rows with no link: {', '.join(empty)}")
    warnings = check_rules(good, args.rules) if args.rules != "none" else []
    for w in warnings:
        print(f"WARN {w}")

    if args.out:
        if errors:
            print(f"not writing {args.out}: fix the {errors} error(s) first")
        else:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with args.out.open("w", encoding="utf-8") as f:
                for rec, _ in good:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"wrote {len(good)} records to {args.out}")
    if args.extras_out and good and not errors:
        args.extras_out.parent.mkdir(parents=True, exist_ok=True)
        with args.extras_out.open("w", encoding="utf-8", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(good[0][1]))
            wr.writeheader()
            wr.writerows(x for _, x in good)
        print(f"wrote sheet extras to {args.extras_out}")
    print(f"{len(good)} converted, {errors} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
