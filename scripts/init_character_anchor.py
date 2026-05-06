#!/usr/bin/env python3
"""Initialize a character anchor library."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "1.0.0"


DIRECTORIES = [
    "references/raw",
    "references/golden",
    "references/rejected",
    "anchor-library",
    "prompt-library",
    "outputs/approved/prompt-cards",
    "outputs/product-gallery",
    "outputs/candidates",
    "outputs/failed",
    "outputs/blocked",
    "feedback",
    "adapters",
    "quality",
    "training-package",
]


ANCHOR_FILES = {
    "anchor-card.md": """# {display_name} Anchor Card

## Identity Summary

## Age Presentation

## Face Anchors

## Hair Anchors

## Body And Proportion Anchors

## Distinctive Details

## Temperament And Expression Range

## Visual Style Baseline

## Allowed Variations

## Forbidden Changes

## Golden References

## Common Drift Risks

## Current Best Reusable Prompt
""",
    "anchor-library/identity.md": "# Identity\n\n",
    "anchor-library/face.md": "# Face\n\n",
    "anchor-library/body.md": "# Body\n\n",
    "anchor-library/presence.md": "# Presence\n\n",
    "anchor-library/motion.md": "# Motion\n\n",
    "anchor-library/wardrobe-logic.md": "# Wardrobe Logic\n\n",
    "anchor-library/voice-and-dialogue.md": "# Voice And Dialogue\n\n",
    "anchor-library/style.md": "# Style\n\n",
    "anchor-library/temperament.md": "# Temperament\n\n",
    "anchor-library/invariants.md": "# Invariants\n\n",
    "anchor-library/allowed-variations.md": "# Allowed Variations\n\n",
    "anchor-library/negative-rules.md": "# Negative Rules\n\n",
    "quality/review-rubric.md": "# Review Rubric\n\n",
}


JSON_FILES = {
    "consent.json": {
        "schema_version": SCHEMA_VERSION,
        "source_type": "fictional_or_user_authorized",
        "user_asserted_authorized": None,
        "allowed_uses": [],
        "disallowed_uses": [],
        "public_release_allowed": None,
        "notes": [],
    },
    "references/index.json": {
        "schema_version": SCHEMA_VERSION,
        "items": [],
    },
    "feedback/correction-rules.json": {
        "schema_version": SCHEMA_VERSION,
        "identity_corrections": [],
        "style_corrections": [],
        "composition_corrections": [],
        "technical_corrections": [],
        "prompt_corrections": [],
    },
    "adapters/model-providers.json": {
        "schema_version": SCHEMA_VERSION,
        "default_llm": None,
        "default_vision_reviewer": None,
        "default_image_generator": None,
        "providers": [],
        "privacy_mode": {
            "prefer_local_for_biometrics": True,
            "allow_remote_generation": None,
        },
    },
    "training-package/manifest.json": {
        "schema_version": SCHEMA_VERSION,
        "anchor_version": "0.1.0",
        "target_adapter_type": None,
        "included_images": [],
        "excluded_images": [],
        "captions": [],
        "safety_exclusions": [],
        "quality_notes": [],
    },
}


JSONL_FILES = [
    "prompt-library/raw-prompts.jsonl",
    "prompt-library/compiled-prompts.jsonl",
    "prompt-library/optimized-recipes.jsonl",
    "outputs/approved/index.jsonl",
    "outputs/product-gallery/index.jsonl",
    "outputs/candidates/index.jsonl",
    "outputs/failed/index.jsonl",
    "outputs/blocked/index.jsonl",
    "feedback/feedback.jsonl",
    "quality/scores.jsonl",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def write_json(path: Path, data: dict, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def write_text(path: Path, text: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a character anchor library.")
    parser.add_argument("--root", required=True, help="Workspace root or characters directory.")
    parser.add_argument("--character-id", required=True, help="Stable lowercase id, e.g. example-character.")
    parser.add_argument("--display-name", required=True, help="Human-readable character name.")
    parser.add_argument("--anchor-version", default="0.1.0", help="Initial anchor version.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing template files.")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", args.character_id):
        parser.error("--character-id must be lowercase letters, digits, and hyphens, up to 63 chars")

    root = Path(args.root).expanduser().resolve()
    character_root = root / args.character_id if root.name.lower() == "characters" else root / "characters" / args.character_id

    character_root.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        (character_root / directory).mkdir(parents=True, exist_ok=True)

    created_at = now_iso()
    profile = {
        "schema_version": SCHEMA_VERSION,
        "character_id": args.character_id,
        "display_name": args.display_name,
        "anchor_version": args.anchor_version,
        "created_at": created_at,
        "updated_at": created_at,
        "status": "draft",
        "authorization_status": "unknown",
        "age_policy": {
            "declared_adult": None,
            "age_uncertain": True,
            "minor_safe_mode": True,
        },
        "notes": [],
    }
    write_json(character_root / "profile.json", profile, args.overwrite)

    json_files = dict(JSON_FILES)
    json_files["training-package/manifest.json"] = {
        **json_files["training-package/manifest.json"],
        "anchor_version": args.anchor_version,
    }
    for relative_path, payload in json_files.items():
        write_json(character_root / relative_path, payload, args.overwrite)

    for relative_path, text in ANCHOR_FILES.items():
        write_text(character_root / relative_path, text.format(display_name=args.display_name), args.overwrite)

    for relative_path in JSONL_FILES:
        target = character_root / relative_path
        if not target.exists() or args.overwrite:
            write_text(target, "", args.overwrite)

    print(character_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
