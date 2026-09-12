#!/usr/bin/env python3
"""Stamp every page to a released pain001 version.

Rewrites version literals (``0.0.NN`` / ``v0.0.NN``) in ``_posts/`` to the
given version, except on history lines (the same rule the version gate
uses) and on the generated corpus pages, which the corpus generator
stamps itself. Usage: python3 scripts/stamp_version.py 0.0.71
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
VERSION = re.compile(r"\b(v?)0\.0\.(\d{2,3})\b")
HISTORY = re.compile(r"^generator:|min_pain001:|\bonward\b|\bsince\b|<!-- history -->")


def stamp(target: str) -> int:
    """Rewrite older literals to ``target``; return the number of pages touched."""
    minor = int(target.rsplit(".", 1)[1])
    touched = 0
    for page in sorted(POSTS.glob("*.md")):
        if page.name.startswith("example-corpus") or page.name.startswith("corpus-"):
            continue
        out = []
        changed = False
        for line in page.read_text(encoding="utf-8").splitlines(keepends=True):
            if HISTORY.search(line):
                out.append(line)
                continue
            new = VERSION.sub(lambda m: f"{m.group(1)}{target}" if int(m.group(2)) < minor else m.group(0), line)
            changed |= new != line
            out.append(new)
        if changed:
            page.write_text("".join(out), encoding="utf-8")
            touched += 1
    return touched


if __name__ == "__main__":
    if len(sys.argv) != 2 or not re.fullmatch(r"0\.0\.\d{2,3}", sys.argv[1]):
        sys.exit("usage: stamp_version.py 0.0.NN")
    print(f"stamped {stamp(sys.argv[1])} page(s) to {sys.argv[1]}")
