# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/release_backfill.py's refusals and SBOM handling.

Pins that a checkout with no built site, a bad tag, or an SBOM that is
not attestable is refused; that an SBOM's own serialNumber is kept; and
that the committed docs/ tree is used when there is no site/.
"""

from __future__ import annotations

import json
import tarfile

import pytest

import release_backfill as rb


def test_no_built_site_is_refused(tmp_path):
    with pytest.raises(SystemExit, match=r"no built site in .*/site or .*/docs; build the tag first"):
        rb.site_tree(tmp_path)


def test_bad_tag_is_refused(tmp_path):
    with pytest.raises(SystemExit, match=r"not a release tag: 'release-1'"):
        rb.main(["--src", str(tmp_path), "--tag", "release-1", "--out", str(tmp_path / "dist")])


def test_unattestable_sbom_is_refused(tmp_path):
    (tmp_path / "sbom.cdx.json").write_text(json.dumps({"bomFormat": "CycloneDX"}), encoding="utf-8")
    with pytest.raises(SystemExit, match=r"SBOM not attestable, missing: specVersion"):
        rb.sbom_for(tmp_path, "0.0.3")


def test_existing_serial_is_kept(tmp_path):
    sbom = {"bomFormat": "CycloneDX", "specVersion": "1.6", "serialNumber": "urn:uuid:keep"}
    (tmp_path / "sbom.cdx.json").write_text(json.dumps(sbom), encoding="utf-8")
    assert rb.sbom_for(tmp_path, "0.0.9")["serialNumber"] == "urn:uuid:keep"


def test_docs_tree_backfill_without_licences(tmp_path, capsys):
    src = tmp_path / "src"
    (src / "docs" / "a").mkdir(parents=True)
    (src / "docs" / "index.html").write_text("<p>home</p>", encoding="utf-8")
    (src / "docs" / "a" / "index.html").write_text("<p>a</p>", encoding="utf-8")
    out = tmp_path / "dist"
    assert rb.main(["--src", str(src), "--tag", "v0.0.1", "--out", str(out), "--mtime", "1600000000"]) == 0
    assert "[backfill] v0.0.1: docs/ (2 pages) -> pain001-site-v0.0.1.tar.gz" in capsys.readouterr().out
    with tarfile.open(out / "pain001-site-v0.0.1.tar.gz") as tar:
        members = tar.getmembers()
    assert [m.name for m in members] == ["site", "site/a", "site/a/index.html", "site/index.html"]
    assert {m.mtime for m in members} == {1600000000}
    sbom = json.loads((out / "pain001-site-v0.0.1.cdx.json").read_text(encoding="utf-8"))
    assert sbom["serialNumber"] == rb.serial_for("0.0.1")
    assert sbom["metadata"]["component"]["version"] == "0.0.1"
