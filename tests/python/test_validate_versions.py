# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_versions.py (issue #61).

The version-currency gate ensures site documentation does not cite stale
versions of the pain001 suite unless on lines explicitly documenting
historical compatibility.
"""

from __future__ import annotations

from pathlib import Path

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
