# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""scripts/validate_readme.py holds README.md to the workspace template.

Pins the CI gate on the README's shape: the exact order of level-2
headings, the centred project heading the order is resolved against,
the structural markers, and the ban on unresolved template tokens. The
repository's own README must pass it.
"""

from __future__ import annotations

from pathlib import Path

import validate_readme

ROOT = Path(__file__).resolve().parents[2]
# REUSE-IgnoreStart
# A README fixture, not this file's licence declaration.
HEAD = (
    "<!-- SPDX-License-Identifier: MIT -->\n"
    '<p align="center">x</p>\n<h1 align="center">Demo</h1>\n'
    "ossf-scorecard\n"
)
# REUSE-IgnoreEnd


def _readme(tmp_path, headings, head=HEAD):
    body = head + "".join(f"\n## {h}\n\ntext\n" for h in headings)
    path = tmp_path / "README.md"
    path.write_text(body, encoding="utf-8")
    return path


def _required(project="Demo"):
    return [h.format(project=project) for h in validate_readme.REQUIRED_HEADINGS]


def test_the_repository_readme_conforms():
    assert validate_readme.validate(ROOT / "README.md") == []


def test_a_conforming_readme_passes(tmp_path):
    assert validate_readme.validate(_readme(tmp_path, _required())) == []


def test_a_missing_file_is_reported(tmp_path):
    assert validate_readme.validate(tmp_path / "nope.md") == [f"{tmp_path / 'nope.md'} is missing"]


def test_tokens_and_structure_are_reported(tmp_path):
    path = _readme(tmp_path, _required(), head="{{PROJECT}}\n")
    issues = validate_readme.validate(path)
    assert issues[0].startswith("unresolved template variables")
    assert "missing required structure: ossf-scorecard" in issues
    assert issues[-1] == 'missing centred project heading: <h1 align="center">'


def test_missing_and_unexpected_headings(tmp_path):
    headings = [h for h in _required() if h != "Benchmarks"] + ["Extra"]
    issues = validate_readme.validate(_readme(tmp_path, headings))
    assert issues == ["missing heading: ## Benchmarks", "unexpected heading: ## Extra"]


def test_headings_out_of_order(tmp_path):
    headings = _required()
    headings[1], headings[2] = headings[2], headings[1]
    (issue,) = validate_readme.validate(_readme(tmp_path, headings))
    assert issue.startswith("required headings are present but out of order")


def test_main_exit_codes(tmp_path, monkeypatch, capsys):
    good = _readme(tmp_path, _required())
    monkeypatch.setattr("sys.argv", ["validate_readme.py", str(good)])
    assert validate_readme.main() == 0
    assert "conforms to the workspace template" in capsys.readouterr().out
    monkeypatch.setattr("sys.argv", ["validate_readme.py", str(tmp_path / "gone.md")])
    assert validate_readme.main() == 1
    assert "1 problem(s)" in capsys.readouterr().err
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr("sys.argv", ["validate_readme.py"])
    assert validate_readme.main() == 0
