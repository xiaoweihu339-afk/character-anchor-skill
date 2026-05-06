# Golden Gallery Workflow

## Purpose

The golden gallery is the core output of Character Anchor Skill. It is a curated set of approved reference images that can be reused whenever a user needs to generate new images or video keyframes of the same person or character.

The user may start with many raw materials:

- photos
- screenshots
- video clips
- Live Photos
- generated images
- previous keyframes
- failed outputs
- user feedback

The skill should turn this messy input into a clean, reusable reference system.

## Main Pipeline

```text
raw media upload
-> media inventory and coverage audit
-> authorization and safety check
-> primary subject identification
-> technical quality filtering
-> reference quality gate
-> identity-stable reference selection
-> coverage and usable-reference report
-> user chooses deeper screening or generation
-> golden candidate generation
-> face similarity and likeness review
-> user review
-> golden gallery coverage gap report
-> approved golden gallery
-> scene or keyframe generation
-> successful product image archive
-> feedback and correction rules
```

Unsafe or unauthorized media exits the active workflow:

```text
unauthorized media -> blocked metadata only
unsafe prompt/output -> blocked metadata
low-quality or identity-drifting media -> references/rejected/
```

## Media Inventory And Coverage Audit

For large uploads, do not let a contact sheet or small sample become the whole review. Sampling can help triage, but it must be labeled as sampling.

Before reference cleaning, record:

- total image count
- total video count
- total Live Photo count
- total processed image count
- total processed video count
- video frame extraction strategy
- frame interval or scene-change method
- contact sheets created
- files skipped and why
- coverage percentage
- whether the current review is full, partial, sampled, or user-selected

Rules:

- Do not claim full review if only sampled contact sheets were inspected.
- Before generating golden candidates, tell the user how many images, videos, and extracted frames were actually reviewed.
- Do not promote references from unprocessed videos.
- For videos, extract frames by interval and scene change when possible.
- For large batches, process in batches and keep a manifest for every batch.
- If coverage is partial, report what remains unprocessed.
- Let the user decide whether to continue deeper screening or generate golden candidates from the current usable references.

Suggested coverage statuses:

- `full_review`: all eligible media inspected.
- `batched_review`: all media scheduled and processed in batches.
- `sampled_preview`: only a sample was inspected; not enough for final selection.
- `partial_review`: some media processed, some unprocessed.
- `user_selected_only`: only user-marked files were reviewed.

## Reference Cleaning

Raw media should be split into:

- `references/raw/`: archived original material.
- `references/rejected/`: authorized but low-quality, technically flawed, identity-drifting, or not useful as a reference.
- `references/golden/`: approved references that can be reused as identity anchors.

Do not store unauthorized real-person media as reusable files. Keep only minimal blocked metadata for authorization failures. Do not place unauthorized, NSFW, minor-unsafe, or age-uncertain adult-oriented media into `references/golden/`.

Filtering should consider:

- whether the target character is clearly identifiable
- whether other people appear in the frame
- whether the image needs cropping, masking, or rejection before it can be used
- face visibility
- image sharpness
- lighting quality
- angle usefulness
- age presentation
- expression clarity
- body proportion visibility
- styling relevance
- identity stability
- hard defects that make the reference unsafe for AI identity anchoring

## Reference Quality Gate

Do not rely on a single broad AI judgment such as "good reference" or "bad reference". Split reference screening into explicit gates.

Hard reject or quarantine references with:

- blurred or low-resolution face
- extreme compression artifacts
- heavy beauty filter or face distortion
- face too small or partially hidden
- strong motion blur
- extreme lighting that changes facial structure
- multiple prominent people
- target subject unclear
- age presentation mismatch
- expression too extreme for identity anchoring

Classify surviving references by use:

- `face_anchor`: clear face identity, useful for likeness.
- `angle_anchor`: useful side/profile or 3/4 angle.
- `expression_anchor`: useful expression, only if identity remains stable.
- `body_anchor`: useful full-body or proportion reference.
- `wardrobe_anchor`: useful clothing logic, not identity.
- `style_anchor`: useful visual style, not identity.
- `context_only`: useful scene context, not identity.
- `reject`: should not affect generation.

Recommended workflow:

1. Keep more raw media than you promote.
2. Let AI remove hard-defect references and classify the survivors by role.
3. Report coverage, rejected counts, usable reference counts, and usable reference location to the user.
4. Ask whether to continue deeper screening or generate golden candidates from the current usable references.
5. Never let low-confidence or hard-defect references enter `references/golden/`.
6. If golden candidates look unlike the target, audit the source references before changing the generation model.

The goal is not to keep many references. The goal is to keep references that reliably preserve identity.

Source references are AI-filtered for technical usability. Generated golden images are user-reviewed for likeness.

## Primary Subject Identification

Raw media often contains more than one person. Before selecting golden references, identify which person is the target character and prevent other faces or bodies from entering the active identity anchor.

For each raw reference, record:

- target subject presence
- number of other visible people
- whether other faces are prominent
- whether the target is cropped, occluded, or too small
- whether the image should be cropped, masked, rejected, or kept as context-only

Suggested routing:

- Clear target-only image: eligible for `references/golden/`.
- Target plus minor background people: crop or mask before promotion.
- Multiple prominent people: keep in `references/raw/` only, or reject for identity anchoring.
- Unclear target identity: reject until the user identifies the target.
- Unauthorized additional people: metadata-only blocked route unless authorization is confirmed.

