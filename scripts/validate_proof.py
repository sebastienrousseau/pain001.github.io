#!/usr/bin/env python3
"""Every figure in the homepage proof band must equal its source.

The proof band is the site's answer to a named-customer wall: four
figures a reviewer can check. A figure typed by hand drifts the day a
scenario, a message edition or a locale is added, and a stale proof
figure is worse than none. The homepage already carried one: it said
"12 supported message definitions" while pain001 generated 13.

Each ``<dd data-proof-key="...">`` in site/index.html is recomputed:

  scenarios  English corpus pages in _posts/, every one of which must
             record "Official XSD: passed" (the label claims it)
  countries  distinct country codes among those scenarios
  editions   message-specification pages, one per pain.* edition
  languages  translated landing pages in the built site (html lang is
             not English)

Run after a build. Fix a failure by changing the figure, never the
source.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
SITE = ROOT / "site"

CORPUS = re.compile(r"^corpus-([a-z]{2})-[a-z0-9-]+\.md$")
EDITION = re.compile(r"^message-spec-pain\.\d{3}\.\d{3}\.\d{2}\.md$")
XSD_PASSED = "- **Official XSD**: passed."
FIGURE = re.compile(r'data-proof-key="([a-z]+)">([^<]+)<')
HTML_LANG = re.compile(r'<html[^>]*\blang="([^"]+)"')


def sources() -> tuple[dict[str, int], list[str]]:
    problems = []
    scenarios = sorted(p for p in POSTS.iterdir() if CORPUS.match(p.name))
    for page in scenarios:
        if XSD_PASSED not in page.read_text(encoding="utf-8"):
            problems.append(f"{page.name}: no '{XSD_PASSED}' line")
    countries = {CORPUS.match(p.name).group(1) for p in scenarios}
    editions = [p for p in POSTS.iterdir() if EDITION.match(p.name)]
    languages = 0
    for d in SITE.iterdir():
        index = d / "index.html"
        if d.is_dir() and index.exists():
            m = HTML_LANG.search(index.read_text(encoding="utf-8", errors="ignore")[:2000])
            if m and not m.group(1).lower().startswith("en"):
                languages += 1
    return {
        "scenarios": len(scenarios),
        "countries": len(countries),
        "editions": len(editions),
        "languages": languages,
    }, problems


def main() -> int:
    home = SITE / "index.html"
    if not home.exists():
        print("error: site/index.html not found; run the build first")
        return 1
    shown = {k: v.strip() for k, v in FIGURE.findall(home.read_text(encoding="utf-8"))}
    truth, failures = sources()
    for key, value in truth.items():
        if key not in shown:
            failures.append(f"{key}: no data-proof-key=\"{key}\" figure on the homepage")
        elif shown[key] != str(value):
            failures.append(f"{key}: homepage shows {shown[key]}, source says {value}")
        else:
            print(f"ok   {key} = {value}")
    for extra in sorted(set(shown) - set(truth)):
        failures.append(f"{extra}: figure has no source in this gate")
    for f in failures:
        print(f"FAIL {f}")
    print("result:", "FAIL" if failures else "CLEAN")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
