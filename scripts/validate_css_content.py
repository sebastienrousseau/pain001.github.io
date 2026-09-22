#!/usr/bin/env python3
"""No emoji doing structural work in CSS.

The theme toggle renders its icon with `content: "☀️"` and
`content: "\U0001F319"`. An emoji in a CSS `content` property is not a
design decision that survives contact with users:

- it rasterises from the platform's emoji font, so the control looks
  different on macOS, Windows, Android and in a Linux VM, and identical
  to nothing else on the page;
- it ignores every colour token, so it cannot follow the theme it exists
  to switch, and it cannot take a focus or hover colour;
- it carries its own implicit meaning to a screen reader unless
  suppressed, and its meaning is not the control's label.

An inline SVG that inherits `currentColor` does all three correctly.

This gate is deliberately narrow: emoji in page content is fine, and so
is an emoji in a comment. Only `content:` in a stylesheet is rejected.

Run against the stylesheet sources in static/css.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS_DIR = ROOT / "static" / "css"

CONTENT_RE = re.compile(r"content\s*:\s*(['\"])(.*?)\1", re.S)

# Pictographic ranges plus the variation selector that makes a glyph
# render in colour. Deliberately excludes arrows, box drawing and
# typographic marks, which are legitimate in `content`.
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U0001F000-\U0001F2FF"
    "☀-➿"
    "️"
    "]"
)


def main() -> int:
    if not CSS_DIR.is_dir():
        print(f"{CSS_DIR} not found", file=sys.stderr)
        return 1

    hits: list[tuple[str, int, str]] = []
    files = sorted(CSS_DIR.glob("*.css"))
    for css in files:
        body = css.read_text(encoding="utf-8", errors="replace")
        for match in CONTENT_RE.finditer(body):
            value = match.group(2)
            if EMOJI_RE.search(value):
                line = body.count("\n", 0, match.start()) + 1
                hits.append((css.name, line, value))

    print(f"scanned {len(files)} stylesheet(s)")
    if hits:
        print(f"FAIL {len(hits)} emoji in a CSS content property")
        for name, line, value in hits[:8]:
            print(f"     {name}:{line}  content: {value!r}")
        print("     use an inline SVG that inherits currentColor instead")
        return 1

    print("result: CLEAN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
