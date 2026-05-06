# Golden Candidate Review

## Purpose

Golden candidates are generated images that may become golden references, but they are not trusted references yet.

The most common failure is simple: the image looks good, but it does not look like the target person or character. This must be treated as a failed identity candidate, not as a golden reference.

This review applies to AI-generated golden candidates, not to every source reference. Source references should first be filtered by AI for hard defects such as wrong person, blur, occlusion, multi-person contamination, subtitles, watermarks, and unusable framing.

## Review Order

Review in this order:

1. Authorization and safety.
2. Face similarity.
3. User likeness judgment.
4. Age presentation.
5. Body and proportion match.
6. Hair and distinctive marks.
7. Presence and temperament.
8. Style usefulness.
9. Future reference usefulness.

Face similarity comes before style, composition, or beauty.

## Promotion Rule

Promote a candidate into `references/golden/` only when:

- the user agrees it looks like the target
- face similarity is strong
- age presentation matches
- body/proportion does not conflict with the anchor
- the image is safe and authorized
- the image is useful for future generation

## Failure Diagnosis

When a candidate fails, record the drift source:

- eyes changed
- nose changed
- mouth changed
- jaw or chin changed
- age drift
- body proportion drift
- hair drift
- expression drift
- temperament drift
- style overpowering identity
- wrong subject learned from multi-person input

## Retry Strategy

Do not simply generate more candidates with the same prompt.

Instead:

- strengthen `anchor-library/face.md`
- add drift cases to `anchor-library/negative-rules.md`
- update `feedback/correction-rules.json`
- use fewer but cleaner golden source references
- crop or mask references that contain other people
- reduce style words that overpower identity
- prioritize frontal and 3/4 face references before full-scene images

## Routing

- Strong likeness and approved: `references/golden/`
- Good image but weak likeness: `outputs/candidates/`
- Clear identity drift: `outputs/failed/`
- Unsafe or unauthorized: `outputs/blocked/` metadata only
