#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Decide which pain001 release to regenerate for, and pin its wheel.

The regenerate workflow used to wait for the library's publish job to
send a repository_dispatch. That needs a personal access token stored
in the library repository, which never existed, so the site silently
fell behind every release. The workflow now also polls PyPI on a
schedule, and this script answers its two questions without any token.

  target [VERSION]  Print the version to regenerate for, or nothing.
                    With VERSION (a dispatch or a manual run) it is
                    that version. Without it (the schedule) it is the
                    newest release on PyPI, but only when that is newer
                    than the release the demo's runtime manifest pins.

  pin VERSION       Point static/pyodide/pain001-runtime.json at that
                    release's wheel on PyPI: file, size, SHA-256 and
                    URL. build.sh then downloads it and refuses it if
                    a byte differs. Prints a warning when the release's
                    core dependencies differ from the pinned one's,
                    because the demo's other wheels may then need
                    updating by hand.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "static" / "pyodide" / "pain001-runtime.json"
PYPI = "https://pypi.org/pypi/pain001{}/json"
VERSION = re.compile(r"\d+\.\d+\.\d+")
WHEEL_URL = "https://files.pythonhosted.org/packages/py3/p/pain001/{}"


def pypi(version: str = "") -> dict:
    with urllib.request.urlopen(PYPI.format(f"/{version}" if version else ""), timeout=30) as response:  # nosec B310 - fixed https URL
        return json.load(response)


def semver(version: str) -> tuple[int, ...]:
    return tuple(int(n) for n in version.split("."))


def core_deps(info: dict) -> list[str]:
    """Requirements that apply without any extra, normalised for comparison."""
    return sorted(r.replace(" ", "") for r in info.get("requires_dist") or [] if "extra ==" not in r)


def target(requested: str) -> str:
    if requested:
        if not VERSION.fullmatch(requested):
            raise SystemExit(f"[library] not a release version: {requested!r}")
        return requested
    latest = pypi()["info"]["version"]
    pinned = json.loads(MANIFEST.read_text(encoding="utf-8"))["pain001"]
    return latest if semver(latest) > semver(pinned) else ""


def pin(version: str) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    release = pypi(version)
    wheel = next((u for u in release["urls"] if u["packagetype"] == "bdist_wheel"
                  and u["filename"].endswith("-py3-none-any.whl")), None)
    if wheel is None:
        raise SystemExit(f"[library] pain001 {version} has no pure-Python wheel on PyPI")
    entry = next(w for w in manifest["wheels"] if w["file"].startswith("pain001-"))
    previous = manifest["pain001"]
    manifest["total_bytes"] += wheel["size"] - entry["bytes"]
    entry.update(file=wheel["filename"], bytes=wheel["size"], sha256=wheel["digests"]["sha256"],
                 url=WHEEL_URL.format(wheel["filename"]))
    manifest["pain001"] = version
    manifest["pain001_source"] = f"pypi:pain001=={version} (sha256 verified against PyPI at vendoring)"
    MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[library] demo runtime pinned to {wheel['filename']} ({wheel['digests']['sha256'][:12]})")
    if previous != version and core_deps(release["info"]) != core_deps(pypi(previous)["info"]):
        print(f"::warning::pain001 {version} changed its core dependencies since {previous}; "
              "check the demo's other wheels in static/pyodide/pain001-runtime.json")


def main(argv: list[str]) -> int:
    if argv[:1] == ["target"] and len(argv) <= 2:
        print(target(argv[1] if len(argv) == 2 else ""))
        return 0
    if argv[:1] == ["pin"] and len(argv) == 2 and VERSION.fullmatch(argv[1]):
        pin(argv[1])
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
