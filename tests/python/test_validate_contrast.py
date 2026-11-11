# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_contrast.py.

Pins the PRISM token gate on a synthetic stylesheet: every declared
pair meets its WCAG floor in light and dark, the two dark blocks agree,
the Display P3 overrides keep their sRGB luminance and agree between
their dark blocks, and a `.theme-dark` band restates the dark tokens
exactly. Also pins the luminance arithmetic and the rule-block parser.
"""

from __future__ import annotations

import sys

import pytest

import validate_contrast as gate

# Tokens painted as grounds (white); every other token is ink (black).
# Every pair in the gate then sets black against white, 21:1.
WHITE = set(gate.GROUNDS) | {
    "--accent-ink", "--cta-ink", "--accent-soft", "--green-soft", "--clay-soft",
    "--gold-soft", "--burgundy-soft", "--hero-bg", "--hero-surface", "--code-bg",
    "--code-bar", "--badge-blue-to", "--badge-clay-to", "--badge-green-to",
    "--badge-gold-to", "--badge-burgundy-to", "--badge-navy-to",
}
NAMES = sorted(
    set(gate.GROUNDS) | set(gate.TEXT_ON_GROUNDS)
    | {t for pair in gate.TEXT_PAIRS + gate.NON_TEXT_PAIRS for t in pair}
)


def _decls(overrides: dict[str, str] | None = None, indent: str = "    ") -> str:
    tokens = {n: "#fff" if n in WHITE else "#000000" for n in NAMES}
    tokens.update(overrides or {})
    return "".join(f"{indent}{k}: {v};\n" for k, v in tokens.items())


def _css(light=None, media=None, toggle=None, p3=None, band=None) -> str:
    css = (":root,\n:root[data-theme=\"light\"] {\n  /* light */\n" + _decls(light) + "}\n"
           "@media (prefers-color-scheme: dark) {\n"
           "  :root:not([data-theme=\"light\"]) {\n" + _decls(media) + "  }\n}\n"
           "@media screen {\n"
           "  :root[data-theme=\"dark\"] {\n" + _decls(toggle) + "  }\n}\n")
    if p3 is not None:
        light_p3, media_p3, toggle_p3 = p3
        css += ("@media (color-gamut: p3) {\n"
                "  :root,\n  :root[data-theme=\"light\"] { --accent: " + light_p3 + "; }\n"
                "  @media (prefers-color-scheme: dark) {\n"
                "    :root:not([data-theme=\"light\"]) { --accent: " + media_p3 + "; }\n  }\n"
                "  :root[data-theme=\"dark\"] { --accent: " + toggle_p3 + "; }\n}\n")
    if band is not None:
        css += "\n.theme-dark {\n" + band + "}\n"
    return css


def _run(tmp_path, monkeypatch, css: str) -> int:
    path = tmp_path / "prism.css"
    path.write_text(css, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["validate_contrast.py", str(path)])
    return gate.main()


def test_luminance_of_hex_and_p3():
    assert gate.luminance("#fff") == pytest.approx(1.0)
    assert gate.luminance("#000000") == 0.0
    assert gate.luminance("#808080") == pytest.approx(0.2158605)
    assert gate.luminance("color(display-p3 1 1 1)") == pytest.approx(1.0)
    assert gate.luminance("color(display-p3 0.01 0 0)") == pytest.approx(0.2289746 * 0.01 / 12.92)
    assert gate.ratio("#000", "#fff") == pytest.approx(21.0)
    with pytest.raises(ValueError, match="not a hex colour: red"):
        gate.luminance("red")


def test_block_reads_nested_rule_without_comments():
    css = "a { --x: #fff; /* --y: #000; */ b { c: d; } --z: #000; }"
    assert gate.block(css, "a") == {"--x": "#fff", "--z": "#000"}
    with pytest.raises(SystemExit, match="no rule matching 'q'"):
        gate.block(css, "q")


def test_check_reports_undeclared_and_low_contrast(capsys):
    tokens = {n: "#fff" if n in WHITE else "#000" for n in NAMES}
    tokens["--ink"] = "#777"
    del tokens["--signal"]
    failures = gate.check("light", tokens)
    assert "light: --signal on --bg: token not declared" in failures
    assert "light: --ink #777 on --bg #fff = 4.48:1, needs 7:1" in failures
    assert capsys.readouterr().out == "light: 69 pair(s)\n"


def test_clean_stylesheet_passes(tmp_path, monkeypatch, capsys):
    css = _css(p3=("color(display-p3 0 0 0)",) * 3, band=_decls(indent="  "))
    assert _run(tmp_path, monkeypatch, css) == 0
    out = capsys.readouterr().out
    for name in ("light", "dark", "light P3", "dark P3"):
        assert f"{name}: 69 pair(s)" in out
    assert out.endswith("result: CLEAN\n")


def test_default_path_is_the_repository_stylesheet(tmp_path, monkeypatch, capsys):
    path = tmp_path / "prism.css"
    path.write_text(_css(), encoding="utf-8")
    monkeypatch.setattr(gate, "CSS", path)
    monkeypatch.setattr(sys, "argv", ["validate_contrast.py"])
    assert gate.main() == 0
    assert "P3" not in capsys.readouterr().out


def test_low_contrast_and_dark_drift_fail(tmp_path, monkeypatch, capsys):
    css = _css(light={"--ink": "#777"}, media={"--line": "#111"})
    assert _run(tmp_path, monkeypatch, css) == 1
    out = capsys.readouterr().out
    assert "FAIL light: --ink #777 on --bg #fff = 4.48:1, needs 7:1" in out
    assert "FAIL dark blocks disagree on --line: media '#111' vs toggle '#000000'" in out
    assert out.endswith("result: FAIL\n")


def test_p3_drift_fails(tmp_path, monkeypatch, capsys):
    css = _css(p3=("color(display-p3 0.5 0.5 0.5)", "color(display-p3 0 0 0)", "color(display-p3 0.01 0 0)"))
    assert _run(tmp_path, monkeypatch, css) == 1
    out = capsys.readouterr().out
    assert "FAIL P3 dark blocks disagree" in out
    assert "FAIL light P3: --accent color(display-p3 0.5 0.5 0.5) has luminance 0.2140" in out
    assert "restate it from the sRGB token" in out
    assert "FAIL light P3: --accent color(display-p3 0.5 0.5 0.5) on --bg #fff" in out
    # A P3 value within 1% of a zero luminance is still a drift.
    assert "FAIL dark P3: --accent color(display-p3 0.01 0 0) has luminance 0.0002" in out


def test_theme_dark_band_must_restate_dark_tokens(tmp_path, monkeypatch, capsys):
    css = _css(band="  --ink: #000000;\n  --bg: #eee;\n")
    assert _run(tmp_path, monkeypatch, css) == 1
    out = capsys.readouterr().out
    assert "FAIL .theme-dark --bg '#eee' differs from the dark theme's '#fff'" in out
    assert "--ink" not in out.split("FAIL .theme-dark")[1].split("\n")[0]
