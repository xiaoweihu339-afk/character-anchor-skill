# Changelog

All notable changes to Character Anchor Skill will be recorded here.

## 0.3.0 - Media-First Workflow Scaffold

- Reframed the next real-use path around user media first: inventory, coverage honesty, hard-defect screening, review galleries, generation request payloads, and feedback recording.
- Added `audit_media_coverage.py` to count raw media without pretending that inventory equals visual review.
- Added `build_review_gallery.py` to create local HTML review galleries when chat image display is unreliable.
- Added `update_face_lock.py` and `quality/face-lock/face-lock.json` to record face geometry ratios before golden-candidate generation.
- Added `generate_golden.py` to create structured external golden-candidate generation requests without claiming this repository contains a built-in image generator.
- Added `record_golden_feedback.py` to capture user likeness feedback for generated golden candidates.
- Added `docs/v0.3-roadmap.md` to document the gap between the file-based MVP and the product-value MVP.

## 0.1.1 - New User Quick Start Fixes

- Added `SKILL.md` as a portable skill/workflow definition.
- Added `.gitkeep` files so required empty reference directories survive GitHub clone.
- Clarified that this repository is a file-based workflow MVP and reference implementation.
- Clarified that locally initialized character libraries are ignored by Git by default for privacy.
- Clarified that the Mira Vale demo is text-only and has no golden image IDs.
- Added standard project files for release hygiene.

## 0.1.0 - Initial MVP Release

- Added file-based character anchor library structure.
- Added fictional text-only demo character `characters/mira-vale`.
- Added prompt compiler, validator, and character initializer scripts.
- Added English and Chinese README files.
- Added documentation for architecture, schemas, safety, reference quality, media coverage, golden gallery workflow, product gallery, model adapters, roadmap, and portfolio framing.
