# Product Gallery

## Purpose

The product gallery stores successful generated images and video keyframes that users actually like. It is the user's personal result archive and one of the most valuable learning sources for prompt optimization.

Golden references and product images are related, but not the same:

- Golden references guide future generation.
- Product images are finished outputs created for user requests.

Some product images can later be promoted into golden references after review.

## Why Store Product Images

Successful product images reveal:

- what the user wants
- which prompt patterns worked
- which golden references were useful
- which model settings worked
- what visual taste the user prefers
- which images are worth reusing or adapting

This makes the skill faster and more personalized over time.

## Suggested Record

Each line in `outputs/product-gallery/index.jsonl` should follow this shape:

```json
{
  "product_id": "product_20260506_0001",
  "output_path": "outputs/product-gallery/product_20260506_0001.png",
  "raw_request": "",
  "compiled_prompt": "",
  "negative_prompt": "",
  "golden_references": [],
  "model_or_provider": "",
  "model_parameters": {},
  "user_rating": null,
  "liked_points": [],
  "identity_similarity": null,
  "body_similarity": null,
  "presence_similarity": null,
  "reuse_intent": [],
  "promote_to_golden_candidate": false,
  "created_at": ""
}
```

## Optimization Uses

The product gallery can feed:

- prompt optimization
- golden gallery refinement
- user preference modeling
- portfolio browsing
- repeated scene generation
- video keyframe continuity

## Promotion Rule

A product image should only be promoted into the golden gallery when it is:

- liked by the user
- authorized
- safe
- strong in face similarity
- identity-stable
- useful as a future reference

A beautiful output that drifts from the character should remain a product image, not a golden identity reference.
