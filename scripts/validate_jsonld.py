#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Every JSON-LD block on the built site parses, and the homepage
states the software, its owner and its version.

Checks, against the built site/:
  1. every <script type="application/ld+json"> on every page is valid
     JSON with an @context of https://schema.org;
  2. no page claims an aggregateRating or a review: there are no
     on-page reviews to back one;
  3. the homepage graph has one SoftwareApplication whose
     softwareVersion is the suite version in static/corpus/index.json,
     offered at price 0, linked to the Organization and the Person;
  4. every Dataset description is 50 to 5000 characters, the range
     Google's Dataset rich result accepts.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BLOCK_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
PERSON_ID = "https://sebastienrousseau.com/#person"
DATASET_DESCRIPTION = (50, 5000)


def blocks(html: str) -> list[str]:
    return BLOCK_RE.findall(html)


def nodes(data) -> list[dict]:
    if isinstance(data, list):
        return [n for item in data for n in nodes(item)]
    if isinstance(data, dict):
        graph = data.get("@graph")
        return [n for n in graph if isinstance(n, dict)] if isinstance(graph, list) else [data]
    return []


def dataset_problems(rel: str, data) -> list[str]:
    """Search Console's Dataset report rejects these as critical errors."""
    low, high = DATASET_DESCRIPTION
    problems = []
    for node in nodes(data):
        if node.get("@type") != "Dataset":
            continue
        length = len(str(node.get("description", "")))
        if not low <= length <= high:
            problems.append(f"{rel}: Dataset description is {length} characters, not {low} to {high}")
    return problems


def page_problems(rel: str, html: str) -> list[str]:
    problems = []
    for text in blocks(html):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            problems.append(f"{rel}: JSON-LD does not parse ({exc.msg})")
            continue
        context = data.get("@context") if isinstance(data, dict) else None
        if context not in ("https://schema.org", "https://schema.org/"):
            problems.append(f"{rel}: JSON-LD @context is {context!r}")
        if re.search(r'"(aggregateRating|review)"', text):
            problems.append(f"{rel}: JSON-LD claims a rating or review")
        problems += dataset_problems(rel, data)
    return problems


def home_problems(html: str, version: str) -> list[str]:
    found = [n for text in blocks(html) for n in nodes(json.loads(text))]
    apps = [n for n in found if n.get("@type") == "SoftwareApplication"]
    if len(apps) != 1:
        return [f"homepage has {len(apps)} SoftwareApplication nodes, not 1"]
    app = apps[0]
    problems = []
    if app.get("softwareVersion") != version:
        problems.append(f"homepage softwareVersion {app.get('softwareVersion')!r} is not {version!r}")
    if (app.get("offers") or {}).get("price") != "0":
        problems.append("homepage SoftwareApplication is not offered at price 0")
    if (app.get("author") or {}).get("@id") != PERSON_ID:
        problems.append("homepage SoftwareApplication author is not the Person entity")
    if not any(n.get("@type") == "Organization" and n.get("@id") == (app.get("publisher") or {}).get("@id") for n in found):
        problems.append("homepage SoftwareApplication publisher is not an Organization in the graph")
    return problems


def main() -> int:
    version = json.loads((ROOT / "static" / "corpus" / "index.json").read_text(encoding="utf-8"))["pain001"]
    problems: list[str] = []
    pages = sorted(SITE.rglob("*.html"))
    count = 0
    for page in pages:
        html = page.read_text(encoding="utf-8")
        count += len(blocks(html))
        problems += page_problems(page.relative_to(SITE).as_posix(), html)
    problems += home_problems((SITE / "index.html").read_text(encoding="utf-8"), version)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print(f"JSON-LD: {count} block(s) on {len(pages)} page(s) parse; homepage states Pain001 {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
