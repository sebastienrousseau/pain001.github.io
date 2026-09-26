#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
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

A downloaded file is kept only when it is what its name says: served as
CSS or JavaScript, and not an HTML page. The fingerprints are not content
hashes, so they cannot be checked; this stops a CDN challenge or error page
from being published as a stylesheet or script (security review SR-3).
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
EXPECTED_TYPES = {
    ".css": {"text/css"},
    ".js": {"application/javascript", "text/javascript"},
}


def fetch(url: str) -> tuple[bytes, str] | None:
    """Return the body at ``url`` and its Content-Type, or None on any failure."""
    # The CDN answers a bare urllib user agent with a challenge page.
    request = urllib.request.Request(
        url, headers={"User-Agent": "pain001-site-build/1 (+https://pain001.com)"}
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as r:  # noqa: S310
            return r.read(), r.headers.get("Content-Type", "")
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None


def is_asset(path: str, body: bytes, content_type: str) -> bool:
    """True when a download is the stylesheet or script its path names."""
    mime = content_type.split(";", 1)[0].strip().lower()
    if mime not in EXPECTED_TYPES.get(Path(path).suffix, set()):
        return False
    return not body.lstrip().startswith(b"<")


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
        got = fetch(site + page)
        if got:
            wanted.update(ASSET.findall(got[0].decode("utf-8", "replace")))
    carried = skipped = 0
    for path in sorted(wanted):
        target = out / path.lstrip("/")
        if target.exists():
            continue
        got = fetch(site + path)
        if not got or not got[0]:
            continue
        body, content_type = got
        if not is_asset(path, body, content_type):
            print(f"[carry-forward] skipped {path}: served as {content_type or 'no type'}, not the asset it names")
            skipped += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        carried += 1
    print(f"[carry-forward] {len(wanted)} live asset(s) referenced, {carried} carried into {out}, "
          f"{skipped} skipped as not CSS or JavaScript")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
