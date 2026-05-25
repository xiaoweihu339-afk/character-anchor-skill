# Character Anchor Schemas

Use JSON for structured files and JSONL for append-only event logs. Keep paths relative to the character root unless a tool requires absolute paths.

The current schema version is `1.1.0`.

## profile.json

```json
{
  "schema_version": "1.1.0",
  "character_id": "example-character",
  "display_name": "Example Character",
  "anchor_version": "1.1.0",
  "created_at": "2026-05-24T00:00:00+08:00",
  "updated_at": "2026-05-24T00:00:00+08:00",
  "status": "draft",
  "wizard_state": "profile_started",
  "codex_image_model_first": true,
  "basic_identity": {
    "gender_or_presentation": null,
    "age_presentation": null,
    "height": null,
    "body_type": null,
    "temperament": null,
    "visual_style": null
  },
  "golden_required_types": [
    "front-closeup",
    "left-closeup",
    "right-closeup",
    "full-body-face-visible"
  ],
  "active_golden_refs": {
    "front-closeup": null,
    "left-closeup": null,
    "right-closeup": null,
    "full-body-face-visible": null
  },
  "drift_thresholds": {
    "minimum_identity_score": 4,
    "maximum_drift_risk": 2
  },
  "authorization_status": "user_asserted_authorized",
  "age_policy": {
    "declared_adult": null,
    "age_uncertain": true,
    "minor_safe_mode": true
  },
  "version_history": [],
  "notes": []
}
```

## consent.json

```json
{
  "schema_version": "1.1.0",
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
  "schema_version": "1.1.0",
  "items": [
    {
      "id": "ref_0001",
      "path": "references/raw/ref_0001.png",
      "source": "user_upload",
      "authorization_status": "user_asserted_authorized",
      "age_status": "unknown",
      "quality": "draft",
      "role": "raw",
      "golden_type": null,
      "user_approved": false,
      "active": false,
      "notes": []
    }
  ]
}
```

Allowed `golden_type` values are `front-closeup`, `left-closeup`, `right-closeup`, and `full-body-face-visible`.

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

## prompt-library/compiled-prompts.jsonl

Each line:

```json
{
  "prompt_id": "prompt_20260524_0001",
  "raw_request": "",
  "raw_request_language": "zh-CN",
  "anchor_version": "1.1.0",
  "expanded_prompt": "",
  "codex_compiled_prompt": "",
  "negative_prompt": "",
  "model_or_provider": "codex-image",
  "reference_images": [],
  "golden_reference_types": [],
  "allowed_variations": [],
  "blocked_variations": [],
  "safety_status": "pending",
  "quality_checks": [],
  "created_at": "2026-05-24T00:00:00+08:00"
}
```

## quality/scores.jsonl

Each line:

```json
{
  "score_id": "score_20260524_0001",
  "output_id": "",
  "prompt_id": "",
  "output_path": "",
  "reference_images": [],
  "codex_scores": {
    "identity_score": null,
    "face_shape_match": null,
    "facial_feature_match": null,
    "hair_match": null,
    "body_proportion_match": null,
    "outfit_anchor_match": null,
    "style_match": null,
    "age_match": null,
    "reference_alignment": null,
    "drift_risk": null
  },
  "drift_notes": [],
  "user_feedback_summary": null,
  "overall_status": "candidate",
  "eligible_for_golden_promotion": false,
  "created_at": "2026-05-24T00:00:00+08:00"
}
```

## outputs/approved/prompt-cards

Use Markdown. Include these sections:

```markdown
# Output Title

## Output
output_path:

## Raw User Request

## Anchor Version

## Codex Compiled Prompt

## Reusable Expanded Prompt

## Concise Prompt

## Negative Prompt

## References Used

## Golden References Used

## Model And Parameters

## Codex Review Scores

## User Feedback

## Success Reasons

## Golden Promotion

## Safe Variations
```

## feedback/feedback.jsonl

Each line:

```json
{
  "feedback_id": "feedback_20260524_0001",
  "output_id": "",
  "prompt_id": "",
  "user_rating": null,
  "identity_similarity": null,
  "liked_points": [],
  "disliked_points": [],
  "reuse_as_reference": false,
  "golden_promotion_type": null,
  "correction_notes": [],
  "correction_rule_candidates": [],
  "created_at": "2026-05-24T00:00:00+08:00"
}
```

## feedback/correction-rules.json

```json
{
  "schema_version": "1.1.0",
  "identity_corrections": [],
  "face_corrections": [],
  "style_corrections": [],
  "composition_corrections": [],
  "technical_corrections": [],
  "prompt_corrections": [],
  "scoring_adjustments": []
}
```

## adapters/model-providers.json

```json
{
  "schema_version": "1.1.0",
  "default_llm": "codex",
  "default_vision_reviewer": "codex-vision",
  "default_image_generator": "codex-image",
  "providers": [
    {
      "provider_id": "codex-image",
      "adapter_type": "image_generator",
      "interface": "codex_builtin",
      "enabled": true,
      "default": true,
      "input_contract": {
        "prompt": "string",
        "reference_images": "array?",
        "size": "string?",
        "quality": "string?"
      },
      "output_contract": {
        "image_path": "string",
        "metadata": "object"
      },
      "safety_notes": []
    }
  ],
  "privacy_mode": {
    "prefer_local_for_biometrics": true,
    "allow_remote_generation": null
  }
}
```

## training-package/manifest.json

```json
{
  "schema_version": "1.1.0",
  "anchor_version": "1.1.0",
  "target_adapter_type": null,
  "included_images": [],
  "excluded_images": [],
  "captions": [],
  "safety_exclusions": [],
  "quality_notes": []
}
```
