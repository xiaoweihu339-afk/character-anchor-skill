#!/usr/bin/env python3
"""Compile a scene request through a character anchor library."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ANCHOR_PARTS = [
    ("identity", "anchor-library/identity.md"),
    ("face", "anchor-library/face.md"),
    ("body", "anchor-library/body.md"),
    ("presence", "anchor-library/presence.md"),
    ("motion", "anchor-library/motion.md"),
    ("wardrobe_logic", "anchor-library/wardrobe-logic.md"),
    ("temperament", "anchor-library/temperament.md"),
    ("style", "anchor-library/style.md"),
    ("invariants", "anchor-library/invariants.md"),
    ("allowed_variations", "anchor-library/allowed-variations.md"),
    ("negative_rules", "anchor-library/negative-rules.md"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def compact_markdown(text: str, exclude_sections: set[str] | None = None) -> str:
    exclude_sections = exclude_sections or set()
    lines = []
    skipped_heading_level: int | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            heading_level = len(line) - len(line.lstrip("#"))
            heading_text = line.lstrip("#").strip().lower()
            if skipped_heading_level is not None and heading_level <= skipped_heading_level:
                skipped_heading_level = None
            if heading_text in exclude_sections:
                skipped_heading_level = heading_level
            elif heading_level > 1:
                lines.append(f"{line.lstrip('#').strip()}:")
            continue
        if skipped_heading_level is not None:
            continue
        lines.append(line)
    return "\n".join(lines)


def load_profile(character_root: Path) -> dict:
    profile_path = character_root / "profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"Missing profile.json in {character_root}")
    return json.loads(profile_path.read_text(encoding="utf-8"))


def load_reference_index(character_root: Path) -> dict:
    index_path = character_root / "references" / "index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"Missing references/index.json in {character_root}")
    return json.loads(index_path.read_text(encoding="utf-8"))


def require_anchor_files(character_root: Path) -> None:
    missing = [
        relative_path
        for _, relative_path in ANCHOR_PARTS
        if not (character_root / relative_path).is_file()
    ]
    if missing:
        missing_list = ", ".join(missing)
        raise FileNotFoundError(f"Missing required anchor files: {missing_list}")


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
            "Reference images must be golden reference ids, indexed golden paths, "
            f"or existing files under references/golden/: {invalid_list}"
        )


def compile_prompt(character_root: Path, raw_request: str, provider: str, reference_images: list[str]) -> dict:
    profile = load_profile(character_root)
    require_anchor_files(character_root)
    validate_reference_images(character_root, reference_images)
    anchor_version = profile.get("anchor_version", "0.1.0")
    display_name = profile.get("display_name", character_root.name)

    parts: dict[str, str] = {}
    for key, relative_path in ANCHOR_PARTS:
        exclude_sections = {"requires user confirmation"} if key == "allowed_variations" else set()
        parts[key] = compact_markdown(read_text(character_root / relative_path), exclude_sections)

    prompt_id = "prompt_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    expanded_prompt = "\n".join(
        [
            f"Create {display_name} in the requested scene while preserving the character anchor.",
            "",
            "Raw scene request:",
            raw_request,
            "",
            "Identity lock:",
            parts["identity"] or "Use the identity defined in the anchor card.",
            "",
            "Face consistency:",
            parts["face"] or "Preserve stable face shape, eyes, nose, mouth, jawline, and age presentation.",
            "",
            "Body and proportion consistency:",
            parts["body"] or "Preserve stable body proportions, posture baseline, and physical presence.",
            "",
            "Presence and temperament:",
            " ".join(filter(None, [parts["presence"], parts["temperament"]]))
            or "Preserve the character's recognizable emotional presence and expression range.",
            "",
            "Motion and wardrobe logic:",
            " ".join(filter(None, [parts["motion"], parts["wardrobe_logic"]]))
            or "Allow pose and clothing changes only when they fit the established character logic.",
            "",
            "Style baseline:",
            parts["style"] or "Keep the existing visual style unless the request explicitly asks for a style variant.",
            "",
            "Non-negotiable invariants:",
            parts["invariants"] or "Do not change core identity anchors.",
            "",
            "Allowed variations:",
            parts["allowed_variations"] or "Scene, outfit, pose, expression, camera, and lighting may vary without redesigning the character.",
        ]
    )

    negative_prompt = parts["negative_rules"] or (
        "Do not change face identity, age presentation, body proportions, hair structure, "
        "temperament, or recognizable presence. Avoid generic beauty-face drift."
    )

    payload = {
        "prompt_id": prompt_id,
        "raw_request": raw_request,
        "anchor_version": anchor_version,
        "expanded_prompt": expanded_prompt,
        "negative_prompt": negative_prompt,
        "model_or_provider": provider,
        "reference_images": reference_images,
        "allowed_variations": ["scene", "outfit", "pose", "expression", "camera", "lighting"],
        "blocked_variations": ["identity redesign", "age drift", "body-proportion drift", "temperament replacement"],
        "safety_status": "requires_review",
        "quality_checks": [
            "face_match",
            "body_proportion_match",
            "presence_match",
            "style_match",
            "drift_risk",
        ],
        "created_at": now_iso(),
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a character-consistent prompt.")
    parser.add_argument("character_root", help="Path to characters/<character-id>.")
    parser.add_argument("--request", required=True, help="Raw scene or generation request.")
    parser.add_argument("--provider", default="provider-neutral", help="Target model or provider label.")
    parser.add_argument("--reference-image", action="append", default=[], help="Golden reference image id or path. Can be passed multiple times.")
    parser.add_argument("--write", action="store_true", help="Append to prompt-library JSONL files.")
    args = parser.parse_args()

    character_root = Path(args.character_root).expanduser().resolve()
    try:
        payload = compile_prompt(character_root, args.request, args.provider, args.reference_image)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.write:
        append_jsonl(character_root / "prompt-library" / "raw-prompts.jsonl", {
            "prompt_id": payload["prompt_id"],
            "raw_request": args.request,
            "anchor_version": payload["anchor_version"],
            "model_or_provider": payload["model_or_provider"],
            "reference_images": payload["reference_images"],
            "created_at": payload["created_at"],
        })
        append_jsonl(character_root / "prompt-library" / "compiled-prompts.jsonl", payload)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
