#!/usr/bin/env python3
"""Check the site's dated regulatory claims against their primary sources.

The site gates every version string, link and snippet, but the dates the
pitch leans on (Swift's Standards Release timing, the Fedwire release, the
CHAPS purpose-code mandate) were only ever checked by a person. Swift
deferred one on 27 August 2026 and the site repeated the old date in 35
languages for four weeks. This is the gate that would have caught it.

``scripts/dated_claims.json`` lists each claim with the source it cites,
the sentences that source must still contain, and a review date by which
the source is expected to change. For every claim this script:

1. fetches the source: directly, or through the Internet Archive for hosts
   that refuse non-browser clients (swift.com answers 403); for those it
   first asks the archive for a fresh capture so the check is current, and
   reports the capture date it ended up reading;
2. fails if any expected sentence is missing (the source changed: re-read
   it and update the pages listed under ``cited_on``);
3. fails once the review date has passed (the source promised an update,
   or the claim is near enough to its date to deserve a second look).

A source that cannot be fetched at all is reported and counts as a
failure too: a check that silently skips is the failure mode the rest of
this repository's gates are built to avoid.

Usage: python3 scripts/check_dated_claims.py [--json report.json]
Exit status 0 when every claim holds, 1 otherwise.
"""

from __future__ import annotations

import datetime as dt
import gzip
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAIMS = ROOT / "scripts" / "dated_claims.json"
USER_AGENT = "pain001.com dated-claims check (+https://pain001.com/security.txt)"
WAYBACK_SAVE = "https://web.archive.org/save/"
WAYBACK_RAW = "https://web.archive.org/web/2id_/"  # latest capture, raw body


def _get(url: str, timeout: int = 60) -> tuple[str, str]:
    """Return (final_url, text) for a URL, decoding gzip and deflate."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
        raw = response.read()
        final = response.url
        encoding = response.headers.get("Content-Encoding", "")
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    elif encoding == "deflate":
        raw = zlib.decompress(raw)
    return final, raw.decode("utf-8", "replace")


def visible_text(page: str) -> str:
    """The page as a reader sees it: no markup, one space between words."""
    page = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", page, flags=re.S | re.I)
    page = html.unescape(re.sub(r"<[^>]+>", " ", page))
    return re.sub(r"\s+", " ", page).strip()


def fetch_direct(url: str) -> tuple[str, str]:
    """Fetch a source that serves ordinary clients. Returns (note, text)."""
    _, page = _get(url)
    return "read live", visible_text(page)


def fetch_wayback(url: str) -> tuple[str, str]:
    """Fetch a source through the Internet Archive.

    Asks for a fresh capture first (best effort: the save endpoint is
    rate-limited and may refuse), then reads the latest capture and names
    its date so a stale archive is visible in the report."""
    try:
        _get(WAYBACK_SAVE + url, timeout=90)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        pass  # no fresh capture; the latest existing one is still checked
    final, page = _get(WAYBACK_RAW + url, timeout=90)
    stamp = re.search(r"/web/(\d{4})(\d{2})(\d{2})\d*id_/", final)
    when = "-".join(stamp.groups()) if stamp else "unknown date"
    return f"read from the Internet Archive capture of {when}", visible_text(page)


def check(claim: dict, today: dt.date) -> dict:
    """Check one claim. Returns a report row with ``ok`` and ``problems``."""
    problems: list[str] = []
    note = ""
    try:
        fetch = fetch_wayback if claim.get("via") == "wayback" else fetch_direct
        note, text = fetch(claim["source"])
    except Exception as exc:  # noqa: BLE001 - any failure to read is a finding
        problems.append(f"source could not be read: {exc.__class__.__name__}: {exc}")
        text = ""
    if text:
        folded = re.sub(r"\s+", " ", text).casefold()
        for sentence in claim.get("expect", []):
            if re.sub(r"\s+", " ", sentence).casefold() not in folded:
                problems.append(f"expected sentence not found: {sentence!r}")
    review_by = dt.date.fromisoformat(claim["review_by"])
    if today > review_by:
        problems.append(f"review date {review_by.isoformat()} has passed: {claim.get('review_note', '')}".rstrip())
    return {"id": claim["id"], "source": claim["source"], "fetched": note,
            "cited_on": claim.get("cited_on", []), "ok": not problems, "problems": problems}


def main(argv: list[str]) -> int:
    out = None
    if "--json" in argv:
        out = Path(argv[argv.index("--json") + 1])
    data = json.loads(CLAIMS.read_text(encoding="utf-8"))
    today = dt.date.today()
    rows = [check(claim, today) for claim in data["claims"]]
    for row in rows:
        mark = "ok  " if row["ok"] else "FAIL"
        print(f"{mark} {row['id']}: {row['fetched'] or 'not fetched'}")
        for problem in row["problems"]:
            print(f"       - {problem}")
        if not row["ok"]:
            print(f"       pages citing it: {', '.join(row['cited_on'])}")
    failed = [row for row in rows if not row["ok"]]
    print(f"{len(rows) - len(failed)} of {len(rows)} dated claims hold ({today.isoformat()})")
    if out is not None:
        out.write_text(json.dumps({"date": today.isoformat(), "claims": rows}, indent=2) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
