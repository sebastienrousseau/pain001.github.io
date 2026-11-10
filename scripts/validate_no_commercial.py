#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The built site offers nothing for sale and names no employer.

Decision D0 (10 November 2026): Pain001 is free open-source software
maintained in a personal capacity, with no paid support, services,
briefings, sponsorships, donations or referral fees under any name, and
the site never mentions HSBC. This gate fails the build when a phrase of
the retired commercial offer, a funding-platform link, a link to the
retired /enterprise/ or /thanks/ pages, or "hsbc" in any case appears in
any built text file.

Run after a build. Fix a failure by removing the copy, never by adding
an exception here.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
TEXT = {".html", ".xml", ".txt", ".json", ".css", ".js", ".md"}
# The redirect stubs for the retired pages are the only files allowed to
# exist at those paths; nothing else may link to them.
STUBS = {"enterprise/index.html", "thanks/index.html"}
FORBIDDEN = [
    (re.compile(r"hsbc", re.I), "an employer's name (hsbc)"),
    (re.compile(r"book (?:an? )?(?:architecture )?briefing", re.I), "a briefing offer"),
    (re.compile(r"architecture briefing", re.I), "a briefing offer"),
    (re.compile(r"paid (?:support|options?|engagement|services?)", re.I), "a paid offer"),
    (re.compile(r"no prices on this page", re.I), "the enquiry page"),
    (re.compile(r"private profile derivation", re.I), "the retired paid profile offer"),
    (re.compile(r"supported release channel", re.I), "the retired paid support channel"),
    (re.compile(r"throat to choke", re.I), "the retired enterprise copy"),
    (re.compile(r"formspree", re.I), "the retired enquiry form"),
    (re.compile(r"github\.com/sponsors|buymeacoffee|ko-fi\.com|patreon\.com|opencollective\.com|liberapay", re.I),
     "a funding link"),
    (re.compile(r'href="/(?:[a-z-]+/)?(?:enterprise|thanks)/'), "a link to a retired page"),
]


def main() -> int:
    if not (SITE / "index.html").is_file():
        print(f"error: {SITE}/index.html not found; run the build first")
        return 1
    failures = []
    for path in sorted(SITE.rglob("*")):
        if path.suffix not in TEXT or not path.is_file():
            continue
        rel = path.relative_to(SITE).as_posix()
        if rel in STUBS or rel.startswith("pyodide/"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, what in FORBIDDEN:
            m = pattern.search(text)
            if m:
                failures.append(f"{rel}: {what}: {text[max(0, m.start() - 40):m.end() + 40]!r}")
    for line in failures:
        print("FAIL", line)
    print(f"validate_no_commercial: {len(failures)} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
