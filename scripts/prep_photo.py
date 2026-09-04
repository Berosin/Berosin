#!/usr/bin/env python3
"""
prep_photo.py — turn a raw portrait into a clean, high-contrast grayscale
image that's ready to be converted into ASCII art.

Pipeline:
  1. Remove the background with rembg so the subject is isolated.
  2. Boost local contrast with OpenCV's CLAHE (contrast-limited adaptive
     histogram equalization) — this is what gives a flat face real
     highlights and shadows.
  3. Composite onto pure white so the background maps to the blank end
     of the ASCII ramp (white -> spaces).

Usage:
    python scripts/prep_photo.py source-photo.jpg
Output:
    source-prepped.png (grayscale, same basename as input, in the same dir)
"""
import sys
import os
import io

import numpy as np
import cv2
from PIL import Image
from rembg import remove, new_session

# Use the lightweight u2netp model (~4.7MB) instead of the default heavyweight
# model — plenty accurate for a portrait cutout and far less memory-hungry.
_SESSION = new_session("u2netp")


def prep_photo(input_path: str, output_path: str | None = None) -> str:
    if output_path is None:
        root, _ext = os.path.splitext(input_path)
        output_path = f"{root}-prepped.png"

    with open(input_path, "rb") as f:
        raw_bytes = f.read()

    # 1. Remove background -> RGBA with subject isolated
    print("[1/3] Removing background with rembg ...")
    cutout_bytes = remove(raw_bytes, session=_SESSION)
    cutout = Image.open(io.BytesIO(cutout_bytes)).convert("RGBA")

    # 2. Boost local contrast with CLAHE (operates on the L channel)
    print("[2/3] Boosting local contrast with CLAHE ...")
    rgb = np.array(cutout.convert("RGB"))
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l_channel)

    lab_eq = cv2.merge((l_eq, a_channel, b_channel))
    rgb_eq = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2RGB)

    # carry the alpha mask from the cutout over to the contrast-boosted image
    alpha = np.array(cutout)[:, :, 3]
    rgba_eq = np.dstack([rgb_eq, alpha])
    subject = Image.fromarray(rgba_eq, mode="RGBA")

    # 3. Composite onto pure white
    print("[3/3] Compositing onto white background ...")
    white_bg = Image.new("RGBA", subject.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, subject).convert("L")

    composited.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <source-photo>")
        sys.exit(1)
    prep_photo(sys.argv[1])