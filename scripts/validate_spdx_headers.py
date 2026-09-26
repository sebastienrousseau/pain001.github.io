#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Fail when a source file does not carry its own licence and copyright.

REUSE compliance (``reuse lint``) is satisfied by REUSE.toml, which can
annotate files from outside. The OpenSSF Best Practices gold criteria ask
for more: a copyright statement and a licence statement inside each
source file. This gate checks the first ten lines of every tracked source
file for both SPDX tags.

Vendored and generated files are exempt; their provenance is recorded in
REUSE.toml and THIRD_PARTY_NOTICES.md.

Usage: python3 scripts/validate_spdx_headers.py
"""

from __future__ import annotations

import re
import subprocess
import sys

SOURCE = re.compile(r"\.(py|js|mjs|cjs|sh|css|html|yml|yaml|toml)$|(^|/)Makefile$")
EXEMPT = re.compile(
    r"^static/(pyodide|corpus|market|coverage)/"  # fetched runtime, generated corpus
    r"|^static/js/cf-beacon\.min\.js$"  # vendored Cloudflare beacon
    r"|^_posts/"  # page content, not source code
    r"|^docs/"  # documentation
)
TAGS = ("SPDX-FileCopyrightText:", "SPDX-License-Identifier:")


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files"], check=True, capture_output=True, text=True).stdout
    return [f for f in out.splitlines() if SOURCE.search(f) and not EXEMPT.search(f)]


def missing(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="replace") as handle:
        head = "".join(handle.readline() for _ in range(10))
    return [tag.rstrip(":") for tag in TAGS if tag not in head]


def main() -> int:
    files = tracked()
    bad = {f: m for f in files if (m := missing(f))}
    for path, tags in sorted(bad.items()):
        print(f"[spdx] {path}: missing {', '.join(tags)}")
    print(f"[spdx] {len(files) - len(bad)} of {len(files)} source files carry their own SPDX header")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
