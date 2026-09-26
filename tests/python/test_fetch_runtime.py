# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests for scripts/fetch_runtime.py.

Guards commit 017d243b ("fetch the demo runtime, stop committing it"):
the demo's binaries are downloaded at build time, and a file is used
only when its SHA-256 matches the committed manifest, so a changed or
tampered upstream fails the build instead of shipping.
"""

import hashlib
import json

import pytest

import fetch_runtime as fr

GOOD = b"the real wheel bytes"
SHA = hashlib.sha256(GOOD).hexdigest()


@pytest.fixture
def runtime(tmp_path, monkeypatch):
    rt = tmp_path / "pyodide"
    rt.mkdir()
    manifest = rt / "pain001-runtime.json"
    manifest.write_text(json.dumps({
        "runtime": [{"file": "pyodide.js", "bytes": 1, "sha256": "x"}],  # no url: committed
        "wheels": [{"file": "a.whl", "bytes": len(GOOD), "sha256": SHA, "url": "https://example.test/a.whl"}],
    }), encoding="utf-8")
    monkeypatch.setattr(fr, "RUNTIME", rt)
    monkeypatch.setattr(fr, "MANIFEST", manifest)
    monkeypatch.setattr(fr, "CACHE", tmp_path / "cache")
    return rt


def _serve(monkeypatch, payload, calls):
    def fake_download(url, dest):
        calls.append(url)
        dest.write_bytes(payload)
    monkeypatch.setattr(fr, "download", fake_download)


def test_only_entries_with_a_url_are_fetched(runtime):
    assert [e["file"] for e in fr.binaries()] == ["a.whl"]


def test_verified_download_is_cached_and_copied(runtime, monkeypatch):
    calls = []
    _serve(monkeypatch, GOOD, calls)

    assert fr.fetch(fr.binaries()[0]) == "downloaded"
    assert (runtime / "a.whl").read_bytes() == GOOD
    assert (fr.CACHE / SHA).read_bytes() == GOOD

    (runtime / "a.whl").unlink()
    assert fr.fetch(fr.binaries()[0]) == "cached"
    assert fr.fetch(fr.binaries()[0]) == "present"
    assert calls == ["https://example.test/a.whl"]


def test_a_download_with_the_wrong_hash_is_refused(runtime, monkeypatch):
    _serve(monkeypatch, b"tampered bytes", [])

    with pytest.raises(SystemExit, match="refusing to use it"):
        fr.fetch(fr.binaries()[0])

    assert not (runtime / "a.whl").exists()
    assert not any(fr.CACHE.iterdir())  # the bad download is not kept


def test_a_modified_local_file_is_replaced(runtime, monkeypatch):
    (runtime / "a.whl").write_bytes(b"edited by hand")
    _serve(monkeypatch, GOOD, [])

    assert fr.fetch(fr.binaries()[0]) == "downloaded"
    assert (runtime / "a.whl").read_bytes() == GOOD


def test_check_mode_reports_missing_and_passes_when_present(runtime, capsys):
    assert fr.main(["--check"]) == 1
    assert "missing or modified: a.whl" in capsys.readouterr().out

    (runtime / "a.whl").write_bytes(GOOD)
    assert fr.main(["--check"]) == 0
    assert "1 of 1 binaries verified" in capsys.readouterr().out
