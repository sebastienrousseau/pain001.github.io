#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Package the release assets for a tag that was published without them.

v0.0.1 and v0.0.2 predate the release workflow; v0.0.3 and v0.0.4 were
tagged but their release runs failed on SBOM attestation (fixed in v0.0.5).
Every tag should still carry what a release promises: the site archive,
its CycloneDX SBOM and SHA256SUMS. This script produces exactly the three
files the release workflow produces, from a checkout of the old tag, and
release-backfill.yml attests and publishes them.

What goes in the archive is the site as it was published at that tag:

- if the checkout has a built site/ (v0.0.3 onwards, after running the
  tag's own build.sh), that tree;
- otherwise the committed docs/ tree, which is what GitHub Pages served
  for v0.0.1 and v0.0.2.

The archive is packaged byte-for-byte from that tree and is reproducible:
sorted entries, owner 0, and every timestamp set to the tag's commit time,
so rerunning the backfill yields the same checksum. The SBOM asset is the
site's own sbom.cdx.json given the deterministic serialNumber
scripts/sbom_serial.py adds (the attestation action requires one); a site
with no SBOM (v0.0.1) gets a minimal CycloneDX 1.5 document that names the
site and nothing else, which is true of a hand-written static site.

Usage:
  python3 scripts/release_backfill.py --src <tag checkout> --tag vX.Y.Z \\
      --out dist [--mtime <unix seconds>]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import sys
import tarfile
import uuid
from pathlib import Path

NAMESPACE = "https://pain001.com/sbom.cdx.json"  # same as scripts/sbom_serial.py
LICENCE_FILES = ("LICENSE", "LICENSE-APACHE", "LICENSE-MIT", "THIRD_PARTY_NOTICES.md")


def site_tree(src: Path) -> Path:
    for candidate in (src / "site", src / "docs"):
        if (candidate / "index.html").is_file():
            return candidate
    raise SystemExit(f"[backfill] no built site in {src}/site or {src}/docs; build the tag first")


def serial_for(version: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{NAMESPACE}#{version}')}"


def sbom_for(site: Path, version: str) -> dict:
    path = site / "sbom.cdx.json"
    if path.is_file():
        sbom = json.loads(path.read_text(encoding="utf-8"))
        sbom.setdefault("serialNumber", serial_for(version))
    else:
        sbom = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.5",
            "serialNumber": serial_for(version),
            "version": 1,
            "metadata": {"component": {
                "type": "application", "bom-ref": f"pain001.com@{version}",
                "name": "pain001.com", "version": version,
                "description": "Hand-written static site; no build toolchain or runtime dependencies.",
            }},
            "components": [],
        }
    missing = [k for k in ("bomFormat", "serialNumber", "specVersion") if not sbom.get(k)]
    if missing:
        raise SystemExit(f"[backfill] SBOM not attestable, missing: {', '.join(missing)}")
    return sbom


def add(tar: tarfile.TarFile, path: Path, arcname: str, mtime: int) -> None:
    info = tar.gettarinfo(str(path), arcname)
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    info.mtime = mtime
    if info.isfile():
        with path.open("rb") as handle:
            tar.addfile(info, handle)
    else:
        tar.addfile(info)


def package(src: Path, site: Path, out: Path, name: str, mtime: int) -> Path:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tar:
        add(tar, site, "site", mtime)
        for path in sorted(site.rglob("*")):
            add(tar, path, "site/" + path.relative_to(site).as_posix(), mtime)
        for licence in LICENCE_FILES:
            if (src / licence).is_file():
                add(tar, src / licence, licence, mtime)
    target = out / name
    with target.open("wb") as handle, gzip.GzipFile(fileobj=handle, mode="wb", mtime=0, filename="") as gz:
        gz.write(raw.getvalue())
    return target


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--src", required=True, type=Path)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mtime", type=int, default=0)
    args = parser.parse_args(argv)
    if not re.fullmatch(r"v\d+\.\d+\.\d+", args.tag):
        raise SystemExit(f"[backfill] not a release tag: {args.tag!r}")
    version = args.tag[1:]
    site = site_tree(args.src)
    args.out.mkdir(parents=True, exist_ok=True)
    archive = package(args.src, site, args.out, f"pain001-site-v{version}.tar.gz", args.mtime)
    sbom = args.out / f"pain001-site-v{version}.cdx.json"
    sbom.write_text(json.dumps(sbom_for(site, version), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  ./{p.name}\n" for p in sorted((archive, sbom)))
    (args.out / "SHA256SUMS").write_text(sums, encoding="utf-8")
    pages = sum(1 for _ in site.rglob("index.html"))
    print(f"[backfill] {args.tag}: {site.relative_to(args.src)}/ ({pages} pages) -> {archive.name}, {sbom.name}, SHA256SUMS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
