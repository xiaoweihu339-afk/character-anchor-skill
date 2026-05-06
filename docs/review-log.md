# Review Log

This document records the first structured review of Character Anchor Skill before the initial GitHub release.

本文档记录 Character Anchor Skill 初版发布前的第一次结构化 review。

## Review Scope

- README and onboarding flow
- Project structure
- Golden Gallery and Product Gallery concepts
- Safety and authorization rules
- CLI scripts
- Demo character anchor quality
- JSON/JSONL schema consistency
- Documentation consistency
- Pre-release repository hygiene

## Round 1: README Entry Point

Finding:

- README over-promised product archive support.

Fix:

- Changed MVP wording from "archive successful product images" to "reserve a product gallery structure".

## Round 2: Project Structure

Finding:

- No blocking issue. The directory structure works as a file-based data model.

Decision:

- Keep the structure as the MVP contract.

## Round 3: Golden Gallery And Product Gallery

Findings:

- Rejected examples were described as part of the golden gallery.
- Product image promotion rule omitted safety and identity checks.
- Unauthorized media routing was ambiguous.

Fixes:

- Clarified that rejected examples belong in `references/rejected/` or failure logs.
- Product image promotion now requires authorization, safety, face similarity, identity stability, and future usefulness.
- Unauthorized real-person media is metadata-only and should not become a reusable file.

## Round 4: Optimization And Safety

Finding:

- Safety and optimization sections were conceptually sound.

Fix:

- Synchronized remaining safety checklist wording around metadata-only handling.

## Round 5: Quick Start

Findings:

- Quick Start command used `--write`, which mutated tracked demo JSONL logs.
- Quick Start mixed "create your own character" and "try the demo" flows.

Fixes:

- Split Quick Start into "Try the demo" and "Create your own character".
- Removed `--write` from the default demo command.

## Round 6: Demo, Portfolio, And Status

Findings:

- Demo example still used mutating `--write`.
- Portfolio case study implied product archiving was already implemented.
- README did not link to the demo walkthrough.

Fixes:

- Removed `--write` from the main demo example.
- Softened portfolio wording to "reserves a product gallery structure".
- Added a link to `examples/mira-vale.md`.

## Round 7: Init Script

Finding:

- `created_at` and `updated_at` used separate timestamp calls.

Fix:

- Generated one timestamp and reused it for both fields.

## Round 8: Validator Script

Finding:

- Validator checked whether JSON files were parseable, but not whether required fields existed.

Fix:

- Added required-field checks for core JSON files.
- Avoided noisy field errors when JSON parsing itself fails.

## Round 9: Prompt Compiler Safety And Reliability

Findings:

- Missing anchor files silently fell back to generic prompt text.
- `safety_status` was hard-coded as `safe_fictional_character`.
- `prompt_id` could collide within the same second.

Fixes:

- Missing anchor files now produce an error.
- `safety_status` is now `requires_review`.
- `prompt_id` includes microseconds.
- CLI errors now print concise `ERROR:` messages instead of Python tracebacks.

## Round 10: Prompt Compiler Traceability

Findings:

- Raw prompt logs omitted provider and anchor version.
- `reference_images` was always empty.
- Markdown compaction flattened bullets and section structure.

Fixes:

- Raw prompt logs now include `anchor_version`, `model_or_provider`, and `reference_images`.
- Added `--reference-image`.
- Markdown compaction now preserves line structure and useful subheadings.

## Round 11: Reference Image CLI

Findings:

- README did not mention `--reference-image`.
- CLI did not validate reference image ids or paths.

Fixes:

- README now includes an optional `--reference-image` example.
- CLI validates references against golden ids, indexed golden paths, or files under `references/golden/`.

## Round 12: Demo Character Core Anchors

Findings:

- Body anchors were too broad.
- Face anchors needed more identity-stable geometry.
- Anchor card mixed permanent identity marks with optional props.

Fixes:

- Added face geometry: eye spacing, brow distance, cheekbones, mouth width, jaw taper.
- Added body proportion cues: shoulder-hip relation, narrow silhouette, torso length, arm position.
- Separated permanent identity mark from optional props and accessories.

## Round 13: Remaining Demo Character Files

Findings:

