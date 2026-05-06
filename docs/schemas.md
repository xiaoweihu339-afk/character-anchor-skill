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

## references/coverage-manifest.json (planned)

Future-only suggested shape for large media ingestion. The current MVP does not create or validate this file yet:

```json
{
  "schema_version": "1.0.0",
  "coverage_status": "partial_review",
  "total_images": 0,
  "total_videos": 0,
  "total_live_photos": 0,
  "processed_images": 0,
  "processed_videos": 0,
  "processed_live_photos": 0,
  "video_frame_strategy": {
    "method": "interval_and_scene_change",
    "frame_interval_seconds": null,
    "scene_change_detection": false,
    "max_frames_per_video": null
  },
  "contact_sheets": [],
  "batches": [],
  "skipped_files": [],
  "unprocessed_files": [],
  "coverage_notes": []
}
```

Suggested `coverage_status` values:

- `full_review`
- `batched_review`
- `sampled_preview`
- `partial_review`
- `user_selected_only`

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
