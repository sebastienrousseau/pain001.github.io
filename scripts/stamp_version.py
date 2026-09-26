#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Stamp every page to a released pain001 version.

Rewrites version literals (``0.0.NN`` / ``v0.0.NN``) in ``_posts/`` to the
given version, except on history lines (the same rule the version gate
uses) and on the generated corpus pages, which the corpus generator
stamps itself. Usage: python3 scripts/stamp_version.py 0.0.71

The translation tables under ``scripts/*_i18n/`` are stamped too. Their
English keys are the page's own sentences, so a sentence that names the
version (the documentation page's "pain001 v0.0.70") changes with every
release; left alone, the key matches nothing on the rebuilt page, the
live-key gate fails, and every locale ships that sentence in English.
Keys and translated values move together, which also retires stale
versions a translation kept after the English moved on.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
TABLES = ROOT / "scripts"
VERSION = re.compile(r"\b(v?)0\.0\.(\d{2,3})\b")
HISTORY = re.compile(r"^generator:|min_pain001:|\bonward\b|\bsince\b|<!-- history -->")


def restamp(text: str, minor: int, target: str) -> str:
    """Rewrite literals older than ``target`` in one line of text."""
    return VERSION.sub(lambda m: f"{m.group(1)}{target}" if int(m.group(2)) < minor else m.group(0), text)


def stamp_tables(target: str) -> int:
    """Stamp every translation table; return the number of files touched."""
    minor = int(target.rsplit(".", 1)[1])
    touched = 0
    for table in sorted(TABLES.glob("*_i18n/*.json")):
        text = table.read_text(encoding="utf-8")
        new = "".join(line if HISTORY.search(line) else restamp(line, minor, target)
                      for line in text.splitlines(keepends=True))
        if new != text:
            table.write_text(new, encoding="utf-8")
            touched += 1
    return touched


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
            new = restamp(line, minor, target)
            changed |= new != line
            out.append(new)
        if changed:
            page.write_text("".join(out), encoding="utf-8")
            touched += 1
    return touched


if __name__ == "__main__":
    if len(sys.argv) != 2 or not re.fullmatch(r"0\.0\.\d{2,3}", sys.argv[1]):
        sys.exit("usage: stamp_version.py 0.0.NN")
    pages, tables = stamp(sys.argv[1]), stamp_tables(sys.argv[1])
    print(f"stamped {pages} page(s) and {tables} translation table(s) to {sys.argv[1]}")
