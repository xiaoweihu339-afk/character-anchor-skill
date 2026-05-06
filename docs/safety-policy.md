# Safety Policy

## Priority

Safety policy overrides identity consistency, user preference, aesthetic goals, and provider-specific features.

## Consent And Authorization

Only build or update a character anchor library when the user indicates they have rights or authorization for the source media. If authorization is unclear, ask before processing private biometric media.

## Age Rules

- If the subject is a minor, only allow ordinary, non-sexual, age-appropriate content.
- If age is uncertain, treat the subject as a minor for safety decisions.
- If authorized media includes childhood or student-age material, record it only as rejected/non-active metadata unless there is a safe, age-appropriate reason to retain it.
- Do not store unsafe or unauthorized real-person media as reusable files.
- Do not use minor or age-uncertain media as an anchor for adult, romantic, revealing, or glamorized generation.

## Blocked Content

Block requests or outputs involving:

- NSFW or explicit sexual content.
- Nudity or visible sexual body parts.
- Sexualized minors or age-ambiguous sexual framing.
- Excessive exposure, transparent clothing used for erotic effect, or fetish framing.
- Erotic posing, suggestive biting/licking/framing, or adult-service implications.
- Requests to make a person look younger for sexualized content.
- Voice cloning or impersonation without explicit authorization.

## Safe Rewrite

When the user's request is mostly safe but contains risky wording, rewrite toward:

- Ordinary portrait.
- Fashion editorial without erotic framing.
- Age-appropriate daily life.
- Non-revealing styling.
- Neutral camera language.

If the unsafe intent is central, refuse and offer a safe alternative.

## Output Handling

Unsafe generated outputs must not enter:

- `outputs/approved/`
- `outputs/candidates/`
- `outputs/failed/`
- `training-package/`
- active prompt recipes

Record metadata only in `outputs/blocked/index.jsonl`: timestamp, prompt id, provider, risk labels, and blocked reason.
