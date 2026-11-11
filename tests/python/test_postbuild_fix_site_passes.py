# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Whole-site head and asset passes in postbuild_fix.

Pins the passes that walk the built tree and repair metadata or assets:
social descriptions, the service worker cache version, version
requirement notes, double-encoded head entities, taxonomy page heads,
the web manifest, stylesheet bundling, minimum social cards and the
noindex utility pages. Each pass must leave a page it has nothing to fix
untouched on disk.
"""

import hashlib
import json

import postbuild_fix as pb


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8")


def test_fix_social_descriptions(tmp_path, capsys):
    put(tmp_path / "a" / "index.html",
        '<head><meta name="description" content=" Authored "><meta property="og:description" content="synth">'
        '<meta content="synth" name="twitter:description"></head>')
    put(tmp_path / "b" / "index.html", '<head><meta name="description" content=""></head>')
    put(tmp_path / "c" / "index.html", "<head></head>")
    put(tmp_path / "d" / "index.html", '<head><meta name="description" content="x"></head>')
    pb.fix_social_descriptions(tmp_path)
    assert read(tmp_path / "a" / "index.html") == (
        '<head><meta name="description" content=" Authored "><meta property="og:description" content="Authored">'
        '<meta content="Authored" name="twitter:description"></head>')
    assert "aligned on 1 page(s)" in capsys.readouterr().out


SW = 'const CACHE = "pain001-try-old";\nself.x = 1;\n'


def test_stamp_sw_cache_version_skips_a_missing_or_unmarked_worker(tmp_path, capsys):
    assert pb.stamp_sw_cache_version(tmp_path) is None
    put(tmp_path / "sw.js", "no constant here")
    assert pb.stamp_sw_cache_version(tmp_path) is None
    assert "CACHE constant not found" in capsys.readouterr().out


def expected_cache_version():
    """The hash of the /try/ assets the fixture writes, in stamping order."""
    h = hashlib.sha256()
    for part in (b"fr", b"js", b"s", b"w.whl", b"5"):
        h.update(part)
    return h.hexdigest()[:12]


def test_stamp_sw_cache_version(tmp_path, capsys):
    put(tmp_path / "sw.js", SW)
    put(tmp_path / "fr" / "try" / "index.html", "fr")
    put(tmp_path / "js" / "try-page.js", "js")
    put(tmp_path / "js" / "other.js", "ignored")
    put(tmp_path / "samples" / "a.xml", "s")
    put(tmp_path / "pyodide" / "w.whl", "wheel")
    first = pb.stamp_sw_cache_version(tmp_path)
    assert first == expected_cache_version()
    assert read(tmp_path / "sw.js") == SW.replace("old", first)
    put(tmp_path / "try" / "index.html", "en")
    second = pb.stamp_sw_cache_version(tmp_path)
    assert second != first and second in read(tmp_path / "sw.js")
    mtime = (tmp_path / "sw.js").stat().st_mtime_ns
    assert pb.stamp_sw_cache_version(tmp_path) == second
    assert (tmp_path / "sw.js").stat().st_mtime_ns == mtime
    assert "cache version pain001-try-" in capsys.readouterr().out


def test_add_version_requirements(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    site = tmp_path / "site"
    pb.add_version_requirements(site)
    assert capsys.readouterr().out == ""
    posts = tmp_path / "_posts"
    put(posts / "a.md", 'id: "https://pain001.com/"\nmin_pain001: "0.0.90"\n')
    put(posts / "b.md", 'id: "https://pain001.com/docs/"\nmin_pain001: 0.0.91\n')
    put(posts / "c.md", 'id: "https://pain001.com/missing/"\nmin_pain001: "1"\n')
    put(posts / "d.md", 'id: "https://pain001.com/done/"\nmin_pain001: "1"\n')
    put(posts / "e.md", 'id: "https://pain001.com/plain/"\nmin_pain001: "1"\n')
    put(posts / "f.md", 'id: "https://pain001.com/plain/"\n')
    put(site / "index.html", '<article class="content-body"><p>x</p></article>')
    put(site / "docs" / "index.html", "<article class=content-body><p>y</p></article>")
    put(site / "done" / "index.html", '<p class="version-requirement"></p>')
    put(site / "plain" / "index.html", "<article><p>z</p></article>")
    pb.add_version_requirements(site)
    home = read(site / "index.html")
    assert home.startswith('<article class="content-body"><p class="version-requirement">'
                           "<strong>Requires Pain001 v0.0.90 or later.</strong>")
    assert "v0.0.91 or later" in read(site / "docs" / "index.html")
    assert read(site / "plain" / "index.html") == "<article><p>z</p></article>"
    assert "version-requirement note on 2 page(s)" in capsys.readouterr().out


def test_fix_double_encoded_meta(tmp_path, capsys):
    put(tmp_path / "a.html", '<head><meta property="og:title" content="A &amp;amp; B &amp;#39;"></head>'
        "<body>&amp;amp;</body>")
    put(tmp_path / "b.html", "<p>no head &amp;amp;</p>")
    put(tmp_path / "c.html", "<head>&amp;</head>")
    pb.fix_double_encoded_meta(tmp_path)
    assert read(tmp_path / "a.html") == ('<head><meta property="og:title" content="A &amp; B &#39;"></head>'
                                         "<body>&amp;amp;</body>")
    assert read(tmp_path / "b.html") == "<p>no head &amp;amp;</p>"
    assert "on 1 page(s)" in capsys.readouterr().out


def test_fix_tag_pages(tmp_path, capsys):
    put(tmp_path / "tags" / "a" / "index.html", "<head></head><body></body>")
    full = ('<head>Content-Security-Policy property="og:image" css/taxonomy.css name="viewport" rel="icon"'
            "</head><body>pain001-analytics.js</body>")
    put(tmp_path / "tags" / "b" / "index.html", full)
    put(tmp_path / "tags" / "c" / "index.html", "<head></head>")
    pb.fix_tag_pages(tmp_path)
    a = read(tmp_path / "tags" / "a" / "index.html")
    assert a == ("<head>" + pb.CSP_META + pb.OG_IMAGE_META + pb.TAXONOMY_CSS + pb.TAXONOMY_VIEWPORT
                 + pb.TAXONOMY_ICONS + "</head><body>" + pb.BEACON_TAG + "</body>")
    assert read(tmp_path / "tags" / "b" / "index.html") == full
    assert "pain001-analytics" not in read(tmp_path / "tags" / "c" / "index.html")
    assert "patched tag page" in capsys.readouterr().out


def test_fix_manifest(tmp_path, capsys):
    pb.fix_manifest(tmp_path)
    assert not (tmp_path / "manifest.json").exists()
    put(tmp_path / "manifest.json", json.dumps({
        "theme_color": None,
        "icons": [{"src": "https://pain001.com/img/a.png"}, {"src": "/img/b.png"}, "bad"],
    }))
    pb.fix_manifest(tmp_path)
    data = json.loads(read(tmp_path / "manifest.json"))
    assert data["theme_color"] == "#0b0e14" and data["background_color"] == "#ffffff"
    assert data["icons"] == [{"src": "/img/a.png"}, {"src": "/img/b.png"}, "bad"]
    put(tmp_path / "manifest.json", json.dumps({"theme_color": "red", "background_color": "#000"}))
    pb.fix_manifest(tmp_path)
    assert json.loads(read(tmp_path / "manifest.json")) == {"theme_color": "#0b0e14", "background_color": "#000"}
    put(tmp_path / "manifest.json", json.dumps({"theme_color": "#123456"}))
    pb.fix_manifest(tmp_path)
    assert json.loads(read(tmp_path / "manifest.json"))["theme_color"] == "#123456"
    assert "theme_color fixed" in capsys.readouterr().out


def link(href):
    return '<link rel="stylesheet" href="%s" />' % href


def test_bundle_stylesheets(tmp_path, capsys):
    put(tmp_path / "a.css", "a { color: red; }\n")
    put(tmp_path / "highlight.abc123.css", "b { color: blue; }\n")
    page = "<head>" + link("/a.css") + '<link rel="canonical" href="/x/">' + link("/highlight.css") + "</head>"
    put(tmp_path / "p1.html", page)
    put(tmp_path / "sub" / "p2.html", page)
    put(tmp_path / "ext.html", link("https://cdn.example/x.css"))
    put(tmp_path / "missing.html", link("/nope.css"))
    put(tmp_path / "none.html", "<head></head>")
    pb.bundle_stylesheets(tmp_path)
    bundles = list((tmp_path / "css").glob("site-*.css"))
    assert len(bundles) == 1
    payload = bundles[0].read_text()
    assert "red" in payload and "blue" in payload
    out = read(tmp_path / "p1.html")
    assert out.count('rel="stylesheet"') == 1
    assert out.startswith('<head><link rel="stylesheet" href="/css/%s" integrity="sha384-' % bundles[0].name)
    assert '<link rel="canonical" href="/x/"></head>' in out
    assert read(tmp_path / "sub" / "p2.html") == out
    assert read(tmp_path / "ext.html") == link("https://cdn.example/x.css")
    assert read(tmp_path / "missing.html") == link("/nope.css")
    assert "1 CSS bundle(s) linked from 2 page(s)" in capsys.readouterr().out


def test_bundle_stylesheets_ambiguous_highlight_is_left_alone(tmp_path):
    put(tmp_path / "highlight.a.css", "a{}")
    put(tmp_path / "highlight.b.css", "b{}")
    put(tmp_path / "p.html", link("/highlight.css"))
    pb.bundle_stylesheets(tmp_path)
    assert read(tmp_path / "p.html") == link("/highlight.css")


def test_ensure_social_metadata(tmp_path, capsys):
    put(tmp_path / "a.html", "<head><title> A &amp; <b>B</b> \"q\" </title></head>")
    put(tmp_path / "b.html", "<head></head>")
    put(tmp_path / "c.html", "<title>x</title>")
    done = ("<head><title>d</title><meta property='og:title' content='d'>"
            '<meta property="og:type" content="article"><meta name="twitter:card" content="x"></head>')
    put(tmp_path / "d.html", done)
    pb.ensure_social_metadata(tmp_path)
    assert read(tmp_path / "a.html") == (
        '<head><title> A &amp; <b>B</b> "q" </title><meta property="og:title" content="A &amp; B &quot;q&quot;" />'
        '<meta property="og:type" content="website" /><meta name="twitter:card" content="summary_large_image" />'
        "</head>")
    assert read(tmp_path / "d.html") == done
    assert "social card metadata on 1 page(s)" in capsys.readouterr().out


def test_mark_noindex_pages(tmp_path, capsys):
    put(tmp_path / "404" / "index.html", '<head><link rel="canonical" href="/404/">\n</head>')
    put(tmp_path / "offline" / "index.html", "<head>" + pb._ROBOTS_NOINDEX + "</head>")
    pb.mark_noindex_pages(tmp_path)
    expected = "<head>" + pb._ROBOTS_NOINDEX + "</head>"
    assert read(tmp_path / "404" / "index.html") == expected
    assert read(tmp_path / "404.html") == expected
    assert read(tmp_path / "offline" / "index.html") == expected
    assert not (tmp_path / "thanks").exists()
    assert "noindex on 1 utility page(s)" in capsys.readouterr().out
