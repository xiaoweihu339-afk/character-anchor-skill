# Model Adapter Notes

## Principle

Keep the character asset library provider-neutral. A prompt compiled for one model should still have a neutral source record that can be transformed for another model.

## Adapter Types

- `llm`: text understanding, summarization, prompt expansion, feedback extraction.
- `vision_reviewer`: identity, quality, safety, and similarity review.
- `image_generator`: image generation or editing.
- `video_generator`: future video generation.
- `voice_analyzer`: voice profile description.
- `training`: LoRA, Face Adapter, embedding, or fine-tune package preparation.

## Provider Records

Each provider entry should include:

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

- OpenAI image or vision APIs.
- Local LLMs for private analysis.
- ComfyUI workflow JSON.
- Stable Diffusion WebUI payloads.
- Flux or other diffusion endpoints.
- Midjourney manual workflow records.
- Runway or video providers.
- Custom HTTP adapters.

Do not put provider credentials in the character library. Use environment variables or external secret stores.
