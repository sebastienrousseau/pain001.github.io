#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Verify the runtime and snippet environment share the suite version."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    """Reject a stale browser runtime or documentation validation environment."""
    version = (ROOT / "VERSION").read_text().strip()
    runtime = "static/pyodide/pain001-runtime.json"
    pins = {runtime: json.loads((ROOT / runtime).read_text())["pain001"]}
    for suffix in ("in", "txt"):
        path = "requirements/snippets." + suffix
        match = re.search(r"(?m)^pain001==([^\s]+)", (ROOT / path).read_text())
        pins[path] = match.group(1) if match else None
    stale = [path for path, pinned in pins.items() if pinned != version]
    if stale:
        for path in stale:
            print(f"{path} does not match VERSION {version}")
        return 1
    print(f"runtime and snippet pins match pain001 {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
