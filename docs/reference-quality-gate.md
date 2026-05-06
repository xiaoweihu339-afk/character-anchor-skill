# Reference Quality Gate

## Purpose

Poor source reference selection makes every later step slower. If the selected references are blurry, filtered, identity-drifting, crowded, or badly lit, golden candidate generation will produce images that look unlike the target.

The reference quality gate prevents weak references from entering the active identity workflow.

## Core Rule

Do not ask AI to simply "pick the best photos." Require it to remove hard-defect references, explain the usable reference set, and report what it inspected.

Source reference screening is an AI responsibility. The user should not need to judge every raw reference unless they ask for deeper manual control.

The user-facing decision after screening is:

- continue deeper screening, such as more video frames, tighter crops, or stricter target-subject review
- use the current usable references to generate golden image candidates

## Screening Layers

### 1. Technical Quality

Reject or quarantine:

- blurred face
- low resolution
- compression artifacts
- motion blur
- extreme shadows
- overexposure
- heavy filters
- face distortion

### 2. Target Subject Quality

Reject or quarantine:

- target face too small
- target face partially hidden
- target not clearly identified
- multiple prominent people
- other faces close to the target
- cropped face without enough structure

### 3. Identity Stability

Reject or quarantine:

- childhood or age-mismatched references for adult workflows
- extreme expression that changes face structure
- stylized or edited image that changes identity
- heavy makeup that hides stable geometry
- angle too extreme to identify the person

### 4. Use Classification

A surviving reference should be assigned one or more roles:

- `face_anchor`
- `angle_anchor`
- `expression_anchor`
- `body_anchor`
- `wardrobe_anchor`
- `style_anchor`
- `context_only`

Only `face_anchor`, strong `angle_anchor`, and strong `body_anchor` references should influence identity.

## User Decision Point

The user does not need to approve every source reference before golden candidate generation.

Report:

- how many images, videos, and extracted frames were inspected
- how many source references passed hard-defect screening
- how many were rejected or quarantined
- where the usable reference set is stored
- which screening depth was used: full review, batched review, sampled preview, or user-selected only

Then ask:

- Continue deeper screening?
- Or generate golden image candidates from the current usable references?

## If Golden Candidates Look Wrong

Audit the reference set first.

Common causes:

- too many weak references
- reference set contains other people
- style references were treated as identity references
- face reference is low resolution
- expression reference changed facial structure
- filtered photos distorted the face
- model overfit to outfit or makeup

Recommended fix:

1. Audit whether the usable reference set still contains hard defects.
2. Reduce the reference set if weak references slipped through.
3. Keep the clearest face anchors for face generation.
4. Separate style/context references from identity references.
5. Add failure reasons to `quality_failure_reasons`.
6. Retry golden candidate generation with stricter face anchors.

## Minimum Promotion Rule

A reference can become golden only when it is:

- authorized
- safe
- clearly the target subject
- technically usable
- identity-stable
- assigned an appropriate reference role
- passed AI hard-defect screening

The generated golden image, not each source reference, is where user likeness judgment is required.
