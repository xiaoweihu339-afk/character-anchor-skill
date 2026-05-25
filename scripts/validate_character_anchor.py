#!/usr/bin/env python3
"""Validate the structure and JSON files of a character anchor library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCHEMA_VERSION = "1.1.0"
GOLDEN_REQUIRED_TYPES = {
    "front-closeup",
    "left-closeup",
    "right-closeup",
    "full-body-face-visible",
}
VALID_WIZARD_STATES = {
    "profile_started",
    "basic_identity_complete",
    "raw_reference_added",
    "golden_incomplete",
    "anchor_ready",
}


REQUIRED_DIRS = [
    "references/raw",
    "references/golden",
    "references/rejected",
    "anchor-library",
    "prompt-library",
    "outputs/approved",
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
    "outputs/candidates/index.jsonl",
    "outputs/failed/index.jsonl",
    "outputs/blocked/index.jsonl",
    "feedback/feedback.jsonl",
    "quality/scores.jsonl",
]


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - CLI validator should report all parse errors.
        errors.append(f"Invalid JSON: {path} ({exc})")
        return None


def validate_jsonl(path: Path, errors: list[str]) -> None:
    line_number = 0
    try:
        for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
            if not line.strip():
                continue
            json.loads(line)
    except Exception as exc:  # noqa: BLE001
        location = f"{path}:{line_number}" if line_number else str(path)
        errors.append(f"Invalid JSONL: {location} ({exc})")


def validate_profile(profile: dict, errors: list[str], warnings: list[str]) -> None:
    is_v11 = profile.get("schema_version") == SCHEMA_VERSION or profile.get("codex_image_model_first") is True
    if not is_v11:
        warnings.append(f"profile.json is pre-{SCHEMA_VERSION}; run init/update workflow to adopt the Codex guided fields")
        if profile.get("age_policy", {}).get("minor_safe_mode") is not True:
            warnings.append("profile.json age_policy.minor_safe_mode is not true")
        return

    if profile.get("schema_version") != SCHEMA_VERSION:
        warnings.append(f"profile.json schema_version is not {SCHEMA_VERSION}")

    if profile.get("codex_image_model_first") is not True:
        errors.append("profile.json codex_image_model_first must be true for v1.1")

    wizard_state = profile.get("wizard_state")
    if wizard_state not in VALID_WIZARD_STATES:
        errors.append(f"profile.json wizard_state must be one of {sorted(VALID_WIZARD_STATES)}")

    basic_identity = profile.get("basic_identity")
    if not isinstance(basic_identity, dict):
        errors.append("profile.json basic_identity must be an object")
    else:
        for field in [
            "gender_or_presentation",
            "age_presentation",
            "height",
            "body_type",
            "temperament",
            "visual_style",
        ]:
            if field not in basic_identity:
                errors.append(f"profile.json basic_identity missing field: {field}")

    required = set(profile.get("golden_required_types", []))
    if required != GOLDEN_REQUIRED_TYPES:
        errors.append("profile.json golden_required_types must contain all v1.1 required golden types")

    active = profile.get("active_golden_refs")
    if not isinstance(active, dict):
        errors.append("profile.json active_golden_refs must be an object")
        return

    missing_golden = [golden_type for golden_type in sorted(GOLDEN_REQUIRED_TYPES) if not active.get(golden_type)]
    if missing_golden:
        warnings.append(f"golden references incomplete: {', '.join(missing_golden)}")
        if wizard_state == "anchor_ready":
            errors.append("profile.json wizard_state cannot be anchor_ready while golden references are incomplete")

    if profile.get("age_policy", {}).get("minor_safe_mode") is not True:
        warnings.append("profile.json age_policy.minor_safe_mode is not true")


def validate_references_index(index: dict, warnings: list[str]) -> None:
    if index.get("schema_version") != SCHEMA_VERSION:
        warnings.append(f"references/index.json is pre-{SCHEMA_VERSION}; golden-role completeness was not enforced for this library")
        return

    approved_golden = set()
    for item in index.get("items", []):
        golden_type = item.get("golden_type")
        if golden_type and golden_type not in GOLDEN_REQUIRED_TYPES:
            warnings.append(f"references/index.json has unknown golden_type: {golden_type}")
        if golden_type in GOLDEN_REQUIRED_TYPES and item.get("user_approved") is True and item.get("active") is True:
            approved_golden.add(golden_type)

    missing = sorted(GOLDEN_REQUIRED_TYPES - approved_golden)
    if missing:
        warnings.append(f"references/index.json active approved golden refs incomplete: {', '.join(missing)}")


def validate_model_providers(providers: dict, errors: list[str]) -> None:
    if providers.get("schema_version") != SCHEMA_VERSION:
        return

    if providers.get("default_image_generator") != "codex-image":
        errors.append("adapters/model-providers.json default_image_generator must be codex-image")

    provider_records = providers.get("providers")
    if not isinstance(provider_records, list):
        errors.append("adapters/model-providers.json providers must be a list")
        return

    codex_provider = next((item for item in provider_records if item.get("provider_id") == "codex-image"), None)
    if not codex_provider:
        errors.append("adapters/model-providers.json missing codex-image provider")
    elif codex_provider.get("enabled") is not True:
        errors.append("adapters/model-providers.json codex-image provider must be enabled")


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
        validate_profile(parsed["profile.json"], errors, warnings)

    if "references/index.json" in parsed:
        validate_references_index(parsed["references/index.json"], warnings)

    if "adapters/model-providers.json" in parsed:
        validate_model_providers(parsed["adapters/model-providers.json"], errors)

    consent = parsed.get("consent.json", {})
    if consent.get("user_asserted_authorized") is not True:
        warnings.append("consent.json user_asserted_authorized is not true")

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
