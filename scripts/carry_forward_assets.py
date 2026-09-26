#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Keep the previous deploy's fingerprinted assets alongside the new ones.

Browsers and the CDN cache HTML for up to ten minutes. If a deploy
dropped the old ``/_csp/<hash>.css`` and ``.js`` files, every cached page
404'd its stylesheet and scripts during that window. The built tree used
to be committed, so the old files were simply copied forward; now the
site is deployed from the workflow, so the old hashes are read from the
live pages and downloaded into the new build. Old hashes are tiny.

Usage: carry_forward_assets.py <output-dir> [--site https://pain001.com]
Never fails the build: an unreachable site means nothing to carry.

Skipped when SOURCE_DATE_EPOCH is set. That marks a reproducible (release)
build, whose output must depend only on the commit, not on what happens to
be deployed; the carried files matter only to a live deploy.
"""
from __future__ import annotations

import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

PAGES = ("/", "/try/", "/documentation/", "/example-corpus/")
ASSET = re.compile(r"/_csp/[0-9a-f]{8,}\.(?:css|js)")


def fetch(url: str) -> bytes | None:
    """Return the body at ``url`` or None on any failure."""
    # The CDN answers a bare urllib user agent with a challenge page.
    request = urllib.request.Request(
        url, headers={"User-Agent": "pain001-site-build/1 (+https://pain001.com)"}
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as r:  # noqa: S310
            return r.read()
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None


def main(argv: list[str] | None = None) -> int:
    """Download every fingerprinted asset the live pages reference."""
    args = argv if argv is not None else sys.argv[1:]
    out = Path(args[0]) if args else Path("site")
    if os.environ.get("SOURCE_DATE_EPOCH"):
        print("[carry-forward] SOURCE_DATE_EPOCH set: reproducible build, nothing carried")
        return 0
    site = "https://pain001.com"
    if "--site" in args:
        site = args[args.index("--site") + 1].rstrip("/")
    wanted: set[str] = set()
    for page in PAGES:
        body = fetch(site + page)
        if body:
            wanted.update(ASSET.findall(body.decode("utf-8", "replace")))
    carried = 0
    for path in sorted(wanted):
        target = out / path.lstrip("/")
        if target.exists():
            continue
        body = fetch(site + path)
        if body:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            carried += 1
    print(f"[carry-forward] {len(wanted)} live asset(s) referenced, {carried} carried into {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
