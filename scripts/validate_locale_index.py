#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Indexed pages never lead crawlers into an unindexed locale (decision D4).

Only English and INDEXED_LOCALES (scripts/postbuild_fix.py) are indexed;
every other locale is noindex, follow. An indexed page that links to an
unindexed locale, or lists one as an hreflang alternate, sends crawlers to
pages Search Console then reports as "Crawled, not indexed". /languages/
is the one indexed page allowed to list every locale.

Checks, after a build:

- every page under an unindexed locale carries robots noindex and no
  hreflang alternate or canonical link;
- no indexed page except /languages/ links to an unindexed locale;
- no indexed page lists an unindexed locale as an hreflang alternate;
- the sitemap lists no page under an unindexed locale.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from postbuild_fix import INDEXED_LOCALES, LOCALES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
UNINDEXED = {slug for slug in LOCALES if slug not in INDEXED_LOCALES}
UNINDEXED_CODES = {LOCALES[slug] for slug in UNINDEXED}
HREF = re.compile(r'\bhref="/([a-z]{2,3}(?:-[a-z]+)?)/')
ALTERNATE = re.compile(r'<link rel="alternate"[^>]*\bhreflang="([^"]+)"')
NOINDEX = re.compile(r'<meta name="robots" content="noindex[^"]*"')
CANONICAL = re.compile(r'<link rel="canonical"')
ALLOWED = {"languages/index.html"}


def problems(site: Path) -> list[str]:
    out = []
    for page in sorted(site.rglob("*.html")):
        rel = page.relative_to(site).as_posix()
        html = page.read_text(encoding="utf-8", errors="replace")
        first = rel.split("/", 1)[0]
        if first in UNINDEXED:
            if not NOINDEX.search(html):
                out.append(f"{rel}: unindexed locale page without robots noindex")
            if ALTERNATE.search(html) or CANONICAL.search(html):
                out.append(f"{rel}: unindexed locale page keeps an hreflang or canonical link")
            continue
        if NOINDEX.search(html):
            continue
        if rel not in ALLOWED:
            bad = sorted({m.group(1) for m in HREF.finditer(html) if m.group(1) in UNINDEXED})
            if bad:
                out.append(f"{rel}: links to unindexed locale(s) {', '.join(bad)}")
        alt = sorted({m.group(1) for m in ALTERNATE.finditer(html) if m.group(1) in UNINDEXED_CODES})
        if alt:
            out.append(f"{rel}: hreflang alternate(s) for unindexed locale(s) {', '.join(alt)}")
    sitemap = site / "sitemap.xml"
    if sitemap.is_file():
        listed = re.findall(r"<loc>https://pain001\.com/([^/<]+)/", sitemap.read_text(encoding="utf-8"))
        bad = sorted({s for s in listed if s in UNINDEXED})
        if bad:
            out.append(f"sitemap.xml lists unindexed locale(s) {', '.join(bad)}")
    return out


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "site")
    if not (site / "index.html").is_file():
        print(f"error: {site}/index.html not found; run the build first")
        return 1
    found = problems(site)
    for line in found[:200]:
        print("FAIL", line)
    print(f"validate_locale_index: {len(found)} problem(s); indexed: en, {', '.join(INDEXED_LOCALES)}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
