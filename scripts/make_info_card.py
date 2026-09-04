#!/usr/bin/env python3
"""
make_info_card.py — hand-authors a small SVG that looks like the output of
the `neofetch` command: a title bar, then colored key/value rows (Now,
Prev, Stack, Highlights).

Each line fades and slides in on a short stagger so the panel looks like
it's printing next to the portrait.

A STATIC=1 env var emits a frozen frame (no animation) for local Quick
Look previews / non-SMIL renderers.

Usage:
    python scripts/make_info_card.py [-o info-card.svg]
    STATIC=1 python scripts/make_info_card.py
"""
import os
import argparse

# ---- edit this to keep the card current -----------------------------------
DATA = {
    "user": "berosin@github",
    "rows": [
        ("Now", "Relivio — DAO-governed disaster relief + explainable AI"),
        ("Prev", "ANORA — RAG-based cloud knowledge assistant"),
        ("Stack", "React/Next.js · Node/FastAPI/Spring · Ethereum/Foundry"),
        ("Highlights", "16 repos · Full-stack + AI + Web3 builder"),
    ],
}
# -----------------------------------------------------------------------------

WIDTH = 560
PADDING = 20
TITLEBAR_H = 34
ROW_H = 30
LABEL_COLOR = "#7ee787"     # green, neofetch-style key color
VALUE_COLOR = "#c9d1d9"     # light gray value text
BG_COLOR = "#0d1117"        # GitHub-dark background
BORDER_COLOR = "#30363d"
TITLE_TEXT_COLOR = "#8b949e"
FONT = "SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace"

STAGGER = 0.18   # seconds between each row's entrance
SLIDE_DUR = 0.5  # seconds for a row to fade + slide in


def escape_xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(data: dict, static: bool) -> str:
    rows = data["rows"]
    height = TITLEBAR_H + PADDING * 2 + ROW_H * len(rows)

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" font-family="{FONT}">'
    )

    # card background + border
    parts.append(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10" '
        f'fill="{BG_COLOR}" stroke="{BORDER_COLOR}"/>'
    )

    # title bar with traffic-light dots
    parts.append(f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{TITLEBAR_H}" rx="10" fill="#161b22"/>')
    parts.append(f'<rect x="0.5" y="{TITLEBAR_H - 10}" width="{WIDTH - 1}" height="10" fill="#161b22"/>')
    for i, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        cx = PADDING + i * 18
        parts.append(f'<circle cx="{cx}" cy="{TITLEBAR_H / 2:.1f}" r="6" fill="{color}"/>')
    parts.append(
        f'<text x="{WIDTH / 2:.1f}" y="{TITLEBAR_H / 2 + 4:.1f}" text-anchor="middle" '
        f'font-size="12" fill="{TITLE_TEXT_COLOR}">{escape_xml(data["user"])}</text>'
    )

    # rows
    y0 = TITLEBAR_H + PADDING
    max_label_w = max(len(label) for label, _ in rows)

    for i, (label, value) in enumerate(rows):
        y = y0 + i * ROW_H + 18
        label_x = PADDING
        value_x = PADDING + (max_label_w + 2) * 8  # approx monospace advance

        row_group_attrs = ""
        anim = ""
        if not static:
            begin = round(i * STAGGER, 3)
            row_group_attrs = f' opacity="0" transform="translate(-12,0)"'
            anim = (
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{begin}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" '
                f'from="-12 0" to="0 0" begin="{begin}s" dur="{SLIDE_DUR}s" '
                f'fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>'
            )

        parts.append(f'<g{row_group_attrs}>')
        parts.append(
            f'  <text x="{label_x}" y="{y}" font-size="13" font-weight="700" '
            f'fill="{LABEL_COLOR}" xml:space="preserve">{escape_xml(label)}</text>'
        )
        parts.append(
            f'  <text x="{value_x}" y="{y}" font-size="13" '
            f'fill="{VALUE_COLOR}" xml:space="preserve">{escape_xml(value)}</text>'
        )
        parts.append(anim)
        parts.append("</g>")

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="info-card.svg")
    args = parser.parse_args()

    static = os.environ.get("STATIC") == "1"
    svg = build_svg(DATA, static=static)

    with open(args.output, "w") as f:
        f.write(svg)
    print(f"Saved: {args.output} ({'static' if static else 'animated'})")


if __name__ == "__main__":
    main()