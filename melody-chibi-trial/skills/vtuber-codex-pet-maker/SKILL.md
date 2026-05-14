---
name: vtuber-codex-pet-maker
description: Create Codex pet packages from virtual streamer, VTuber, mascot, anime character, or streamer reference images and character notes. Use when the user wants to make, adapt, package, QA, install, or publish a Codex desktop pet with pet.json, preview.webp, spritesheet.webp, and an optional install zip.
---

# VTuber Codex Pet Maker

## Goal

Turn a virtual streamer character into an original, small-screen Codex Pet: a readable chibi desktop companion with a valid atlas, a clean manifest, and upload/install-ready package files.

## Inputs To Collect

- Character name and desired public display name.
- Character origin/source, such as a Bilibili VTuber or mascot.
- Reference images, GIFs, or screenshots.
- Core traits to preserve: hair, eyes, outfit colors, accessories, species motif, expression, and mood.
- Target tone: cute, soft, chaotic, elegant, spooky, utility, etc.
- Whether the result is a fan adaptation, original redesign, or official asset.

If public upload is intended, keep the pet as an original chibi adaptation and avoid implying official endorsement unless the user has rights or permission.

## Codex Pet Contract

Default package files:

- `pet.json`
- `spritesheet.webp`
- `preview.webp`

Default atlas:

- Size: `1536x1872`
- Grid: `8x9`
- Cell: `192x208`
- Transparent background

Default row order:

1. idle
2. run right
3. run left
4. waving
5. jumping
6. failed
7. waiting
8. running task
9. review

Each row contains 8 atlas frames. If source animations have more than 8 frames, sample or redraw to 8 stable frames while preserving loop readability.

## Design Rules

- Make the character readable at desktop-pet size before preserving fine costume detail.
- Prefer oversized head, compact body, clear silhouette, and large expressive eyes.
- Preserve iconic character cues, not every original detail.
- Use consistent body anchor, foot placement, head scale, eye placement, and outline treatment across frames.
- Avoid backgrounds, shadows, text, watermarks, stray pixels, and inconsistent outlines.
- Keep facial edits local. Do not add extra face components when only the mouth should change.
- When adapting a known streamer, describe it as inspired by or based on the streamer rather than a direct official replica unless the user states it is official.

## Workflow

1. Define the identity:
   - Choose `id` as a short lowercase slug, such as `melody`.
   - Choose `displayName` as the user-facing name, such as `泽音melody`.
   - Write a short description that introduces the pet, not the implementation.

2. Build or refine the art:
   - Use references to create an original chibi design.
   - Generate or edit one action at a time when consistency is fragile.
   - For a single expression correction, operate on exact pixels or a small crop rather than repainting the whole face.

3. Assemble the atlas:
   - Normalize every frame to `192x208`.
   - Align the character anchor in every frame.
   - Fill all 9 rows and 8 columns.
   - Export `spritesheet.webp` with alpha.

4. Create the preview:
   - Use the cleanest idle frame.
   - Export as `preview.webp`, normally `192x208`.

5. Write `pet.json`:

```json
{
  "id": "character-slug",
  "displayName": "Character Display Name",
  "description": "Short character-first description.",
  "spritesheetPath": "spritesheet.webp"
}
```

6. Package:
   - Put `pet.json`, `spritesheet.webp`, and `preview.webp` in a folder named after the `id`.
   - Zip that folder for upload or sharing.
   - For local Codex install, copy the folder to `~/.codex/pets/<id>/`.

7. Validate:
   - Confirm atlas size is exactly `1536x1872`.
   - Confirm preview is present and readable.
   - Confirm alpha exists around the pet.
   - Preview each action as an animation and check for jitter, stray lines, changing outlines, or surprise extra limbs.
   - Inspect the zip listing and confirm the top-level manifest folder matches the intended `id`.

## Reusable Prompt

Use this compact prompt when the user wants a new VTuber Codex Pet:

```text
Create an original Codex Pet package based on the provided VTuber references.

Character:
- Source/origin: {VTuber or mascot source}
- Public display name: {display name}
- Package id: {short lowercase id}
- Short description: {one-sentence character description}
- Key traits to preserve: {hair, eyes, outfit colors, accessories, species motif, expression, vibe}

Style:
- Small chibi desktop companion, readable at Codex pet size
- Cute, clear silhouette, oversized head, compact body
- Transparent background, no text, no watermark, no shadows
- Original adaptation, not a one-to-one copy unless official permission is stated

Deliver:
- pet.json
- spritesheet.webp: 1536x1872, 8x9 grid, 192x208 cells
- preview.webp from the cleanest idle frame
- zip package with top-level folder named {id}

Actions:
1 idle
2 run right
3 run left
4 waving
5 jumping
6 failed
7 waiting
8 running task
9 review

Before finalizing, validate dimensions, transparency, frame alignment, zip manifest name, and animation readability.
```
