# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_jsonld.py beyond the postbuild round trip.

Pins graph flattening for lists and scalars, the @context check, each
homepage SoftwareApplication requirement, and the command's exit codes
and messages against a site in tmp_path.
"""

from __future__ import annotations

import json

import validate_jsonld as v

ORG = {"@type": "Organization", "@id": "https://pain001.com/#org"}
APP = {"@type": "SoftwareApplication", "softwareVersion": "0.0.86", "offers": {"price": "0"},
       "author": {"@id": v.PERSON_ID}, "publisher": {"@id": "https://pain001.com/#org"}}


def _script(data) -> str:
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def test_nodes_flattens_lists_graphs_and_ignores_scalars():
    assert v.nodes([{"@graph": [ORG, "x"]}, APP, 3]) == [ORG, APP]
    assert v.nodes("text") == []


def test_wrong_or_missing_context_is_reported():
    html = _script({"@context": "http://schema.org"}) + _script([1]) + _script({"@context": "https://schema.org/"})
    assert v.page_problems("p.html", html) == ["p.html: JSON-LD @context is 'http://schema.org'",
                                               "p.html: JSON-LD @context is None"]


def test_a_complete_homepage_passes():
    assert v.home_problems(_script({"@context": "https://schema.org", "@graph": [ORG, APP]}), "0.0.86") == []


def test_each_homepage_requirement_is_reported():
    app = {"@type": "SoftwareApplication", "softwareVersion": "0.0.86"}
    assert v.home_problems(_script([app]), "0.0.86") == [
        "homepage SoftwareApplication is not offered at price 0",
        "homepage SoftwareApplication author is not the Person entity",
        "homepage SoftwareApplication publisher is not an Organization in the graph",
    ]


def _site(tmp_path, monkeypatch, home):
    site = tmp_path / "site"
    (site / "a").mkdir(parents=True)
    (site / "index.html").write_text(home, encoding="utf-8")
    (site / "a" / "index.html").write_text(_script({"@context": "https://schema.org"}), encoding="utf-8")
    corpus = tmp_path / "static" / "corpus"
    corpus.mkdir(parents=True)
    (corpus / "index.json").write_text(json.dumps({"pain001": "0.0.86"}), encoding="utf-8")
    monkeypatch.setattr(v, "ROOT", tmp_path)
    monkeypatch.setattr(v, "SITE", site)


def test_main_passes_a_valid_site(tmp_path, monkeypatch, capsys):
    _site(tmp_path, monkeypatch, _script({"@context": "https://schema.org", "@graph": [ORG, APP]}))
    assert v.main() == 0
    assert capsys.readouterr().out == "JSON-LD: 2 block(s) on 2 page(s) parse; homepage states Pain001 0.0.86\n"


def test_main_reports_problems_on_stderr(tmp_path, monkeypatch, capsys):
    _site(tmp_path, monkeypatch, _script({"@context": "https://schema.org", "@graph": [ORG, dict(APP, review=[])]}))
    assert v.main() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "index.html: JSON-LD claims a rating or review\n"


def _dataset(description: str) -> str:
    return _script({"@context": "https://schema.org", "@type": "Dataset", "description": description})


def test_a_dataset_description_outside_50_to_5000_characters_is_reported():
    assert v.page_problems("a.html", _dataset("x" * 49)) == [
        "a.html: Dataset description is 49 characters, not 50 to 5000"]
    assert v.page_problems("b.html", _dataset("x" * 5001)) == [
        "b.html: Dataset description is 5001 characters, not 50 to 5000"]
    assert v.page_problems("c.html", _dataset("x" * 50)) == []
    assert v.page_problems("d.html", _dataset("x" * 5000)) == []