- Review rubric lagged behind the improved face/body anchors.
- Notebook was listed as an allowed pose but not marked optional.
- Style baseline lacked avoid rules.

Fixes:

- Updated review rubric with more specific face and body criteria.
- Clarified notebook is allowed but not required.
- Added style drift avoid list.

## Round 14: Schemas

Findings:

- `raw-prompts.jsonl` schema was missing.
- `compiled-prompts.jsonl` safety status example differed from implementation.
- Product gallery schema lived outside the central schema doc.

Fixes:

- Added `raw-prompts.jsonl` schema.
- Updated compiled prompt `safety_status` to `requires_review`.
- Added suggested safety status values.
- Added `outputs/product-gallery/index.jsonl` schema and cross-link.

## Round 15: Documentation Consistency

Findings:

- Architecture doc did not mention `product-gallery`.
- Safety policy still suggested childhood/student-age media could be stored in `references/rejected/`.
- Roadmap duplicated face/visual similarity scoring.

Fixes:

- Architecture now includes product gallery output.
- Safety policy now uses conservative metadata-only language for unsafe or unauthorized real-person media.
- Roadmap merged duplicate scoring items.

## Round 16: Pre-Release Check

Checks:

- `validate_character_anchor.py characters/mira-vale`: passed.
- `compile_prompt.py` demo command: passed.
- Temporary test directories: none.
- Old JSONL schema residue: removed.
- README and docs: aligned with MVP implementation.

Result:

- No P1/P2 issues remain.
- The project is ready for user testing before the first GitHub release.

## Remaining Future Work

- Add product image archiving command.
- Add product-to-golden promotion command.
- Add image/video ingestion.
- Add face similarity scoring.
- Add visual review helper.
- Add UI for browsing anchors, golden references, and product gallery.
- Add provider-specific adapters.

## Follow-Up Review: New User Testing Preparation

Additional questions were reviewed before user testing.

Resolved or verified:

- `created_at` and `updated_at` already share one timestamp in `init_character_anchor.py`.
- `--reference-image` is implemented in `compile_prompt.py`.
- No `__pycache__/` or `.pyc` files were present in the working tree.

Improvements added:

- Added a README "Current vs Planned" Mermaid diagram to show product roadmap thinking.
- Added the same roadmap diagram to `README.zh-CN.md`.
- Clarified that `## Requires User Confirmation` in `allowed-variations.md` is intentionally excluded from compiled allowed variations.
- Added `Makefile` with `validate`, `compile`, `demo`, and `init-example` targets.
- Changed the `--reference-image` README example to use a placeholder instead of a non-existent demo id.
- Added a clean sample compiled prompt log for `characters/mira-vale`.

Decision:

- These changes improve onboarding and portfolio readability without expanding MVP scope.

## New User Trial Feedback

Result:

- The main demo flow works for a new user.

Friction points:

- Consent warnings need an immediate explanation in README so users know what to do next.
- After initializing a new character, users need guidance that empty templates are only structural scaffolding.

Fixes:

- README and `README.zh-CN.md` now explain that consent warnings should be resolved by filling `consent.json` and confirming fictional, user-owned, or authorized media.
- README and `README.zh-CN.md` now explain that users should fill `anchor-card.md` and `anchor-library/` before compiling prompts for stable results.

## New User Trial Follow-Up: Reference Image Example

Finding:

- The README mentioned `--reference-image` near Quick Start, but the text-only Mira Vale demo has no golden image references. New users could misread the example as directly runnable against the demo.

Clarification:

- `--reference-image` is implemented in `compile_prompt.py`.
- It succeeds only when the reference is an indexed golden id/path or an existing file under `references/golden/`.

Fix:

- README and `README.zh-CN.md` now explicitly say the Mira Vale demo has no image references and that the `--reference-image` pattern applies after a character has approved golden references.

## New User Trial Follow-Up: Demo Character Clarity

Finding:

- The README described `characters/mira-vale` as a text-only demo, but did not make it clear that the demo is filled with text anchors rather than an empty scaffold.

Fix:

- README and `README.zh-CN.md` now clarify that Mira Vale includes a filled anchor card, face/body/presence/motion/wardrobe anchors, negative rules, a review rubric, and sample prompt logs.
- README and `README.zh-CN.md` also clarify that the demo intentionally does not include real images or golden references.

