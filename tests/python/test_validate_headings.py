# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_headings.py.

Pins the H1 gate: every page has exactly one H1, and the count of H1s
over 60 visible characters is a ratchet against
scripts/headings_baseline.json (fail above it, a note below it, ok at
it, zero allowed when the baseline is absent).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import validate_headings as gate

LONG = "x" * 61


@pytest.fixture
def site(tmp_path, monkeypatch):
    site = tmp_path / "site"
    site.mkdir()
    monkeypatch.setattr(gate, "SITE", site)
    monkeypatch.setattr(gate, "BASELINE", tmp_path / "headings_baseline.json")
    return site


def _page(site: Path, rel: str, body: str) -> None:
    d = site / rel
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(f"<html><body>{body}</body></html>", encoding="utf-8")


def _baseline(site: Path, n: int) -> None:
    (site.parent / "headings_baseline.json").write_text(json.dumps({"overlong_h1": n}), encoding="utf-8")


def test_missing_site_is_an_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gate, "SITE", tmp_path / "absent")
    assert gate.main() == 1
    assert "site/ not built" in capsys.readouterr().err


def test_text_decodes_entities_and_drops_tags():
    assert gate.text("ISO&nbsp;20022 <em>A &amp;\n B</em>") == "ISO 20022 A & B"


def test_clean_site_without_baseline_passes(site, capsys):
    _page(site, "", "<h1>Home</h1>")
    # Exactly 60 visible characters once entities are decoded is allowed.
    _page(site, "why", "<h1>" + "&amp;" * 60 + "</h1>")
    assert gate.main() == 0
    out = capsys.readouterr().out
    assert "scanned 2 page(s)" in out
    assert "ok   0 over-long H1(s), at the baseline" in out
    assert "result: CLEAN" in out


def test_missing_and_multiple_h1_fail(site, capsys):
    _page(site, "none", "<p>no heading</p>")
    _page(site, "two", "<h1>One</h1><H1 class='x'>Two</H1>")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL 1 page(s) with no H1: ['none/index.html']" in out
    assert "FAIL 1 page(s) with more than one H1: ['two/index.html']" in out
    assert "result: CLEAN" not in out


def test_overlong_above_baseline_fails(site, capsys):
    _baseline(site, 1)
    _page(site, "a", f"<h1>{LONG}</h1>")
    _page(site, "b", f"<h1>{LONG}yy</h1>")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL 2 H1(s) over 60 chars, baseline allows 1" in out
    assert out.index(" 63 chars  b/index.html") < out.index(" 61 chars  a/index.html")


def test_overlong_at_baseline_is_ok(site, capsys):
    _baseline(site, 1)
    _page(site, "a", f"<h1>{LONG}</h1>")
    assert gate.main() == 0
    assert "ok   1 over-long H1(s), at the baseline" in capsys.readouterr().out


def test_overlong_below_baseline_asks_to_lower_it(site, capsys):
    _baseline(site, 3)
    _page(site, "a", f"<h1>{LONG}</h1>")
    assert gate.main() == 0
    out = capsys.readouterr().out
    assert "note 1 over-long H1(s), baseline allows 3" in out
    assert "lower overlong_h1 to 1 in headings_baseline.json" in out
    assert "result: CLEAN" in out
