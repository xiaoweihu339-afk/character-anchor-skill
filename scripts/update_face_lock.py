#!/usr/bin/env python3
"""Create or update a structured face geometry lock for golden candidate generation."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "1.0.0"
GEOMETRY_FIELDS = [
    "face_length_to_width",
    "forehead_height_ratio",
    "eye_spacing_ratio",
    "eye_width_ratio",
    "brow_to_eye_distance_ratio",
    "nose_length_ratio",
    "nose_width_ratio",
    "mouth_width_ratio",
    "upper_lip_to_lower_lip_ratio",
    "jaw_width_ratio",
    "chin_length_ratio",
    "cheekbone_width_ratio",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def default_face_lock() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "draft",
        "measurement_unit": "relative_ratio",
        "source_references": [],
        "face_geometry": {field: None for field in GEOMETRY_FIELDS},
        "qualitative_locks": [],
        "tuning_notes": [],
        "updated_at": None,
    }


def load_face_lock(path: Path) -> dict:
    if not path.exists():
        return default_face_lock()
    return json.loads(path.read_text(encoding="utf-8"))


def parse_measurements(values: list[str]) -> dict[str, float]:
    measurements: dict[str, float] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"measurement must be key=value: {value}")
        key, raw_number = value.split("=", 1)
        key = key.strip()
        if key not in GEOMETRY_FIELDS:
            allowed = ", ".join(GEOMETRY_FIELDS)
            raise ValueError(f"unknown measurement '{key}'. Allowed fields: {allowed}")
        measurements[key] = float(raw_number.strip())
    return measurements


def append_values(existing: list, values: list[str]) -> list:
    result = list(existing)
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Update quality/face-lock/face-lock.json.")
    parser.add_argument("character_root", help="Path to characters/<character-id>.")
    parser.add_argument("--measurement", action="append", default=[], help="Face geometry ratio as key=value. Can be repeated.")
    parser.add_argument("--source-reference", action="append", default=[], help="Reference id/path used to estimate the face lock.")
    parser.add_argument("--qualitative-lock", action="append", default=[], help="Text lock such as 'moderate eye spacing'.")
    parser.add_argument("--tuning-note", action="append", default=[], help="Feedback note such as 'jaw should be less sharp'.")
    parser.add_argument("--status", choices=["draft", "estimated", "reviewed", "locked"], default=None)
    parser.add_argument("--dry-run", action="store_true", help="Print without writing.")
    args = parser.parse_args()

    character_root = Path(args.character_root).expanduser().resolve()
    if not character_root.is_dir():
        parser.error(f"character_root is not a directory: {character_root}")

    try:
        measurements = parse_measurements(args.measurement)
    except ValueError as exc:
        parser.error(str(exc))

    path = character_root / "quality" / "face-lock" / "face-lock.json"
    face_lock = load_face_lock(path)
    face_lock.setdefault("face_geometry", {})
    for field in GEOMETRY_FIELDS:
        face_lock["face_geometry"].setdefault(field, None)
    face_lock["face_geometry"].update(measurements)
    face_lock["source_references"] = append_values(face_lock.get("source_references", []), args.source_reference)
    face_lock["qualitative_locks"] = append_values(face_lock.get("qualitative_locks", []), args.qualitative_lock)
    face_lock["tuning_notes"] = append_values(face_lock.get("tuning_notes", []), args.tuning_note)
    if args.status:
        face_lock["status"] = args.status
    face_lock["updated_at"] = now_iso()

    if not args.dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(face_lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(face_lock, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
