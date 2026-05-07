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

## Review 23: Three-Round New User Trial From GitHub

Checks run from fresh GitHub clones:

- Round 1: follow README demo flow with `validate_character_anchor.py` and `compile_prompt.py`.
- Round 2: initialize a new character library, validate it, and compile a prompt from the empty template.
- Round 3: try the optional `--reference-image` path, check `make demo` availability on Windows, and inspect whether the repository presents itself as an installable skill.

Findings:

- Round 1 failed at the first validation step because GitHub does not preserve empty directories. The cloned `characters/mira-vale/references/` only contained `index.json`, so `references/raw/`, `references/golden/`, and `references/rejected/` were missing.
- Round 1 prompt compilation still worked, which means the compiler path is healthy but the README validation path is blocked.
- Round 2 successfully created and validated a new draft character library, with the expected authorization warning. Prompt compilation from the empty template worked.
- Round 2 showed a usability ambiguity: `.gitignore` correctly keeps local test characters private, but a new user may not understand that their newly initialized character is intentionally ignored by Git.
- Round 3 showed that the optional `--reference-image` command fails clearly when no golden reference exists, which is good, but README could explain that the Mira Vale demo has no golden image IDs.
- Round 3 showed that `make demo` is not available on a default Windows environment, so the Python commands should remain the primary Quick Start.
- The repository name says "skill", but the public package did not include a top-level `SKILL.md`, so new users may not know whether this is an installable Codex skill or a workflow MVP.

Recommended fixes:

- Add `.gitkeep` files to required empty directories in `characters/mira-vale/references/raw/`, `references/golden/`, and `references/rejected/`.
- Add a short README note: Mira Vale is a text-only demo and does not include golden reference image IDs yet.
- Add a short README note explaining that user-created character libraries are ignored by default for privacy, and how to move them into a private repo if desired.
- Add a top-level `SKILL.md` or clarify that this repository is a workflow MVP rather than an installable Codex skill.
- Consider adding a minimal GitHub Actions check that runs demo validation and prompt compilation.

## Review 24: New User Trial Fixes

Fixes:

- Added `.gitkeep` files so required empty reference directories survive a GitHub clone.
- Added top-level `SKILL.md` as a portable skill definition and workflow summary.
- README and `README.zh-CN.md` now clarify that this is a workflow MVP/reference implementation, not a packaged app.
- README and `README.zh-CN.md` now explain that locally initialized character libraries are ignored by Git by default for privacy.
- README and `README.zh-CN.md` now clarify that the Mira Vale text-only demo has no golden reference image IDs.

## Review 25: Second-Version Publish Review

Checks run:

- Reviewed diff from the first published upload folder to the second-version working tree.
- Ran `python scripts/validate_character_anchor.py characters/mira-vale`.
- Ran `python scripts/compile_prompt.py characters/mira-vale --request "Mira walks through a rain-soaked train station at night, holding her notebook." --provider provider-neutral`.
- Scanned the second-version upload folder for private test-character keywords.
- Copied the second-version folder to a clean temporary directory, initialized Git, staged all files, and confirmed `.gitkeep` files are included.
- Re-ran validation and prompt compilation from the clean temporary copy.

Findings:

- The second version fixes the first new-user blocker: required empty reference directories now survive Git staging through `.gitkeep`.
- The Mira Vale demo validates successfully and the prompt compiler still works.
- The upload folder contains no private test-character keyword matches.
- `SKILL.md` improves the repository's skill framing while still clarifying that this is a workflow MVP and reference implementation.
- User privacy behavior is now documented: newly initialized local character libraries are ignored by Git by default.
- Git emitted normal Windows LF-to-CRLF warnings during temporary staging. This is not release-blocking, but a future `.gitattributes` file could standardize line endings.

Decision:

- Second version is ready to commit and push as a follow-up fix release.

## Review 26: Standard Project Documents

Previous version backup:

- `<local-v0.2-backup-path>`

Finding:

- The second-version local folder had `SKILL.md`, but it was still uncommitted and not visible on GitHub. The project also lacked a few standard release hygiene files that help new users understand version history, contribution rules, and line-ending behavior.

Decision:

- Keep the second-version quick-start fixes and add a small standard document set rather than expanding the MVP feature scope.

Fixes:

- Added `CHANGELOG.md` with `0.1.0` and `0.1.1` release notes.
- Added `CONTRIBUTING.md` with safety, privacy, local test character, and review-log rules.
- Added `.gitattributes` to standardize text line endings and mark common media files as binary.
- README and `README.zh-CN.md` now link to changelog and contribution rules.

