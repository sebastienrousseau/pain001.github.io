# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""In-process tests for scripts/validate_no_commercial.py (decision D0).

test_no_commercial.py runs the gate as a subprocess, which coverage does
not see. These call main() directly to pin which files are scanned: only
text suffixes, never the two retired-page redirect stubs, never the
vendored pyodide tree, and the failure line quotes the matched context.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import validate_no_commercial as gate


@pytest.fixture
def site(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "site"
    root.mkdir()
    (root / "index.html").write_text("<p>Free software.</p>", encoding="utf-8")
    monkeypatch.setattr(gate, "SITE", root)
    return root


def _write(site: Path, rel: str, text: str) -> None:
    path = site / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_stubs_pyodide_binaries_and_directories_are_not_scanned(site, capsys):
    _write(site, "enterprise/index.html", "paid support, see HSBC")
    _write(site, "thanks/index.html", "formspree")
    _write(site, "pyodide/pyodide.js", "patreon.com")
    _write(site, "img/hsbc.png", "hsbc")
    (site / "folder.json").mkdir()
    assert gate.main() == 0
    assert capsys.readouterr().out == "validate_no_commercial: 0 problem(s)\n"


def test_each_pattern_in_a_file_is_reported_with_context(site, capsys):
    _write(site, "fr/index.html", 'x' * 60 + "throat to choke" + "y" * 60)
    _write(site, "feed.xml", "Private profile derivation and Formspree")
    assert gate.main() == 1
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "FAIL feed.xml: the retired paid profile offer: 'Private profile derivation and Formspree'"
    assert out[1] == "FAIL feed.xml: the retired enquiry form: 'Private profile derivation and Formspree'"
    assert out[2] == f"FAIL fr/index.html: the retired enterprise copy: '{'x' * 40}throat to choke{'y' * 40}'"
    assert out[3] == "validate_no_commercial: 3 problem(s)"


def test_a_missing_build_is_an_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gate, "SITE", tmp_path)
    assert gate.main() == 1
    assert capsys.readouterr().out == f"error: {tmp_path}/index.html not found; run the build first\n"
