# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_versions.py (issue #61).

The version-currency gate ensures site documentation does not cite stale
versions of the pain001 suite unless on lines explicitly documenting
historical compatibility.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError

import pytest
import validate_versions as gate


@pytest.fixture
def posts_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Point validate_versions.POSTS at a temporary directory and return helper."""
    monkeypatch.setattr(gate, "POSTS", tmp_path)

    def write_page(name: str, content: str) -> Path:
        p = tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p

    return write_page


def test_page_citing_current_version_passes(posts_dir, capsys):
    posts_dir(
        "current.md",
        "# Installation\n\nInstall pain001 v0.0.72 or package version 0.0.72.\n",
    )
    assert gate.main(["--current", "0.0.72"]) == 0
    assert "every page is at or above pain001 0.0.72" in capsys.readouterr().out


def test_stale_version_fails(posts_dir, capsys):
    posts_dir(
        "stale.md",
        "---\ntitle: Stale Guide\n---\nRequires v0.0.58 for processing.\n",
    )
    assert gate.main(["--current", "0.0.72"]) == 1
    out = capsys.readouterr().out
    assert "pages cite a suite version older than 0.0.72:" in out
    assert "stale.md:4: v0.0.58" in out


@pytest.mark.parametrize(
    "line",
    [
        "min_pain001: 0.0.58",
        "Available in v0.0.58 onward across all loaders.",
        "Supported since v0.0.58 in the CLI.",
        "Legacy behavior in v0.0.58 <!-- history -->",
    ],
)
def test_history_forms_allowed(posts_dir, capsys, line):
    posts_dir("history.md", f"---\ntitle: History\n---\n{line}\n")
    assert gate.main(["--current", "0.0.72"]) == 0
    assert "every page is at or above pain001 0.0.72" in capsys.readouterr().out


def test_dotted_quad_not_mistaken_for_version(posts_dir, capsys):
    posts_dir(
        "network.md",
        "# Server Configuration\n\nBind to 0.0.0.0 or listen on http://0.0.0.0:8000.\n",
    )
    assert gate.main(["--current", "0.0.72"]) == 0
    assert "every page is at or above pain001 0.0.72" in capsys.readouterr().out


def test_released_version_survives_connection_reset(monkeypatch):
    """A transient TLS reset must not discard a later valid PyPI response."""
    import time

    calls = []
    waits = []

    def response(url, timeout):
        calls.append((url, timeout))
        if len(calls) < 3:
            raise URLError(ConnectionResetError("connection reset by peer"))
        return BytesIO(b'{"info":{"version":"0.0.84"}}')

    monkeypatch.setattr(gate.urllib.request, "urlopen", response)
    monkeypatch.setattr(time, "sleep", waits.append)
    assert gate.released_version() == "0.0.84"
    assert calls == [(gate.PYPI, 30)] * 3
    assert waits == [1, 2]


def test_released_version_fails_closed_after_bounded_attempts(monkeypatch):
    """An unavailable registry must fail rather than silently use stale data."""
    import time

    calls = []

    def response(url, timeout):
        calls.append(url)
        raise URLError(ConnectionResetError("connection reset by peer"))

    monkeypatch.setattr(gate.urllib.request, "urlopen", response)
    monkeypatch.setattr(time, "sleep", lambda delay: None)
    with pytest.raises(URLError):
        gate.released_version()
    assert calls == [gate.PYPI] * 3


def test_released_version_does_not_retry_access_denied(monkeypatch):
    """Permanent HTTP errors remain immediate failures."""
    calls = []

    def response(url, timeout):
        calls.append(url)
        raise HTTPError(url, 403, "Forbidden", {}, None)

    monkeypatch.setattr(gate.urllib.request, "urlopen", response)
    with pytest.raises(HTTPError):
        gate.released_version()
    assert calls == [gate.PYPI]
