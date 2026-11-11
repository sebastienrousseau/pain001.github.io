# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/library_release.py's PyPI read and command line.

Pins the PyPI JSON URL for the latest and a named release, and the
command forms: `target [VERSION]`, `pin VERSION`, and usage on anything
else.
"""

from __future__ import annotations

import io

import pytest

import library_release as lr


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_pypi_reads_latest_and_named_release(monkeypatch):
    seen = []

    def fake_urlopen(url, timeout):
        seen.append((url, timeout))
        return _Response(b'{"info": {"version": "0.0.86"}}')

    monkeypatch.setattr(lr.urllib.request, "urlopen", fake_urlopen)
    assert lr.pypi() == {"info": {"version": "0.0.86"}}
    lr.pypi("0.0.85")
    assert seen == [("https://pypi.org/pypi/pain001/json", 30), ("https://pypi.org/pypi/pain001/0.0.85/json", 30)]


def test_main_target_prints_the_version(monkeypatch, capsys):
    monkeypatch.setattr(lr, "target", lambda requested: requested or "0.0.90")
    assert lr.main(["target", "0.0.86"]) == 0
    assert lr.main(["target"]) == 0
    assert capsys.readouterr().out == "0.0.86\n0.0.90\n"


def test_main_pin_calls_pin(monkeypatch):
    pinned = []
    monkeypatch.setattr(lr, "pin", pinned.append)
    assert lr.main(["pin", "0.0.86"]) == 0
    assert pinned == ["0.0.86"]


@pytest.mark.parametrize("argv", [[], ["target", "a", "b"], ["pin"], ["pin", "latest"], ["other"]])
def test_main_prints_usage_otherwise(argv, monkeypatch):
    monkeypatch.setattr(lr, "pin", lambda v: pytest.fail("pinned"))
    with pytest.raises(SystemExit) as exc:
        lr.main(argv)
    assert exc.value.code == lr.__doc__
