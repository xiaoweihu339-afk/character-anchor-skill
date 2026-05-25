# Character Anchor Architecture

## Purpose

Build a reusable character anchor library that keeps a character recognizable across Codex image generation and optional provider-specific workflows. The library stores assets, but its purpose is identity consistency: guided setup, stable anchors, controlled variation, drift detection, feedback learning, and safe reuse.

## v1.1 Main Loop

```text
user starts or continues wizard
-> collect basic identity one field at a time
-> archive and safety-screen original reference
-> build anchor card
-> create or select four required golden references
-> user approves golden references
-> compile Codex image prompt
-> generate candidate output
-> Codex visual review and scoring
-> user approval, rejection, or correction
-> approved/candidate/failed/blocked routing
-> feedback capture and correction rule updates
-> optional model adapter or training-package export
```

## Wizard States

- `profile_started`: profile exists, but basic identity is still incomplete.
- `basic_identity_complete`: name, presentation, age presentation, height, body type, temperament, and visual style are captured.
- `raw_reference_added`: at least one original reference is archived in `references/raw/` and indexed.
- `golden_incomplete`: at least one required golden reference type is missing or not user-approved.
- `anchor_ready`: all required golden reference types are present, user-approved, and active.

If the state is `golden_incomplete`, Codex may generate but must warn about drift risk and route outputs to `outputs/candidates/` by default.

## Required Golden References

Use a small set of high-quality anchors instead of every uploaded image. v1.1 requires four approved golden reference roles:

- `front-closeup`: clear frontal headshot.
- `left-closeup`: left side headshot.
- `right-closeup`: right side headshot.
- `full-body-face-visible`: full body image with visible face.

Golden references should have clear facial information, stable style, no extreme filters, and no identity-distorting pose or camera effect. Do not promote low-quality, heavy-filtered, distorted, childhood, or age-uncertain media into active adult-oriented anchors.

## Layers

- `Identity Layer`: non-negotiable face, body, age presentation, and character identity traits.
- `Wizard Layer`: basic identity fields, setup state, missing steps, and next prompt to ask the user.
- `Golden Reference Layer`: original references, required golden roles, active references, and rejected candidates.
- `Variation Layer`: allowed changes such as outfit, pose, camera, lighting, scene, expression, and rendering style.
- `Style Layer`: baseline aesthetics and optional style variants.
- `Feedback Layer`: user taste, correction notes, repeated success patterns, and repeated drift patterns.
- `Safety Layer`: age, consent, NSFW, exposure, voice, and publication constraints.
- `Model Adapter Layer`: provider-neutral prompts and provider-specific payloads, with Codex image generation as the default.

## Libraries

- `anchor-card.md`: human-readable source of truth for the character.
- `profile.json`: structured identity, wizard state, required golden roles, active references, and version history.
- `references/`: raw media, golden references, rejected references, and indexes.
- `anchor-library/`: identity anchors, face/body/style descriptions, invariants, allowed variations, and negative rules.
- `prompt-library/`: raw requests, Codex compiled prompts, provider-neutral prompts, and optimized recipes.
- `outputs/`: approved, candidate, failed, and blocked output routing.
- `feedback/`: user ratings, correction data, and reusable rules.
- `adapters/`: model/provider definitions and formatting choices.
- `quality/`: review rubrics, scores, and drift analysis.
- `training-package/`: optional manifests for LoRA, Face Adapter, embedding, or other training workflows.

## Anchor Card First

Create or update `anchor-card.md` before optimizing prompts. Keep it short enough to read, but specific enough to prevent identity drift.

The anchor card should answer:

- Who is this character?
- What did the user define in the basic identity wizard?
- What must remain recognizable?
- What can safely change?
- Which required golden references are complete or missing?
- What failures have already happened?
- What is the current best reusable Codex prompt?

## Prompt Cards

Every approved output should have a prompt card in `outputs/approved/prompt-cards/`. A prompt card makes the successful result reusable by humans and models.

Include:

- Output path.
- Raw user request.
- Anchor version.
- Codex compiled prompt.
- Reusable expanded prompt.
- Concise prompt.
- Negative prompt.
- Original reference and golden references used.
- Model/provider metadata.
- Codex review scores.
- User feedback.
- Success reasons.
- Golden promotion status.
- Safe variation ideas.

## Versioning

Version character anchors with semantic or milestone versions:

```text
0.1.0 archived references
0.3.0 draft anchor card
0.5.0 identity and variation rules
0.7.0 prompt recipes and failure rules
0.9.0 feedback-informed stable anchor
1.0.0 stable character anchor library
1.1.0 guided Codex image workflow with required golden references
```

Keep version history in `profile.json` and `quality/scores.jsonl`.
