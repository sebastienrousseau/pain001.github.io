# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/sbom_serial.py.

Pins the timestamp source (SOURCE_DATE_EPOCH, else the HEAD commit, else
none), the derived serialNumber, the usage and missing-file exits, and
the final attestability check.
"""

from __future__ import annotations

import json
import subprocess
import sys
import uuid

import pytest

import sbom_serial


class _Done:
    def __init__(self, stdout):
        self.stdout = stdout


def test_timestamp_from_source_date_epoch(monkeypatch):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")
    assert sbom_serial.source_timestamp() == "2023-11-14T22:13:20Z"


def test_timestamp_from_head_commit(monkeypatch):
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    seen = []
    monkeypatch.setattr(sbom_serial.subprocess, "run", lambda cmd, **k: seen.append(cmd) or _Done("0\n"))
    assert sbom_serial.source_timestamp() == "1970-01-01T00:00:00Z"
    assert seen == [["git", "log", "-1", "--format=%ct"]]


def test_timestamp_none_when_git_fails_or_answers_nonsense(monkeypatch):
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)

    def broken(cmd, **kwargs):
        raise subprocess.CalledProcessError(128, cmd)

    monkeypatch.setattr(sbom_serial.subprocess, "run", broken)
    assert sbom_serial.source_timestamp() is None
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "yesterday")
    assert sbom_serial.source_timestamp() is None


def _run(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["sbom_serial.py", *args])
    return sbom_serial.main()


def test_usage_and_missing_file(tmp_path, monkeypatch, capsys):
    assert _run(monkeypatch) == 2
    assert "Usage: sbom_serial.py <output-dir>" in capsys.readouterr().err
    assert _run(monkeypatch, str(tmp_path)) == 1
    assert f"[sbom] {tmp_path / 'sbom.cdx.json'} not found" in capsys.readouterr().err


@pytest.fixture
def site(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "VERSION").write_text("0.0.86\n", encoding="utf-8")
    monkeypatch.setattr(sbom_serial, "source_timestamp", lambda: "2026-11-11T00:00:00Z")
    return tmp_path


def _write(site, sbom):
    (site / "sbom.cdx.json").write_text(json.dumps(sbom), encoding="utf-8")


def test_serial_and_timestamp_are_added(site, monkeypatch, capsys):
    _write(site, {"specVersion": "1.5", "bomFormat": "CycloneDX", "metadata": {"timestamp": "now"}})
    assert _run(monkeypatch, str(site)) == 0
    serial = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'https://pain001.com/sbom.cdx.json#0.0.86')}"
    assert capsys.readouterr().out == f"[sbom] serialNumber {serial} (CycloneDX 1.5)\n"
    text = (site / "sbom.cdx.json").read_text(encoding="utf-8")
    assert text.endswith("}\n") and text.index('"bomFormat"') < text.index('"specVersion"')
    sbom = json.loads(text)
    assert sbom["serialNumber"] == serial and sbom["metadata"]["timestamp"] == "2026-11-11T00:00:00Z"


def test_existing_serial_kept_and_no_metadata_left_alone(site, monkeypatch):
    _write(site, {"specVersion": "1.5", "bomFormat": "CycloneDX", "serialNumber": "urn:uuid:x"})
    assert _run(monkeypatch, str(site)) == 0
    sbom = json.loads((site / "sbom.cdx.json").read_text(encoding="utf-8"))
    assert sbom == {"specVersion": "1.5", "bomFormat": "CycloneDX", "serialNumber": "urn:uuid:x"}


def test_unattestable_result_fails(site, monkeypatch, capsys):
    monkeypatch.setattr(sbom_serial, "source_timestamp", lambda: None)
    _write(site, {"metadata": {"timestamp": "keep"}, "serialNumber": "urn:uuid:x"})
    assert _run(monkeypatch, str(site)) == 1
    assert "[sbom] still unattestable, missing: bomFormat, specVersion" in capsys.readouterr().err
    assert json.loads((site / "sbom.cdx.json").read_text(encoding="utf-8"))["metadata"]["timestamp"] == "keep"