Do not promote a reference into the golden gallery if the model may learn another person's face, body, or style as part of the target character.

## Golden Candidate Generation

After selecting usable references, the workflow should generate candidate golden references. The goal is not only to create beautiful images. The goal is to create references that are useful for future generation.

Generated candidates are not golden references by default. They must pass identity review before promotion. If a candidate does not resemble the target, route it to `outputs/failed/` or keep it in `outputs/candidates/` with failure notes.

A useful golden gallery should include:

- frontal face
- 3/4 face
- 90-degree side or profile face
- back view for hair, shoulder line, posture, and wardrobe continuity
- neutral expression
- smile or warm expression
- worried or intense expression
- upper-body reference
- full-body proportion reference
- long-shot silhouette reference for distant video keyframes
- motion or action reference
- wardrobe baseline
- style baseline

## Golden Gallery Coverage

Track coverage as a checklist, even when the MVP cannot automatically generate every missing view.

Recommended coverage dimensions:

- `front_face`: frontal face identity.
- `three_quarter_face`: 3/4 angle facial structure.
- `profile_90`: true 90-degree side profile.
- `back_view`: hair, shoulders, posture, and wardrobe back logic.
- `neutral_expression`: stable baseline face.
- `expression_range`: approved emotional range.
- `upper_body`: torso, shoulder line, and hand/arm posture.
- `full_body`: height impression, body proportions, and stance.
- `long_shot`: distant silhouette for video keyframes.
- `motion_reference`: walking, dancing, gesture, or action continuity.
- `wardrobe_baseline`: repeatable clothing logic.
- `style_baseline`: lighting, texture, and rendering baseline.

Before generating scene images or video keyframes, report coverage gaps:

```text
Current coverage: front_face, three_quarter_face, upper_body, full_body
Missing coverage: profile_90, back_view, long_shot, motion_reference
Risk: enough for portrait generation, weak for video keyframes and distant shots
```

Missing coverage does not block every workflow. It should inform the user what the current gallery can support:

- Portrait work can start with strong face and upper-body coverage.
- Video keyframes need profile, back view, long-shot, full-body, and motion coverage.
- Fashion or wardrobe continuity needs front/back wardrobe references.
- Action-heavy scenes need motion references.

Future versions can automatically generate or request missing coverage, but the MVP should at least make the gap visible.

## Approval Loop

User satisfaction is central. Golden references should not be promoted automatically just because they look technically good.

Each candidate should be reviewed for:

- authorization status
- safety status
- face similarity
- age match
- body proportion match
- temperament match
- style usefulness
- future prompt usefulness
- drift risk
- user rating

Only approved candidates become active golden references.

Candidates should not be approved if they are beautiful but unsafe, unauthorized, age-drifting, or identity-drifting.

## Golden Candidate Failure Loop

When golden candidates do not look like the target, diagnose the failure before generating more images.

Record:

- which raw references were used
- which prompt and negative prompt were used
- which model/provider and parameters were used
- face similarity score
- user likeness rating
- what drifted: eyes, nose, mouth, jaw, age, body, hair, expression, or style
- whether the candidate should be retried, rejected, or used only as a style reference

Suggested routing:

- Strong face match and user-approved: promote to `references/golden/`.
- Good composition but weak likeness: keep in `outputs/candidates/` or `outputs/product-gallery/`, not golden.
- Clear identity drift: route to `outputs/failed/` with failure notes.
- Unsafe or unauthorized: route to `outputs/blocked/` as metadata only.

Do not keep generating more golden candidates with the same prompt when the face is wrong. First update `anchor-library/face.md`, `anchor-library/negative-rules.md`, or `feedback/correction-rules.json`.

Minimum promotion rule:

- Face similarity must be strong.
- User must agree it looks like the target.
- Age presentation must match.
- Body/proportion must not conflict with the anchor.
- Safety and authorization must pass.

## Calling The Golden Gallery

When generating a new image or video keyframe, the user should be able to call:

- all golden references
- face-only golden references
- body/proportion references
- expression references
- wardrobe references
- style references
- a specific approved reference by ID

The prompt compiler should combine the selected golden references with:

- raw scene request
- identity rules
- face invariants
- body invariants
- presence rules
- allowed variations
- negative rules
- model-specific adapter formatting

## Core Quality Priority

Face consistency is the highest-priority target. If a result has strong composition but poor face similarity, it should not be approved as an identity-stable output.

Body and presence consistency matter because video keyframes must feel like the same person across movement, distance, outfit changes, and emotional beats.

## Product Gallery

The product gallery is the user's archive of successful generated images or video keyframes. These are not just outputs. They are learning material.

Store successful product images in:

```text
outputs/product-gallery/
  index.jsonl
```

Each item should record:

- product image path
- raw user request
- compiled prompt
- negative prompt
- selected golden references
- model or provider
- model parameters
- user rating
- why the user liked it
- identity similarity notes
- whether it can be promoted into the golden gallery

The product gallery helps with three things:

- The user can review their own finished images.
- The system can learn which prompts and references fit the user's taste.
- Strong product images can become new golden references after approval.

Product images should not be promoted into golden references unless they pass authorization, safety, face similarity, and identity-stability checks.
