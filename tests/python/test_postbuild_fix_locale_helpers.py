# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Localisation helpers in postbuild_fix.

Pins the small transforms the locale generators compose: RTL direction,
hreflang clusters, chrome and status-strip translation, translation-table
loading, language-menu retargeting, the English-only submenu cue, and the
corpus page helpers. Anchored replacements must never touch body text.
"""

import postbuild_fix as pb

TOKENS = ["T%d" % i for i in range(26)]
STRIP = ["S%d" % i for i in range(8)]


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_add_rtl_dir_only_for_rtl_locales():
    assert pb.add_rtl_dir('<html lang="fr">', "fr") == '<html lang="fr">'
    assert pb.add_rtl_dir('<html lang="ar"><html>', "ar") == '<html lang="ar" dir="rtl"><html>'
    assert pb.add_rtl_dir('<html dir="rtl">', "he") == '<html dir="rtl">'


def test_hreflang_clusters_omit_self():
    fr = pb.hreflang_cluster("fr")
    assert 'hreflang="fr"' not in fr
    assert '<link rel="alternate" hreflang="x-default" href="https://pain001.com/" />' in fr
    assert 'hreflang="en"' not in pb.hreflang_cluster("en")
    assert fr.count("<link") == len(pb.LOCALES) + 1
    why = pb.path_hreflang_cluster("why/", "de")
    assert 'href="https://pain001.com/fr/why/"' in why and 'hreflang="de"' not in why
    assert 'href="https://pain001.com/try/"' in pb.try_hreflang_cluster("fr")


def test_translate_chrome_replaces_anchored_strings_only():
    html = (
        '<button id="ssg-search-btn" type="button" aria-label="Search"><i></i><span>Search</span></button>'
        '<a href="/">Home</a><a>Docs</a><p>Docs are great. Home sweet Home.</p>'
        "<span>5 min read</span><h2>Contents</h2><time>26 July 2026</time>"
        '<p>Open-source ISO 20022 payment initiation. Validated files, local processing, no lock-in.</p>'
        '<button aria-label="Switch to dark theme" title="Switch theme"></button>'
    )
    out = pb.translate_chrome(html, TOKENS)
    assert '<button id="ssg-search-btn" type="button" aria-label="T20"><i></i><span>T20</span></button>' in out
    assert ">T0</a>" in out and ">T8</a>" in out
    assert "<p>Docs are great. Home sweet Home.</p>" in out
    assert "<span>5 T2</span>" in out and ">T4</h2>" in out and ">2026-07-26<" in out
    assert "<p>T11</p>" in out
    assert 'aria-label="T18" data-label-dark="T18" data-label-light="T19" title="T18"' in out


def test_translate_status_strip():
    html = (
        '<section aria-label="Current standards and project status">'
        "<strong>Next CBPR+ milestone:</strong> 14 Nov 2026</a>"
        "<strong>Address rule:</strong> structured or hybrid</a></section>"
    )
    out = pb.translate_status_strip(html, STRIP)
    assert out == (
        '<section aria-label="S0"><strong>S1</strong> 2026-11-14</a>'
        "<strong>S2</strong> S3</a></section>"
    )


def home_with_strip(milestone="14 Nov 2026"):
    rows = (("Next CBPR+ milestone:", milestone), ("Relay version:", "09"),
            ("Latest release:", "0.0.85"), ("Message definitions:", "2019"),
            ("Reviewed:", "1 Nov 2026"))
    items = "".join('<a href="#"><strong>%s</strong> %s</a>' % r for r in rows)
    return '<section class="status-strip" aria-label="x">' + items + "</section>"


def test_status_strip_values(tmp_path):
    assert pb.status_strip_values(tmp_path) is None
    put(tmp_path / "index.html", "<p>no strip</p>")
    assert pb.status_strip_values(tmp_path) is None
    put(tmp_path / "index.html", home_with_strip())
    vals = pb.status_strip_values(tmp_path)
    assert vals == {"milestone": "2026-11-14", "relay": "09", "release": "0.0.85",
                    "msgdefs": "2019", "reviewed": "1 Nov 2026"}
    put(tmp_path / "index.html", home_with_strip("14 Foo 2026"))
    assert pb.status_strip_values(tmp_path)["milestone"] == "14 Foo 2026"
    put(tmp_path / "index.html", home_with_strip("TBC"))
    assert pb.status_strip_values(tmp_path)["milestone"] == "TBC"


def test_status_strip_html():
    vals = {"milestone": "M", "relay": "R", "release": "L", "msgdefs": "D", "reviewed": "V"}
    out = pb.status_strip_html(STRIP, vals)
    assert out.startswith('<section class="status-strip" aria-label="S0">')
    assert '<a href="/iso20022-roadmap/"><strong>S1</strong> M</a>' in out
    assert '<a href="https://pypi.org/project/pain001/" rel="external"><strong>S5</strong> L</a>' in out
    assert '<strong>S2</strong> S3</a>' in out


def test_fix_try_strip(tmp_path, capsys):
    pb.fix_try_strip(tmp_path)
    put(tmp_path / "index.html", "<main>no strip</main>")
    put(tmp_path / "try" / "index.html", '<main id="main-content"><h1>Try</h1></main>')
    pb.fix_try_strip(tmp_path)
    assert "status-strip" not in (tmp_path / "try" / "index.html").read_text()
    put(tmp_path / "index.html", home_with_strip())
    pb.fix_try_strip(tmp_path)
    out = (tmp_path / "try" / "index.html").read_text()
    assert out.startswith('<main id="main-content"><section class="status-strip"')
    assert "mirrored onto /try/" in capsys.readouterr().out
    pb.fix_try_strip(tmp_path)
    assert (tmp_path / "try" / "index.html").read_text() == out


def test_load_i18n_tables(tmp_path, monkeypatch, capsys):
    scripts = tmp_path / "scripts"
    monkeypatch.setattr(pb, "__file__", str(scripts / "postbuild_fix.py"))
    assert pb.load_try_i18n("fr") is None
    put(scripts / "try_i18n" / "fr.json", '{"text": {"a": "b"}}')
    assert pb.load_try_i18n("fr") == {"text": {"a": "b"}}
    put(scripts / "pages_i18n" / "de.json", "{not json")
    assert pb.load_pages_i18n("de") is None
    assert "invalid JSON" in capsys.readouterr().err


def test_apply_chrome_extra_longest_first():
    html = '<a>Guide</a><a>Guide all</a><b aria-label="Open">x</b>'
    d = {"chrome": {"Guide": "G", "Guide all": "GA"}, "chrome_aria": {"Open": "Ouvrir"}}
    assert pb.apply_chrome_extra(html, d) == '<a>G</a><a>GA</a><b aria-label="Ouvrir">x</b>'
    assert pb.apply_chrome_extra(html, {}) == html


def test_lang_and_retag_helpers():
    assert pb.lang_badge('<b class="ap-lang-current">EN</b>', "pt-br") == '<b class="ap-lang-current">PT</b>'
    assert pb.retag_body_lang('<div lang="en"><a lang="en">', "fr") == '<div lang="fr"><a lang="en">'
    assert pb.retag_html_lang('<html class="no-js" lang="en-GB" data-x>', "fr") == '<html class="no-js" lang="fr" data-x>'
    assert pb.retag_html_lang('<html lang="en-GB">', "ar", rtl=True) == '<html lang="ar" dir="rtl">'


def test_retarget_lang_menus():
    menu = ('<a class="ap-lang-item" href="/" hreflang="en">'
            '<a class="ap-lang-item" href="/fr/" hreflang="fr">')
    assert pb.retarget_lang_menu_to_try(menu) == (
        '<a class="ap-lang-item" href="/try/" hreflang="en">'
        '<a class="ap-lang-item" href="/fr/try/" hreflang="fr">')
    assert pb.retarget_lang_menu_corpus(menu, "corpus-x") == (
        '<a class="ap-lang-item" href="/corpus-x/" hreflang="en">'
        '<a class="ap-lang-item" href="/fr/corpus-x/" hreflang="fr">')


def test_retarget_journey_nav_spares_the_english_menu_entry():
    html = '<a href="/why/">Why</a><a href="/glossary/">G</a><a href="/why/" hreflang="en">EN</a>'
    assert pb.retarget_journey_nav(html, "fr") == (
        '<a href="/fr/why/">Why</a><a href="/fr/glossary/">G</a><a href="/why/" hreflang="en">EN</a>')


def test_mark_english_submenu_tags_once():
    html = ('<ul id="sub-docs" class="ap-sub"><li><a href="/message-specs/">Specs</a></li>'
            '<li><a href="/languages/">L (EN)</a></li><li><a href="/fr/why/">W</a></li></ul>'
            '<p><a href="/message-specs/">Specs</a></p>')
    out = pb.mark_english_submenu(html)
    assert '<a href="/message-specs/" hreflang="en">Specs\u00a0(EN)</a>' in out
    assert '<a href="/languages/">L (EN)</a>' in out
    assert out.endswith('<p><a href="/message-specs/">Specs</a></p>')
    assert pb.mark_english_submenu(out) == out


def test_corpus_helpers():
    cluster = pb.corpus_hreflang_cluster("corpus-x", "en")
    assert cluster == '<link rel="alternate" hreflang="x-default" href="https://pain001.com/corpus-x/" />'
    assert pb.is_translated_corpus("de/corpus-de-x")
    assert not pb.is_translated_corpus("ja/corpus-x")
    assert not pb.is_translated_corpus("corpus-x")
    bare = '<head><link rel="canonical" href="/x/"></head>'
    assert pb.noindex_translated_corpus(bare) == '<head><meta name="robots" content="noindex, follow" /></head>'
    robots = '<head><meta name="robots" content="index" /></head>'
    assert pb.noindex_translated_corpus(robots) == '<head><meta name="robots" content="noindex, follow" /></head>'
    assert pb.iso_english_dates("<td>3 March 2026</td><p>3 March 2026 x</p>") == (
        "<td>2026-03-03</td><p>3 March 2026 x</p>")
