#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Every indexable page has a search-result-sized title and description.

Search engines cut a title past about 65 characters and a description
past about 160, and treat one under 50 as missing; an audit in November
2026 found 230 indexable pages with a longer description and 44 with a
longer title. This gate fails the build on any indexable page (no
robots noindex, not a redirect stub) whose <title> is over 65 characters
or whose meta description is outside 50..160, counted in characters
after entity decoding, so a translated page is held to the same limits.
It also fails a page whose alternate links name one hreflang twice: every
translated page once kept the template's self link as hreflang="en" beside
the cluster's real English alternate, which Search Console cannot resolve.

    python3 scripts/validate_seo_meta.py [site]
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TITLE_MAX = 65
DESCRIPTION_RANGE = (50, 160)


class Head(HTMLParser):
    """The title, description, robots, refresh and hreflang links of one page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title: str | None = None
        self.meta: dict[str, str] = {}
        self.hreflangs: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: v or "" for k, v in attrs}
        if tag == "title" and self.title is None:
            self._in_title, self.title = True, ""
        elif tag == "meta":
            self._meta(a)
        elif tag == "link":
            self._link(a)

    def _meta(self, a: dict[str, str]) -> None:
        key = (a.get("name") or a.get("http-equiv") or "").lower()
        if key and key not in self.meta:
            self.meta[key] = a.get("content", "")

    def _link(self, a: dict[str, str]) -> None:
        if a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflangs.append(a["hreflang"].lower())

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title = (self.title or "") + data


def head(html: str) -> Head:
    parser = Head()
    parser.feed(html.split("</head>", 1)[0])
    return parser


def indexable(h: Head) -> bool:
    return "noindex" not in h.meta.get("robots", "").lower() and "refresh" not in h.meta


def page_problems(rel: str, html: str) -> list[str]:
    h = head(html)
    if not indexable(h):
        return []
    problems = []
    title = " ".join((h.title or "").split())
    if len(title) > TITLE_MAX:
        problems.append(f"{rel}: title is {len(title)} characters, over {TITLE_MAX}: {title}")
    description = " ".join(h.meta.get("description", "").split())
    low, high = DESCRIPTION_RANGE
    if not low <= len(description) <= high:
        problems.append(f"{rel}: description is {len(description)} characters, not {low} to {high}")
    for lang in sorted({x for x in h.hreflangs if h.hreflangs.count(x) > 1}):
        problems.append(f"{rel}: hreflang {lang} is named by {h.hreflangs.count(lang)} alternate links")
    return problems


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    site = Path(args[0]) if args else ROOT / "site"
    problems: list[str] = []
    pages = [p for p in sorted(site.rglob("*.html")) if "_csp" not in p.parts]
    for page in pages:
        problems += page_problems(page.relative_to(site).as_posix(), page.read_text(encoding="utf-8"))
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"SEO meta: {len(problems)} problem(s) on {len(pages)} page(s)", file=sys.stderr)
        return 1
    print(f"SEO meta: titles and descriptions within limits on {len(pages)} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
