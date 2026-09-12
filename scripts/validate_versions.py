#!/usr/bin/env python3
"""Fail when a page cites a suite version older than the released one.

The pain001 suite ships one version number across its five packages.
A page that names an older version reads as stale to a buyer and as
wrong to an agent. A literal such as ``v0.0.58`` is allowed only where
it records history: a ``min_pain001:`` frontmatter key, a sentence that
says ``onward`` or ``since``, or a line ending in ``<!-- history -->``.

The current version comes from PyPI; ``--current X.Y.Z`` overrides it
for offline runs.

Usage:
    python3 scripts/validate_versions.py [--current 0.0.69]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
VERSION = re.compile(r"\bv?0\.0\.(\d{2,3})\b")
HISTORY = re.compile(r"^generator:|min_pain001:|\bonward\b|\bsince\b|<!-- history -->")
PYPI = "https://pypi.org/pypi/pain001/json"


def released_version() -> str:
    """The newest pain001 version on PyPI."""
    with urllib.request.urlopen(PYPI, timeout=30) as response:  # nosec B310
        return str(json.load(response)["info"]["version"])


def stale_lines(current: int) -> list[str]:
    """Every ``file:line: literal`` that names a version below ``current``."""
    found: list[str] = []
    for page in sorted(POSTS.glob("*.md")):
        for number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if HISTORY.search(line):
                continue
            for match in VERSION.finditer(line):
                if int(match.group(1)) < current:
                    found.append(f"{page.name}:{number}: {match.group(0)}")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--current", help="suite version to check against")
    args = parser.parse_args(argv)
    version = args.current or released_version()
    current = int(version.rsplit(".", 1)[1])
    stale = stale_lines(current)
    if stale:
        print(f"pages cite a suite version older than {version}:")
        print("\n".join("  " + s for s in stale))
        return 1
    print(f"every page is at or above pain001 {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
