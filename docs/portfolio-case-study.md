# Portfolio Case Study

## Project

Character Anchor Skill

## Problem

AI-generated characters often drift across outputs. Users may upload many source images, videos, or Live Photos, but the raw material is usually messy: different lighting, angles, expressions, quality levels, outfits, and identity stability. Without a curated reference workflow, future images and video keyframes easily lose face similarity, body proportions, age presentation, posture, temperament, wardrobe logic, or acting style.

## Solution

Character Anchor Skill treats a character as a reusable golden reference system instead of a single face image. It starts from raw character media, filters usable references, supports the creation of AI-generated golden reference candidates, records user approval, and then uses the approved golden gallery for future image and video keyframe generation.

Face consistency is the core quality target. Body proportion, presence, motion, wardrobe logic, and temperament are secondary anchors that make the character feel continuous across scenes.

The MVP reserves a product gallery structure where successful product images and their prompts can be collected. This can help the user browse previous outputs, help the system learn user preference, and support promotion into future golden references when outputs are identity-stable.

## MVP

The first version includes:

- a standard character anchor library structure
- initialization and validation scripts
- prompt compilation from raw scene request to expanded character-consistent prompt
- a fictional demo character, Mira Vale
- documentation for architecture, schemas, safety, and model adapters
- a documented golden gallery workflow for future image/video reference generation
- a product gallery concept for successful user-approved outputs and prompt reuse

## Design Decision

The MVP is file-based and model-agnostic. This makes it easy to inspect, version, publish, and adapt to different AI tools such as image generators, video generators, local ComfyUI workflows, face reference tools, and manual prompt workflows.

Safety is part of the initial design instead of a later patch. The MVP requires consent metadata, minor-safe defaults for age uncertainty, NSFW blocking rules, and separate routing for rejected or blocked material.

## What This Demonstrates

- AI workflow product thinking
- raw media curation and reference selection logic
- golden reference gallery design
- product image and prompt archive design
- prompt engineering beyond one-off prompting
- structured data and JSONL event logs
- safety-aware handling of character assets
- consent and authorization-aware workflow design
- continuity design for AI video and fictional characters

## Next Milestones

- Add image and video reference indexing.
- Add golden reference candidate generation.
- Add user approval and rejection workflows.
- Add product gallery browsing and prompt reuse.
- Add prompt cards for approved outputs.
- Add provider adapters.
- Add face-focused visual review rubrics and scoring helpers.
- Build a small UI for browsing anchors and compiling prompts.
