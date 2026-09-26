#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Refresh the traction table on the governance page from public sources.

Runs before the site build. Reads PyPI download statistics and the GitHub
repository API and rewrites the block between ``<!-- traction:start -->``
and ``<!-- traction:end -->`` in ``_posts/governance.md``. When a source
is unreachable the previous figures stay in place and the script exits 0,
so an offline build still succeeds with the last published numbers.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "_posts" / "governance.md"
PYPISTATS = "https://pypistats.org/api/packages/pain001/recent"
GITHUB = "https://api.github.com/repos/sebastienrousseau/pain001"
BLOCK = re.compile(r"<!-- traction:start -->.*?<!-- traction:end -->", re.S)


def fetch(url: str) -> dict:
    """Return the JSON body of a public endpoint."""
    request = urllib.request.Request(url, headers={"User-Agent": "pain001.com build"})
    with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310
        return json.load(response)


def render(month: int, week: int, stars: int, forks: int, day: str) -> str:
    """The table between the markers."""
    return (
        "<!-- traction:start -->\n"
        "Figures refreshed at each site build from public sources (PyPI download "
        "statistics and the GitHub API); the date is the build date.\n\n"
        "| Measure | Value | Source |\n| :--- | ---: | :--- |\n"
        f"| pain001 downloads, last 30 days | {month:,} | PyPI |\n"
        f"| pain001 downloads, last 7 days | {week:,} | PyPI |\n"
        f"| GitHub stars | {stars:,} | GitHub |\n"
        f"| GitHub forks | {forks:,} | GitHub |\n\n"
        f"Refreshed {day}. Page views are counted by Cloudflare Web Analytics, "
        "cookieless and without identifiers ([privacy](/privacy/)); the browser "
        "demo is not measured, by design.\n"
        "<!-- traction:end -->"
    )


def main() -> int:
    try:
        stats = fetch(PYPISTATS)["data"]
        repo = fetch(GITHUB)
    except Exception as exc:  # noqa: BLE001 - any network failure keeps the old figures
        print(f"traction: sources unreachable ({exc}); keeping the published figures")
        return 0
    text = PAGE.read_text(encoding="utf-8")
    if not BLOCK.search(text):
        print("traction: no markers on the governance page")
        return 1
    day = dt.date.today().isoformat()
    new = render(int(stats["last_month"]), int(stats["last_week"]), int(repo["stargazers_count"]), int(repo["forks_count"]), day)
    PAGE.write_text(BLOCK.sub(lambda _: new, text), encoding="utf-8")
    print(f"traction: refreshed for {day}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
