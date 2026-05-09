#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageSequence


def bounds_to_pixels(left: float, top: float, right: float, bottom: float) -> tuple[int, int, int, int]:
    """Convert floating editor bounds to Pillow crop bounds: left/top inclusive, right/bottom exclusive."""
    x1 = math.floor(left)
    y1 = math.floor(top)
    x2 = math.ceil(right)
    y2 = math.ceil(bottom)
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"Invalid bounds: {(left, top, right, bottom)}")
    return x1, y1, x2, y2


def transform_frame(
    frame: Image.Image,
    bounds: tuple[int, int, int, int],
    fill_rgba: tuple[int, int, int, int],
    dx: int,
    dy: int,
    rotate_clockwise: float,
) -> Image.Image:
    base = frame.convert("RGBA")
    x1, y1, x2, y2 = bounds

    layer_m = base.crop((x1, y1, x2, y2))

    pixels = base.load()
    for y in range(y1, y2):
        for x in range(x1, x2):
            pixels[x, y] = fill_rgba

    rotated = layer_m.rotate(
        -rotate_clockwise,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor=(0, 0, 0, 0),
    )

    original_cx = x1 + (x2 - x1) / 2 + dx
    original_cy = y1 + (y2 - y1) / 2 + dy
    paste_x = round(original_cx - rotated.width / 2)
    paste_y = round(original_cy - rotated.height / 2)
    base.alpha_composite(rotated, (paste_x, paste_y))
    return base


def main() -> None:
    parser = argparse.ArgumentParser(description="Cut a rectangular region into a layer, fill the source area, transform the layer, and paste it back.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--left", type=float, required=True)
    parser.add_argument("--top", type=float, required=True)
    parser.add_argument("--right", type=float, required=True)
    parser.add_argument("--bottom", type=float, required=True)
    parser.add_argument("--fill", default="254,240,231,255", help="RGBA fill, e.g. 254,240,231,255")
    parser.add_argument("--dx", type=int, default=-2)
    parser.add_argument("--dy", type=int, default=-2)
    parser.add_argument("--rotate-clockwise", type=float, default=33.9)
    parser.add_argument("--duration", type=int, default=None, help="GIF frame duration override in ms")
    args = parser.parse_args()

    fill_rgba = tuple(int(part) for part in args.fill.split(","))
    if len(fill_rgba) != 4:
        raise ValueError("--fill must contain four comma-separated RGBA values")

    bounds = bounds_to_pixels(args.left, args.top, args.right, args.bottom)
    image = Image.open(args.input)
    frames = [
        transform_frame(frame, bounds, fill_rgba, args.dx, args.dy, args.rotate_clockwise)
        for frame in ImageSequence.Iterator(image)
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.suffix.lower() == ".gif" or getattr(image, "is_animated", False):
        duration = args.duration if args.duration is not None else image.info.get("duration", 100)
        frames[0].save(
            args.output,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=image.info.get("loop", 0),
            disposal=2,
        )
    else:
        frames[0].save(args.output)


if __name__ == "__main__":
    main()
