#!/usr/bin/env python3
"""Create a golden-candidate generation request payload for an external image workflow."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "1.0.0"
DEFAULT_COVERAGE_TARGETS = [
    "front_face",
    "three_quarter_face",
    "ninety_degree_profile",
    "back_view",
    "upper_body",
    "full_body",
    "long_shot_silhouette",
    "motion_reference",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_optional(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip()


def load_reference_index(character_root: Path) -> dict:
    index_path = character_root / "references" / "index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"Missing references/index.json in {character_root}")
    return load_json(index_path)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_reference_images(character_root: Path, reference_images: list[str]) -> None:
    if not reference_images:
        return

    reference_index = load_reference_index(character_root)
    golden_items = [
        item
        for item in reference_index.get("items", [])
        if isinstance(item, dict) and item.get("role") == "golden"
    ]
    golden_ids = {item.get("id") for item in golden_items}
    golden_paths = {item.get("path") for item in golden_items}
    golden_root = (character_root / "references" / "golden").resolve()

    invalid: list[str] = []
    for reference in reference_images:
        if reference in golden_ids or reference in golden_paths:
            continue

        candidate_path = (character_root / reference).resolve()
        if candidate_path.is_file() and is_relative_to(candidate_path, golden_root):
            continue

        invalid.append(reference)

    if invalid:
        invalid_list = ", ".join(invalid)
        raise ValueError(
            "Reference images must be approved golden reference ids, indexed golden paths, "
            f"or existing files under references/golden/: {invalid_list}"
        )


def build_payload(character_root: Path, request: str, provider: str, reference_images: list[str], coverage_targets: list[str]) -> dict:
    profile = load_json(character_root / "profile.json")
    anchor_card = read_optional(character_root / "anchor-card.md")
    face_anchor = read_optional(character_root / "anchor-library" / "face.md")
    body_anchor = read_optional(character_root / "anchor-library" / "body.md")
    negative_rules = read_optional(character_root / "anchor-library" / "negative-rules.md")
    face_lock_path = character_root / "quality" / "face-lock" / "face-lock.json"
    face_lock = load_json(face_lock_path) if face_lock_path.is_file() else None

    request_id = "golden_request_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return {
        "schema_version": SCHEMA_VERSION,
        "request_id": request_id,
        "created_at": now_iso(),
        "character_id": profile.get("character_id", character_root.name),
        "display_name": profile.get("display_name", character_root.name),
        "anchor_version": profile.get("anchor_version", "unknown"),
        "provider": provider,
        "status": "request_payload_only",
        "honesty_note": (
            "This script does not generate images by itself. It creates a structured "
            "request payload for an external identity-preserving image workflow."
        ),
        "raw_request": request,
        "reference_images": reference_images,
        "coverage_targets": coverage_targets,
        "identity_inputs": {
            "anchor_card": anchor_card,
            "face_anchor": face_anchor,
            "face_lock": face_lock,
            "body_anchor": body_anchor,
            "negative_rules": negative_rules,
        },
        "quality_gate_before_promotion": [
            "authorization_confirmed",
            "safe_for_intended_use",
            "target_identity_match",
            "face_similarity_review",
            "user_likeness_review",
            "coverage_target_label_confirmed",
        ],
        "suggested_output_route": "outputs/candidates/",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an external golden-candidate generation request payload.")
    parser.add_argument("character_root", help="Path to characters/<character-id>.")
    parser.add_argument("--request", required=True, help="Generation goal for the golden candidate batch.")
    parser.add_argument("--provider", default="provider-neutral", help="External workflow/provider label.")
    parser.add_argument("--reference-image", action="append", default=[], help="Reference id/path used by the external workflow.")
    parser.add_argument(
        "--allow-unvalidated-reference",
        action="store_true",
        help="Allow non-golden references in the payload. Use only for private experiments.",
    )
    parser.add_argument("--coverage-target", action="append", default=[], help="Coverage target to request. Can be repeated.")
    parser.add_argument("--output", help="Optional output JSON path.")
    parser.add_argument("--write", action="store_true", help="Write under outputs/candidates/golden-generation-requests/.")
    args = parser.parse_args()

    character_root = Path(args.character_root).expanduser().resolve()
    if not character_root.is_dir():
        parser.error(f"character_root is not a directory: {character_root}")

    coverage_targets = args.coverage_target or DEFAULT_COVERAGE_TARGETS
    try:
        if not args.allow_unvalidated_reference:
            validate_reference_images(character_root, args.reference_image)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    payload = build_payload(character_root, args.request, args.provider, args.reference_image, coverage_targets)
    if args.allow_unvalidated_reference:
        payload["reference_validation"] = "skipped_by_user_for_private_experiment"
    else:
        payload["reference_validation"] = "approved_golden_references_only"

    output_path: Path | None = None
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    elif args.write:
        output_path = character_root / "outputs" / "candidates" / "golden-generation-requests" / f"{payload['request_id']}.json"

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        payload["written_to"] = str(output_path)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
