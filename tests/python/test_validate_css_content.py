# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_css_content.py.

Pins that an emoji in a stylesheet `content:` value fails with its file
and line, while arrows, emoji in comments, and other properties pass,
and that a missing stylesheet directory is an error.
"""

from __future__ import annotations

import pytest

import validate_css_content as gate


@pytest.fixture
def css_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "CSS_DIR", tmp_path)
    return tmp_path


def test_missing_directory_is_an_error(tmp_path, monkeypatch, capsys):
    missing = tmp_path / "css"
    monkeypatch.setattr(gate, "CSS_DIR", missing)
    assert gate.main() == 1
    assert f"{missing} not found" in capsys.readouterr().err


def test_clean_stylesheets_pass(css_dir, capsys):
    (css_dir / "a.css").write_text(
        '/* ☀️ in a comment is fine */\n.x::after { content: "→"; }\n'
        ".y { font-family: 'Sun ☀'; }\n", encoding="utf-8")
    (css_dir / "notes.txt").write_text('content: "☀️"', encoding="utf-8")
    assert gate.main() == 0
    out = capsys.readouterr().out
    assert "scanned 1 stylesheet(s)" in out
    assert "result: CLEAN" in out


def test_emoji_in_content_fails_with_location(css_dir, capsys):
    (css_dir / "theme.css").write_text(
        '.a {}\n.toggle::before { content: "☀️"; }\n'
        ".dark::before { content: '\U0001F319'; }\n", encoding="utf-8")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL 2 emoji in a CSS content property" in out
    assert "theme.css:2  content: '☀️'" in out
    assert "theme.css:3  content: '\U0001F319'" in out
    assert "result: CLEAN" not in out
