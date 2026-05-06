#!/usr/bin/env python3
"""Validate the structure and JSON files of a character anchor library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_DIRS = [
    "references/raw",
    "references/golden",
    "references/rejected",
    "anchor-library",
    "prompt-library",
    "outputs/approved",
    "outputs/product-gallery",
    "outputs/candidates",
    "outputs/failed",
    "outputs/blocked",
    "feedback",
    "adapters",
    "quality",
    "training-package",
]


REQUIRED_FILES = [
    "anchor-card.md",
    "anchor-library/identity.md",
    "anchor-library/face.md",
    "anchor-library/body.md",
    "anchor-library/presence.md",
    "anchor-library/motion.md",
    "anchor-library/wardrobe-logic.md",
    "anchor-library/voice-and-dialogue.md",
    "anchor-library/style.md",
    "anchor-library/temperament.md",
    "anchor-library/invariants.md",
    "anchor-library/allowed-variations.md",
    "anchor-library/negative-rules.md",
    "quality/review-rubric.md",
]


REQUIRED_JSON = [
    "profile.json",
    "consent.json",
    "references/index.json",
    "feedback/correction-rules.json",
    "adapters/model-providers.json",
    "training-package/manifest.json",
]


REQUIRED_JSONL = [
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


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - CLI validator should report all parse errors.
        errors.append(f"Invalid JSON: {path} ({exc})")
        return None


def validate_jsonl(path: Path, errors: list[str]) -> None:
    line_number = 0
    try:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            json.loads(line)
    except Exception as exc:  # noqa: BLE001
        location = f"{path}:{line_number}" if line_number else str(path)
        errors.append(f"Invalid JSONL: {location} ({exc})")


def require_fields(relative: str, payload: dict, fields: list[str], errors: list[str]) -> None:
    for field in fields:
        if field not in payload:
            errors.append(f"Missing field in {relative}: {field}")


def require_list_field(relative: str, payload: dict, field: str, errors: list[str]) -> None:
    if field not in payload:
        errors.append(f"Missing field in {relative}: {field}")
    elif not isinstance(payload[field], list):
        errors.append(f"Field must be a list in {relative}: {field}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a character anchor library.")
    parser.add_argument("character_root", help="Path to characters/<character-id>.")
    args = parser.parse_args()

    root = Path(args.character_root).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        errors.append(f"Character root does not exist: {root}")
    elif not root.is_dir():
        errors.append(f"Character root is not a directory: {root}")

    for relative in REQUIRED_DIRS:
        if not (root / relative).is_dir():
            errors.append(f"Missing directory: {relative}")

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing file: {relative}")

    parsed: dict[str, dict] = {}
    for relative in REQUIRED_JSON:
        path = root / relative
        if not path.is_file():
            errors.append(f"Missing JSON file: {relative}")
            continue
        payload = load_json(path, errors)
        if payload is not None:
            parsed[relative] = payload

    for relative in REQUIRED_JSONL:
        path = root / relative
        if not path.is_file():
            errors.append(f"Missing JSONL file: {relative}")
            continue
        validate_jsonl(path, errors)

    if "profile.json" in parsed:
        profile = parsed["profile.json"]
        require_fields(
            "profile.json",
            profile,
            ["schema_version", "character_id", "display_name", "anchor_version", "created_at", "updated_at", "status"],
            errors,
        )
        if profile.get("age_policy", {}).get("minor_safe_mode") is not True:
            warnings.append("profile.json age_policy.minor_safe_mode is not true")

    if "consent.json" in parsed:
        consent = parsed["consent.json"]
        require_fields(
            "consent.json",
            consent,
            ["schema_version", "source_type", "user_asserted_authorized", "allowed_uses", "disallowed_uses", "public_release_allowed"],
            errors,
        )
        for field in ["allowed_uses", "disallowed_uses", "notes"]:
            require_list_field("consent.json", consent, field, errors)
        if consent.get("user_asserted_authorized") is not True:
            warnings.append("consent.json user_asserted_authorized is not true")

    if "references/index.json" in parsed:
        references_index = parsed["references/index.json"]
        require_fields("references/index.json", references_index, ["schema_version", "items"], errors)
        require_list_field("references/index.json", references_index, "items", errors)

    if "feedback/correction-rules.json" in parsed:
        correction_rules = parsed["feedback/correction-rules.json"]
        for field in [
            "identity_corrections",
            "style_corrections",
            "composition_corrections",
            "technical_corrections",
            "prompt_corrections",
        ]:
            require_list_field("feedback/correction-rules.json", correction_rules, field, errors)

    if "adapters/model-providers.json" in parsed:
        model_providers = parsed["adapters/model-providers.json"]
        require_fields("adapters/model-providers.json", model_providers, ["schema_version", "providers", "privacy_mode"], errors)
        require_list_field("adapters/model-providers.json", model_providers, "providers", errors)

    if "training-package/manifest.json" in parsed:
        training_manifest = parsed["training-package/manifest.json"]
        for field in ["included_images", "excluded_images", "captions", "safety_exclusions", "quality_notes"]:
            require_list_field("training-package/manifest.json", training_manifest, field, errors)

    if errors:
        print("INVALID")
        for error in errors:
            print(f"ERROR: {error}")
    else:
        print("VALID")

    for warning in warnings:
        print(f"WARNING: {warning}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
