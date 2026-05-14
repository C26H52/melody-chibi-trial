# VTuber Codex Pet Maker Prompt

Create an original Codex Pet package based on the provided VTuber references.

Character:
- Source/origin: `{VTuber or mascot source}`
- Public display name: `{display name}`
- Package id: `{short lowercase id}`
- Short description: `{one-sentence character description}`
- Key traits to preserve: `{hair, eyes, outfit colors, accessories, species motif, expression, vibe}`

Style:
- Small chibi desktop companion, readable at Codex pet size.
- Cute, clear silhouette, oversized head, compact body.
- Transparent background, no text, no watermark, no shadows.
- Original adaptation, not a one-to-one copy unless official permission is stated.

Deliver:
- `pet.json`
- `spritesheet.webp`: `1536x1872`, `8x9` grid, `192x208` cells.
- `preview.webp` from the cleanest idle frame.
- Zip package with top-level folder named `{id}`.

Actions:
1. idle
2. run right
3. run left
4. waving
5. jumping
6. failed
7. waiting
8. running task
9. review

Before finalizing, validate dimensions, transparency, frame alignment, zip manifest name, and animation readability.
