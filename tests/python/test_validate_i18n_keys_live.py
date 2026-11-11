# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_i18n_keys_live.py.

Pins that every English text and aria key in the translation tables
still occurs inside <main> of the built page it translates: keyed and
flat (try_i18n) tables, entity-normalised matching, skipped pages that
were not built, absent tables, and the failure exit code.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import validate_i18n_keys_live as gate


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "ROOT", tmp_path)
    monkeypatch.setattr(gate, "SITE", tmp_path / "site")
    (tmp_path / "site").mkdir()
    return tmp_path


def _table(root: Path, dirname: str, data: dict) -> None:
    d = root / "scripts" / dirname
    d.mkdir(parents=True, exist_ok=True)
    (d / "en.json").write_text(json.dumps(data), encoding="utf-8")


def _page(root: Path, slug: str, html: str) -> None:
    d = root / "site" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def test_missing_site_is_an_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gate, "SITE", tmp_path / "absent")
    assert gate.main() == 1
    assert "site/ not built" in capsys.readouterr().err


def test_page_html_is_main_or_whole_page(root):
    _page(root, "a", "<nav>x</nav><main><p>y</p></main><footer/>")
    _page(root, "b", "<p>no main</p>")
    assert gate.page_html("a") == "<main><p>y</p>"
    assert gate.page_html("b") == "<p>no main</p>"
    assert gate.page_html("absent") is None


def test_no_tables_passes(root):
    assert gate.main() == 0


def test_live_keys_pass_and_unbuilt_pages_skip(root, capsys):
    _table(root, "pages_i18n", {
        "why": {"text": {"Fish & chips": "", "Plain": ""}, "aria": {"Close": ""}},
        "gone": {"text": {"x": ""}},
        "_version": "1",
    })
    _table(root, "try_i18n", {"text": {"Run it": ""}, "meta": {}})
    _page(root, "why", '<main>Fish &amp; chips. Plain. <button aria-label="Close"></button></main>')
    _page(root, "try", "<main>Run it</main>")
    assert gate.main() == 0
    out = capsys.readouterr().out
    assert "OK pages_i18n/why: 3 key(s) all present" in out
    assert "SKIP pages_i18n/gone: no built page" in out
    assert "OK try_i18n/try: 1 key(s) all present" in out


def test_stale_keys_fail(root, capsys):
    _table(root, "docs_i18n", {"docs": {"text": {"Old sentence": ""}, "aria": {"Gone": ""}}})
    _page(root, "docs", '<main>New sentence <a aria-label="Here"></a></main>')
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL docs_i18n/docs: 1 text key(s) and 1 aria key(s) match nothing" in out
    assert "      Old sentence" in out
    assert "      Gone" in out
    assert "1 page(s) carry stale keys" in out
