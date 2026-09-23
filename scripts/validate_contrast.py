#!/usr/bin/env python3
"""Compute every PRISM colour-token pair and fail under its WCAG floor.

pa11y samples rendered pages; it only sees the pairs a sampled page
happens to paint. This gate reads the token blocks in
``static/css/prism.css`` directly and checks each declared pairing in
both colour schemes, so a token that no audited page currently uses is
held to the same bar.

Floors:
  text     7:1  WCAG 1.4.6 Contrast (Enhanced), AAA
  non-text 3:1  WCAG 1.4.11 Non-text Contrast (borders, focus ring)

The ``@media (color-gamut: p3)`` block restates the chromatic tokens in
Display P3 with more chroma and, by contract, the same luminance. Each P3
value is held to within 1% of its sRGB token's luminance and the pairs
are re-run with the P3 values in place, so a P3 block left behind by a
palette change fails here instead of silently repainting wide-gamut
screens in the old colours.

It also asserts that the two dark blocks — the ``prefers-color-scheme``
media block and the explicit ``[data-theme="dark"]`` toggle — declare the
same values. They are hand-maintained copies, and a drift between them
means the theme looks different depending on how dark was chosen.

Usage: python3 scripts/validate_contrast.py [path/to/prism.css]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "static" / "css" / "prism.css"

GROUNDS = ("--bg", "--bg-soft", "--surface", "--surface-soft")
TEXT_ON_GROUNDS = (
    "--ink",
    "--ink-soft",
    "--ink-muted",
    "--accent",
    "--accent-hover",
    "--brand",
    "--signal",
)
TEXT_PAIRS = (
    ("--accent-ink", "--accent"),
    ("--cta-ink", "--cta-bg"),
    ("--cta-ink", "--cta-bg-hover"),
    ("--accent-ink", "--accent-hover"),
    ("--on-accent-soft", "--accent-soft"),
    ("--ink", "--accent-soft"),
    ("--ink-soft", "--accent-soft"),
    ("--accent", "--accent-soft"),
    ("--green-text", "--green-soft"),
    ("--clay-text", "--clay-soft"),
    ("--gold-text", "--gold-soft"),
    ("--burgundy-text", "--burgundy-soft"),
    ("--green-text", "--surface"),
    ("--burgundy-text", "--surface"),
    ("--hero-ink", "--hero-bg"),
    ("--hero-ink", "--hero-surface"),
    ("--hero-ink-soft", "--hero-bg"),
    ("--hero-ink-soft", "--hero-surface"),
    ("--hero-accent", "--hero-bg"),
    ("--hero-gold", "--hero-bg"),
    ("--hero-clay", "--hero-bg"),
    ("--code-plain", "--code-bg"),
    ("--code-keyword", "--code-bg"),
    ("--code-function", "--code-bg"),
    ("--code-string", "--code-bg"),
    ("--code-comment", "--code-bg"),
    ("--code-property", "--code-bg"),
    ("--code-number", "--code-bg"),
    ("--code-comment", "--code-bar"),
    ("--code-plain", "--code-bar"),
)
NON_TEXT_PAIRS = (
    ("--line", "--bg"),
    ("--line", "--surface"),
    ("--focus", "--bg"),
    ("--focus", "--surface"),
    ("--focus", "--hero-bg"),
    # The icon-badge glyph against the lightest stop of each gradient.
    ("--badge-ink", "--badge-blue-to"),
    ("--badge-ink", "--badge-clay-to"),
    ("--badge-ink", "--badge-green-to"),
    ("--badge-ink", "--badge-gold-to"),
    ("--badge-ink", "--badge-burgundy-to"),
    ("--badge-ink", "--badge-navy-to"),
)

P3 = re.compile(r"^color\(display-p3\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\)$")
HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
DECL = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")


def block(css: str, selector_pattern: str, start: int = 0) -> dict[str, str]:
    """Return the declarations of the first rule whose selector matches."""
    m = re.compile(selector_pattern + r"\s*\{").search(css, start)
    if not m:
        raise SystemExit(f"error: no rule matching {selector_pattern!r}")
    depth, i = 1, m.end()
    while depth:
        depth += {"{": 1, "}": -1}.get(css[i], 0)
        i += 1
    body = re.sub(r"/\*.*?\*/", "", css[m.end() : i - 1], flags=re.DOTALL)
    return {k: v.strip() for k, v in DECL.findall(body)}


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(value: str) -> float:
    p3 = P3.match(value)
    if p3:
        # Display P3 shares the sRGB transfer curve; Y row of its matrix.
        r, g, b = (_lin(float(x)) for x in p3.groups())
        return 0.2289746 * r + 0.6917385 * g + 0.0792869 * b
    m = HEX.match(value)
    if not m:
        raise ValueError(f"not a hex colour: {value}")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    chans = []
    for k in range(0, 6, 2):
        c = int(h[k : k + 2], 16) / 255
        chans.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = chans
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check(name: str, tokens: dict[str, str]) -> list[str]:
    failures = []
    pairs = [(t, g, 7.0) for t in TEXT_ON_GROUNDS for g in GROUNDS]
    pairs += [(t, g, 7.0) for t, g in TEXT_PAIRS]
    pairs += [(t, g, 3.0) for t, g in NON_TEXT_PAIRS]
    for fg, bg, floor in pairs:
        if fg not in tokens or bg not in tokens:
            failures.append(f"{name}: {fg} on {bg}: token not declared")
            continue
        r = ratio(tokens[fg], tokens[bg])
        if r < floor:
            failures.append(
                f"{name}: {fg} {tokens[fg]} on {bg} {tokens[bg]} = "
                f"{r:.2f}:1, needs {floor:g}:1"
            )
    print(f"{name}: {len(pairs)} pair(s)")
    return failures


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else CSS
    css = path.read_text(encoding="utf-8")
    light = block(css, r':root,\s*:root\[data-theme="light"\]')
    media_dark = block(css, r':root:not\(\[data-theme="light"\]\)')
    toggle_dark = block(css, r'\n  :root\[data-theme="dark"\]')

    failures = check("light", light) + check("dark", toggle_dark)

    at = css.find("@media (color-gamut: p3)")
    if at != -1:
        p3_light = block(css, r':root,\s*:root\[data-theme="light"\]', at)
        p3_dark = block(css, r'\n  :root\[data-theme="dark"\]', at)
        p3_media = block(css, r':root:not\(\[data-theme="light"\]\)', at)
        if p3_media != p3_dark:
            failures.append("P3 dark blocks disagree")
        for name, base, over in (("light", light, p3_light), ("dark", toggle_dark, p3_dark)):
            for key, value in over.items():
                a, b = luminance(value), luminance(base[key])
                if abs(a - b) > 0.01 * b:
                    failures.append(
                        f"{name} P3: {key} {value} has luminance {a:.4f}, "
                        f"sRGB {base[key]} has {b:.4f}; restate it from the sRGB token"
                    )
            failures += check(f"{name} P3", {**base, **over})

    # A `.theme-dark` band restates the dark tokens inside a light page;
    # it must restate them exactly, or the band escapes the gate.
    if ".theme-dark {" in css:
        band = block(css, r"\n\.theme-dark")
        for key, value in band.items():
            if key.startswith("--") and toggle_dark.get(key) != value:
                failures.append(f".theme-dark {key} {value!r} differs from the dark theme's {toggle_dark.get(key)!r}")

    for key in sorted(set(media_dark) | set(toggle_dark)):
        if media_dark.get(key) != toggle_dark.get(key):
            failures.append(
                f"dark blocks disagree on {key}: media "
                f"{media_dark.get(key)!r} vs toggle {toggle_dark.get(key)!r}"
            )

    for f in failures:
        print(f"FAIL {f}")
    print("result:", "FAIL" if failures else "CLEAN")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
