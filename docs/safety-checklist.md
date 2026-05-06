# Safety Checklist

## MVP Rule

The MVP does not try to solve automated safety classification. It uses explicit gates, metadata, and review rules so unsafe or unauthorized material does not become active reference data.

## Before Ingesting Raw Media

Confirm:

- The user owns the media or is authorized to use it.
- The source is not stolen, scraped, leaked, or private without permission.
- The subject is fictional, user-owned, or authorized.
- Any other visible people are authorized, blurred/cropped out, or excluded from active references.
- The intended use is allowed by the user and by the project policy.
- Age is known, or the workflow will use minor-safe mode.

If authorization is unclear, stop and ask before processing.

## Blocked Requests

Do not support:

- NSFW or explicit sexual generation.
- Nudity, erotic framing, fetish framing, or adult-service implications.
- Sexualized minors or age-ambiguous sexual framing.
- Requests to make a real person appear sexual, nude, younger, or compromised.
- Real-person impersonation without explicit authorization.
- Voice cloning or biometric reuse without explicit authorization.

## Routing

Use these destinations:

- `references/raw/`: archived authorized source material.
- `references/rejected/`: authorized but low-quality, technically flawed, identity-drifting, or not useful reference material.
- `references/golden/`: approved, safe, useful identity references.
- `outputs/product-gallery/`: user-approved successful final outputs.
- `outputs/blocked/`: unsafe output metadata only.

Unauthorized or unsafe real-person media should be recorded as minimal blocked metadata only, not stored as reusable files. Blocked outputs should not be stored as reusable assets.

## Golden Reference Approval

A golden reference must be:

- authorized
- safe
- identity-stable
- useful for future generation
- approved by the user or reviewer

Face consistency is necessary but not sufficient. A face-matching image should still be rejected if it is unsafe, unauthorized, age-drifting, or not useful as a future reference.

## Product Image Promotion

A product image can become a golden reference only when it is:

- liked by the user
- safe
- authorized
- strong in face similarity
- identity-stable
- useful for future prompts

A successful product image can remain in the product gallery even if it should not become a golden reference.