## Product Risk Review: Multiple People In Raw Media

Problem:

- User-uploaded photos, videos, and Live Photos may contain other people besides the target character. If these frames are used directly, the system may accidentally learn another person's face, body, outfit, or style as part of the target identity.

Decision:

- Add `primary subject identification` as a required stage before quality filtering and golden reference selection.

Fixes:

- README and `README.zh-CN.md` now include primary subject identification in the workflow.
- `docs/golden-gallery-workflow.md` now includes a dedicated Primary Subject Identification section.
- `docs/schemas.md` now documents reference fields for `subject_role`, `contains_other_people`, `other_people_count`, `target_visibility`, and `recommended_action`.
- `docs/safety-checklist.md` now requires other visible people to be authorized, blurred/cropped out, or excluded from active references.

## Product Risk Review: Golden Candidates Do Not Look Like Target

Problem:

- Early user testing found that generated golden images may look good but not resemble the target. If promoted, these images would poison the golden gallery and make future keyframes drift.

Decision:

- Treat golden images as candidates until they pass face similarity and user likeness review.
- Do not promote beautiful-but-wrong images into `references/golden/`.

Fixes:

- README and `README.zh-CN.md` now include face similarity and user likeness review in the workflow.
- `docs/golden-gallery-workflow.md` now includes a Golden Candidate Failure Loop.
- Added `docs/golden-candidate-review.md`.
- `quality/review-rubric.md` now states that weak face match blocks golden promotion.
- `docs/schemas.md` now documents candidate and failed output records for likeness review and drift diagnosis.

## Product Risk Review: Poor AI-Selected Source References

Problem:

- User testing found that AI-selected source references can be low quality, which slows the workflow and causes poor golden candidates.

Decision:

- Add a reference quality gate before identity-stable reference selection and golden candidate generation.
- References should be classified by use, not simply accepted or rejected.

Fixes:

- README and `README.zh-CN.md` now include `reference quality gate` in the workflow.
- `docs/golden-gallery-workflow.md` now includes a Reference Quality Gate section.
- Added `docs/reference-quality-gate.md`.
- `docs/schemas.md` now documents `reference_use`, `quality_scores`, and `quality_failure_reasons`.

## Product Risk Review: AI Reviewer Takes Sampling Shortcuts

Problem:

- With hundreds or thousands of uploaded images and videos, AI may inspect only sampled contact sheets or a small subset of videos, then present the result as if the full dataset was reviewed.

Decision:

- Add media inventory and coverage audit before safety, quality filtering, and reference selection.
- Sampling is allowed for triage, but must be labeled as sampling.
- Golden references should not be promoted from unreviewed media.

Fixes:

- README and `README.zh-CN.md` now include media inventory and coverage audit in the workflow.
- `docs/golden-gallery-workflow.md` now includes a Media Inventory And Coverage Audit section.
- Added `docs/media-coverage-audit.md`.
- `docs/schemas.md` now documents a future `references/coverage-manifest.json` shape and coverage statuses.

## Review 17: Coverage Audit MVP Wording

Findings:

- README listed media coverage tracking as an MVP feature even though the current CLI does not create a coverage manifest, validate one, or run a media ingest/audit command.
- `docs/schemas.md` documented `references/coverage-manifest.json`, but the project initializer and validator do not include it.
- The Current vs Planned roadmap did not make coverage audit visible as its own planned capability.

Fixes:

- README and `README.zh-CN.md` now describe coverage audit as a documented workflow for future large media ingestion, not as an implemented tracking tool.
- The roadmap diagram now includes Media Coverage Audit / 素材覆盖率审计 as a planned node.
- `docs/schemas.md` now labels `references/coverage-manifest.json` as planned and future-only.

## Review 18: Keep User Test Data Out Of The Skill Package

Finding:

- Local new-user tests created private character libraries under `characters/`, including real test assets that should not be mixed into the reusable public skill package.

Fixes:

- `.gitignore` now ignores all local character libraries under `characters/` by default, while explicitly allowing the fictional `characters/mira-vale` demo.
- Removed the temporary local test scaffold.
- README and `README.zh-CN.md` now state that the public package intentionally includes only the Mira Vale demo and keeps local test character libraries private by default.

