#!/usr/bin/env python3
"""The published security.txt must be a usable RFC 9116 file.

Production served /security.txt as a 200 with zero bytes, and
/.well-known/security.txt as a 404, while the enterprise page listed it
as evidence for reviewers. Two causes, both silent: the generator writes
an empty file that nothing replaced, and the Pages upload drops
dot-directories unless told otherwise.

Checks, against the built site/:
  1. both paths exist, are non-empty and byte-identical;
  2. at least one Contact, and exactly one Expires, are present
     (RFC 9116 section 2.5);
  3. Expires is in the future and at most a year away (section 2.5.5
     recommends less than a year), so the file cannot quietly lapse;
  4. Canonical names the .well-known URL.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
CANONICAL = "https://pain001.com/.well-known/security.txt"


def fields(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for line in text.splitlines():
        if line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        out.setdefault(key.strip().lower(), []).append(value.strip())
    return out


def main() -> int:
    failures = []
    paths = [SITE / ".well-known" / "security.txt", SITE / "security.txt"]
    bodies = []
    for p in paths:
        if not p.exists() or p.stat().st_size == 0:
            failures.append(f"{p.relative_to(SITE)}: missing or empty")
        else:
            bodies.append(p.read_bytes())
    if len(bodies) == 2 and bodies[0] != bodies[1]:
        failures.append("the two security.txt copies differ")
    if bodies:
        f = fields(bodies[0].decode("utf-8"))
        if not f.get("contact"):
            failures.append("no Contact field")
        expires = f.get("expires", [])
        if len(expires) != 1:
            failures.append(f"expected exactly one Expires field, found {len(expires)}")
        else:
            when = dt.datetime.fromisoformat(expires[0].replace("Z", "+00:00"))
            now = dt.datetime.now(dt.timezone.utc)
            if when <= now:
                failures.append(f"Expires {expires[0]} is in the past")
            elif when - now > dt.timedelta(days=366):
                failures.append(f"Expires {expires[0]} is more than a year away")
        if CANONICAL not in f.get("canonical", []):
            failures.append(f"Canonical does not name {CANONICAL}")
    for msg in failures:
        print(f"FAIL {msg}")
    print("result:", "FAIL" if failures else "CLEAN")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
