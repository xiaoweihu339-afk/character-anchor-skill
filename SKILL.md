---
name: character-anchor
description: Build and maintain character anchor libraries for consistent character identity across AI image generation, video keyframes, writing, and model-specific prompt workflows.
---

# Character Anchor

Character Anchor is a workflow for keeping the same character recognizable across generated images, video keyframes, and scene prompts.

Use this repository as a workflow MVP and reference implementation. Version `0.3.0` is media-first, but still model-agnostic. It includes:

- a file-based character library structure
- a fictional text-only demo character
- prompt compilation scripts
- validation scripts
- media coverage inventory
- local HTML review galleries
- face geometry lock records
- external golden-generation request payloads
- golden candidate feedback logging
- safety, coverage, reference quality, and golden gallery documentation

## Core Rule

Preserve identity first, then satisfy the scene.

Do not process private or real-person media unless the user confirms they own it or are authorized to use it. If age is unknown, use minor-safe handling. Do not generate NSFW, erotic, fetish, or overexposed outputs.

## Workflow

1. Confirm authorization and safety.
2. Ask whether the user has messy bulk media or a curated 10-30 image set.
3. Store raw media under `references/raw/` in a private lab, not in the public skill package.
4. Run `scripts/audit_media_coverage.py` so the user sees what was counted and what was not visually reviewed.
5. Use AI/human review to filter source references for hard defects.
6. Build `scripts/build_review_gallery.py` HTML galleries when chat image previews are unreliable.
7. Record face geometry in `quality/face-lock/face-lock.json`.
8. Report coverage, rejected counts, usable reference counts, face-lock status, and reference locations.
9. Ask whether to continue deeper screening or prepare golden candidate generation.
10. Use `scripts/generate_golden.py` to create an external generation request payload that includes the face lock.
11. Let the user judge generated likeness.
12. Tune the face lock when repeated drift appears.
13. Record feedback with `scripts/record_golden_feedback.py`.
14. Route approved candidates to `references/golden/` only after safety and likeness review.

## Demo

Run:

```bash
python scripts/validate_character_anchor.py characters/mira-vale
python scripts/compile_prompt.py characters/mira-vale --request "Mira walks through a rain-soaked train station at night, holding her notebook." --provider provider-neutral
```

The public demo is text-only and fictional. It intentionally contains no real-person images.

Media-first helpers:

```bash
python scripts/audit_media_coverage.py <path-to-raw-media>
python scripts/build_review_gallery.py <path-to-images> --output outputs/tmp/review-gallery.html
python scripts/update_face_lock.py characters/mira-vale --measurement eye_spacing_ratio=1.0 --qualitative-lock "moderate eye spacing" --dry-run
python scripts/generate_golden.py characters/mira-vale --request "Create front, side, back, full-body, and long-shot golden candidates."
python scripts/record_golden_feedback.py characters/mira-vale --candidate-id candidate_0001 --user-rating 4 --dry-run
```

`generate_golden.py` creates a request payload only. It does not generate images unless an external image workflow consumes the payload.