Verification planned:

- Validate Mira Vale.
- Compile the Mira Vale demo prompt.
- Check Git status and staged files before committing.
- Scan public files for private test-character keywords.

## Review 27: Real Codex Skill Invocation Test

Source:

- Private Codex test thread: `<private-test-thread>`
- Test root: `<private-lab-test-root>`
- Pre-review backup: `<local-pre-review-27-backup-path>`

What happened:

- The user asked Codex to copy the public skill folder into a private lab directory and avoid modifying the original skill source.
- The test first drifted into a text-first fictional character flow, asking the user to provide manual appearance fields.
- The user corrected the flow and provided an authorized raw media directory.
- The workflow imported 355 files, generated an index, ran hard-defect screening, created contact sheets, performed deeper screening, and eventually produced four 1024x1024 "golden" reference images.
- The final "golden" images were standardized crops from source media, not AI-generated new golden images.

Findings:

- P0: The workflow still lacks an actual AI golden-image generation engine. When the user asked to continue until four golden images existed, the assistant produced cropped/standardized source references rather than AI-generated golden candidates.
- P0: There is no face-profile extraction layer before golden generation. The workflow does not extract landmarks, embeddings, stable face proportions, or identity descriptors that can guide IP-Adapter, InstantID, PuLID, or another identity-preserving generator.
- P1: The first-use path still starts too text-first. Even when testing a media-driven skill, the assistant first asked the user for manual appearance fields instead of asking whether the user wants to upload raw media.
- P1: The upload path needs explicit mode selection: large messy media dump versus curated 10-30 image set.
- P1: The system could not reliably show contact sheet images inside the chat. It eventually had to create local HTML galleries, which should become part of the expected review artifact workflow.
- P1: The hard screening criteria were initially too loose. Candidate packs included small faces, hats, occlusion, text overlays, and low-value context images until the user corrected the standard.
- P1: Identity clustering was improvised during the session and should become a documented/scripted stage before golden promotion.
- P2: Windows/PowerShell issues appeared repeatedly: wildcard copy behavior, relative path calculation compatibility, UTF-8 BOM in JSON, and long-running frame extraction/scoring timeouts.
- P2: The system preserved the original skill source and raw media, which confirms that the lab-copy isolation workflow is useful and should be documented.

Recommended v0.3 direction:

- Make the default real-use flow media-first: minimal character creation, upload mode selection, ingest, coverage audit, hard screening, identity clustering, face-profile extraction, golden candidate generation, user likeness review.
- Add `docs/v0.3-roadmap.md` using the user test as the rationale.
- Add `scripts/audit_media_coverage.py` for reproducible counts, frame extraction coverage, skipped files, and coverage status.
- Add `scripts/build_review_gallery.py` to create local HTML galleries and contact sheets for candidate review.
- Add `scripts/extract_face_profile.py` to extract face landmarks, embeddings, and stable face geometry from confirmed references.
- Add `scripts/generate_golden.py` as a provider-adapter entry point for ComfyUI/IP-Adapter, InstantID, PuLID, or another identity-preserving generator.
- Add `scripts/record_golden_feedback.py` to capture user review of generated golden candidates into `feedback/`, `quality/scores.jsonl`, and `outputs/failed/`.

Decision:

- Current `0.1.x` is a solid file-based workflow MVP, but not yet the product-value MVP. The next major iteration should focus on the generation engine and media-first UX, not more README polish.

## Review 28: v0.3 Media-First Version

Previous version backup:

- `<local-pre-v0.3-backup-path>`

Findings:

- P0: The repo should not imply that it can already generate identity-stable golden images without an external image workflow.
- P1: The practical user flow should start from raw media, coverage honesty, hard-defect reference screening, and local review artifacts.
- P1: Chat previews are unreliable for large image batches, so a local HTML gallery helper is part of the workflow rather than an ad hoc workaround.
- P2: The project needs a feedback capture command so user likeness judgments become structured data instead of disappearing in conversation.

Decisions:

- Make `0.3.0` a media-first workflow scaffold, not a full generation engine.
- Keep all real-person and test data outside the public package.
- Make generation honesty explicit: `generate_golden.py` creates an external request payload only.

Fixes:

