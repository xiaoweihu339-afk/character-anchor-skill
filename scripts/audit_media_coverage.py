#!/usr/bin/env python3
"""Create an honest media coverage inventory for a raw character media folder."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "1.0.0"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".heic", ".heif"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    return "unsupported"


def relative_or_absolute(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def build_manifest(source_root: Path, max_inventory_items: int) -> dict:
    files = [path for path in source_root.rglob("*") if path.is_file()]
    files.sort(key=lambda item: item.as_posix().lower())

    counts = {"image": 0, "video": 0, "unsupported": 0}
    inventory = []
    for path in files:
        media_type = classify(path)
        counts[media_type] += 1
        if len(inventory) < max_inventory_items:
            inventory.append(
                {
                    "path": relative_or_absolute(path, source_root),
                    "media_type": media_type,
                    "size_bytes": path.stat().st_size,
                }
            )

    omitted = max(0, len(files) - len(inventory))
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "created_at": now_iso(),
        "source_root": str(source_root),
        "review_stage": "inventory_only",
        "coverage_status": "inventory_only_not_visual_review",
        "total_files": len(files),
        "total_images": counts["image"],
        "total_videos": counts["video"],
        "total_unsupported_files": counts["unsupported"],
        "processed_images": 0,
        "processed_videos": 0,
        "sampled_images": 0,
        "sampled_videos": 0,
        "inspected_video_frames": 0,
        "coverage_honesty_note": (
            "This manifest counts files only. It does not mean the images, videos, "
            "faces, or frames have been visually reviewed."
        ),
        "recommended_next_step": (
            "Run hard-defect screening or build a review gallery before selecting "
            "usable references or generating golden candidates."
        ),
        "inventory_preview": inventory,
        "inventory_preview_omitted_files": omitted,
    }
    return manifest


def write_manifest(character_root: Path, manifest: dict) -> Path:
    output_dir = character_root / "quality" / "coverage"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "coverage-manifest.json"
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit raw media coverage without pretending to review every image or frame.")
    parser.add_argument("source_root", help="Folder containing raw images/videos to inventory.")
    parser.add_argument("--character-root", help="Optional characters/<character-id> root for --write.")
    parser.add_argument("--write", action="store_true", help="Write quality/coverage/coverage-manifest.json under --character-root.")
    parser.add_argument("--max-inventory-items", type=int, default=500, help="Maximum file entries to include in the manifest preview.")
    args = parser.parse_args()

    source_root = Path(args.source_root).expanduser().resolve()
    if not source_root.is_dir():
        parser.error(f"source_root is not a directory: {source_root}")

    manifest = build_manifest(source_root, args.max_inventory_items)
    if args.write:
        if not args.character_root:
            parser.error("--write requires --character-root")
        output_path = write_manifest(Path(args.character_root).expanduser().resolve(), manifest)
        manifest["written_to"] = str(output_path)

    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
