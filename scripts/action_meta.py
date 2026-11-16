#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Copy the GitHub Action's name and description onto the CI page.

The core repository is a GitHub Action, and its ``action.yml`` is the
one place its name and description are written. The regenerate workflow
runs this script against the library checked out at the release tag, and
it rewrites the block between ``<!-- action:start -->`` and
``<!-- action:end -->`` in ``_posts/developers-ci.md``, so the page states
what the release's ``action.yml`` says, never a hand-kept copy.

Usage: python3 scripts/action_meta.py <pain001 checkout>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "_posts" / "developers-ci.md"
BLOCK = re.compile(r"<!-- action:start -->.*?<!-- action:end -->", re.S)


def read_action(checkout: Path) -> tuple[str, str]:
    """The ``name`` and ``description`` of the checkout's action.yml."""
    data = yaml.safe_load((checkout / "action.yml").read_text(encoding="utf-8"))
    name = str(data.get("name") or "").strip()
    description = " ".join(str(data.get("description") or "").split())
    if not name or not description:
        raise SystemExit("[action] action.yml has no name or no description")
    return name, description


def render(name: str, description: str) -> str:
    """The paragraph between the markers."""
    return (
        "<!-- action:start -->\n"
        f"The action is named **{name}**, and its `action.yml` describes it "
        f"as: {description}\n"
        "<!-- action:end -->"
    )


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: action_meta.py <pain001 checkout>")
        return 2
    name, description = read_action(Path(argv[0]))
    text = PAGE.read_text(encoding="utf-8")
    if not BLOCK.search(text):
        print("[action] no markers on the CI page")
        return 1
    PAGE.write_text(BLOCK.sub(lambda _: render(name, description), text), encoding="utf-8")
    print(f"[action] {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
