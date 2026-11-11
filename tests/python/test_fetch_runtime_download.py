# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/fetch_runtime.py downloads and its fetch command.

Pins that a download is retried on a network error and gives up with a
named error after four attempts, and that the default (non --check) run
fetches every manifest binary and prints how each one was obtained.
"""

from __future__ import annotations

import hashlib
import io
import json
import urllib.error

import pytest

import fetch_runtime as fr

GOOD = b"wheel bytes"
SHA = hashlib.sha256(GOOD).hexdigest()


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@pytest.fixture
def no_sleep(monkeypatch):
    waits = []
    monkeypatch.setattr(fr.time, "sleep", waits.append)
    return waits


def test_download_retries_then_writes(tmp_path, monkeypatch, no_sleep):
    calls = []

    def fake_urlopen(request, timeout):
        calls.append((request.full_url, request.get_header("User-agent"), timeout))
        if len(calls) < 3:
            raise urllib.error.URLError("refused")
        return _Response(GOOD)

    monkeypatch.setattr(fr.urllib.request, "urlopen", fake_urlopen)
    dest = tmp_path / "a.part"
    fr.download("https://example.test/a.whl", dest)
    assert dest.read_bytes() == GOOD
    assert calls[0] == ("https://example.test/a.whl", fr.USER_AGENT, 120)
    assert no_sleep == [2, 4]


def test_download_gives_up_after_four_attempts(tmp_path, monkeypatch, no_sleep):
    def fail(request, timeout):
        raise TimeoutError("slow")

    monkeypatch.setattr(fr.urllib.request, "urlopen", fail)
    with pytest.raises(SystemExit, match=r"could not download https://example.test/a.whl: slow"):
        fr.download("https://example.test/a.whl", tmp_path / "a.part")
    assert no_sleep == [2, 4, 6, 8]


def test_main_fetches_every_binary_and_summarises(tmp_path, monkeypatch, capsys):
    rt = tmp_path / "pyodide"
    rt.mkdir()
    manifest = rt / "pain001-runtime.json"
    manifest.write_text(json.dumps({
        "runtime": [{"file": "pyodide.js", "sha256": SHA, "url": "https://example.test/p.js"}],
        "packages": [{"file": "b.whl", "sha256": SHA, "url": "https://example.test/b.whl"}],
        "wheels": [{"file": "c.whl", "sha256": SHA, "url": "https://example.test/c.whl"}],
    }), encoding="utf-8")
    (rt / "pyodide.js").write_bytes(GOOD)
    monkeypatch.setattr(fr, "RUNTIME", rt)
    monkeypatch.setattr(fr, "MANIFEST", manifest)
    monkeypatch.setattr(fr, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(fr, "download", lambda url, dest: dest.write_bytes(GOOD))
    assert fr.main([]) == 0
    out = capsys.readouterr().out
    assert out == "[runtime] 3 binaries verified against the manifest (1 cached, 1 downloaded, 1 present)\n"
    assert (rt / "c.whl").read_bytes() == GOOD

    (rt / "c.whl").write_bytes(b"edited")
    assert fr.main(["--check"]) == 1
    assert "[runtime] missing or modified: c.whl" in capsys.readouterr().out
