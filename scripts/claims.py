#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The claims register: data/claims.yml (decision D5).

Every adoption or quality figure the site shows has one entry here, with
its evidence URL and the release it was verified for. This module is used
three ways:

- ``python3 scripts/claims.py refresh`` runs before the build and refreshes
  the live figures (GitHub stars, PyPI downloads in the last month, the
  OpenSSF Scorecard score, the number of releases) from public sources,
  stamping them with the current VERSION. When a source is unreachable the
  previous figure and its verified_in stay, so an offline build still
  succeeds, and validate_claims.py then reports the figure as stale.
- postbuild_fix.py calls :func:`fill` to write each figure into every
  ``data-claim="<id>"`` element of the built pages.
- validate_claims.py checks the built pages against the register.

The file is YAML whose body is JSON, so the standard library reads it.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "data" / "claims.yml"
VERSION = ROOT / "VERSION"
CORE = "sebastienrousseau/pain001"
CLAIM_ELEMENT = re.compile(r'(<(\w+)\b[^>]*\bdata-claim="([a-z0-9_]+)"[^>]*>)(.*?)(</\2>)', re.S)


# Split so REUSE does not read these string literals as this file's header.
HEADER = (
    "# SPDX-" "FileCopyrightText: 2023-2026 Sebastien Rousseau\n"
    "# SPDX-" "License-Identifier: Apache-2.0 OR MIT\n"
)


def load(path: Path = REGISTER) -> dict:
    """The register as a dict with a ``claims`` list.

    The file is YAML whose body is JSON: leading ``#`` comment lines (the
    SPDX header) are skipped and the rest is parsed as JSON.
    """
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    while lines and lines[0].lstrip().startswith("#"):
        lines.pop(0)
    return json.loads("".join(lines))


def dump(register: dict, path: Path = REGISTER) -> None:
    """Write the register back with its SPDX header."""
    path.write_text(HEADER + json.dumps(register, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def by_id(register: dict) -> dict[str, dict]:
    """Claims keyed by id."""
    return {c["id"]: c for c in register["claims"]}


def render(claim: dict) -> str:
    """The figure as the site shows it."""
    value, kind = claim["value"], claim["format"]
    if kind == "count":
        return f"{int(value):,}"
    if kind == "score":
        return f"{float(value):.1f}"
    return str(value)


def fill(html: str, register: dict) -> str:
    """Write each register figure into its ``data-claim`` elements.

    An id the register does not hold is left untouched for
    validate_claims.py to report.
    """
    claims = by_id(register)

    def sub(m: re.Match) -> str:
        claim = claims.get(m.group(3))
        return m.group(0) if claim is None else m.group(1) + render(claim) + m.group(5)

    return CLAIM_ELEMENT.sub(sub, html)


def fetch(url: str):
    """The JSON body of a public endpoint."""
    request = urllib.request.Request(url, headers={"User-Agent": "pain001.com build"})
    with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310
        return json.load(response)


def release_count() -> int:
    """Published core releases, following the API's pages of 100."""
    total, page = 0, 1
    while True:
        batch = fetch(f"https://api.github.com/repos/{CORE}/releases?per_page=100&page={page}")
        total += len(batch)
        if len(batch) < 100:
            return total
        page += 1


def live_values() -> dict[str, object]:
    """Each live figure that its source returned; a failed source is absent."""
    out: dict[str, object] = {}
    sources = {
        "github_stars": lambda: fetch(f"https://api.github.com/repos/{CORE}")["stargazers_count"],
        "pypi_downloads_month": lambda: fetch("https://pypistats.org/api/packages/pain001/recent")["data"]["last_month"],
        "openssf_scorecard": lambda: fetch(f"https://api.securityscorecards.dev/projects/github.com/{CORE}")["score"],
        "releases_since_2023": release_count,
    }
    for key, get in sources.items():
        try:
            out[key] = get()
        except Exception as exc:  # noqa: BLE001 - any failure keeps the previous figure
            print(f"[claims] {key}: source unreachable ({exc}); keeping the previous figure")
    return out


def refresh(register: dict, values: dict[str, object], version: str) -> dict:
    """Apply fetched live values, stamping each with ``version``."""
    for claim in register["claims"]:
        if claim["source"] == "live" and claim["id"] in values:
            claim["value"] = values[claim["id"]]
            claim["verified_in"] = version
    return register


def main(argv: list[str]) -> int:
    if argv[1:] != ["refresh"]:
        print("usage: claims.py refresh")
        return 2
    register = refresh(load(), live_values(), VERSION.read_text(encoding="utf-8").strip())
    dump(register)
    print(f"[claims] {len(register['claims'])} claim(s) in data/claims.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