## Review 19: User-Visible Coverage Honesty

Decision:

- The system should honestly tell users how much media it actually reviewed before reference selection or golden candidate generation.
- This balances full scanning and small sampling: full inventory is required, deep review can be batched or sampled, but the coverage level must be visible.

Fixes:

- README and `README.zh-CN.md` now state that review coverage should be user-visible.
- `docs/media-coverage-audit.md` now requires a user-facing coverage summary before golden candidate generation.
- `docs/golden-gallery-workflow.md` now requires the workflow to report inspected image, video, and frame counts before generating golden candidates.

## Review 20: Split Source Reference Screening From Generated Likeness Review

Decision:

- Users should not need to judge every source reference. AI should filter source references for hard defects such as wrong subject, blur, occlusion, multi-person contamination, subtitles, watermarks, and unusable framing.
- After screening, the system should report coverage, pass/reject counts, and usable reference locations.
- The user decision point is whether to continue deeper screening or generate golden candidates from the current usable references.
- User likeness review applies to AI-generated golden images, not to every raw source reference.

Fixes:

- README and `README.zh-CN.md` now include coverage/reference reporting and the deeper-screening vs generation decision point.
- `docs/reference-quality-gate.md` now defines source reference screening as AI-led hard-defect filtering.
- `docs/golden-gallery-workflow.md` now separates AI-filtered source references from user-reviewed generated golden images.
- `docs/media-coverage-audit.md` now asks the user to choose between deeper screening and golden candidate generation after the coverage report.
- `docs/golden-candidate-review.md` now clarifies that likeness review applies to generated candidates.
- Optional tutorial documentation now explains the simplified user-facing flow.

## Review 21: Golden Gallery Coverage Gaps

Finding:

- User testing found that generated golden galleries can lack important video-oriented coverage such as back view, true 90-degree profile, long-shot silhouette, full-body, and motion references.

Decision:

- Add coverage-gap awareness now, but keep automatic gap completion out of the MVP.
- The MVP should record and report missing coverage dimensions so users know whether a gallery is suitable for portraits, video keyframes, distant shots, wardrobe continuity, or action-heavy scenes.

Fixes:

- README and `README.zh-CN.md` now list back view, 90-degree profile, long-shot, full-body, and motion references as important golden gallery coverage.
- `docs/golden-gallery-workflow.md` now includes a Golden Gallery Coverage section and example gap report.
- `docs/architecture.md` now mentions back-view, long-shot, and motion references for video keyframes.
- `docs/mvp-roadmap.md` keeps automatic coverage-gap completion out of the MVP.
- Mira Vale's review rubric now includes a Coverage Fit section.
- Optional tutorial documentation now explains that missing golden gallery angles should be recorded.

## Review 22: Publish Readiness Check

Checks run:

- `python scripts/validate_character_anchor.py characters/mira-vale`
- `python scripts/compile_prompt.py characters/mira-vale --request "Mira walks through a rain-soaked train station at night, holding her notebook." --provider provider-neutral`
- `python scripts/compile_prompt.py characters/mira-vale --request "Mira in a quiet archive room." --provider provider-neutral --reference-image missing_ref`
- `python scripts/init_character_anchor.py` and `validate_character_anchor.py` against a temporary character library outside the repo
- `git add --dry-run .`
- private test-data keyword search excluding ignored local test directories

Findings:

- The CLI MVP path works: demo validation passes, prompt compilation works, invalid golden-reference IDs fail with a clear `ERROR:` message, and initialization creates a valid draft character library.
- Git ignore rules prevent ignored local test character directories from being staged by normal `git add .`.
- Release-blocking documentation issue: optional tutorial docs still mentioned private/local test characters. These should be removed or rewritten before public release.

Decision:

- Not release-ready until the private test-character references are removed from public docs or the affected tutorial files are excluded from the release package.

Fixes:

- Optional tutorial docs now list only `mira-vale` as the public demo and describe local test characters generically as ignored/private.
- Optional generated tutorial docs now remove private test-character names and explain that real-person or authorized-material character libraries must stay local or private.
