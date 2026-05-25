---
name: character-anchor
description: Build and maintain guided character anchor asset libraries for consistent character identity across Codex image generation, reference-image workflows, feedback loops, and optional model adapters. Use when Codex needs to create, update, audit, or apply a stable character library from user descriptions, authorized reference images, generated outputs, prompt history, quality scores, or correction feedback so the same character remains recognizable across scenes, outfits, poses, styles, and providers.
---

# Character Anchor

## Core Rule

Treat this skill as a guided character consistency workflow, not as a one-off generation workflow.

Use the asset library to preserve identity. Keep identity anchors, allowed variations, style choices, prompts, outputs, failures, feedback, and safety decisions separate so future work can reuse the same character without drifting.

Do not process a real person's media unless the user says they own it or are authorized to use it. If age is unknown, apply minor-safe rules. If a request involves minors, age ambiguity, overexposure, sexual content, or NSFW intent, stop or rewrite to a safe non-sexual version before ingest, prompt compilation, or generation.

## Codex Image Model First

Default to Codex built-in image generation for v1.1 workflows. Keep the library model-agnostic, but compile ordinary generation requests for Codex first unless the user explicitly asks for another provider.

- Use the user's raw request plus the character anchor, original reference image, approved golden references, allowed variations, and negative drift rules.
- Prefer English compiled prompts for image generation. Preserve the user's original language in `prompt-library/raw-prompts.jsonl`.
- Do not assume raw embedding, LoRA, IP-Adapter, ComfyUI, Stable Diffusion, or external adapter support in the default path.
- External adapters remain optional future routes under `adapters/model-providers.json` and `training-package/`.
- Never use the most recent generated image as a default reference unless the user explicitly approves it as golden.

## Guided Wizard Workflow

Guide users one step at a time. When a user says "new character", "create a character library", "continue this character", or "generate assets for this character", inspect `profile.json` and continue from `wizard_state`.

New character wizard:

1. Ask for the character name or confirm the provided name.
2. Collect basic identity one field at a time: gender or presentation, age presentation, height, body type, temperament, and visual style.
3. Ask the user to upload or identify the original reference image.
4. Archive the original reference in `references/raw/` and index it in `references/index.json`.
5. Guide the user to create or select four required golden references:
   - `front-closeup`: frontal headshot.
   - `left-closeup`: left side headshot.
   - `right-closeup`: right side headshot.
   - `full-body-face-visible`: full body image with visible face.
6. Ask the user to approve each golden reference before promoting it into `references/golden/`.
7. Mark the library `anchor_ready` only after the required golden reference types are present and user-approved.

Wizard states:

```text
profile_started
basic_identity_complete
raw_reference_added
golden_incomplete
anchor_ready
```

If golden references are incomplete, generation is allowed but degraded. Warn the user that drift risk is higher and route generated images to `outputs/candidates/` by default.

## Quick Start

1. If creating a new library, run `scripts/init_character_anchor.py` with `--root`, `--character-id`, and `--display-name`.
2. Fill `profile.json` through the guided wizard and keep `anchor-card.md` as the human-readable source of truth.
3. Archive user-provided media in `references/raw/` and index it in `references/index.json`.
4. Promote only user-approved, identity-stable references into `references/golden/`.
5. Keep the four required golden reference types complete before treating the character as stable.
6. Compile each request through the prompt workflow: raw request -> anchor-expanded prompt -> safety-screened prompt -> Codex compiled prompt.
7. Route generated outputs into approved, candidates, failed, or blocked folders.
8. Record Codex scores and user feedback so correction rules improve future generations.
9. Run `scripts/validate_character_anchor.py` before publishing, sharing, or using the library as a clean template.

## Library Contract

Use this top-level shape for each character:

```text
characters/<character-id>/
  anchor-card.md
  profile.json
  consent.json
  README.md (optional project-level copy, not required inside each character)

  references/
    raw/
    golden/
    rejected/
    index.json

  anchor-library/
    identity.md
    face.md
    body.md
    style.md
    temperament.md
    invariants.md
    allowed-variations.md
    negative-rules.md

  prompt-library/
    raw-prompts.jsonl
    compiled-prompts.jsonl
    optimized-recipes.jsonl

  outputs/
    approved/
      prompt-cards/
    candidates/
    failed/
    blocked/

  feedback/
    feedback.jsonl
    correction-rules.json

  adapters/
    model-providers.json

  quality/
    review-rubric.md
    scores.jsonl

  training-package/
    manifest.json
```

Keep `training-package/` optional. Use it only when the user explicitly wants training, LoRA, face adapter, embedding export, or dataset preparation.

Load `references/architecture.md` when designing or changing the library workflow. Load `references/schemas.md` when editing JSON files. Load `references/safety-policy.md` before handling minors, age ambiguity, exposure, NSFW, voice data, real people, or public release. Load `references/model-adapters.md` when connecting any provider beyond the default Codex image generation path.

## Anchor Card

