#!/usr/bin/env python3
"""Record user feedback for a generated golden candidate."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def split_values(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        result.extend(item.strip() for item in value.split(",") if item.strip())
    return result


def build_feedback(args: argparse.Namespace) -> dict:
    feedback_id = "feedback_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return {
        "feedback_id": feedback_id,
        "candidate_id": args.candidate_id,
        "output_path": args.output_path,
        "prompt_id": args.prompt_id,
        "user_rating": args.user_rating,
        "identity_similarity": args.identity_similarity,
        "liked_points": split_values(args.liked_point),
        "disliked_points": split_values(args.disliked_point),
        "correction_notes": split_values(args.correction_note),
        "reuse_as_reference": args.reuse_as_reference,
        "promote_to_golden_candidate": args.promote_to_golden_candidate,
        "created_at": now_iso(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Record golden candidate feedback into feedback/feedback.jsonl.")
    parser.add_argument("character_root", help="Path to characters/<character-id>.")
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--output-path", default="")
    parser.add_argument("--prompt-id", default="")
    parser.add_argument("--user-rating", type=float, default=None)
    parser.add_argument("--identity-similarity", type=float, default=None)
    parser.add_argument("--liked-point", action="append", default=[])
    parser.add_argument("--disliked-point", action="append", default=[])
    parser.add_argument("--correction-note", action="append", default=[])
    parser.add_argument("--reuse-as-reference", action="store_true")
    parser.add_argument("--promote-to-golden-candidate", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Print feedback without writing files.")
    args = parser.parse_args()

    character_root = Path(args.character_root).expanduser().resolve()
    if not character_root.is_dir():
        parser.error(f"character_root is not a directory: {character_root}")

    feedback = build_feedback(args)
    if not args.dry_run:
        append_jsonl(character_root / "feedback" / "feedback.jsonl", feedback)

    print(json.dumps(feedback, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
