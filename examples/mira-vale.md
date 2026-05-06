# Mira Vale Demo

Mira Vale is a fictional adult character included to demonstrate text-only character anchoring.

## Test Request

```text
Mira walks through a rain-soaked train station at night, holding her notebook.
```

## Command

```bash
python scripts/compile_prompt.py characters/mira-vale --request "Mira walks through a rain-soaked train station at night, holding her notebook." --provider provider-neutral
```

Add `--write` if you want to append the prompt to the character's JSONL logs.

## What To Check

The compiled prompt should preserve:

- adult age presentation
- oval face and calm almond eyes
- lean medium-height body proportions
- reserved posture
- quiet, observant presence
- practical wardrobe logic
- cinematic realism

It should block:

- teen-like styling
- generic beauty drift
- glamour redesign
- body-proportion drift
- bubbly or seductive personality replacement
