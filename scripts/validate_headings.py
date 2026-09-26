#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Headings must be headlines, not SEO titles.

`_layouts/page.html` renders `<h1>{{title}}</h1>`, so every page's H1 is
whatever string was written for the `<title>` tag and the search result.
On 664 of 668 pages those are the same string, and on 293 of them it runs
past 60 characters. The worst is 121 characters, which renders as six
lines filling the whole first viewport of `/enterprise/` -- the page a
bank's procurement reviewer lands on.

Nothing caught it: the markup is valid, the heading order is correct, the
contrast passes, and the page is perfectly accessible. It is a content
design defect, so it needs a content gate.

This is a ratchet, in the same spirit as the coverage floors in
AGENTS.md: the baseline records how many over-long H1s exist today, and
the gate fails if that number grows. Lower the baseline as pages are
given a real `headline`; never raise it.

Run against site/ after a build.
"""

from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BASELINE = ROOT / "scripts" / "headings_baseline.json"

# A headline longer than this wraps past two lines at the display size the
# PRISM hero uses, which is where the defect becomes visible.
MAX_HEADLINE = 60

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
TAGS_RE = re.compile(r"<[^>]+>")


def text(markup: str) -> str:
    # Decode entities before counting: "ISO&nbsp;20022" is nine visible
    # characters, not fourteen, and "&amp;" is one.
    return re.sub(r"\s+", " ", unescape(TAGS_RE.sub("", markup))).strip()


def main() -> int:
    if not SITE.is_dir():
        print("site/ not built; run ./build.sh first", file=sys.stderr)
        return 1

    missing: list[str] = []
    multiple: list[str] = []
    overlong: list[tuple[int, str]] = []

    pages = sorted(SITE.rglob("index.html"))
    for page in pages:
        rel = str(page.relative_to(SITE))
        html = page.read_text(encoding="utf-8", errors="replace")
        heads = H1_RE.findall(html)

        if not heads:
            missing.append(rel)
            continue
        if len(heads) > 1:
            multiple.append(rel)

        headline = text(heads[0])
        if len(headline) > MAX_HEADLINE:
            overlong.append((len(headline), rel))

    baseline = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.is_file() else {}
    allowed = int(baseline.get("overlong_h1", 0))

    print(f"scanned {len(pages)} page(s)")
    bad = 0

    # These two are absolute: there is no legitimate page without exactly one H1.
    if missing:
        bad += 1
        print(f"FAIL {len(missing)} page(s) with no H1: {missing[:4]}")
    if multiple:
        bad += 1
        print(f"FAIL {len(multiple)} page(s) with more than one H1: {multiple[:4]}")

    count = len(overlong)
    if count > allowed:
        bad += 1
        worst = sorted(overlong, reverse=True)[:5]
        print(f"FAIL {count} H1(s) over {MAX_HEADLINE} chars, baseline allows {allowed}")
        for length, rel in worst:
            print(f"     {length:3} chars  {rel}")
        print("     give the page a short `headline` in its front matter,")
        print("     or lower scripts/headings_baseline.json if you fixed some")
    elif count < allowed:
        # Tightening is the point of a ratchet; say so loudly rather than
        # letting the baseline quietly drift above reality.
        print(f"note {count} over-long H1(s), baseline allows {allowed}")
        print(f"     lower overlong_h1 to {count} in {BASELINE.name} to lock the gain in")
    else:
        print(f"ok   {count} over-long H1(s), at the baseline")

    if not bad:
        print("result: CLEAN")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
