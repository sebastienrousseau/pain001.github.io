# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Content passes in postbuild_fix that run late in the main pass.

Pins the taxonomy link languages and topic index, named table regions,
bold paragraphs promoted to headings, dated content (expired ribbons and
the timeline's past and next items), page photo bands, tag page titles
and the deferred search script.
"""

import json

import postbuild_fix as pb


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8")


def tag_page(links, name="ISO", count="3"):
    items = "".join('<li><a href="%s">t</a></li>' % h for h in links)
    meta = '<p class="taxonomy-meta">%s pages</p>' % count if count else ""
    label = '<span class="tag-name">%s</span>' % name if name else ""
    return ('<html lang="en-GB"><body><h1>' + label + "</h1>" + meta
            + '<ul class="taxonomy-page-list">' + items + "</ul></body></html>")


def test_taxonomy_language_and_index(tmp_path, capsys):
    put(tmp_path / "ar" / "index.html", '<html lang="ar" dir="rtl">')
    put(tmp_path / "fr" / "index.html", '<html class="x" lang="fr">')
    put(tmp_path / "en" / "index.html", '<html lang="en-US">')
    put(tmp_path / "bare" / "index.html", "<html>")
    links = ["/ar/", "/fr/", "/en/", "/bare/", "/missing/", "/ar/"]
    put(tmp_path / "tags" / "a" / "index.html", tag_page(links))
    put(tmp_path / "tags" / "b" / "index.html", "<html><body>no list</body></html>")
    put(tmp_path / "tags" / "c" / "index.html", tag_page(["/fr/"], name=""))
    put(tmp_path / "tags" / "d" / "index.html", tag_page([], name="SEPA", count=""))
    put(tmp_path / "tags" / "index.html", "<article><p>Pick a topic</p></article>")
    pb.taxonomy_language_and_index(tmp_path)
    a = read(tmp_path / "tags" / "a" / "index.html")
    assert a.count('<a href="/ar/" lang="ar" dir="rtl">') == 2
    assert '<a href="/fr/" lang="fr">' in a
    for plain in ("/en/", "/bare/", "/missing/"):
        assert '<a href="%s">' % plain in a
    assert '<a href="/fr/" lang="fr">' in read(tmp_path / "tags" / "c" / "index.html")
    index = read(tmp_path / "tags" / "index.html")
    assert index == (
        '<article><p>Pick a topic</p><ul class="topic-list" aria-label="Topics">'
        '<li><a href="/tags/a/"><span>ISO</span><span class="topic-count">3 pages</span></a></li>'
        '<li><a href="/tags/d/"><span>SEPA</span><span class="topic-count"> pages</span></a></li>'
        "</ul></article>")
    assert "lang on 4 link(s), 2 topic(s) indexed" in capsys.readouterr().out
    pb.taxonomy_language_and_index(tmp_path)
    assert read(tmp_path / "tags" / "index.html") == index


def test_taxonomy_same_language_links_untagged(tmp_path, capsys):
    put(tmp_path / "fr" / "index.html", '<html lang="fr-FR">')
    put(tmp_path / "tags" / "x" / "index.html", tag_page(["/fr/"]).replace('lang="en-GB"', 'lang="fr"'))
    pb.taxonomy_language_and_index(tmp_path)
    assert '<a href="/fr/">' in read(tmp_path / "tags" / "x" / "index.html")
    assert "lang on 0 link(s), 1 topic(s) indexed" in capsys.readouterr().out
    assert not (tmp_path / "tags" / "index.html").exists()


REGION = '<div role="region" aria-label="Table, scrollable horizontally" tabindex="0">'


def test_name_table_regions(tmp_path, capsys):
    html = (REGION + "<table><th>A</th></table>"
            '<h2 id="x">Fees &amp; <em>limits</em> <a>#</a></h2>'
            + REGION + "<table><th>Col</th></table>"
            + REGION + "<table><th>Col</th></table>"
            + REGION + "<table><th> </th></table>"
            + "<h3>Next</h3>" + REGION + "<table></table>")
    put(tmp_path / "p.html", html)
    put(tmp_path / "q.html", "<p>no region</p>")
    pb.name_table_regions(tmp_path)
    labels = [chunk.split('"')[0] for chunk in read(tmp_path / "p.html").split('aria-label="')[1:]]
    assert labels == ["Table: A", "Fees &amp; limits: Col", "Fees &amp; limits: Col (2)",
                      "Fees &amp; limits", "Next"]
    assert "named table regions on 1 page(s)" in capsys.readouterr().out


def test_promote_bold_questions(tmp_path, capsys):
    long = "This sentence is long enough to be a paragraph that ends in a stop."
    main = ("<main><p><strong>First?</strong></p><h2>Costs</h2>"
            "<p><strong>What does it cost?</strong></p>\n<p> <b>Is it free?</b> </p>"
            "<p><strong>" + long + "</strong></p><p><strong> </strong></p>"
            "<h6>Deep</h6><p><strong>Deeper?</strong></p></main>")
    put(tmp_path / "a" / "index.html", "<body>" + main + "</body>")
    put(tmp_path / "b" / "index.html", "<body><strong>x</strong></body>")
    put(tmp_path / "c" / "index.html", "<main><p>no bold</p></main>")
    put(tmp_path / "d" / "index.html", "<main><p><strong> </strong></p></main>")
    put(tmp_path / "e" / "index.html", '<main><h2>A</h2><p>an intro paragraph long enough to separate</p>'
        '<h4 class="promoted"><strong>Q</strong></h4>'
        "<p><strong>R?</strong></p></main>")
    pb.promote_bold_questions(tmp_path)
    out = read(tmp_path / "a" / "index.html")
    assert '<h2 class="promoted"><strong>First?</strong></h2>' in out
    assert '<h3 class="promoted"><strong>What does it cost?</strong></h3>' in out
    assert '<h3 class="promoted"><b>Is it free?</b></h3>' in out
    assert "<p><strong>" + long + "</strong></p>" in out
    assert '<h6 class="promoted"><strong>Deeper?</strong></h6>' in out
    assert read(tmp_path / "d" / "index.html") == "<main><p><strong> </strong></p></main>"
    assert '<h3 class="promoted"><strong>R?</strong></h3>' in read(tmp_path / "e" / "index.html")
    assert "promoted 5 bold paragraph(s)" in capsys.readouterr().out


TIMELINE = (
    '<div class="ribbon" data-expires="2000-01-01">old</div>'
    '<div class="ribbon" data-expires="2999-01-01">new</div><ol data-timeline>'
    '<li class="milestone"><time datetime="2001-01-01">a</time><span class="milestone-flag">Next</span></li>'
    '<li class="milestone is-next"><span class="milestone-flag" hidden>Next</span></li>'
    '<li class="milestone"><time datetime="2999-02-02">c</time><span class="milestone-flag">Next</span></li>'
    "</ol>"
)


def test_mark_dated_content(tmp_path, capsys):
    put(tmp_path / "t" / "index.html", TIMELINE)
    put(tmp_path / "x" / "index.html", "<p>static</p>")
    pb.mark_dated_content(tmp_path)
    out = read(tmp_path / "t" / "index.html")
    assert "old" not in out and ">new</div>" in out
    items = out.split("<li ")[1:]
    assert items[0].startswith('class="milestone is-past">') and 'flag" hidden>' in items[0]
    assert items[1].startswith('class="milestone is-next">') and '<span class="milestone-flag">Next' in items[1]
    assert items[2].startswith('class="milestone">') and 'flag" hidden>' in items[2]
    assert read(tmp_path / "x" / "index.html") == "<p>static</p>"
    assert "dated content marked for" in capsys.readouterr().out


def test_page_key():
    assert pb.page_key("fr/why/index.html") == "why"
    assert pb.page_key("index.html") == ""
    assert pb.page_key("tags/iso/index.html") == "tags/iso"


def test_add_page_photos(tmp_path, monkeypatch, capsys):
    photo_map = tmp_path / "page_photos.json"
    photo_map.write_text(json.dumps({"pages": {"why": "stem-a", "": "stem-home"}}), encoding="utf-8")
    monkeypatch.setattr(pb, "PAGE_PHOTO_MAP", photo_map)
    monkeypatch.setattr(pb, "band_path", lambda stem: "/img/band/" + stem)
    site = tmp_path / "site"
    hero = '<html><head><title>x</title></head><body><section class="page-hero"><h1>x</h1></section></body></html>'
    put(site / "why" / "index.html", hero)
    put(site / "fr" / "why" / "index.html", hero)
    put(site / "index.html", '<head></head><article class="taxonomy-page">')
    put(site / "tags" / "iso" / "index.html", '<head></head><article class="taxonomy-page">')
    put(site / "done" / "index.html", '<img class="page-photo">' + hero)
    put(site / "plain" / "index.html", "<head></head><p>none</p>")
    pb.add_page_photos(site)
    why = read(site / "why" / "index.html")
    assert why.startswith('<html><head>\n<link rel="preload" as="image" type="image/avif" '
                          'href="/img/band/stem-a-960.avif" imagesrcset="/img/band/stem-a-640.avif 640w, ')
    assert ('<picture class="page-photo-frame"><source type="image/avif" srcset="/img/band/stem-a-640.avif 640w'
            in why)
    assert 'src="/img/band/stem-a-960.webp"' in why and why.count("1600w") == 3
    assert why.index("<picture") < why.index('<section class="page-hero">')
    assert read(site / "fr" / "why" / "index.html") == why
    assert '<picture class="page-photo-frame">' in read(site / "index.html")
    assert "page-photo-frame" not in read(site / "tags" / "iso" / "index.html")
    out = capsys.readouterr().out
    assert "page photo on 3 page(s)" in out
    assert "WARNING no photo mapped for: ['tags/iso']" in out


def test_add_page_photos_all_mapped(tmp_path, monkeypatch, capsys):
    photo_map = tmp_path / "page_photos.json"
    photo_map.write_text('{"pages": {}}', encoding="utf-8")
    monkeypatch.setattr(pb, "PAGE_PHOTO_MAP", photo_map)
    (tmp_path / "site").mkdir()
    pb.add_page_photos(tmp_path / "site")
    assert "WARNING" not in capsys.readouterr().out


def test_retitle_tag_pages(tmp_path, capsys):
    title = "Tag: ISO 20022 \u2014 Pain001: ISO 20022 Payment Initiation Suite"
    put(tmp_path / "tags" / "iso" / "index.html", "<title>%s</title>" % title)
    put(tmp_path / "tags" / "x" / "index.html", "<title>Other</title>")
    pb.retitle_tag_pages(tmp_path)
    assert read(tmp_path / "tags" / "iso" / "index.html") == "<title>Pages tagged ISO 20022 on Pain001</title>"
    put(tmp_path / "search-index.json", '[{"title": "%s"}]' % title)
    pb.retitle_tag_pages(tmp_path)
    assert read(tmp_path / "search-index.json") == '[{"title": "Pages tagged ISO 20022 on Pain001"}]'
    out = capsys.readouterr().out
    assert "tag titles rewritten in 1 file(s)" in out


def test_defer_ssg_search(tmp_path, capsys):
    put(tmp_path / "a.html", '<script src="/_csp/abc123.js"></script>')
    put(tmp_path / "b.html", '<script src="/_csp/abc123.js" defer></script>')
    pb.defer_ssg_search(tmp_path)
    assert read(tmp_path / "a.html") == '<script defer src="/_csp/abc123.js"></script>'
    assert read(tmp_path / "b.html") == '<script src="/_csp/abc123.js" defer></script>'
    assert "search script deferred on 1 page(s)" in capsys.readouterr().out


def test_promote_bold_questions_reads_only_the_opening_tag(tmp_path):
    """Regression: a short authored heading directly before a promoted one
    was skipped as if it were promoted, because the check looked 40
    characters past the heading's start and saw the next heading's class.
    The new heading then landed a level too high (h2 instead of h3)."""
    page = tmp_path / "index.html"
    page.write_text('<main><h2>A</h2><h4 class="promoted"><strong>Q?</strong></h4>'
                    "<p><strong>Next?</strong></p></main>", encoding="utf-8")
    pb.promote_bold_questions(tmp_path)
    assert '<h3 class="promoted"><strong>Next?</strong></h3>' in page.read_text(encoding="utf-8")
