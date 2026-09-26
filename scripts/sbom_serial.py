#!/usr/bin/env python3
"""Give the generated CycloneDX SBOM a serialNumber.

ssg's sbom plugin emits a valid CycloneDX 1.5 document, but without the
optional `serialNumber` field. GitHub's attestation action sniffs the format
with

    bomFormat && serialNumber && specVersion

(see actions/attest, src/sbom.ts), so an SBOM without a serialNumber is
rejected as "Unsupported SBOM format. Must be valid SPDX or CycloneDX JSON."
and the release never publishes. That is what happened to v0.0.4.

The value is derived, not random: a UUIDv5 over the site's base URL and
version. Rebuilds of a version therefore carry the same serial, so this pass
adds no nondeterminism of its own.

ssg also stamps the build time into metadata.timestamp, which made the SBOM
differ between two builds of one commit. The timestamp is set to
SOURCE_DATE_EPOCH when it is set (the reproducible-builds convention), and
otherwise to the time of the commit being built, so the SBOM describes the
source, not the moment it was built.

The proper fix belongs in ssg's sbom plugin; this keeps releases publishable
until that lands, and becomes a no-op once the generator emits the field.

Usage: sbom_serial.py <output-dir>
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

NAMESPACE = "https://pain001.com/sbom.cdx.json"


def source_timestamp() -> str | None:
    """SOURCE_DATE_EPOCH, else the HEAD commit time, as CycloneDX wants it."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if not epoch:
        try:
            epoch = subprocess.run(["git", "log", "-1", "--format=%ct"], check=True,
                                   capture_output=True, text=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    if not epoch.isdigit():
        return None
    return dt.datetime.fromtimestamp(int(epoch), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2

    sbom_path = Path(sys.argv[1]) / "sbom.cdx.json"
    if not sbom_path.is_file():
        print(f"[sbom] {sbom_path} not found", file=sys.stderr)
        return 1

    sbom = json.loads(sbom_path.read_text(encoding="utf-8"))

    stamp = source_timestamp()
    if stamp and isinstance(sbom.get("metadata"), dict):
        sbom["metadata"]["timestamp"] = stamp

    if not sbom.get("serialNumber"):
        version = Path("VERSION").read_text(encoding="utf-8").strip()
        serial = uuid.uuid5(uuid.NAMESPACE_URL, f"{NAMESPACE}#{version}")
        sbom["serialNumber"] = f"urn:uuid:{serial}"

    # Rewrite with the generator's own shape: sorted keys, 2-space indent and a
    # trailing newline, so the diff against ssg's output is the one added key.
    sbom_path.write_text(
        json.dumps(sbom, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # Assert the exact condition the attestation action checks, so a future
    # change to this script cannot silently reintroduce an unpublishable SBOM.
    check = json.loads(sbom_path.read_text(encoding="utf-8"))
    missing = [k for k in ("bomFormat", "serialNumber", "specVersion") if not check.get(k)]
    if missing:
        print(f"[sbom] still unattestable, missing: {', '.join(missing)}", file=sys.stderr)
        return 1

    print(f"[sbom] serialNumber {sbom['serialNumber']} (CycloneDX {check['specVersion']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
