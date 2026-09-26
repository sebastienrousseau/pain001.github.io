#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Fetch the browser demo's WebAssembly runtime and verify every byte.

The demo at /try/ runs the pain001 library in Pyodide. Its binaries (the
Python runtime compiled to WebAssembly, the zipped standard library, and
the wheels the library needs) used to be committed under static/pyodide/.
OpenSSF Scorecard flags committed binaries (Binary-Artifacts) because a
reviewer cannot read them, and it was right to: nothing in the repository
proved the committed bytes were the published ones.

They are now fetched at build time. static/pyodide/pain001-runtime.json
stays committed and is the single source of truth: each binary's file
name, size, SHA-256 and upstream URL (the Pyodide release on its CDN, or
PyPI). A file is written into static/pyodide/ only after its hash matches
the manifest, so the site ships exactly the bytes the manifest pins, and
a changed or tampered upstream fails the build instead of shipping.

Downloads are cached by hash under $PAIN001_RUNTIME_CACHE (default
~/.cache/pain001-runtime), so repeat builds and CI reruns do not refetch.

Usage: python3 scripts/fetch_runtime.py [--check]
  --check   verify what is in static/pyodide/ without downloading;
            exit 1 if anything is missing or does not match.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / "static" / "pyodide"
MANIFEST = RUNTIME / "pain001-runtime.json"
CACHE = Path(os.environ.get("PAIN001_RUNTIME_CACHE", Path.home() / ".cache" / "pain001-runtime"))
USER_AGENT = "pain001.com build (+https://pain001.com/security.txt)"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def binaries() -> list[dict]:
    """Every manifest entry that carries an upstream URL."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = [e for key in ("runtime", "packages", "wheels") for e in manifest.get(key, [])]
    return [e for e in entries if e.get("url")]


def download(url: str, dest: Path) -> None:
    last: Exception | None = None
    for attempt in range(1, 5):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=120) as response, dest.open("wb") as out:  # nosec B310 - fixed https URLs from the manifest
                shutil.copyfileobj(response, out)
            return
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = exc
            time.sleep(2 * attempt)
    raise SystemExit(f"[runtime] could not download {url}: {last}")


def fetch(entry: dict) -> str:
    """Put a verified copy of one binary in static/pyodide/. Returns how."""
    target = RUNTIME / entry["file"]
    want = entry["sha256"]
    if target.is_file() and sha256(target) == want:
        return "present"
    cached = CACHE / want
    if not (cached.is_file() and sha256(cached) == want):
        CACHE.mkdir(parents=True, exist_ok=True)
        partial = cached.with_suffix(".part")
        download(entry["url"], partial)
        got = sha256(partial)
        if got != want:
            partial.unlink(missing_ok=True)
            raise SystemExit(
                f"[runtime] {entry['file']}: {entry['url']} served sha256 {got}, "
                f"the manifest pins {want}; refusing to use it")
        partial.replace(cached)
        how = "downloaded"
    else:
        how = "cached"
    shutil.copyfile(cached, target)
    return how


def main(argv: list[str]) -> int:
    entries = binaries()
    if "--check" in argv:
        bad = [e["file"] for e in entries
               if not (RUNTIME / e["file"]).is_file() or sha256(RUNTIME / e["file"]) != e["sha256"]]
        for name in bad:
            print(f"[runtime] missing or modified: {name}")
        print(f"[runtime] {len(entries) - len(bad)} of {len(entries)} binaries verified")
        return 1 if bad else 0
    counts: dict[str, int] = {}
    for entry in entries:
        how = fetch(entry)
        counts[how] = counts.get(how, 0) + 1
    summary = ", ".join(f"{n} {how}" for how, n in sorted(counts.items()))
    print(f"[runtime] {len(entries)} binaries verified against the manifest ({summary})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
