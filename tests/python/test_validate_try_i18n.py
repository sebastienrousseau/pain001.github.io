# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_try_i18n.py.

Each locale table for the demo page must carry the same keys as en.json
in every section and keep the HTML tags of each text entry; a value left
equal to its English key is counted as untranslated-looking but passes.

The script resolves its tables from its own location, so the tests run
its real source with ``__file__`` pointing into a temporary directory.
The stand-in file name differs from the script's, which makes coverage
attribute the lines to the compiled source path, scripts/.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "validate_try_i18n.py"
SECTIONS = ("meta", "text", "aria", "chrome", "chrome_aria")


def _run(tmp_path: Path, monkeypatch, capsys, tables: dict[str, object]) -> tuple[int, str]:
    d = tmp_path / "try_i18n"
    d.mkdir()
    for slug, content in tables.items():
        body = content if isinstance(content, str) else json.dumps(content)
        (d / f"{slug}.json").write_text(body, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [str(SCRIPT)])
    code = compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")
    with pytest.raises(SystemExit) as exc:
        exec(code, {"__name__": "__main__", "__file__": str(tmp_path / "harness.py")})
    return exc.value.code, capsys.readouterr().out


def _table(text: dict[str, str]) -> dict[str, dict[str, str]]:
    table = {sec: {"k": "v"} for sec in SECTIONS}
    table["text"] = text
    return table


EN = _table({"Run <b>the</b> demo now": "Run <b>the</b> demo now", "Go": "Go"})


def test_a_complete_translation_passes(tmp_path, monkeypatch, capsys):
    fr = _table({"Run <b>the</b> demo now": "Lancez <b>la</b> démo", "Go": "Allez"})
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "fr": fr})
    assert code == 0
    assert out == "OK fr text=2\n"


def test_untranslated_values_are_counted_but_pass(tmp_path, monkeypatch, capsys):
    # "Go" equals its key but has too few words to count.
    de = _table({"Run <b>the</b> demo now": "Run <b>the</b> demo now", "Go": "Go"})
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "de": de})
    assert code == 0
    assert out == "OK de text=2 (untranslated-looking: 1)\n"


def test_missing_and_extra_keys_fail_per_section(tmp_path, monkeypatch, capsys):
    es = _table({"Run <b>the</b> demo now": "Ejecute <b>la</b> demo", "Go": "Ir"})
    del es["aria"]["k"]
    es["chrome"]["extra"] = "x"
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "es": es})
    assert code == 1
    assert out == "FAIL es: aria: missing=1 extra=0 e.g. ['k']; chrome: missing=0 extra=1\n"


def test_a_dropped_tag_fails(tmp_path, monkeypatch, capsys):
    it = _table({"Run <b>the</b> demo now": "Esegui la demo", "Go": "Andiamo", "Stray": "x"})
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "it": it})
    assert code == 1
    assert "FAIL it: text: missing=0 extra=1; tag mismatch: 'Run <b>the</b> demo now'" in out


def test_invalid_json_fails_and_other_locales_still_run(tmp_path, monkeypatch, capsys):
    pt = _table({"Run <b>the</b> demo now": "Execute <b>a</b> demo", "Go": "Vá"})
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "nl": "{not json", "pt": pt})
    assert code == 1
    lines = out.splitlines()
    assert lines[0].startswith("FAIL nl: invalid JSON (")
    assert lines[1] == "OK pt text=2"