- Added `scripts/audit_media_coverage.py` for inventory-only media coverage reports.
- Added `scripts/build_review_gallery.py` for local HTML review galleries.
- Added `scripts/generate_golden.py` for external golden-candidate generation request payloads.
- Added `scripts/record_golden_feedback.py` for user likeness feedback logging.
- Added `docs/v0.3-roadmap.md`.
- Updated README, `README.zh-CN.md`, `SKILL.md`, `CHANGELOG.md`, `docs/mvp-roadmap.md`, and `docs/schemas.md`.
- Added `quality/coverage/` to initialized and validated character libraries.

Verification planned:

- Validate Mira Vale.
- Compile the Mira Vale demo prompt.
- Run all four new v0.3 helper scripts in non-mutating or temporary-output mode.
- Scan the public package for private test-character names.

Verification completed:

- `python scripts\validate_character_anchor.py characters\mira-vale`: passed.
- `python scripts\compile_prompt.py characters\mira-vale --request "Mira walks through a rain-soaked train station at night, holding her notebook." --provider provider-neutral`: passed.
- `python scripts\audit_media_coverage.py characters\mira-vale`: passed and reported inventory-only coverage.
- `python scripts\build_review_gallery.py characters\mira-vale --output %TEMP%\character-anchor-review-gallery.html`: passed.
- `python scripts\generate_golden.py characters\mira-vale --request "Create front, side, back, full-body, and long-shot golden candidates." --provider provider-neutral`: passed and reported request-payload-only status.
- `python scripts\record_golden_feedback.py characters\mira-vale --candidate-id demo-candidate --user-rating 4 --dry-run`: passed without mutating demo logs.
- New initialized character library validates with the expected consent warning.
- PowerShell keyword scan found no private test-character names in the public upload folder.

## Review 29: v0.3 Publish-Readiness Review

Checks run:

- Reviewed README, Chinese README, SKILL, changelog, schemas, v0.3 roadmap, and review log diffs.
- Reviewed the four new v0.3 scripts.
- Ran `git diff --check`.
- Ran `python scripts\generate_golden.py characters\mira-vale --request "test" --reference-image definitely_missing_ref --provider provider-neutral`.
- Ran init + coverage `--write` + validate in a temporary character library.

Findings:

- P2: README and Chinese README still describe AI source-reference filtering and AI-generated golden candidates as part of the feature flow, but v0.3 only provides inventory, gallery, request-payload, and feedback helpers. This can overstate the current implementation.
- P2: `generate_golden.py` accepts any `--reference-image` value and writes it into the generation payload without checking whether it exists, is approved, or is under `references/golden/`.
- P3: The public review log contains local absolute paths and a Codex thread id. These are useful for private traceability, but should be sanitized before a public GitHub release.

Passed checks:

- `git diff --check`: passed.
- Temporary init + coverage write + validate: passed with the expected consent warning.

Recommendation:

- Fix the P2 wording and reference validation before publishing v0.3.
- Sanitize local paths in the public review log, or move detailed private audit evidence into a local-only/private log.

## Review 30: Review 29 Fixes

Pre-fix backup:

- `<local-pre-review-29-fixes-backup-path>`

Findings fixed:

- README and Chinese README over-promised AI source filtering and AI-generated golden candidates as if those were implemented inside v0.3.
- `generate_golden.py` accepted arbitrary `--reference-image` values.
- Public review log contained local absolute paths and a private Codex thread id.

Fixes:

- README and `README.zh-CN.md` now describe v0.3 as reserving an AI/human screening workflow and creating external golden-candidate generation request payloads.
- `generate_golden.py` now validates `--reference-image` against approved golden ids, indexed golden paths, or files under `references/golden/`.
- Added `--allow-unvalidated-reference` for private experiments only, and marks such payloads as validation-skipped.
- `docs/schemas.md` now documents `reference_validation`.
- `docs/v0.3-roadmap.md` clarifies that unvalidated references are private-experiment material.
- Public review log local paths and private thread id were replaced with placeholders.

Verification planned:

- Run `generate_golden.py` with a missing reference and confirm it fails.
- Run `generate_golden.py` with `--allow-unvalidated-reference` and confirm it marks validation as skipped.
- Re-run validation, compile, diff check, and private-keyword scan.

Verification completed:

