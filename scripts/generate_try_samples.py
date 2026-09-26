#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Turn the example corpus into one-click inputs for the browser demo.

For every market file of the demo's edition, the records twin gives the
flat rows that regenerate it; those rows become a CSV the demo can load.
Only files whose twin has no gap and no missing required column are
included, so every sample runs clean through the library in the browser
(tests/engine.integration.mjs proves it).

Run with the library's own environment:

    cd <pain001 checkout> && poetry run python3 \\
        <this repository>/scripts/generate_try_samples.py

Writes static/corpus/try-samples.json.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

import pain001
from pain001.corpus import api
from pain001.twins.records import to_records

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "corpus" / "try-samples.json"
MESSAGE_TYPE = "pain.001.001.09"
#: Scheme rulebooks the demo offers; a scenario's first matching rail is preselected.
DEMO_SCHEMES = {
    "sepa-sct", "sepa-inst", "sepa-b2b", "cbpr-cross-border", "uk-fps", "uk-chaps",
    "uk-bacs", "us-ach", "us-wire", "us-rtp", "ch-domestic", "se-bankgiro", "de-ccu",
    "hk-fps", "sg-fast", "anti-duplicate",
}


def rails_of(provenance: dict) -> list[str]:
    """Rail profile names the corpus judged this file by, in sidecar order."""
    profiles = (provenance.get("validation") or {}).get("profiles") or {}
    return [str(name) for name in profiles]


def to_csv(rows: list[dict]) -> str:
    """Rows as CSV with only the columns that carry a value somewhere."""
    columns = [c for c in rows[0] if any(str(r.get(c, "")).strip() for r in rows)]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({c: row.get(c, "") for c in columns})
    return buffer.getvalue()


def main() -> int:
    samples = []
    skipped = []
    for entry in sorted(api.list_files("market"), key=lambda f: (f.country, f.scenario_id)):
        if entry.version != MESSAGE_TYPE or entry.variant:
            continue
        xml = api.get_file(entry.scenario_id, entry.version)
        twin = to_records(xml, entry.version)
        if twin.gap or twin.missing_required or not twin.rows:
            skipped.append((entry.scenario_id, twin.gap, twin.missing_required))
            continue
        provenance = api.provenance(entry.scenario_id, entry.version)
        scheme = next((r for r in rails_of(provenance) if r in DEMO_SCHEMES), "")
        samples.append({
            "id": entry.scenario_id,
            "country": entry.country,
            "family": entry.family,
            "description": str(provenance.get("description", "")).strip(),
            "scheme": scheme,
            "records": len(twin.rows),
            "csv": to_csv(twin.rows),
        })
    OUT.write_text(json.dumps({
        "pain001": pain001.__version__,
        "message_type": MESSAGE_TYPE,
        "samples": samples,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(samples)} samples, {len(skipped)} skipped")
    for scenario, gap, missing in skipped:
        print(f"  skipped {scenario}: gap={gap[:2]} missing={missing[:3]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
