# MVP Roadmap

## Two-Day Goal

Publish a GitHub-ready MVP that proves the Character Anchor concept with one fictional character, reusable scripts, clear documentation, a basic validation loop, and a clear golden gallery direction.

## Day 1

- Create independent repository structure.
- Reuse and polish `init_character_anchor.py`.
- Add `compile_prompt.py`.
- Extend anchor files beyond face consistency:
  - body
  - presence
  - motion
  - wardrobe logic
  - voice and dialogue
- Build a fictional demo character.
- Document the raw media to golden gallery workflow.
- Add product gallery concept for successful outputs and prompt reuse.
- Add visible safety and authorization gates.

## Day 2

- Run validation.
- Generate sample compiled prompts.
- Polish README and docs.
- Add portfolio case study.
- Push to GitHub.

## v0.3 Update

The first published MVP proved the file structure and prompt compiler. Real user testing showed that the next useful version needs to start from raw media, not manual text fields.

v0.3 adds a media-first scaffold:

- media coverage inventory
- local HTML review galleries
- external golden-generation request payloads
- golden candidate feedback logging

v0.3 still does not include a built-in image generator or automatic face similarity scoring. See `docs/v0.3-roadmap.md`.

## Not In MVP

- Production-grade real-person reference ingestion.
- Automatic video frame extraction.
- Built-in automatic golden reference generation.
- Automatic golden gallery coverage-gap completion for missing back view, 90-degree profile, long-shot, and motion references.
- Successful product image and prompt archiving.
- Automated NSFW and authorization-risk review.
- Face adapter or LoRA training.
- Automatic face and visual similarity scoring.
- Web UI.
- Direct integration with video generation providers.

These are good next milestones, but the MVP should stay small enough to test and publish.
