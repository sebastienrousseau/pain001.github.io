#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Every figure the site shows comes from the claims register (decision D5).

Checks, after a build:

- every ``data-claim`` element on a built page names a claim in
  data/claims.yml and shows exactly that claim's figure;
- every claim lists the pages it appears on, and appears on each of them;
- every claim was verified for the current release (VERSION), so a
  figure cannot outlive the release it was checked for. Live figures are
  stamped by ``scripts/claims.py refresh``; manual ones are re-checked by
  hand at each release.

Fix a failure by correcting the register or the page, never by
loosening this check.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from claims import CLAIM_ELEMENT, REGISTER, VERSION, by_id, load, render  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def problems(site: Path, register: dict, version: str) -> list[str]:
    out = []
    claims = by_id(register)
    seen: dict[str, set[str]] = {}
    for page in sorted(site.rglob("*.html")):
        rel = "/" + page.relative_to(site).as_posix()
        rel = rel[: -len("index.html")] if rel.endswith("index.html") else rel
        for m in CLAIM_ELEMENT.finditer(page.read_text(encoding="utf-8")):
            cid, shown = m.group(3), m.group(4).strip()
            claim = claims.get(cid)
            if claim is None:
                out.append(f"{rel}: data-claim=\"{cid}\" is not in data/claims.yml")
                continue
            seen.setdefault(cid, set()).add(rel)
            if shown != render(claim):
                out.append(f"{rel}: {cid} shows {shown!r}, the register says {render(claim)!r}")
    for cid, claim in claims.items():
        for page in claim["pages"]:
            if page not in seen.get(cid, set()):
                out.append(f"{cid}: listed for {page} but not shown there")
        if claim["verified_in"] != version:
            out.append(f"{cid}: verified in {claim['verified_in']}, the release is {version}; "
                       f"re-check {claim['evidence_url']}")
        if not claim.get("evidence_url", "").startswith("https://"):
            out.append(f"{cid}: no evidence URL")
    return out


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "site")
    if not (site / "index.html").is_file():
        print(f"error: {site}/index.html not found; run the build first")
        return 1
    found = problems(site, load(REGISTER), VERSION.read_text(encoding="utf-8").strip())
    for line in found:
        print("FAIL", line)
    print(f"validate_claims: {len(found)} problem(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
