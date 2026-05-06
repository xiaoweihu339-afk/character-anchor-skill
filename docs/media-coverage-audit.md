# Media Coverage Audit

## Purpose

When users upload hundreds or thousands of images and videos, an AI reviewer may take shortcuts: create a few contact sheets, inspect only a sample, or skip most video content.

This is dangerous because the user may believe the whole dataset was reviewed when only a small subset was inspected.

The media coverage audit makes review coverage explicit.

## Core Rule

Sampling is allowed for triage, but sampling must be labeled as sampling.

Do not present sampled review as full review.

The system must be honest with the user about what it actually reviewed.

Before golden candidate generation, show a user-facing coverage summary that answers:

- how many images were uploaded
- how many images were inspected
- how many videos were uploaded
- how many videos were inspected
- how many frames were extracted from videos
- which files or batches remain unprocessed
- whether the current selection is safe for final golden reference promotion or only good enough for preview
- where the usable references are stored
- whether the next step should be deeper screening or golden candidate generation

## Required Coverage Record

For each ingest session, record:

- total image count
- total video count
- total Live Photo count
- processed image count
- processed video count
- extracted frame count
- contact sheet count
- skipped file count
- unprocessed file count
- coverage status
- coverage notes

## Coverage Status

Use one of:

- `full_review`: all eligible media inspected.
- `batched_review`: all media scheduled and processed in batches.
- `sampled_preview`: only a sample was inspected.
- `partial_review`: some media processed, some unprocessed.
- `user_selected_only`: only files chosen by the user were reviewed.

## Video Handling

Videos should not be treated as one thumbnail.

Recommended strategies:

- extract frames at fixed intervals
- extract scene-change frames
- include first, middle, and last frames
- flag videos with too few extracted frames
- record frame count per video
- keep extracted frames linked to the source video

## Contact Sheets

Contact sheets are useful for quick scanning, but they are not enough by themselves.

Record:

- which files are represented in each contact sheet
- how many total files were not represented
- whether the contact sheet was used only for preview
- whether the user approved using sampled review

## User-Facing Report

Before selecting golden references or generating golden candidates, report:

```text
Total media: 1240 images, 37 videos
Processed: 1240 images, 37 videos
Extracted video frames: 740
Coverage status: full_review
Unprocessed files: 0
```

If partial:

```text
Coverage status: sampled_preview
Only 120 of 1240 images were reviewed.
Only 3 of 37 videos were sampled.
This is a preview, not a full review.
Do not promote golden references until the user approves partial review or requests full processing.
```

After reporting coverage, ask the user to choose:

```text
Usable references are available at: references/golden/

Choose next step:
1. Continue deeper screening.
2. Generate golden image candidates from the current usable references.
```

## Promotion Rule

References should not enter `references/golden/` unless they come from reviewed media.

If a reference comes from sampled or partial review, record that status and ask for user confirmation before promotion.
