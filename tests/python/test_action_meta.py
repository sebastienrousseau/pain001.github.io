# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/action_meta.py: the name and folded description are
read from action.yml, a missing field fails, the block between the
markers is the only text rewritten, a page without markers fails, and a
wrong argument count prints the usage."""

import pytest

import action_meta

ACTION = (
    "name: ISO 20022 Payment File Check (pain001)\n"
    "description: >-\n"
    "  Validate ISO 20022 pain.001 and pain.008 payment XML (SEPA, CBPR+,\n"
    "  FedNow) against XSD, rules and scheme profiles. SARIF.\n"
    "runs:\n  using: composite\n"
)
PAGE = "Before.\n\n<!-- action:start -->\nold\n<!-- action:end -->\n\nAfter.\n"


def _checkout(tmp_path, text=ACTION):
    (tmp_path / "action.yml").write_text(text, encoding="utf-8")
    return tmp_path


def test_read_action_unfolds_the_description(tmp_path):
    name, description = action_meta.read_action(_checkout(tmp_path))
    assert name == "ISO 20022 Payment File Check (pain001)"
    assert description == (
        "Validate ISO 20022 pain.001 and pain.008 payment XML (SEPA, CBPR+, "
        "FedNow) against XSD, rules and scheme profiles. SARIF."
    )


@pytest.mark.parametrize("text", ["name: x\n", "description: y\n"])
def test_read_action_refuses_a_missing_field(tmp_path, text):
    with pytest.raises(SystemExit, match="no name or no description"):
        action_meta.read_action(_checkout(tmp_path, text))


def test_render_keeps_the_markers():
    block = action_meta.render("N", "D.")
    assert block == (
        "<!-- action:start -->\n"
        "The action is named **N**, and its `action.yml` describes it as: D.\n"
        "<!-- action:end -->"
    )


def test_main_rewrites_only_the_block(tmp_path, monkeypatch, capsys):
    page = tmp_path / "developers-ci.md"
    page.write_text(PAGE, encoding="utf-8")
    monkeypatch.setattr(action_meta, "PAGE", page)
    (tmp_path / "core").mkdir()
    checkout = _checkout(tmp_path / "core")
    assert action_meta.main([str(checkout)]) == 0
    text = page.read_text(encoding="utf-8")
    assert text.startswith("Before.\n\n<!-- action:start -->\nThe action is named **ISO 20022")
    assert text.endswith("SARIF.\n<!-- action:end -->\n\nAfter.\n")
    assert "old" not in text
    assert "[action] ISO 20022 Payment File Check (pain001)" in capsys.readouterr().out


def test_main_fails_without_markers(tmp_path, monkeypatch, capsys):
    page = tmp_path / "developers-ci.md"
    page.write_text("No block.\n", encoding="utf-8")
    monkeypatch.setattr(action_meta, "PAGE", page)
    assert action_meta.main([str(_checkout(tmp_path))]) == 1
    assert page.read_text(encoding="utf-8") == "No block.\n"
    assert "no markers" in capsys.readouterr().out


def test_main_prints_usage_on_wrong_arguments(capsys):
    assert action_meta.main([]) == 2
    assert "usage" in capsys.readouterr().out


def test_the_real_page_carries_the_markers():
    assert action_meta.BLOCK.search(action_meta.PAGE.read_text(encoding="utf-8"))
