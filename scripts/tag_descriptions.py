#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""A real description for each tag page.

ssg writes its taxonomy pages outside the layouts with the description
"<n> page(s) under Tags: <term>.", 29 to 38 characters: too short for a
search result to use, so the engine picks text of its own. The pages
are indexable and in the sitemap. This pass, run from build.sh after
postbuild_fix.py, rewrites that sentence wherever ssg put it (the
description, og:description and twitter:description metas):

    python3 scripts/tag_descriptions.py Pain001
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SSG_SENTENCE = re.compile(r'content="(\d+) page\(s\) under Tags: ([^"]+?)\."')


def describe(match: re.Match) -> str:
    count, term = match.group(1), match.group(2)
    noun = "page" if count == "1" else "pages"
    return (f'content="{count} pain001.com {noun} tagged {term}: guides, references and '
            f'example files for ISO 20022 payment initiation."')


def rewrite(html: str) -> str:
    return SSG_SENTENCE.sub(describe, html)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or not Path(args[0]).is_dir():
        print("usage: tag_descriptions.py <built site directory>", file=sys.stderr)
        return 2
    changed = 0
    for page in sorted((Path(args[0]) / "tags").rglob("index.html")):
        html = page.read_text(encoding="utf-8")
        new = rewrite(html)
        if new != html:
            page.write_text(new, encoding="utf-8")
            changed += 1
    print(f"[tag_descriptions] described {changed} tag page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
