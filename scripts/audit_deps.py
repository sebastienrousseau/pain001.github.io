#!/usr/bin/env python3
"""Fail on npm advisories that are not explicitly and currently excepted.

A plain `npm audit` gate is switched off the first week an advisory has no
patched release (pa11y-ci's transitive extract-zip was the case that
prompted this, until pa11y-ci was removed in v0.0.7), and `--audit-level=
critical` would hide genuinely actionable high findings instead.

This gate keeps the floor at high and requires every accepted advisory to be
listed in .npm-audit-exceptions.json with a reason and an expiry date. A new
advisory fails immediately; an accepted one fails again once it expires, so
the list cannot rot silently.

Exit status: 0 clean or fully excepted, 1 otherwise.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

SEVERITY_ORDER = ["info", "low", "moderate", "high", "critical"]
EXCEPTIONS_PATH = Path(".npm-audit-exceptions.json")
GHSA = re.compile(r"GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}", re.I)


def run_audit() -> dict:
    proc = subprocess.run(
        ["npm", "audit", "--json"], capture_output=True, text=True, check=False
    )
    if not proc.stdout.strip():
        print("[deps] npm audit produced no output", file=sys.stderr)
        print(proc.stderr[:2000], file=sys.stderr)
        raise SystemExit(1)
    return json.loads(proc.stdout)


def findings(report: dict, floor: str) -> list[tuple[str, str, str, str]]:
    """Return (advisory_id, package, severity, title) at or above the floor."""
    floor_index = SEVERITY_ORDER.index(floor)
    out: list[tuple[str, str, str, str]] = []
    for package, entry in report.get("vulnerabilities", {}).items():
        severity = entry.get("severity", "info")
        if severity not in SEVERITY_ORDER:
            continue
        if SEVERITY_ORDER.index(severity) < floor_index:
            continue
        for via in entry.get("via", []):
            if not isinstance(via, dict):
                continue  # a string 'via' is an indirect path, not an advisory
            match = GHSA.search(via.get("url", "") or "")
            advisory = match.group(0).upper() if match else f"npm:{via.get('source')}"
            out.append((advisory, package, severity, via.get("title", "")))
    return out


def main() -> int:
    if not EXCEPTIONS_PATH.is_file():
        print(f"[deps] {EXCEPTIONS_PATH} is missing", file=sys.stderr)
        return 1
    config = json.loads(EXCEPTIONS_PATH.read_text(encoding="utf-8"))
    floor = config.get("severityFloor", "high")
    today = dt.date.today()

    accepted: dict[str, dt.date] = {}
    malformed: list[str] = []
    for item in config.get("exceptions", []):
        advisory = str(item.get("advisory", "")).upper()
        if not advisory or not item.get("reason"):
            malformed.append(advisory or "<unnamed>")
            continue
        try:
            accepted[advisory] = dt.date.fromisoformat(item["expires"])
        except (KeyError, ValueError):
            malformed.append(advisory)

    problems: list[str] = [f"exception {a} lacks a reason or a valid expiry" for a in malformed]

    seen: set[str] = set()
    for advisory, package, severity, title in findings(run_audit(), floor):
        seen.add(advisory)
        if advisory not in accepted:
            problems.append(f"{severity:8} {package}: {title} [{advisory}] not excepted")
        elif accepted[advisory] < today:
            problems.append(
                f"{severity:8} {package}: exception for {advisory} expired on {accepted[advisory]}"
            )

    for advisory in accepted:
        if advisory not in seen:
            problems.append(f"exception {advisory} no longer matches any advisory; remove it")

    if problems:
        print(f"[deps] {len(problems)} problem(s) at severity >= {floor}", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(f"[deps] no unexcepted advisories at severity >= {floor}"
          f" ({len(accepted)} documented exception(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
