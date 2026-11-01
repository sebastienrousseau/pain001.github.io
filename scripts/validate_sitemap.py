#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The sitemap lists only canonical, indexable pages, and no noindex page
names itself canonical.

Search Console reported pages that were noindex while their canonical
link pointed at themselves (the translated corpus scenarios), which is
two contradictory signals for one URL.

Checks, against the built site/:
  1. every <loc> in sitemap.xml is a page in the build, carries no robots
     noindex, and its canonical link names that same URL;
  2. no noindex page carries a canonical link to its own URL.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.etree import ElementTree

SITE = Path(__file__).resolve().parent.parent / "site"
BASE_URL = "https://pain001.com"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')
NOINDEX_RE = re.compile(r'<meta name="robots" content="[^"]*noindex')


def page_url(site: Path, page: Path) -> str:
    """The public URL of a built index.html."""
    rel = page.parent.relative_to(site).as_posix()
    return BASE_URL + "/" if rel == "." else f"{BASE_URL}/{rel}/"


def page_path(site: Path, url: str) -> Path:
    """The built index.html that serves a sitemap URL."""
    return site / url.removeprefix(BASE_URL).strip("/") / "index.html"


def canonical(html: str) -> str | None:
    match = CANONICAL_RE.search(html)
    return match.group(1) if match else None


def check_sitemap_url(site: Path, url: str) -> str | None:
    """Why a sitemap URL is not a canonical, indexable page, or None."""
    page = page_path(site, url)
    if not url.startswith(BASE_URL + "/") or not page.is_file():
        return f"{url}: not a page in the build"
    html = page.read_text(encoding="utf-8")
    if NOINDEX_RE.search(html):
        return f"{url}: listed in the sitemap but noindex"
    if canonical(html) != url:
        return f"{url}: canonical is {canonical(html)}"
    return None


def check_noindex_page(site: Path, page: Path) -> str | None:
    """Why a noindex page sends a contradictory canonical, or None."""
    html = page.read_text(encoding="utf-8")
    url = page_url(site, page)
    if NOINDEX_RE.search(html) and canonical(html) == url:
        return f"{url}: noindex yet canonical to itself"
    return None


def problems(site: Path) -> list[str]:
    root = ElementTree.parse(site / "sitemap.xml").getroot()
    urls = [loc.text or "" for loc in root.iter(f"{NS}loc")]
    found = [check_sitemap_url(site, url) for url in urls]
    found += [check_noindex_page(site, p) for p in sorted(site.rglob("index.html"))]
    return [p for p in found if p]


def main() -> int:
    found = problems(SITE)
    for problem in found:
        print(problem, file=sys.stderr)
    print(f"validate_sitemap: {len(found)} problem(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
