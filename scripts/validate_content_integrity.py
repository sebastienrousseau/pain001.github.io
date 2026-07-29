#!/usr/bin/env python3
"""Catch content that the build silently ate.

Two escaping defects shipped for months without any gate noticing,
because the pages were valid HTML and every existing check passed:

1. Inline ``<code>`` lost a level of escaping in postbuild's body
   unescape, so markdown's ``` `<BIC>` ``` became a real ``<BIC>``
   element. The browser swallowed it and readers saw an empty code
   chip — 184 times across 84 pages, on a site about ISO 20022 element
   names.
2. ``og:title``/``twitter:title`` were escaped twice, so a title with
   an ``&`` reached every share card as ``&amp;``.

Both are invisible to a link checker, a schema validator and pa11y. The
tell is structural, so that is what this checks.

Run against docs/ after a build.
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"

# Elements a browser may legitimately encounter here. Anything else in
# the output is markup that was meant to be text.
KNOWN = set(
    """html head body div span p a ul ol li table thead tbody tfoot tr td th
    h1 h2 h3 h4 h5 h6 pre code em strong b i u s small sub sup br hr img figure
    figcaption nav header footer main article section aside form input button
    select option label textarea meta link title style script svg path circle
    rect g line polyline polygon blockquote dl dt dd time abbr kbd samp var
    mark del ins picture source video audio canvas iframe details summary
    dialog template noscript caption colgroup col fieldset legend datalist
    optgroup output progress meter address bdi bdo ruby rt rp wbr area map
    track object param embed base defs use symbol text tspan""".split()
)

TAG_RE = re.compile(r"<([a-zA-Z][\w:-]*)[\s/>]")
# A doubled entity: the "&" of a real entity was escaped a second time.
DOUBLE_ENC_RE = re.compile(r"&amp;(?:amp|lt|gt|quot|#\d+|#x[0-9a-fA-F]+);")
# An element name that survived into the markup inside a code span.
SWALLOWED_RE = re.compile(r"<code\b[^>]*>\s*</?[A-Za-z][\w.-]*>")


def main() -> int:
    if not SITE.is_dir():
        print("docs/ not built; run ./build.sh first", file=sys.stderr)
        return 1

    unknown: collections.Counter[str] = collections.Counter()
    unknown_pages: set[str] = set()
    doubled: list[str] = []
    swallowed: list[str] = []

    pages = sorted(SITE.rglob("*.html"))
    for page in pages:
        html = page.read_text(encoding="utf-8")
        rel = str(page.relative_to(SITE))
        for tag in {m.group(1).lower() for m in TAG_RE.finditer(html)}:
            if tag not in KNOWN:
                unknown[tag] += 1
                unknown_pages.add(rel)
        head = html[: html.find("</head>")] if "</head>" in html else html
        if DOUBLE_ENC_RE.search(head):
            doubled.append(rel)
        if SWALLOWED_RE.search(html):
            swallowed.append(rel)

    print(f"scanned {len(pages)} page(s)")
    bad = 0
    if unknown:
        bad += 1
        print(f"FAIL unknown elements in output: {dict(unknown.most_common(8))}")
        print(f"     e.g. {sorted(unknown_pages)[:4]}")
        print("     markup that should have been text — check inline <code>")
    if swallowed:
        bad += 1
        print(f"FAIL element name eaten by the parser inside <code> on "
              f"{len(swallowed)} page(s): {swallowed[:4]}")
    if doubled:
        bad += 1
        print(f"FAIL double-encoded entity in <head> on {len(doubled)} "
              f"page(s): {doubled[:4]}")
        print("     share cards would show the literal &amp;")
    if not bad:
        print("result: CLEAN")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
