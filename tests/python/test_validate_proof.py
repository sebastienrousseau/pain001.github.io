# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_proof.py.

Every figure in the homepage proof band must equal the count recomputed
from _posts/: corpus scenarios (each recording a passed XSD check), the
distinct countries among them, and message-specification editions. A
figure with no source, a source with no figure, a scenario without the
XSD line, or a missing build each fail the gate.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import validate_proof as gate

PASSED = "- **Official XSD**: passed.\n"


@pytest.fixture
def tree(tmp_path, monkeypatch):
    posts, site = tmp_path / "_posts", tmp_path / "site"
    posts.mkdir()
    site.mkdir()
    monkeypatch.setattr(gate, "POSTS", posts)
    monkeypatch.setattr(gate, "SITE", site)
    for name in ("corpus-fr-sepa-sct.md", "corpus-fr-urgent.md", "corpus-de-sepa-sct.md"):
        (posts / name).write_text(PASSED, encoding="utf-8")
    for name in ("message-spec-pain.001.001.03.md", "message-spec-pain.001.001.09.md",
                 "corpus-index.md", "corpus-fr-sepa-sct.txt", "governance.md"):
        (posts / name).write_text("not counted\n", encoding="utf-8")
    return posts, site


def _home(site: Path, **figures: str) -> None:
    band = "".join(f'<dd data-proof-key="{k}"> {v} </dd>' for k, v in figures.items())
    (site / "index.html").write_text(f"<dl>{band}</dl>", encoding="utf-8")


def test_sources_count_scenarios_countries_and_editions(tree):
    assert gate.sources() == ({"scenarios": 3, "countries": 2, "editions": 2}, [])


def test_matching_figures_pass(tree, capsys):
    _home(tree[1], scenarios="3", countries="2", editions="2")
    assert gate.main() == 0
    assert capsys.readouterr().out == (
        "ok   scenarios = 3\nok   countries = 2\nok   editions = 2\nresult: CLEAN\n")


def test_stale_missing_and_unsourced_figures_fail(tree, capsys):
    (tree[0] / "corpus-de-sepa-sct.md").write_text("- **Official XSD**: failed.\n", encoding="utf-8")
    _home(tree[1], scenarios="12", countries="2", downloads="9k")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "ok   countries = 2" in out
    assert "FAIL corpus-de-sepa-sct.md: no '- **Official XSD**: passed.' line" in out
    assert "FAIL scenarios: homepage shows 12, source says 3" in out
    assert 'FAIL editions: no data-proof-key="editions" figure on the homepage' in out
    assert "FAIL downloads: figure has no source in this gate" in out
    assert out.endswith("result: FAIL\n")


def test_a_missing_build_is_an_error(tree, capsys):
    assert gate.main() == 1
    assert capsys.readouterr().out == "error: site/index.html not found; run the build first\n"
