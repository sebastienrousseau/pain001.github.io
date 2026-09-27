# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests: translated corpus pages stay out of the index.

Search Console listed the translated corpus scenario pages
(/<locale>/corpus-*/) as "Discovered" or "Crawled", "currently not
indexed". They stay published for visitors, but carry noindex, leave the
sitemap and leave every hreflang cluster, while the English scenario pages
stay indexable.
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
    assert '<link rel="canonical" href="https://pain001.com/de/corpus-x/">' in html


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
