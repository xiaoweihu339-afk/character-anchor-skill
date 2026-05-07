# Character Anchor Schemas

Use JSON for structured files and JSONL for append-only event logs. Keep paths relative to the character root unless a tool requires absolute paths.

## profile.json

```json
{
  "schema_version": "1.0.0",
  "character_id": "example-character",
  "display_name": "Example Character",
  "anchor_version": "0.1.0",
  "created_at": "2026-05-05T00:00:00+08:00",
  "updated_at": "2026-05-05T00:00:00+08:00",
  "status": "draft",
  "authorization_status": "user_asserted_authorized",
  "age_policy": {
    "declared_adult": null,
    "age_uncertain": true,
    "minor_safe_mode": true
  },
  "notes": []
}
```

## consent.json

```json
{
  "schema_version": "1.0.0",
  "source_type": "fictional_or_user_authorized",
  "user_asserted_authorized": null,
  "allowed_uses": [],
  "disallowed_uses": [],
  "public_release_allowed": null,
  "notes": []
}
```

## references/index.json

```json
{
  "schema_version": "1.0.0",
  "items": [
    {
      "id": "ref_0001",
      "path": "references/raw/ref_0001.png",
      "source": "user_upload",
      "authorization_status": "user_asserted_authorized",
      "age_status": "unknown",
      "subject_role": "target",
      "contains_other_people": false,
      "other_people_count": 0,
      "target_visibility": "clear",
      "recommended_action": "keep",
      "reference_use": [
        "face_anchor"
      ],
      "quality_scores": {
        "face_visibility": null,
        "sharpness": null,
        "lighting": null,
        "identity_stability": null,
        "subject_isolation": null,
        "overall_reference_quality": null
      },
      "quality_failure_reasons": [],
      "quality": "draft",
      "role": "raw",
      "notes": []
    }
  ]
}
```

## quality/coverage/coverage-manifest.json

Created by `scripts/audit_media_coverage.py --write --character-root characters/<character-id>`. This is an inventory manifest, not a visual review certificate:

```json
{
  "schema_version": "1.0.0",
  "created_at": "2026-05-05T00:00:00+08:00",
  "source_root": "C:/path/to/raw-media",
  "review_stage": "inventory_only",
  "coverage_status": "inventory_only_not_visual_review",
  "total_files": 0,
  "total_images": 0,
  "total_videos": 0,
  "total_unsupported_files": 0,
  "processed_images": 0,
  "processed_videos": 0,
  "sampled_images": 0,
  "sampled_videos": 0,
  "inspected_video_frames": 0,
  "coverage_honesty_note": "",
  "recommended_next_step": "",
  "inventory_preview": [],
  "inventory_preview_omitted_files": 0
}
```

Suggested `coverage_status` values:

- `inventory_only_not_visual_review`
- `full_review`
- `batched_review`
- `sampled_preview`
- `partial_review`
- `user_selected_only`

## quality/face-lock/face-lock.json

Created by `scripts/update_face_lock.py`. This file sits between usable reference selection and golden-candidate generation. It records stable face geometry as relative ratios so future prompts, external image workflows, and user feedback can tune the same identity instead of starting over.

```json
{
  "schema_version": "1.0.0",
  "status": "estimated",
  "measurement_unit": "relative_ratio",
  "source_references": [
    "ref_0001"
  ],
  "face_geometry": {
    "face_length_to_width": 1.42,
    "forehead_height_ratio": null,
    "eye_spacing_ratio": 1.0,
    "eye_width_ratio": null,
    "brow_to_eye_distance_ratio": 0.18,
    "nose_length_ratio": null,
    "nose_width_ratio": null,
    "mouth_width_ratio": 0.42,
    "upper_lip_to_lower_lip_ratio": null,
    "jaw_width_ratio": 0.72,
    "chin_length_ratio": null,
    "cheekbone_width_ratio": 0.86
  },
  "qualitative_locks": [
    "moderate eye spacing",
    "softly tapered jaw"
  ],
  "tuning_notes": [
    "jaw should be less sharp"
  ],
  "updated_at": "2026-05-05T00:00:00+08:00"
}
```

Suggested `status` values:

- `draft`
- `estimated`
- `reviewed`
- `locked`

## outputs/candidates/golden-generation-requests/*.json

Created by `scripts/generate_golden.py`. This is an external generation request payload, not an image output:

