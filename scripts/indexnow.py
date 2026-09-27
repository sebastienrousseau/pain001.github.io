#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tell IndexNow search engines about every URL in the sitemap.

IndexNow (https://www.indexnow.org/) lets a site notify Bing, Yandex,
Seznam, Naver and the other participating engines that URLs changed, so
they recrawl within hours instead of on their own schedule. Engines share
submissions with each other, and no account is needed: the site proves it
owns the host by publishing a key file at its root. The key is
static/<key>.txt, served at https://pain001.com/<key>.txt.

CI runs this after each Pages deploy on main. It reads the sitemap (a
local file, or the live one fetched with a cache-busting query so the
CDN's copy of the previous deploy is not used), POSTs the URLs in batches
of at most 10,000, and logs each HTTP status. It never fails: a search
engine being unreachable must not fail a deploy.

Usage:
  python3 scripts/indexnow.py [--sitemap PATH_OR_URL] [--dry-run]
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "pain001.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
DEFAULT_SITEMAP = "https://pain001.com/sitemap.xml"
BATCH = 10_000
KEY_NAME = re.compile(r"^[0-9a-f]{32}\.txt$")
LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")
USER_AGENT = "pain001.com build (+https://pain001.com/security.txt)"


def find_key(static: Path = ROOT / "static") -> str:
    """The key is the file static/<key>.txt whose content is <key>."""
    for path in sorted(static.glob("*.txt")):
        if KEY_NAME.match(path.name) and path.read_text(encoding="utf-8").strip() == path.stem:
            return path.stem
    raise SystemExit("[indexnow] no key file static/<32 hex>.txt containing its own name")


def read_sitemap(source: str) -> str:
    if source.startswith(("https://", "http://")):
        url = f"{source}{'&' if '?' in source else '?'}cb={int(time.time())}"
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310 - fixed https URL
            return response.read().decode("utf-8")
    return Path(source).read_text(encoding="utf-8")


def site_urls(sitemap_xml: str) -> list[str]:
    """Every <loc> on this host, in order, without duplicates."""
    seen: dict[str, None] = {}
    for url in LOC.findall(sitemap_xml):
        if url.startswith(f"https://{HOST}/") or url == f"https://{HOST}":
            seen.setdefault(url, None)
    return list(seen)


def batches(urls: list[str], size: int = BATCH) -> list[list[str]]:
    return [urls[i:i + size] for i in range(0, len(urls), size)]


def payload(key: str, urls: list[str]) -> dict:
    return {"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}


def submit(body: dict) -> int | str:
    """POST one batch; return the HTTP status, or the error text."""
    request = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310 - fixed https URL
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return f"unreachable ({exc})"


def main(argv: list[str]) -> int:
    source = DEFAULT_SITEMAP
    if "--sitemap" in argv:
        source = argv[argv.index("--sitemap") + 1]
    try:
        key = find_key()
        urls = site_urls(read_sitemap(source))
    except (SystemExit, OSError, urllib.error.URLError, UnicodeDecodeError) as exc:
        print(f"[indexnow] skipped: {exc}")
        return 0
    if not urls:
        print(f"[indexnow] no {HOST} URLs in {source}; nothing submitted")
        return 0
    for number, chunk in enumerate(batches(urls), 1):
        if "--dry-run" in argv:
            print(f"[indexnow] dry run: batch {number} would submit {len(chunk)} URL(s)")
            continue
        status = submit(payload(key, chunk))
        # 200 and 202 mean accepted; anything else is logged, never fatal.
        print(f"[indexnow] batch {number}: {len(chunk)} URL(s) -> {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
