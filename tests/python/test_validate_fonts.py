# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_fonts.py.

Pins the three font checks on a built site: every shipped font is
referenced by an @font-face in a stylesheet a page links, every
referenced font exists, and every declared family is named in a
font-family (directly or through chained custom properties); plus the
payload budget, and that unlinked (carried-forward) stylesheets are
ignored.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import validate_fonts as gate

FACE = '@font-face { font-family: "Serif Four"; src: url("/fonts/serif.woff2") format("woff2"); }\n'


@pytest.fixture
def site(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "SITE", tmp_path)
    (tmp_path / "fonts").mkdir()
    (tmp_path / "css").mkdir()
    return tmp_path


def _font(site: Path, name: str, size: int = 1024) -> None:
    (site / "fonts" / name).write_bytes(b"\0" * size)


def _css(site: Path, name: str, body: str, linked: bool = True) -> None:
    (site / "css" / name).write_text(body, encoding="utf-8")
    if linked:
        page = site / "index.html"
        old = page.read_text(encoding="utf-8") if page.exists() else ""
        page.write_text(old + f'<link rel="stylesheet" href="/css/{name}">', encoding="utf-8")


def test_missing_site_is_an_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gate, "SITE", tmp_path / "absent")
    assert gate.main() == 1
    assert "site/ not built" in capsys.readouterr().err


def test_declared_used_and_shipped_font_passes(site, capsys):
    _font(site, "serif.woff2", 2048)
    _css(site, "main.css", FACE + "h1 { font-family: 'Serif Four', serif; }")
    # A stale carried-forward bundle naming a font no longer shipped.
    _css(site, "old.css", '@font-face { font-family: Gone; src: url(/fonts/gone.woff2); }', linked=False)
    assert gate.main() == 0
    out = capsys.readouterr().out
    assert "scanned 1 font file(s), 1 @font-face block(s) in 1 linked stylesheet(s)" in out
    assert "payload 2 KB of 140 KB budget" in out
    assert "result: CLEAN" in out


def test_family_reached_through_a_custom_property_passes(site):
    _font(site, "serif.woff2")
    _css(site, "main.css", FACE + ':root { --type-display: "Serif Four", serif; }\n'
         "h1 { font-family: var(--type-display); }")
    assert gate.main() == 0


def test_chained_custom_properties_resolve_three_deep(site, capsys):
    # Each level resolves to another var() reference, so the loop runs
    # its full three iterations; what is left unresolved after that is
    # not counted as a family name.
    _font(site, "serif.woff2")
    _css(site, "main.css", FACE + ":root {\n"
         "  --a: varvar(--x(--b), serif;\n"
         "  --b: varvar(--x(--c), serif;\n"
         '  --c: varvar(--x(--d), "Serif Four";\n'
         "}\nh1 { font-family: var(--a); }\n")
    assert gate.main() == 0
    assert "result: CLEAN" in capsys.readouterr().out


def test_unresolvable_custom_property_leaves_family_unused(site, capsys):
    _font(site, "serif.woff2")
    _css(site, "main.css", FACE + "h1 { font-family: var(--missing); }")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL 1 family(ies) declared but never named in a font-family: ['serif four']" in out


def test_orphan_and_dangling_fonts_fail(site, capsys):
    _font(site, "serif.woff2")
    _font(site, "extra.woff", 3072)
    _css(site, "main.css",
         "@font-face { src: url('/fonts/serif.woff2'), url(/fonts/missing.woff2); }\n"
         "body { font-family: system-ui, ; }")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL 1 font(s) shipped but never declared (3 KB wasted): ['extra.woff']" in out
    assert "FAIL 1 @font-face src(s) point at a missing file: ['missing.woff2']" in out
    assert "declared but never named" not in out
    assert "result: CLEAN" not in out


def test_payload_over_budget_fails(site, monkeypatch, capsys):
    monkeypatch.setattr(gate, "MAX_FONT_BYTES", 1024)
    _font(site, "serif.woff2", 2048)
    _css(site, "main.css", FACE + "p { font-family: 'Serif Four'; }")
    assert gate.main() == 1
    assert "FAIL font payload 2 KB exceeds 1 KB" in capsys.readouterr().out
