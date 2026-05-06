# Character Anchor Architecture

## Purpose

Build a reusable, model-agnostic character anchor library that keeps a character recognizable across outputs. The library stores assets, but its purpose is identity consistency: stable anchors, controlled variation, drift detection, feedback learning, and safe reuse.

## Main Loop

```text
authorized input
-> archive and safety screen
-> anchor card creation
-> golden reference selection
-> anchor-library updates
-> prompt compilation
-> model adapter formatting
-> post-generation review
-> approved/candidate/failed/blocked routing
-> successful product gallery archive
-> user feedback capture
-> anchor and prompt rule updates
-> optional training-package export
```

## Layers

- `Identity Layer`: non-negotiable face, body, age presentation, and character identity traits.
- `Variation Layer`: allowed changes such as outfit, pose, camera, lighting, scene, expression, and rendering style.
- `Style Layer`: baseline aesthetics and optional style variants.
- `Feedback Layer`: user taste, correction notes, repeated success patterns, and repeated drift patterns.
- `Safety Layer`: age, consent, NSFW, exposure, voice, and publication constraints.
- `Model Adapter Layer`: provider-neutral prompts and provider-specific payloads.

## Libraries

- `anchor-card.md`: human-readable source of truth for the character.
- `references/`: raw media, golden references, rejected references, and indexes.
- `anchor-library/`: identity anchors, face/body/style descriptions, invariants, allowed variations, and negative rules.
- `prompt-library/`: raw requests, compiled prompts, and optimized recipes.
- `outputs/`: approved outputs, product-gallery archive, candidates, failed outputs, and blocked metadata routing.
- `feedback/`: user ratings, correction data, and reusable rules.
- `adapters/`: model/provider definitions and formatting choices.
- `quality/`: review rubrics, scores, and drift analysis.
- `training-package/`: optional manifests for LoRA, Face Adapter, or other training workflows.

## Anchor Card First

Create or update `anchor-card.md` before optimizing prompts. Keep it short enough to read, but specific enough to prevent identity drift.

The anchor card should answer:

- Who is this character?
- What must remain recognizable?
- What can safely change?
- Which references are golden?
- What failures have already happened?
- What is the current best reusable prompt?

## Golden Reference Selection

Use a small set of high-quality anchors instead of every uploaded image. Prefer:

- Clear frontal face.
- Several expressions without extreme filters.
- Natural lighting.
- Representative side/profile references.
- Back-view, long-shot, and motion references when the character will be used for video keyframes.
- Representative body/proportion references when relevant.
- Adult-safe references when adult outputs are requested.

Do not let low-quality, heavy-filter, distorted, childhood, or age-uncertain media become active adult-oriented identity anchors.

## Prompt Cards

Every approved output should have a prompt card in `outputs/approved/prompt-cards/`. A prompt card makes the successful result reusable by humans and models.

Include:

- Output path.
- Raw user request.
- Anchor version.
- Reusable expanded prompt.
- Concise prompt.
- Negative prompt.
- References used.
- Model/provider metadata.
- Review scores.
- Success reasons.
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
```

Keep version history in `profile.json` and `quality/scores.jsonl`.
