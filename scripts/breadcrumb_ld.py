#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""schema.org BreadcrumbList for every page that shows a breadcrumb trail.

The layouts before the PRISM theme (v0.0.3, September 2026) carried a
BreadcrumbList in their JSON-LD graph; the PRISM layouts kept the
visible trail (``<nav class="breadcrumb">``) but not the markup, and
Search Console's Breadcrumbs report fell to zero. ssg's own breadcrumb
JSON-LD never runs here, because it skips any page whose layout already
has a JSON-LD block.

The markup is read from the trail the page shows, after the locale
passes have translated it, so the names are the ones a reader sees in
that language and the two cannot drift. The current page's item is its
canonical URL. Run after ``postbuild_fix.py`` (see build.sh):

    python3 scripts/breadcrumb_ld.py Pain001
"""
from __future__ import annotations

import html as _html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

BASE = "https://pain001.com/"
NAV_RE = re.compile(r'<nav class="breadcrumb"[^>]*>(.*?)</nav>', re.S)
ITEM_RE = re.compile(r"<li\b[^>]*>(.*?)</li>", re.S)
HREF_RE = re.compile(r'<a\b[^>]*\bhref="([^"]*)"')
TAG_RE = re.compile(r"<[^>]+>")
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')


def trail(page: str) -> list[tuple[str, str | None]]:
    """The visible breadcrumb as (name, href) pairs; href is None for the
    current page. Empty when the page shows no trail."""
    nav = NAV_RE.search(page)
    if not nav:
        return []
    items = []
    for inner in ITEM_RE.findall(nav.group(1)):
        name = " ".join(_html.unescape(TAG_RE.sub("", inner)).split())
        href = HREF_RE.search(inner)
        if name:
            items.append((name, href.group(1) if href else None))
    return items


def breadcrumb_ld(items: list[tuple[str, str | None]], page_url: str) -> dict:
    """The BreadcrumbList for a trail; a link resolves against the site,
    the unlinked current page takes the page's own URL."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": n, "name": name,
             "item": urljoin(BASE, href) if href is not None else page_url}
            for n, (name, href) in enumerate(items, 1)
        ],
    }


def page_url(page: str, rel: str) -> str:
    """The canonical URL, or the URL the file is served at."""
    canonical = CANONICAL_RE.search(page)
    if canonical:
        return canonical.group(1)
    return urljoin(BASE, rel.removesuffix("index.html"))


def add_breadcrumbs(page: str, rel: str) -> str:
    """The page with its BreadcrumbList block before </head>; unchanged
    when it shows no trail of two or more items or already has one."""
    items = trail(page)
    if len(items) < 2 or '"BreadcrumbList"' in page or "</head>" not in page:
        return page
    data = json.dumps(breadcrumb_ld(items, page_url(page, rel)), ensure_ascii=False)
    block = '<script type="application/ld+json">' + data.replace("</", "<\\/") + "</script>\n"
    return page.replace("</head>", block + "</head>", 1)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or not Path(args[0]).is_dir():
        print("usage: breadcrumb_ld.py <built site directory>", file=sys.stderr)
        return 2
    site = Path(args[0])
    added = 0
    for path in sorted(site.rglob("*.html")):
        page = path.read_text(encoding="utf-8")
        new = add_breadcrumbs(page, path.relative_to(site).as_posix())
        if new != page:
            path.write_text(new, encoding="utf-8")
            added += 1
    print(f"[breadcrumb_ld] BreadcrumbList on {added} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
