# Contributing

Thank you for improving Character Anchor Skill.

This project is a workflow MVP for character consistency in AI image and video generation. Contributions should keep the repository safe, reusable, and free of private test data.

## Ground Rules

- Do not commit private, real-person, or user-provided media.
- Do not commit local test character libraries.
- Keep the public demo fictional and text-only unless a future release explicitly adds safe generated assets.
- Keep safety and authorization language conservative.
- Update `docs/review-log.md` for every review, bug fix, product workflow change, or release-readiness check.
- Back up the current version before making version-level changes.

## Local Test Characters

Local character libraries under `characters/` are ignored by default. This protects private experiments and authorized real-person material from accidental publication.

Only `characters/mira-vale/` is intended for the public package.

## Before Opening A Pull Request

Run:

```bash
python scripts/validate_character_anchor.py characters/mira-vale
python scripts/compile_prompt.py characters/mira-vale --request "Mira walks through a rain-soaked train station at night, holding her notebook." --provider provider-neutral
```

Also check that no private test names or media paths are present in public files.

## Documentation

When changing workflow behavior, update the relevant docs and `docs/review-log.md`.

Recommended docs to check:

- `README.md`
- `README.zh-CN.md`
- `docs/golden-gallery-workflow.md`
- `docs/reference-quality-gate.md`
- `docs/media-coverage-audit.md`
- `docs/schemas.md`
- `docs/safety-policy.md`