- Missing `--reference-image` now fails with a clear CLI error.
- `--allow-unvalidated-reference` succeeds and writes `reference_validation: skipped_by_user_for_private_experiment`.
- `python scripts\validate_character_anchor.py characters\mira-vale`: passed.
- `python scripts\compile_prompt.py characters\mira-vale --request "Mira walks through a rain-soaked train station at night, holding her notebook." --provider provider-neutral`: passed.
- `git diff --check`: passed.
- Private test-character keyword scan: no matches.

## Review 32: Final Pre-Publish Check

Checks run:

- `python scripts\validate_character_anchor.py characters\mira-vale`
- `python scripts\compile_prompt.py characters\mira-vale --request "Mira walks through a rain-soaked train station at night, holding her notebook." --provider provider-neutral`
- `python scripts\audit_media_coverage.py characters\mira-vale`
- `python scripts\build_review_gallery.py characters\mira-vale --output %TEMP%\character-anchor-final-gallery.html`
- `python scripts\update_face_lock.py characters\mira-vale --measurement eye_spacing_ratio=1.0 --qualitative-lock "moderate eye spacing" --dry-run`
- `python scripts\generate_golden.py characters\mira-vale --request "Create front, side, back, full-body, and long-shot golden candidates." --provider provider-neutral`
- `python scripts\record_golden_feedback.py characters\mira-vale --candidate-id demo-candidate --user-rating 4 --liked-point "stable face direction" --dry-run`
- `python scripts\generate_golden.py characters\mira-vale --request "bad ref test" --reference-image definitely_missing_ref --provider provider-neutral`
- Temporary init + validate for a new character library.
- Public package scans for private test-character names, local absolute paths, private thread ids, mojibake markers, `__pycache__`, and `.pyc` files.
- `git diff --check`
- `git status --short`
- `git ls-files --others --exclude-standard`

Results:

- Mira Vale validation passed.
- Prompt compilation passed.
- Coverage audit passed and correctly reported `inventory_only_not_visual_review`.
- HTML review gallery generation passed.
- Face Lock dry-run passed.
- Golden request payload generation passed and includes `face_lock`.
- Feedback dry-run passed without mutating demo logs.
- Missing `--reference-image` correctly failed with a clear CLI error.
- Temporary init + validate passed with the expected consent warning.
- No private test-character keyword matches.
- No local absolute path or private thread id matches in public files.
- No mojibake marker matches in public files.
- No `__pycache__` or `.pyc` files found.
- `git diff --check` passed.

Non-blocking note:

- The Mira Vale demo character still reports `anchor_version: 0.1.0`. This can be treated as the demo character's own anchor version, separate from the repository release version `0.3.0`. It is not a release blocker, but can be bumped in a later cleanup if desired.

Decision:

- v0.3 is ready to stage, commit, and push after the user confirms the release scope.
- Public review log scan for local absolute paths and private thread ids: no matches.

## Review 31: Face Geometry Lock Layer

Pre-change backup:

- `<local-pre-face-lock-backup-path>`

Finding:

- The workflow jumped from usable reference selection to external golden-candidate generation without a structured face data lock. This made it harder to preserve and iteratively tune face length, eye spacing, brow-to-eye distance, mouth width, jaw shape, cheekbone width, and related identity geometry.

Decision:

- Add a Face Lock layer between selected references and golden-candidate generation.
- Keep v0.3 dependency-free: the first version stores manually or AI-assisted relative ratios, while later versions can upgrade the same schema with landmark-derived measurements.

Fixes:

- Added `quality/face-lock/face-lock.json`.
- Added `scripts/update_face_lock.py`.
- Initializer now creates the face-lock directory and JSON scaffold.
- Validator now checks the face-lock directory and schema fields.
- `generate_golden.py` now includes the face lock in `identity_inputs`.
- README, Chinese README, SKILL, changelog, roadmap, and schemas now document the Face Lock step.

Verification planned:

- Validate Mira Vale.
- Run `update_face_lock.py` in dry-run mode.
- Confirm `generate_golden.py` payload includes `face_lock`.
- Re-run init + validate on a temporary character library.

Verification completed:

- `python scripts\validate_character_anchor.py characters\mira-vale`: passed.
- `python scripts\update_face_lock.py characters\mira-vale --measurement eye_spacing_ratio=1.0 --qualitative-lock "moderate eye spacing" --dry-run`: passed.
- `python scripts\generate_golden.py characters\mira-vale --request "test face lock" --provider provider-neutral`: payload includes `face_lock`.
- Temporary init + validate: passed with the expected consent warning.
- `git diff --check`: passed.
- Private test-character keyword scan: no matches.
