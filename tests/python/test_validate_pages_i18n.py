# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_pages_i18n.py.

Each page translation table must list the same pages as en.json, the
same keys in each page's meta, text and aria sections, and keep the HTML
tags of each text entry; a value left equal to its English key of more
than two words is counted as untranslated-looking but passes. The table
directory is the first argument, resolved against scripts/ (an absolute
path stays absolute, which is how the tests point it at tmp_path).
"""

from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "validate_pages_i18n.py"


def _page(text: dict[str, str]) -> dict[str, dict[str, str]]:
    return {"meta": {"title": "t"}, "text": text, "aria": {"nav": "n"}}


EN = {"why": _page({"Read <a>the</a> case now": "x", "Short one": "x"}),
      "faq": _page({"Questions": "x"})}


def _run(tmp_path: Path, monkeypatch, capsys, tables: dict[str, object], *argv: str) -> tuple[int, str]:
    d = tmp_path / "pages_i18n"
    d.mkdir()
    for slug, content in tables.items():
        body = content if isinstance(content, str) else json.dumps(content)
        (d / f"{slug}.json").write_text(body, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), *(argv or (str(d),))])
    with pytest.raises(SystemExit) as exc:
        runpy.run_path(str(SCRIPT), run_name="__main__")
    return exc.value.code, capsys.readouterr().out


def test_a_complete_translation_passes(tmp_path, monkeypatch, capsys):
    fr = {"why": _page({"Read <a>the</a> case now": "Lisez <a>le</a> dossier", "Short one": "Court"}),
          "faq": _page({"Questions": "Questions"})}
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "fr": fr})
    assert code == 0
    assert out == "OK fr\n"


def test_untranslated_values_are_counted_but_pass(tmp_path, monkeypatch, capsys):
    de = {"why": _page({"Read <a>the</a> case now": "Read <a>the</a> case now", "Short one": "Kurz"}),
          "faq": _page({"Questions": "Fragen"})}
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "de": de})
    assert code == 0
    assert out == "OK de (untranslated-looking: 1)\n"


def test_page_key_and_tag_mismatches_fail(tmp_path, monkeypatch, capsys):
    # "faq" is missing, "extra" is not in English, and an unknown text key
    # is not tag-checked against a source it does not have.
    es = {"why": {"meta": {"title": "t"}, "aria": {"nav": "n"},
                  "text": {"Read <a>the</a> case now": "Lea el caso", "Short one": "Corto",
                           "Unknown <b>key</b>": "Sin etiqueta"}},
          "extra": _page({})}
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "es": es})
    assert code == 1
    assert out == ("FAIL es: pages: ['extra', 'faq']; why.text: key mismatch; "
                   "why: tag mismatch 'Read <a>the</a> case now'; faq.meta: key mismatch\n")


def test_invalid_json_fails_and_other_locales_still_run(tmp_path, monkeypatch, capsys):
    it = {"why": _page({"Read <a>the</a> case now": "Leggi <a>il</a> caso", "Short one": "Breve"}),
          "faq": _page({"Questions": "Domande"})}
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "fi": "{", "it": it})
    assert code == 1
    lines = out.splitlines()
    assert lines[0].startswith("FAIL fi: invalid JSON (")
    assert lines[1] == "OK it"

