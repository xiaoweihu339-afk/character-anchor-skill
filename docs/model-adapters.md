# Model Adapter Notes

## Principle

Keep the character asset library provider-neutral, but use Codex built-in image generation as the default v1.1 image generator. A prompt compiled for Codex should still have a neutral source record that can be transformed for another model later.

## Default Codex Image Adapter

The default image generator is `codex-image`:

```json
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
```

For Codex image generation, compile an English prompt from the character anchor, original reference, approved golden references, user request, allowed variations, and negative drift rules.

Do not assume default support for raw embedding vectors, LoRA weights, IP-Adapter, ControlNet, or ComfyUI workflow parameters.

## Adapter Types

- `llm`: text understanding, summarization, prompt expansion, feedback extraction.
- `vision_reviewer`: identity, quality, safety, and similarity review.
- `image_generator`: image generation or editing.
- `video_generator`: future video generation.
- `voice_analyzer`: voice profile description.
- `training`: LoRA, Face Adapter, embedding, or fine-tune package preparation.

## Optional Provider Records

Optional provider entries should include:

```json
{
  "provider_id": "openai-image",
  "adapter_type": "image_generator",
  "interface": "openai",
  "enabled": false,
  "input_contract": {
    "prompt": "string",
    "negative_prompt": "string?",
    "reference_images": "array?",
    "aspect_ratio": "string?"
  },
  "output_contract": {
    "image_path": "string",
    "metadata": "object"
  },
  "safety_notes": []
}
```

## Supported Integration Patterns

- Codex built-in image generation.
- OpenAI image or vision APIs.
- Local LLMs for private analysis.
- ComfyUI workflow JSON.
- Stable Diffusion WebUI payloads.
- Flux or other diffusion endpoints.
- Midjourney manual workflow records.
- Runway or video providers.
- Custom HTTP adapters.

Do not put provider credentials in the character library. Use environment variables or external secret stores.
