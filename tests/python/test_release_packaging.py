# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests for release packaging.

scripts/sbom_serial.py guards fix 493d60f3 ("give the SBOM a
serialNumber"): v0.0.4 failed to publish because the attestation action
rejects a CycloneDX SBOM without serialNumber. The serial is derived
from the version, so rebuilds of one version carry the same serial.

scripts/release_backfill.py guards the backfill of v0.0.1 to v0.0.4
(commit 68e9b159): the archive is reproducible, the SBOM is attestable,
and SHA256SUMS uses the release workflow's format.
"""

import hashlib
import json
import tarfile

import pytest

import release_backfill as rb
import sbom_serial


def _site(root, sbom=None):
    site = root / "site"
    (site / "a").mkdir(parents=True)
    (site / "index.html").write_text("<h1>home</h1>", encoding="utf-8")
    (site / "a" / "index.html").write_text("<h1>a</h1>", encoding="utf-8")
    if sbom is not None:
        (site / "sbom.cdx.json").write_text(json.dumps(sbom), encoding="utf-8")
    (root / "LICENSE").write_text("licence", encoding="utf-8")
    return site


# --- sbom_serial.py -------------------------------------------------------

def _run_serial(monkeypatch, tmp_path, sbom, version="0.0.9"):
    out = tmp_path / "out"
    out.mkdir()
    (out / "sbom.cdx.json").write_text(json.dumps(sbom), encoding="utf-8")
    (tmp_path / "VERSION").write_text(version + "\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sbom_serial.sys, "argv", ["sbom_serial.py", str(out)])
    code = sbom_serial.main()
    return code, json.loads((out / "sbom.cdx.json").read_text(encoding="utf-8"))


def test_sbom_gets_a_serial_the_attestation_action_accepts(monkeypatch, tmp_path):
    code, sbom = _run_serial(monkeypatch, tmp_path, {"bomFormat": "CycloneDX", "specVersion": "1.5"})
    assert code == 0
    assert sbom["serialNumber"].startswith("urn:uuid:")
    assert all(sbom.get(k) for k in ("bomFormat", "serialNumber", "specVersion"))


def test_sbom_serial_is_deterministic_per_version(monkeypatch, tmp_path):
    base = {"bomFormat": "CycloneDX", "specVersion": "1.5"}
    serials = []
    for run, version in (("1", "0.0.9"), ("2", "0.0.9"), ("3", "0.0.10")):
        (tmp_path / run).mkdir()
        serials.append(_run_serial(monkeypatch, tmp_path / run, dict(base), version)[1]["serialNumber"])
    assert serials[0] == serials[1] == rb.serial_for("0.0.9")
    assert serials[2] != serials[0]


def test_existing_serial_is_left_alone(monkeypatch, tmp_path):
    sbom = {"bomFormat": "CycloneDX", "specVersion": "1.5", "serialNumber": "urn:uuid:keep"}
    assert _run_serial(monkeypatch, tmp_path, sbom)[1]["serialNumber"] == "urn:uuid:keep"


# --- release_backfill.py --------------------------------------------------

def test_archive_is_byte_identical_across_runs(tmp_path):
    src = tmp_path / "src"
    _site(src, {"bomFormat": "CycloneDX", "specVersion": "1.5"})
    for out in ("out1", "out2"):
        assert rb.main(["--src", str(src), "--tag", "v0.0.3", "--out", str(tmp_path / out), "--mtime", "1790000000"]) == 0

    names = ["pain001-site-v0.0.3.tar.gz", "pain001-site-v0.0.3.cdx.json", "SHA256SUMS"]
    for name in names:
        assert (tmp_path / "out1" / name).read_bytes() == (tmp_path / "out2" / name).read_bytes()

    with tarfile.open(tmp_path / "out1" / names[0]) as tar:
        members = tar.getmembers()
    assert [m.name for m in members] == ["site", "site/a", "site/a/index.html", "site/index.html",
                                         "site/sbom.cdx.json", "LICENSE"]
    assert {m.mtime for m in members} == {1790000000}
    assert {(m.uid, m.gid) for m in members} == {(0, 0)}


def test_backfilled_sbom_is_attestable_with_or_without_a_site_sbom(tmp_path):
    with_sbom, without = tmp_path / "with", tmp_path / "without"
    _site(with_sbom, {"bomFormat": "CycloneDX", "specVersion": "1.5"})
    _site(without)
    for src in (with_sbom, without):
        rb.main(["--src", str(src), "--tag", "v0.0.1", "--out", str(src / "dist")])
        sbom = json.loads((src / "dist" / "pain001-site-v0.0.1.cdx.json").read_text(encoding="utf-8"))
        assert sbom["serialNumber"] == rb.serial_for("0.0.1")
        assert sbom["bomFormat"] == "CycloneDX" and sbom["specVersion"]


def test_sha256sums_matches_the_release_workflow_format(tmp_path):
    src = tmp_path / "src"
    _site(src)
    rb.main(["--src", str(src), "--tag", "v0.0.2", "--out", str(tmp_path / "dist")])
    dist = tmp_path / "dist"
    lines = (dist / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert lines == [
        f"{hashlib.sha256((dist / name).read_bytes()).hexdigest()}  ./{name}"
        for name in sorted(["pain001-site-v0.0.2.cdx.json", "pain001-site-v0.0.2.tar.gz"])
    ]


def test_backfill_uses_committed_docs_when_no_built_site(tmp_path):
    src = tmp_path / "src"
    (src / "docs").mkdir(parents=True)
    (src / "docs" / "index.html").write_text("old site", encoding="utf-8")
    assert rb.site_tree(src) == src / "docs"
    with pytest.raises(SystemExit, match="not a release tag"):
        rb.main(["--src", str(src), "--tag", "0.0.1", "--out", str(tmp_path / "d")])
