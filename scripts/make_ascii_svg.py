#!/usr/bin/env python3
"""
make_ascii_svg.py — convert a prepped (grayscale, white-background) portrait
into a monochrome, self-typing ASCII-art SVG.

The prepped image is downsampled to a character grid (~80 columns wide,
rows auto-computed from the source photo's aspect ratio so nothing gets
stretched), and each pixel's brightness picks a glyph from a density ramp
— sparse characters for bright areas, dense ones for dark:

    RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense)
    #        ^ leading space clears the background to nothing

Design choices:
  * Monochrome — one light-gray fill color. Per-character rainbow coloring
    is exactly what makes most ASCII portraits look like static.
  * High contrast — a busy background washes out to the space glyph, so
    only the subject prints.

Each row is wrapped in a horizontal clip that wipes left-to-right (a small
block "cursor" rides the wipe edge), staggered top to bottom. The whole
portrait prints once and freezes — no looping. Because it's SMIL inside
the SVG, GitHub plays it.

Usage:
    python scripts/make_ascii_svg.py [prepped-image] [-o output.svg]
Default input:  source-prepped.png
Default output: avi-ascii.svg
"""
import sys
import argparse
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)

FILL_COLOR = "#9aa5b1"      # monochrome light-gray, readable on light + dark bg
CURSOR_COLOR = "#e6edf3"    # slightly brighter, rides the wipe edge

CELL_W = 7.0     # px per character column
CELL_H = 13.0    # px per character row
FONT_SIZE = 13
ROW_DUR = 0.7        # seconds for a single row to wipe in
ROW_STAGGER = 0.035  # seconds between the start of each successive row


def image_to_grid(img: Image.Image, cols: int, rows: int) -> list[str]:
    """Downsample to a cols x rows grid and map brightness -> ramp glyph."""
    small = img.convert("L").resize((cols, rows), Image.LANCZOS)
    pixels = list(small.getdata())
    n = len(RAMP) - 1
    lines = []
    for r in range(rows):
        row_pixels = pixels[r * cols:(r + 1) * cols]
        # brightest (255) -> index 0 (space), darkest (0) -> index n (@)
        chars = [RAMP[n - (p * n // 255)] for p in row_pixels]
        lines.append("".join(chars))
    return lines


def rows_for_aspect(img: Image.Image, cols: int) -> int:
    """
    Pick a row count that keeps the rendered SVG the same shape as the
    source photo. A naive `resize((cols, rows))` to a fixed grid ignores
    both the source's aspect ratio and the fact that a monospace character
    cell (CELL_W x CELL_H) isn't square — skip either correction and the
    portrait comes out visibly stretched wide.
    """
    src_w, src_h = img.size
    return max(1, round(cols * (src_h / src_w) * (CELL_W / CELL_H)))


def escape_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg(lines: list[str], cols: int, rows: int) -> str:
    width = cols * CELL_W
    height = rows * CELL_H

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" '
        f'width="{width:.0f}" height="{height:.0f}" '
        f'font-family="SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="transparent"/>')

    for i, line in enumerate(lines):
        row_width = len(line) * CELL_W
        y_baseline = (i + 1) * CELL_H - 3
        begin = round(i * ROW_STAGGER, 3)
        clip_id = f"clip-row-{i}"

        # trailing whitespace doesn't need to render, but keep grid alignment
        safe_line = escape_xml(line)

        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(f'  <rect x="0" y="{i * CELL_H:.1f}" height="{CELL_H:.1f}" width="0">')
        parts.append(
            f'    <animate attributeName="width" from="0" to="{row_width:.1f}" '
            f'begin="{begin}s" dur="{ROW_DUR}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.25 0.1 0.25 1" />'
        )
        parts.append(f'  </rect>')
        parts.append(f'</clipPath>')

        parts.append(f'<g clip-path="url(#{clip_id})">')
        parts.append(
            f'  <text x="0" y="{y_baseline:.1f}" font-size="{FONT_SIZE}" '
            f'fill="{FILL_COLOR}" xml:space="preserve">{safe_line}</text>'
        )
        parts.append(f'</g>')

        # cursor block riding the wipe edge, then fading out once the row is done
        cursor_end = begin + ROW_DUR
        parts.append(
            f'<rect x="0" y="{i * CELL_H + 1:.1f}" width="{CELL_W * 0.8:.1f}" '
            f'height="{CELL_H - 3:.1f}" fill="{CURSOR_COLOR}" opacity="0">'
        )
        parts.append(
            f'  <animate attributeName="x" from="0" to="{row_width:.1f}" '
            f'begin="{begin}s" dur="{ROW_DUR}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.25 0.1 0.25 1" />'
        )
        parts.append(
            f'  <animate attributeName="opacity" values="0;1;1;0" '
            f'keyTimes="0;0.05;0.9;1" begin="{begin}s" dur="{ROW_DUR}s" fill="freeze" />'
        )
        parts.append(f'</rect>')

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="source-prepped.png")
    parser.add_argument("-o", "--output", default="avi-ascii.svg")
    parser.add_argument("--cols", type=int, default=80)
    parser.add_argument(
        "--rows", type=int, default=None,
        help="Defaults to auto-computed from the source image's aspect ratio "
             "so the portrait isn't stretched. Only set this to override.",
    )
    args = parser.parse_args()

    img = Image.open(args.input)
    rows = args.rows if args.rows is not None else rows_for_aspect(img, args.cols)

    lines = image_to_grid(img, args.cols, rows)
    svg = build_svg(lines, args.cols, rows)

    with open(args.output, "w") as f:
        f.write(svg)
    print(f"Saved: {args.output} ({args.cols}x{rows} grid, {len(lines)} rows)")


if __name__ == "__main__":
    main()