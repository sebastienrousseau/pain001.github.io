# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_runtime_i18n.py.

Each runtime string table must carry exactly the keys of en.json and keep
every {placeholder} of each key; a value left equal to a key of more than
two words is counted as untranslated-looking but passes.

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

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "validate_runtime_i18n.py"
EN = {"Loaded {n} rows from {file}": "x", "Run the demo": "x", "Go": "x"}


def _run(tmp_path: Path, monkeypatch, capsys, tables: dict[str, object]) -> tuple[int, str]:
    d = tmp_path / "runtime_i18n"
    d.mkdir()
    for slug, content in tables.items():
        body = content if isinstance(content, str) else json.dumps(content)
        (d / f"{slug}.json").write_text(body, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [str(SCRIPT)])
    code = compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")
    with pytest.raises(SystemExit) as exc:
        exec(code, {"__name__": "__main__", "__file__": str(tmp_path / "harness.py")})
    return exc.value.code, capsys.readouterr().out


def test_a_complete_translation_passes(tmp_path, monkeypatch, capsys):
    fr = {"Loaded {n} rows from {file}": "{n} lignes lues depuis {file}",
          "Run the demo": "Lancer la démo", "Go": "Go"}
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "fr": fr})
    assert code == 0
    assert out == "OK fr keys=3\n"


def test_untranslated_values_are_counted_but_pass(tmp_path, monkeypatch, capsys):
    de = {"Loaded {n} rows from {file}": "{n} Zeilen aus {file}",
          "Run the demo": "Run the demo", "Go": "Go"}
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "de": de})
    assert code == 0
    assert out == "OK de keys=3 (untranslated-looking: 1)\n"


def test_key_and_placeholder_mismatches_fail(tmp_path, monkeypatch, capsys):
    es = {"Loaded {n} rows from {file}": "{n} filas leídas", "Go": "Ir", "Extra key": "x"}
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "es": es})
    assert code == 1
    assert out == ("FAIL es: keys: missing=1 extra=1; "
                   "placeholder mismatch: 'Loaded {n} rows from {file}'\n")


def test_invalid_json_fails_and_other_locales_still_run(tmp_path, monkeypatch, capsys):
    it = {"Loaded {n} rows from {file}": "{n} righe da {file}", "Run the demo": "Avvia", "Go": "Andiamo"}
    code, out = _run(tmp_path, monkeypatch, capsys, {"en": EN, "fi": "[1,", "it": it})
    assert code == 1
    lines = out.splitlines()
    assert lines[0].startswith("FAIL fi: invalid JSON (")
    assert lines[1] == "OK it keys=3"
