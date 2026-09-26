# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests for scripts/stamp_version.py.

Guards fix 283238d5 ("stamp the version into translation tables"): the
0.0.71 regeneration failed its live-key gate because the stamper moved
the pages to the new version but left the translation tables, whose
English keys quote the version, behind.
"""

import json

import stamp_version


def _table(tmp_path, monkeypatch, content):
    tables = tmp_path / "scripts"
    (tables / "docs_i18n").mkdir(parents=True)
    path = tables / "docs_i18n" / "fr.json"
    path.write_text(json.dumps(content, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    monkeypatch.setattr(stamp_version, "TABLES", tables, raising=False)
    return path


def test_tables_keys_and_values_move_to_the_new_version(tmp_path, monkeypatch):
    key = "This reference documents <strong>pain001 v0.0.70</strong>."
    path = _table(tmp_path, monkeypatch, {"documentation": {
        "meta": {"description": "Référence de pain001 v0.0.56"},
        "text": {key: "Cette référence documente <strong>pain001 v0.0.70</strong>."},
    }})

    touched = stamp_version.stamp_tables("0.0.71")

    table = json.loads(path.read_text(encoding="utf-8"))["documentation"]
    assert touched == 1
    assert list(table["text"]) == ["This reference documents <strong>pain001 v0.0.71</strong>."]
    assert "v0.0.71" in next(iter(table["text"].values()))
    assert table["meta"]["description"] == "Référence de pain001 v0.0.71"


def test_tables_keep_newer_versions_and_history_lines(tmp_path, monkeypatch):
    path = _table(tmp_path, monkeypatch, {
        "a": "requires pain001 v0.0.72",
        "b": "supported since v0.0.40",
    })

    assert stamp_version.stamp_tables("0.0.71") == 0
    table = json.loads(path.read_text(encoding="utf-8"))
    assert table == {"a": "requires pain001 v0.0.72", "b": "supported since v0.0.40"}


def test_pages_are_stamped_except_history_and_corpus(tmp_path, monkeypatch):
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "documentation.md").write_text(
        "Reference for pain001 v0.0.70.\nmin_pain001: 0.0.40\n", encoding="utf-8")
    (posts / "corpus-x.md").write_text("pain001 v0.0.70\n", encoding="utf-8")
    monkeypatch.setattr(stamp_version, "POSTS", posts)

    assert stamp_version.stamp("0.0.71") == 1
    assert (posts / "documentation.md").read_text(encoding="utf-8") == (
        "Reference for pain001 v0.0.71.\nmin_pain001: 0.0.40\n")
    assert (posts / "corpus-x.md").read_text(encoding="utf-8") == "pain001 v0.0.70\n"
