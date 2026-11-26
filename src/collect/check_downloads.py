
import argparse
import csv
import json
from pathlib import Path

IDS = [
    "PRcMSX_L3K4", "_vTsmMjUyXg", "tscgXaK9G2o",
    "zmjn65nyd0I", "h9K4pDQL09s", "BgX-g4SnBSE",
    "xOSIj31IzXs", "k68eBsFtpWA", "lLkmO586GgQ",
    "yEfVNUvgvFE", "Syw3DqawJ74", "eRkOF47_JWM",
    "Kes3P0wvAv4", "eaKfK7xJ18A"
]

FIELDS = [
    "video_id", "audio_file", "ar_manual_tracks",
    "ar_auto_tracks", "caption_file", "duration_s",
    "channel", "language", "title"
]


def arabic_tracks(metadata, field):
    tracks = metadata.get(field) or {}
    return sorted(
        key for key in tracks
        if key == "ar" or key.startswith("ar-")
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    output = Path(args.output)

    if output.exists():
        raise SystemExit(
            f"Output already exists; refusing to overwrite: {output}"
        )

    if not data_dir.is_dir():
        raise SystemExit(f"Data directory missing: {data_dir}")

    rows = []

    for video_id in IDS:
        metadata_path = (
            data_dir / "pilot_test" / f"{video_id}.info.json"
        )

        if not metadata_path.exists():
            raise SystemExit(
                f"Missing metadata: {metadata_path}"
            )

        metadata = json.loads(
            metadata_path.read_text(encoding="utf-8")
        )

        audio_candidates = [
            data_dir / "pilot_test" / f"{video_id}.m4a",
            data_dir / "audio" / "pilot14" / f"{video_id}.webm",
        ]

        audio = next(
            (p for p in audio_candidates if p.is_file()),
            None
        )

        caption_files = sorted(
            p for p in data_dir.rglob("*")
            if p.is_file()
            and p.name.startswith(video_id + ".ar")
            and p.suffix.lower() in {".json3", ".vtt"}
        )

        rows.append({
            "video_id": video_id,
            "audio_file": str(audio) if audio else "",
            "ar_manual_tracks": "|".join(
                arabic_tracks(metadata, "subtitles")
            ),
            "ar_auto_tracks": "|".join(
                arabic_tracks(metadata, "automatic_captions")
            ),
            "caption_file": "|".join(
                str(p) for p in caption_files
            ),
            "duration_s": metadata.get("duration", ""),
            "channel": metadata.get("channel", ""),
            "language": metadata.get("language", ""),
            "title": metadata.get("title", ""),
        })

    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"PASS: {len(rows)} videos checked")
    print(f"Audio found: {sum(bool(r['audio_file']) for r in rows)}")
    print(f"Metadata found: {len(rows)}")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
