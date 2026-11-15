# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""BreadcrumbList markup read from the trail each page shows.

Search Console's Breadcrumbs report fell to zero valid items: the PRISM
layouts (v0.0.3) kept the visible trail but dropped the BreadcrumbList
the earlier layouts carried. breadcrumb_ld writes it back from the
visible, translated trail; validate_jsonld checks the two agree.
"""

import json

import breadcrumb_ld as b
import validate_jsonld as v

TRAIL = ('<nav class="breadcrumb" aria-label="Fil d&#39;Ariane"> <ol><li><a href="/">Accueil</a></li>'
         '<li aria-current="page">Pourquoi Pain001 : l&#39;argumentaire</li></ol> </nav>')
CANONICAL = '<link rel="canonical" href="https://pain001.com/fr/why/">'


def _page(body=TRAIL, head=CANONICAL):
    return f"<html><head>{head}</head><body>{body}</body></html>"


def _ld(page):
    return [json.loads(t) for t in v.blocks(page)]


def test_the_trail_is_read_as_shown():
    assert b.trail(_page()) == [("Accueil", "/"), ("Pourquoi Pain001 : l'argumentaire", None)]
    assert b.trail(_page(body="<p>no trail</p>")) == []
    assert b.trail(_page(body='<nav class="breadcrumb"><ol><li> </li></ol></nav>')) == []


def test_the_list_mirrors_the_trail_and_ends_at_the_canonical_url():
    out = b.add_breadcrumbs(_page(), "fr/why/index.html")
    (ld,) = _ld(out)
    assert ld == {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://pain001.com/"},
        {"@type": "ListItem", "position": 2, "name": "Pourquoi Pain001 : l'argumentaire",
         "item": "https://pain001.com/fr/why/"}]}
    assert v.breadcrumb_problems("fr/why/index.html", out) == []


def test_without_a_canonical_the_served_path_is_the_url():
    out = b.add_breadcrumbs(_page(head=""), "glossary/index.html")
    assert _ld(out)[0]["itemListElement"][1]["item"] == "https://pain001.com/glossary/"


def test_pages_without_a_trail_or_already_marked_are_left_alone():
    once = b.add_breadcrumbs(_page(), "fr/why/index.html")
    assert b.add_breadcrumbs(once, "fr/why/index.html") == once
    lone = _page(body='<nav class="breadcrumb"><ol><li aria-current="page">Home</li></ol></nav>')
    assert b.add_breadcrumbs(lone, "index.html") == lone
    headless = TRAIL
    assert b.add_breadcrumbs(headless, "x.html") == headless


def test_a_closing_tag_in_a_name_cannot_end_the_script():
    page = _page(body='<nav class="breadcrumb"><ol><li><a href="/">Home</a></li>'
                      '<li>a &lt;/script&gt; b</li></ol></nav>')
    out = b.add_breadcrumbs(page, "a/index.html")
    assert "a <\\/script> b" in out
    assert _ld(out)[0]["itemListElement"][1]["name"] == "a </script> b"


def test_main_marks_every_page_with_a_trail(tmp_path, capsys):
    (tmp_path / "fr" / "why").mkdir(parents=True)
    (tmp_path / "fr" / "why" / "index.html").write_text(_page(), encoding="utf-8")
    (tmp_path / "index.html").write_text(_page(body=""), encoding="utf-8")
    assert b.main([str(tmp_path)]) == 0
    assert "BreadcrumbList" in (tmp_path / "fr" / "why" / "index.html").read_text(encoding="utf-8")
    assert "BreadcrumbList" not in (tmp_path / "index.html").read_text(encoding="utf-8")
    assert capsys.readouterr().out == "[breadcrumb_ld] BreadcrumbList on 1 page(s)\n"


def test_main_needs_a_site_directory(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["breadcrumb_ld.py"])
    assert b.main() == 2
    assert b.main([str(tmp_path / "missing")]) == 2
    assert "usage" in capsys.readouterr().err


def test_the_validator_reports_a_missing_or_short_list():
    assert v.breadcrumb_problems("a.html", _page()) == [
        "a.html: shows a breadcrumb trail but has 0 BreadcrumbList blocks, not 1"]
    out = b.add_breadcrumbs(_page(), "a.html").replace(
        '{"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://pain001.com/"}, ', "")
    assert v.breadcrumb_problems("a.html", out) == ["a.html: BreadcrumbList has 1 items, the trail shows 2"]
    assert v.breadcrumb_problems("b.html", _page(body="")) == []