```json
{
  "schema_version": "1.0.0",
  "request_id": "golden_request_20260505_000000_000000",
  "character_id": "example-character",
  "display_name": "Example Character",
  "anchor_version": "0.3.0",
  "provider": "provider-neutral",
  "status": "request_payload_only",
  "honesty_note": "This script does not generate images by itself.",
  "raw_request": "",
  "reference_images": [],
  "coverage_targets": [
    "front_face",
    "three_quarter_face",
    "ninety_degree_profile",
    "back_view",
    "upper_body",
    "full_body",
    "long_shot_silhouette",
    "motion_reference"
  ],
  "identity_inputs": {
    "anchor_card": "",
    "face_anchor": "",
    "face_lock": {},
    "body_anchor": "",
    "negative_rules": ""
  },
  "quality_gate_before_promotion": [],
  "reference_validation": "approved_golden_references_only",
  "suggested_output_route": "outputs/candidates/"
}
```

## anchor-library/invariants.md

Use Markdown. Capture identity traits that should not change across normal variations:

```markdown
# Invariants

## Face

## Hair

## Body And Proportions

## Age Presentation

## Distinctive Details

## Temperament
```

## anchor-library/allowed-variations.md

Use Markdown. Separate allowed variation from redesign:

```markdown
# Allowed Variations

## Outfit

## Pose

## Expression

## Scene

## Camera And Lighting

## Style

## Requires User Confirmation
```

## prompt-library/raw-prompts.jsonl

Each line:

```json
{
  "prompt_id": "prompt_20260505_0001",
  "raw_request": "",
  "anchor_version": "0.1.0",
  "model_or_provider": "provider-id",
  "reference_images": [],
  "created_at": "2026-05-05T00:00:00+08:00"
}
```

## prompt-library/compiled-prompts.jsonl

Each line:

```json
{
  "prompt_id": "prompt_20260505_0001",
  "raw_request": "",
  "anchor_version": "0.1.0",
  "expanded_prompt": "",
  "negative_prompt": "",
  "model_or_provider": "provider-id",
  "reference_images": [],
  "allowed_variations": [],
  "blocked_variations": [],
  "safety_status": "requires_review",
  "quality_checks": [],
  "created_at": "2026-05-05T00:00:00+08:00"
}
```

Suggested `safety_status` values:

- `requires_review`: compiled but not safety-reviewed.
- `approved_safe`: reviewed and safe for the intended use.
- `blocked`: unsafe or unauthorized.
- `not_evaluated`: safety status is unknown.

## outputs/approved/prompt-cards

Use Markdown. Include these sections:

```markdown
# Output Title

## Output
output_path:

## Raw User Request

## Anchor Version

## Reusable Expanded Prompt

## Concise Prompt

## Negative Prompt

## References Used

## Model And Parameters

## Review Scores

## Success Reasons

## Safe Variations
```

## outputs/candidates/index.jsonl

Each line:

```json
{
  "candidate_id": "candidate_20260506_0001",
  "output_path": "outputs/candidates/candidate_20260506_0001.png",
  "prompt_id": "",
  "raw_request": "",
  "reference_images": [],
  "model_or_provider": "",
  "face_similarity": null,
  "user_likeness_rating": null,
  "identity_score": null,
  "failure_reasons": [],
  "recommended_action": "retry",
  "promote_to_golden": false,
  "created_at": ""
}
```

## outputs/failed/index.jsonl

Each line:

```json
{
  "failed_id": "failed_20260506_0001",
  "output_path": "outputs/failed/failed_20260506_0001.png",
  "prompt_id": "",
  "failure_reasons": [
    "face_drift"
  ],
  "drift_notes": [],
  "retry_suggestions": [],
  "created_at": ""
}
```

## outputs/product-gallery/index.jsonl

Each line:

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

See `docs/product-gallery.md` for workflow notes and promotion rules.

## feedback/feedback.jsonl

Each line:

```json
{
  "feedback_id": "feedback_20260505_0001",
  "output_id": "",
  "prompt_id": "",
  "user_rating": null,
  "identity_similarity": null,
  "liked_points": [],
  "disliked_points": [],
  "reuse_as_reference": false,
  "promote_to_golden_candidate": false,
  "correction_notes": [],
  "created_at": "2026-05-05T00:00:00+08:00"
}
```

## feedback/correction-rules.json

```json
{
  "schema_version": "1.0.0",
  "identity_corrections": [],
  "style_corrections": [],
  "composition_corrections": [],
  "technical_corrections": [],
  "prompt_corrections": []
}
```

## adapters/model-providers.json

```json
{
  "schema_version": "1.0.0",
  "default_llm": null,
  "default_vision_reviewer": null,
  "default_image_generator": null,
  "providers": [],
  "privacy_mode": {
    "prefer_local_for_biometrics": true,
    "allow_remote_generation": null
  }
}
```

## training-package/manifest.json

```json
{
  "schema_version": "1.0.0",
  "anchor_version": "0.1.0",
  "target_adapter_type": null,
  "included_images": [],
  "excluded_images": [],
  "captions": [],
  "safety_exclusions": [],
  "quality_notes": []
}
```
