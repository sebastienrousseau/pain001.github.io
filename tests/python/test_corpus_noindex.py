# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests: translated corpus pages stay out of the index.

Search Console listed the translated corpus scenario pages
(/<locale>/corpus-*/) as "Discovered" or "Crawled", "currently not
indexed". They stay published for visitors, but carry noindex, leave the
sitemap, every hreflang cluster and their own canonical link, while the
English scenario pages stay indexable.
"""

import postbuild_fix as pb

HEAD = (
    '<html><head><meta name="robots" content="max-snippet:-1, max-image-preview:large">'
    '<link rel="alternate" href="https://pain001.com/de/corpus-x/" hreflang="de" />'
    '<link rel="alternate" hreflang="en" href="https://pain001.com/corpus-x/" />'
    '<link rel="canonical" href="https://pain001.com/de/corpus-x/">'
    "</head><body></body></html>"
)


def test_translated_page_gets_a_single_noindex():
    html = pb.noindex_translated_corpus(HEAD)
    assert html.count('name="robots"') == 1
    assert '<meta name="robots" content="noindex, follow" />' in html


def test_translated_page_loses_its_hreflang_links():
    html = pb.noindex_translated_corpus(HEAD)
    assert "hreflang=" not in html


def test_translated_page_loses_its_self_canonical():
    # Search Console: a page that is noindex yet names itself canonical
    # sends contradictory signals. The noindex page carries no canonical.
    html = pb.noindex_translated_corpus(HEAD)
    assert 'rel="canonical"' not in html


def test_noindex_is_added_when_no_robots_meta_exists():
    html = pb.noindex_translated_corpus("<head></head>")
    assert html == '<head><meta name="robots" content="noindex, follow" /></head>'


def test_english_cluster_lists_no_translations():
    cluster = pb.corpus_hreflang_cluster("corpus-x", "en")
    assert 'hreflang="x-default"' in cluster
    for loc in pb.CORPUS_LOCALES:
        assert "/%s/corpus-x/" % loc not in cluster


def test_sitemap_skips_translated_corpus_pages(tmp_path):
    site = tmp_path / "site"
    for rel in ("", "corpus-x", "de/corpus-x", "fr/corpus-x", "de/why", "try"):
        d = site / rel
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text("<html></html>", encoding="utf-8")
    pb.regen_sitemap(site)
    sitemap = (site / "sitemap.xml").read_text(encoding="utf-8")
    assert "https://pain001.com/corpus-x/" in sitemap
    assert "https://pain001.com/de/why/" in sitemap
    assert "/de/corpus-x/" not in sitemap
    assert "/fr/corpus-x/" not in sitemap


def test_utility_pages_lose_their_self_canonical(tmp_path):
    # /offline/ and /thanks/ were noindex yet canonical to themselves.
    for rel in pb.NOINDEX_PAGES:
        d = tmp_path / rel
        d.mkdir()
        (d / "index.html").write_text(
            '<head><link rel="canonical" href="https://pain001.com/%s/" /></head>' % rel,
            encoding="utf-8")
    pb.mark_noindex_pages(tmp_path)
    for rel in pb.NOINDEX_PAGES:
        html = (tmp_path / rel / "index.html").read_text(encoding="utf-8")
        assert 'name="robots" content="noindex"' in html
        assert 'rel="canonical"' not in html