Create `anchor-card.md` before optimizing prompts or model parameters.

Include:

- Character name or working name.
- Basic identity summary from the wizard.
- Age range or age presentation.
- Face anchors.
- Hair anchors.
- Body and proportion anchors.
- Skin, markings, scars, or distinctive details.
- Clothing or accessory anchors, if stable.
- Temperament and expression range.
- Visual style baseline.
- Allowed variations.
- Forbidden changes.
- Golden references and missing golden reference types.
- Common drift risks.
- Current best reusable Codex prompt.

Make the anchor card readable by a human and usable by an LLM. Do not bury real identity constraints only in JSON.

## Identity Anchors

Separate stable identity from temporary styling.

Stable anchors usually include:

```text
face shape
eye shape and spacing
brow shape
nose bridge and tip
mouth shape
jawline
hairline or signature hair structure
age presentation
height and body proportions
distinctive marks or accessories
overall temperament
baseline visual style
```

Temporary attributes usually include:

```text
outfit
lighting
camera angle
background
pose
facial expression
seasonal styling
rendering style variants
```

Only promote a temporary attribute into a stable anchor when the user explicitly says it must always remain.

## Prompt Compiler

Compile every generation request in layers:

```text
raw user request
+ basic identity lock
+ face/body invariants
+ approved golden reference notes
+ allowed variations
+ scene, pose, outfit, or expression request
+ failure avoidance and negative drift rules
+ safety policy
+ Codex image generation prompt
```

Preserve the raw user request in `prompt-library/raw-prompts.jsonl`.

Store compiled prompts in `prompt-library/compiled-prompts.jsonl` with:

```text
raw_request
raw_request_language
anchor_version
expanded_prompt
codex_compiled_prompt
negative_prompt
model_or_provider
reference_images
golden_reference_types
allowed_variations
blocked_variations
safety_status
quality_checks
```

## Consistency Rules

When applying an anchor, preserve the character first and satisfy the scene second.

If the user asks for a new scene, outfit, pose, or style, keep identity anchors fixed unless the user explicitly asks to redesign the character.

If a request conflicts with the anchor, explain the conflict and choose the smallest safe change.

When creating variations, label them as:

```text
identity-preserving
style-variant
outfit-variant
age-unsafe-or-blocked
redesign
```

Do not silently turn a redesign into a same-character variation.

## Quality Loop

Codex performs the first visual review, but user feedback has higher authority.

Review generated outputs with separate 0-5 scores:

```text
identity_score
face_shape_match
facial_feature_match
hair_match
body_proportion_match
outfit_anchor_match
style_match
age_match
reference_alignment
drift_risk
safety_status
user_rating
overall_status
```

Route outputs:

- `approved`: safe and identity-stable outputs approved by the user.
- `candidates`: promising outputs, incomplete-anchor outputs, or outputs awaiting user judgment.
- `failed`: safe but identity-drifting or technically flawed outputs.
- `blocked`: unsafe or policy-risk metadata only.

For approved outputs, record why they worked. For failed outputs, record what drifted and how to avoid it. Only user-approved outputs may be promoted to `references/golden/`.

## Feedback Loop

Treat user feedback as anchor training data.

When the user says something like "doesn't look like them", "the eyes are wrong", "this version is closer", or "keep this feeling next time", update the relevant anchor file.

Record feedback in `feedback/feedback.jsonl`, convert reusable corrections into `feedback/correction-rules.json`, and use them in the next prompt and quality review.

Promote repeated successful patterns into `prompt-library/optimized-recipes.jsonl`.

Promote repeated failures into `anchor-library/negative-rules.md` or `feedback/correction-rules.json`.

## Safety Workflow

Run safety checks before ingest, before prompt compilation, and after generation.

- Keep minor, childhood, student-age, and age-uncertain references out of adult-oriented workflows.
- Never use minor or age-uncertain references for sexualized, revealing, romanticized, or adult-oriented outputs.
- Block explicit nudity, erotic framing, fetish content, sexualized minors, and overexposure.
- For unsafe outputs from external models, store only minimal metadata and safety reasons in `outputs/blocked/`.
- Prefer safe rewrites for ordinary portrait, fashion, or character design requests.
- Refuse when the core intent is unsafe.

## Model Adapters

Keep the anchor model-agnostic while using Codex image generation as the default adapter.

Store provider details in `adapters/model-providers.json`.

Maintain a neutral compiled prompt before adapting it for Codex image generation, OpenAI image APIs, Midjourney, Stable Diffusion, Flux, ComfyUI, Runway, or other systems.

Model adapters may change formatting, parameter names, and reference-image syntax, but must not weaken identity anchors, golden-reference policy, feedback rules, or safety rules.

## Training Package

Only prepare training manifests from authorized, safe, high-quality data.

Use `training-package/manifest.json` to list:

```text
included images
excluded images
captions
anchor version
identity notes
safety exclusions
quality scores
target adapter type
```

Do not include minor or age-uncertain media in adult identity training sets.
