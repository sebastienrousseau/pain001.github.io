#!/usr/bin/env python3
"""Fonts must be declared, used, and within budget.

The build ships 128 KB of Source Serif 4 into site/fonts/, but the
stylesheet the homepage loads contains no `@font-face` at all: every
heading renders in `--font-sans`, which is the operating system's UI
stack. The site was paying for a typeface it was not wearing, and
nothing noticed, because a font nobody declares still copies cleanly and
every other gate passes.

Three checks, each for a failure that is invisible in the rendered page:

1. every woff2 shipped is referenced by an `@font-face` src somewhere in
   the built CSS -- catches dead weight;
2. every `@font-face` src resolves to a file that exists -- catches a
   404 that silently falls back to a system font;
3. the total font payload stays under budget -- catches a future
   variable-font swap quietly doubling the page.

Run against site/ after a build.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# Room for three subset variable faces (display, interface, mono) with
# headroom. Raise it deliberately, with the perf budget re-measured.
MAX_FONT_BYTES = 140 * 1024

SRC_RE = re.compile(r"url\(\s*['\"]?([^'\")]+\.woff2?)['\"]?\s*\)", re.I)
FACE_RE = re.compile(r"@font-face\s*\{[^}]*\}", re.S | re.I)
FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}]+)", re.I)
# A stack is often reached through a custom property
# (`--type-display: "Source Serif 4", serif;` then `font-family: var(--type-display)`),
# so those have to be resolved or the check reports a family as unused when it
# is simply one indirection away.
VAR_DEF_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;}]*(?:serif|sans|mono|[\"\'][^\"\']+[\"\'])[^;}]*)", re.I)
VAR_USE_RE = re.compile(r"var\(\s*(--[\w-]+)", re.I)
FACE_NAME_RE = re.compile(r"font-family\s*:\s*['\"]?([^;'\"}]+)", re.I)


def main() -> int:
    if not SITE.is_dir():
        print("site/ not built; run ./build.sh first", file=sys.stderr)
        return 1

    font_files = sorted(SITE.rglob("*.woff2")) + sorted(SITE.rglob("*.woff"))
    total = sum(f.stat().st_size for f in font_files)

    referenced: set[str] = set()
    declared: set[str] = set()
    used: set[str] = set()
    faces = 0
    for css in SITE.rglob("*.css"):
        body = css.read_text(encoding="utf-8", errors="replace")
        blocks = FACE_RE.findall(body)
        for block in blocks:
            faces += 1
            for src in SRC_RE.findall(block):
                referenced.add(Path(src).name)
            name = FACE_NAME_RE.search(block)
            if name:
                declared.add(name.group(1).strip().lower())
        # Families named outside an @font-face block are families the page
        # actually asks for. A declared face that never appears here is
        # downloaded by nobody.
        outside = FACE_RE.sub(" ", body)
        var_stacks = {name: value for name, value in VAR_DEF_RE.findall(outside)}
        for stack in FAMILY_RE.findall(outside):
            expanded = stack
            for _ in range(3):  # custom properties can chain
                ref = VAR_USE_RE.search(expanded)
                if not ref:
                    break
                expanded = expanded.replace(ref.group(0) + ")", var_stacks.get(ref.group(1), ""))
                expanded = VAR_USE_RE.sub("", expanded)
            for fam in expanded.split(","):
                fam = fam.strip().strip("'\"").lower()
                if fam and not fam.startswith("var("):
                    used.add(fam)

    shipped = {f.name for f in font_files}
    orphans = sorted(shipped - referenced)
    dangling = sorted(referenced - shipped)

    print(f"scanned {len(font_files)} font file(s), {faces} @font-face block(s)")
    print(f"payload {total / 1024:.0f} KB of {MAX_FONT_BYTES / 1024:.0f} KB budget")

    bad = 0
    if orphans:
        bad += 1
        wasted = sum(f.stat().st_size for f in font_files if f.name in set(orphans))
        print(f"FAIL {len(orphans)} font(s) shipped but never declared "
              f"({wasted / 1024:.0f} KB wasted): {orphans[:4]}")
        print("     add an @font-face, or stop copying them into the build")
    if dangling:
        bad += 1
        print(f"FAIL {len(dangling)} @font-face src(s) point at a missing file: {dangling[:4]}")
        print("     the browser falls back to a system font with no error")
    unused = sorted(declared - used)
    if unused:
        bad += 1
        print(f"FAIL {len(unused)} family(ies) declared but never named in a "
              f"font-family: {unused}")
        print("     the @font-face is inert and the text renders in a fallback")
    if total > MAX_FONT_BYTES:
        bad += 1
        print(f"FAIL font payload {total / 1024:.0f} KB exceeds "
              f"{MAX_FONT_BYTES / 1024:.0f} KB")

    if not bad:
        print("result: CLEAN")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
