# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Locale page generators in postbuild_fix.

Pins how /<slug>/try/, the journey and docs pages, the locale home pages
and the corpus scenario variants are produced from the English build:
lang and dir, self-canonical URLs, reciprocal hreflang clusters,
translated copy (all four key-matching strategies), chrome, and the
locales skipped for lack of a table or of chrome strings. The
translation tables and locale_strings are small fixtures, so the real
tables can change without breaking these tests.
"""

import builtins
import json
import sys
import types

import pytest

import postbuild_fix as pb

TOKENS = ["T%d" % i for i in range(26)]
STRIP = ["S%d" % i for i in range(8)]


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if isinstance(text, str) else json.dumps(text), encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8")


def missing(text, wanted):
    """The wanted fragments that text does not contain, in order."""
    return [want for want in wanted if want not in text]


@pytest.fixture
def env(tmp_path, monkeypatch):
    scripts = tmp_path / "scripts"
    monkeypatch.setattr(pb, "__file__", str(scripts / "postbuild_fix.py"))
    fake = types.ModuleType("locale_strings")
    fake.STRINGS = {"fr": TOKENS, "ar": TOKENS, "de": TOKENS, "es": TOKENS}
    fake.STATUS_STRIP = {"fr": STRIP, "ar": STRIP}
    monkeypatch.setitem(sys.modules, "locale_strings", fake)
    return tmp_path / "site", scripts


@pytest.fixture
def flaky_import(monkeypatch):
    """The first import of locale_strings fails, as it does when scripts/
    is not on sys.path; the function must add it and retry."""
    real = builtins.__import__
    state = {"failed": 0}

    def fake(name, *args, **kwargs):
        if name == "locale_strings" and not state["failed"]:
            state["failed"] += 1
            raise ImportError(name)
        return real(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake)
    monkeypatch.setattr(sys, "path", list(sys.path))
    return state


PAGE = (
    '<html lang="en-GB"><head><title>Try Pain001</title>'
    '<meta name="description" content="Run it">'
    '<link rel="canonical" href="https://pain001.com/try/"></head><body>'
    '<script type="application/ld+json">{"inLanguage": "en-GB"}</script>'
    '<div lang="en"><h1>Try it now</h1><p>It\'s fast</p><p>Tom & Jerry</p>'
    '<button aria-label="Run">x</button><a href="/try/">Try</a><a href="/why/">Why</a>'
    '<b class="ap-lang-current">EN</b>'
    '<a class="ap-lang-item" href="/" hreflang="en">English</a>'
    '<span>Guide</span><a href="/executive-brief-fr/">Brief</a></div></body></html>'
)
TEXT = {
    "Try it now": "Essayez",
    "It&#x27;s fast": "C&#x27;est rapide",
    "Tom &amp; Jerry": "Tom &amp; Jerome",
    "A key that is at least thirty characters long": "absent",
    "short": "absent",
}


FR_TRY = ('<html lang="fr">', '"inLanguage": "fr"', "<title>Essayer Pain001</title>",
          'content="Run it"', 'href="https://pain001.com/fr/try/"', ">Essayez<",
          "C'est rapide", "Tom & Jerome", 'aria-label="Lancer"', ">Guide FR<",
          'href="/fr/try/">Try', 'href="/fr/why/"', 'class="ap-lang-current">FR<',
          '<div lang="fr">', 'href="/try/" hreflang="en"',
          '<script id="try-i18n" type="application/json">{"run": "\\u003cb>"}</script>')


def build_try(env):
    """Write the English /try/ page and its tables, then generate the locales."""
    site, scripts = env
    put(site / "try" / "index.html", PAGE)
    put(scripts / "try_i18n" / "en.json", {"meta": {"title": "Try Pain001", "description": "Run it"}})
    put(scripts / "try_i18n" / "fr.json", {"meta": {"title": "Essayer Pain001"}, "text": TEXT,
                                           "aria": {"Run": "Lancer"}, "chrome": {"Guide": "Guide FR"}})
    put(scripts / "try_i18n" / "ar.json", {"text": {}})
    put(scripts / "try_i18n" / "it.json", {"text": {}})
    put(scripts / "runtime_i18n" / "fr.json", {"run": "<b>"})
    pb.gen_try_locales(site)
    return site


def test_gen_try_locales(env, capsys):
    site = build_try(env)
    assert "generated 2 locale /try/ page(s)" in capsys.readouterr().out
    en = read(site / "try" / "index.html")
    assert 'hreflang="x-default" href="https://pain001.com/try/"' in en
    assert 'class="ap-lang-item" href="/try/" hreflang="en"' in en
    pb.gen_try_locales(site)
    assert read(site / "try" / "index.html").count('hreflang="x-default"') == 1


def test_gen_try_locales_translates_the_french_page(env):
    fr = read(build_try(env) / "fr" / "try" / "index.html")
    assert missing(fr, FR_TRY) == []
    assert 'hreflang="fr"' not in fr


def test_gen_try_locales_sets_rtl_and_skips_locales_without_a_table(env):
    site = build_try(env)
    assert '<html lang="ar" dir="rtl">' in read(site / "ar" / "try" / "index.html")
    assert "try-i18n" not in read(site / "ar" / "try" / "index.html")
    assert not (site / "it").exists() and not (site / "es").exists()


def test_gen_try_locales_without_source_or_english_table(env, flaky_import, capsys):
    site, scripts = env
    pb.gen_try_locales(site)
    assert flaky_import["failed"] == 1
    assert sys.path[0] == str(scripts)
    assert capsys.readouterr().out == ""
    put(site / "try" / "index.html", PAGE)
    put(scripts / "try_i18n" / "fr.json", {"meta": {"title": "Essayer"}})
    pb.gen_try_locales(site)
    assert "<title>Try Pain001</title>" in read(site / "fr" / "try" / "index.html")


FR_WHY = ("<title>Pourquoi</title>", 'content="Run it"', 'href="https://pain001.com/fr/why/"',
          ">Essayez<", "C'est rapide", "Tom & Jerome", 'aria-label="Lancer"', ">Guide FR<",
          'href="/fr/why/">Why', 'href="/fr/executive-brief/"', '<div lang="fr">',
          'class="ap-lang-current">FR<', '<html lang="fr">')


def build_journey(env):
    """Write the English /why/ and /documentation/ pages and tables, then generate."""
    site, scripts = env
    why = PAGE.replace("/try/", "/why/").replace("Try Pain001", "Why Pain001")
    put(site / "why" / "index.html", why)
    put(scripts / "pages_i18n" / "en.json", {"why": {"meta": {"title": "Why Pain001", "eyebrow": None,
                                                              "description": "Run it"}}})
    put(scripts / "pages_i18n" / "fr.json", {"why": {"meta": {"title": "Pourquoi"}, "text": TEXT,
                                                     "aria": {"Run": "Lancer"}}})
    put(scripts / "pages_i18n" / "ar.json", {"solutions": {}})
    put(scripts / "pages_i18n" / "it.json", {"why": {}})
    put(scripts / "pages_i18n" / "de.json", {"why": {}})
    put(scripts / "try_i18n" / "fr.json", {"chrome": {"Guide": "Guide FR"}})
    docs = PAGE.replace("/try/", "/documentation/") + (
        '<link hreflang="x-default" href="https://pain001.com/documentation/">')
    put(site / "documentation" / "index.html", docs)
    put(scripts / "docs_i18n" / "fr.json", {"documentation": {}})
    pb.gen_journey_locales(site)
    return site


def test_gen_journey_locales(env, capsys):
    site = build_journey(env)
    out = capsys.readouterr().out
    assert "generated 2 locale /why/ page(s)" in out
    assert "generated 1 locale /documentation/ page(s)" in out
    assert 'href="https://pain001.com/why/" />' in read(site / "why" / "index.html")
    assert 'class="ap-lang-item" href="/why/" hreflang="en"' in read(site / "why" / "index.html")
    assert read(site / "documentation" / "index.html").count("x-default") == 1
    assert (site / "fr" / "documentation" / "index.html").is_file()


def test_gen_journey_locales_translates_the_french_page(env):
    assert missing(read(build_journey(env) / "fr" / "why" / "index.html"), FR_WHY) == []


def test_gen_journey_locales_falls_back_and_skips_locales_without_a_page(env):
    site = build_journey(env)
    de = read(site / "de" / "why" / "index.html")
    assert "<title>Why Pain001</title>" in de and ">Guide<" in de
    assert not (site / "ar" / "why").exists() and not (site / "it" / "why").exists()


def test_gen_localized_pages_import_fallback(env, flaky_import):
    site, _ = env
    pb._gen_localized_pages(site, ("why",), "pages_i18n")
    assert flaky_import["failed"] == 1
    assert not site.exists()


def home_with_strip():
    rows = (("Next CBPR+ milestone:", "14 Nov 2026"), ("Relay version:", "09"),
            ("Latest release:", "0.0.85"), ("Message definitions:", "2019"),
            ("Reviewed:", "1 Nov 2026"))
    items = "".join('<a href="#"><strong>%s</strong> %s</a>' % r for r in rows)
    return "<head></head><body>" + items + "</body>"


LOCALE_HOME = (
    '<html lang="fr"><head></head><body><main id="main-content"></main>'
    '<div lang="en"></div><a href="/try/">T</a><a href="/why/">W</a>'
    '<b class="ap-lang-current">EN</b><span>Guide</span><a>Docs</a></body></html>'
)


def test_localise_pages(env, capsys):
    site, scripts = env
    put(site / "index.html", home_with_strip())
    put(site / "fr" / "index.html", LOCALE_HOME)
    put(site / "ar" / "index.html", LOCALE_HOME.replace("<head>", '<head><link hreflang="x-default">')
        .replace("<main", '<section class="status-strip"></section><main').replace('lang="fr"', 'lang="ar"'))
    put(site / "ja" / "index.html", LOCALE_HOME.replace('lang="fr"', 'lang="ja"'))
    put(scripts / "try_i18n" / "fr.json", {"chrome": {"Guide": "Guide FR"}})
    put(scripts / "pages_i18n" / "fr.json", {"why": {}})
    pb.localise_pages(site)
    assert "hreflang cluster on 3 locale page(s) + home; RTL dir on 3" in capsys.readouterr().out
    fr = read(site / "fr" / "index.html")
    assert missing(fr, ('hreflang="x-default"', '<main id="main-content"><section class="status-strip" aria-label="S0">',
                        "<strong>S1</strong> 2026-11-14", ">Guide FR<", 'class="ap-lang-current">FR<',
                        '<div lang="fr">', 'href="/fr/try/"', 'href="/fr/why/"', ">T8</a>")) == []
    ar = read(site / "ar" / "index.html")
    assert ar.count("x-default") == 1 and ar.count("status-strip") == 1
    assert '<html lang="ar" dir="rtl">' in ar and 'href="/try/"' in ar and ">T8</a>" in ar
    ja = read(site / "ja" / "index.html")
    assert ">Docs</a>" in ja and "status-strip" not in ja and 'hreflang="x-default"' in ja
    home = read(site / "index.html")
    assert 'hreflang="x-default" href="https://pain001.com/"' in home
    pb.localise_pages(site)
    assert read(site / "index.html") == home


def test_localise_pages_without_home(env, flaky_import, capsys):
    site, _ = env
    put(site / "fr" / "index.html", LOCALE_HOME)
    pb.localise_pages(site)
    assert flaky_import["failed"] == 1
    assert "status-strip" not in read(site / "fr" / "index.html")
    assert not (site / "index.html").exists()
    assert "hreflang cluster on 1 locale page(s)" in capsys.readouterr().out


CORPUS = (
    '<html lang="en-GB"><head><link rel="canonical" href="https://pain001.com/{p}/"></head><body>'
    '<a class="ap-lang-item" href="/" hreflang="en">EN</a>'
    '<a class="ap-lang-item" href="/fr/" hreflang="fr">FR</a>'
    '<time>3 March 2026</time><span>Guide</span><a href="/why/">W</a><a href="/try/">T</a>'
    '<div lang="en"></div><b class="ap-lang-current">EN</b></body></html>'
)


FR_CORPUS = ('<meta name="robots" content="noindex, follow" />', ">2026-03-03<", ">Guide FR<",
             'href="/fr/why/"', 'href="/fr/try/"', '<div lang="fr">', 'class="ap-lang-current">FR<')


def build_corpus(env):
    """Write English and locale corpus pages plus files to rewrite, then relocate."""
    site, scripts = env
    put(site / "corpus-x" / "index.html", CORPUS.format(p="corpus-x"))
    put(site / "corpus-y" / "index.html", CORPUS.format(p="corpus-y").replace("<head>", "<head>x-default"))
    (site / "corpus-z").mkdir()
    (site / "fr").mkdir()
    put(site / "fr-corpus-x" / "index.html", CORPUS.format(p="fr-corpus-x"))
    put(site / "de-corpus-x" / "index.html", CORPUS.format(p="de-corpus-x"))
    put(site / "de" / "corpus-x" / "stale.html", "old")
    put(site / "feed.xml", "<link>https://pain001.com/de-corpus-x/</link>")
    put(site / "notes.txt", "nothing to rewrite")
    put(site / "img.png", "/fr-corpus-x/")
    (site / "folder.json").mkdir()
    put(scripts / "try_i18n" / "fr.json", {"chrome": {"Guide": "Guide FR"}})
    pb.relocate_corpus_locales(site)
    return site


def test_relocate_corpus_locales(env, capsys):
    site = build_corpus(env)
    assert ("2 corpus page(s) clustered; 2 locale variant(s) moved under /<locale>/; "
            "stale paths rewritten in 1 file(s)") in capsys.readouterr().out
    en = read(site / "corpus-x" / "index.html")
    assert '<link rel="alternate" hreflang="x-default" href="https://pain001.com/corpus-x/" />' in en
    assert 'href="/corpus-x/" hreflang="en"' in en and 'href="/fr/corpus-x/" hreflang="fr"' in en
    assert "hreflang=\"x-default\"" not in read(site / "corpus-y" / "index.html")
    assert not (site / "fr-corpus-x").exists() and not (site / "de" / "corpus-x" / "stale.html").exists()


def test_relocate_corpus_locales_translates_the_moved_pages(env):
    site = build_corpus(env)
    fr = read(site / "fr" / "corpus-x" / "index.html")
    assert missing(fr, FR_CORPUS) == []
    assert 'rel="canonical"' not in fr
    assert ">Guide<" in read(site / "de" / "corpus-x" / "index.html")


def test_relocate_corpus_locales_rewrites_stale_paths_in_text_files_only(env):
    site = build_corpus(env)
    assert read(site / "feed.xml") == "<link>https://pain001.com/de/corpus-x/</link>"
    assert read(site / "img.png") == "/fr-corpus-x/"


def test_relocate_corpus_locales_import_fallback(env, flaky_import, capsys):
    site, _ = env
    site.mkdir()
    pb.relocate_corpus_locales(site)
    assert flaky_import["failed"] == 1
    assert "0 corpus page(s) clustered" in capsys.readouterr().out
