# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Site shell, routes and cleanup passes in postbuild_fix.

Pins the stray per-page file cleanup and the /404/ copy, nested route
relocation, the claims register fill, the redirect map stamp and the
legacy redirect stubs, and the PRISM shell normalisation (one CSP, one
header and footer, the inlined theme script, the footer credit) across
authored, taxonomy and redirect pages.
"""

import json
import sys
import types

import pytest

import postbuild_fix as pb


def put(path, text=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8")


def test_remove_stray_per_page_files(tmp_path, capsys):
    for name in pb.STRAY_PER_PAGE_FILES:
        put(tmp_path / name, "root")
        put(tmp_path / "why" / name, "stray")
    put(tmp_path / "404" / "index.html", "x")
    put(tmp_path / "404.html", '<link rel="canonical" href="https://pain001.com/404/" />\n'
        '<meta property="og:url" content="https://pain001.com/404/">')
    put(tmp_path / "tags" / "a" / "index.html",
        '<ul><li><a href="/404/">Not found</a></li>\n<li><a href="/uk/" lang="uk">UA</a></li>'
        '<li><a href="/fr/">FR</a></li></ul>')
    put(tmp_path / "tags" / "b" / "index.html", "<ul></ul>")
    assert pb.remove_stray_per_page_files(tmp_path) == len(pb.STRAY_PER_PAGE_FILES) + 1
    assert all((tmp_path / name).is_file() for name in pb.STRAY_PER_PAGE_FILES)
    assert not any((tmp_path / "why" / name).exists() for name in pb.STRAY_PER_PAGE_FILES)
    assert not (tmp_path / "404").exists()
    assert read(tmp_path / "404.html") == '<meta property="og:url" content="https://pain001.com/404.html">'
    assert read(tmp_path / "tags" / "a" / "index.html") == '<ul><li><a href="/fr/">FR</a></li></ul>'
    assert "removed 6 stray per-page file(s)" in capsys.readouterr().out


def test_remove_stray_keeps_404_dir_without_root_page(tmp_path):
    put(tmp_path / "404" / "index.html", "x")
    assert pb.remove_stray_per_page_files(tmp_path) == 0
    assert (tmp_path / "404" / "index.html").is_file()


def test_relocate_nested_routes(tmp_path, capsys):
    with pytest.raises(SystemExit, match="/docs-bank-profiles/ was not built"):
        pb.relocate_nested_routes(tmp_path)
    put(tmp_path / "docs-bank-profiles" / "index.html", '<link rel="canonical" href="/docs-bank-profiles/">')
    put(tmp_path / "developers-ci" / "index.html", "ci")
    put(tmp_path / "developers" / "ci" / "old.html", "stale")
    put(tmp_path / "rss.xml", "<link>/developers-ci/</link>")
    put(tmp_path / "notes.txt", "unrelated")
    put(tmp_path / "img.png", "/developers-ci/")
    (tmp_path / "dir.json").mkdir()
    pb.relocate_nested_routes(tmp_path)
    assert read(tmp_path / "docs" / "bank-profiles" / "index.html") == (
        '<link rel="canonical" href="/docs/bank-profiles/">')
    assert read(tmp_path / "developers" / "ci" / "index.html") == "ci"
    assert not (tmp_path / "developers" / "ci" / "old.html").exists()
    assert not (tmp_path / "developers-ci").exists()
    assert read(tmp_path / "rss.xml") == "<link>/developers/ci/</link>"
    assert read(tmp_path / "img.png") == "/developers-ci/"
    assert "2 page(s) moved to nested routes, 2 file(s) relinked" in capsys.readouterr().out


def test_fill_claims(tmp_path, monkeypatch, capsys):
    claims = types.ModuleType("claims")
    claims.load = lambda: {"n": "42"}
    claims.fill = lambda html, register: html.replace("??", register["n"])
    monkeypatch.setitem(sys.modules, "claims", claims)
    put(tmp_path / "a.html", '<span data-claim="n">??</span>')
    put(tmp_path / "b.html", '<span data-claim="n">done</span>')
    put(tmp_path / "c.html", "<p>??</p>")
    pb.fill_claims(tmp_path)
    assert read(tmp_path / "a.html") == '<span data-claim="n">42</span>'
    assert read(tmp_path / "c.html") == "<p>??</p>"
    assert "figures written into 1 page(s)" in capsys.readouterr().out


def test_stamp_redirect_map(tmp_path, capsys):
    pb.stamp_redirect_map(tmp_path)
    js = tmp_path / "js" / "redirect.js"
    put(js, "var X = 1;")
    with pytest.raises(SystemExit, match="no REDIRECTS placeholder"):
        pb.stamp_redirect_map(tmp_path)
    put(js, "var REDIRECTS = {};\nvar REDIRECTS = {};")
    pb.stamp_redirect_map(tmp_path)
    first, second = read(js).split("\n")
    table = json.loads(first[len("var REDIRECTS = "):-1])
    assert table["/enterprise/"] == "/for-banks/" and len(table) == len(pb.LEGACY_REDIRECTS)
    assert second == "var REDIRECTS = {};"
    assert "redirect map stamped: 6 path(s)" in capsys.readouterr().out


def test_gen_legacy_redirects(tmp_path, capsys):
    pb.gen_legacy_redirects(tmp_path)
    stub = read(tmp_path / "enterprise" / "index.html")
    assert pb.CSP_META in stub
    assert '<link rel="canonical" href="https://pain001.com/for-banks/" />' in stub
    assert '<p>Continue to <a href="/for-banks/">https://pain001.com/for-banks/</a>.</p>' in stub
    assert '<meta name="robots" content="noindex" />' in stub and "http-equiv=\"refresh\"" not in stub
    assert all((tmp_path / old / "index.html").is_file() for old in pb.LEGACY_REDIRECTS)
    assert "6 legacy redirect stub(s)" in capsys.readouterr().out


HEADER = '<header class="site-header"><nav>Site nav</nav></header>'
FOOTER = '<footer class="site-footer"><p class="footer-credit">Credit</p></footer>'


def shell_site(site):
    put(site / "index.html", "<html><head>" + pb.CSP_META + pb._THEME_INIT_TAG + "</head><body>"
        + HEADER + FOOTER + "</body></html>")
    put(site / "page" / "index.html", '<html><head><meta http-equiv="content-security-policy" content="old">'
        + pb._THEME_INIT_LINK + "</head><body><footer><p>x</p></footer></body></html>")
    put(site / "bare" / "index.html", "<html><head></head><body><p>x</p></body></html>")
    put(site / "frag.html", "<p>fragment</p>")
    put(site / "tags" / "a" / "index.html",
        '<html lang="en"><head><style>a{}</style></head><body><header role="banner"><a href="/">Home</a>'
        "</header><ul></ul><footer><p>tag</p></footer></body></html>")
    put(site / "tags" / "b" / "index.html",
        '<html class="no-js"><head><link rel="stylesheet" href="/css/prism.css" />' + pb._THEME_INIT_TAG
        + '</head><body><script src="/js/prism.js" defer></script></body></html>')
    put(site / "old" / "index.html", '<html><head><script src="/js/redirect.js"></script></head>'
        "<body><main>moved</main></body></html>")
    put(site / "old2" / "index.html", '<html><head><script src="/js/redirect.js"></script></head>'
        '<body><header class="site-header">old</header><main>moved</main></body></html>')


def normalised(site):
    """Write the shell fixture pages and run the shell pass over them."""
    shell_site(site)
    pb.normalise_site_shell(site)
    return site


def test_normalise_site_shell(tmp_path, capsys):
    shell_site(tmp_path)
    home = read(tmp_path / "index.html")  # already carries the shell
    pb.normalise_site_shell(tmp_path)
    page = read(tmp_path / "page" / "index.html")
    assert pb.CSP_META in page and 'content="old"' not in page
    assert pb._THEME_INIT_TAG in page and pb._THEME_INIT_LINK not in page
    assert "<footer><p>x</p>" + pb._FOOTER_CREDIT + "</footer>" in page
    bare = read(tmp_path / "bare" / "index.html")
    assert bare == ("<html><head>" + pb.CSP_META + "</head><body><p>x</p>"
                    '<footer class="footer">' + pb._FOOTER_CREDIT + "</footer></body></html>")
    assert read(tmp_path / "frag.html") == "<p>fragment</p>"
    assert read(tmp_path / "index.html") == home, "an already normalised page is left alone"
    assert "normalised PRISM shell and CSP on 6 page(s)" in capsys.readouterr().out


def test_normalise_site_shell_rebuilds_a_taxonomy_page(tmp_path):
    tag = read(normalised(tmp_path) / "tags" / "a" / "index.html")
    assert tag.startswith('<html class="no-js" lang="en"><head>')
    assert "<style>" not in tag and pb._PRISM_LINKS in tag and pb._THEME_INIT_TAG in tag
    assert '<body class="prism-theme">' + HEADER in tag and FOOTER in tag and 'role="banner"' not in tag
    assert tag.endswith('<script src="/js/prism.js" defer></script>'
                        '<script src="/js/pain001-prism.js" defer></script></body></html>')


def test_normalise_site_shell_dedupes_prism_and_wraps_redirect_pages(tmp_path):
    normalised(tmp_path)
    b = read(tmp_path / "tags" / "b" / "index.html")
    assert b.count("prism.css") == 1 and b.count("prism.js") == 1 and b.count(pb._THEME_INIT_TAG) == 1
    assert b.startswith('<html class="no-js"><head>') and HEADER not in b and "site-footer" not in b
    old = read(tmp_path / "old" / "index.html")
    assert '<body class="prism-theme">' + HEADER + "<main>" in old
    assert FOOTER + '<script src="/js/prism.js" defer>' in old
    assert '<body class="prism-theme">' + HEADER + "<main>" in read(tmp_path / "old2" / "index.html")


def test_normalise_site_shell_without_shared_chrome(tmp_path):
    put(tmp_path / "index.html", "<html><head></head><body></body></html>")
    put(tmp_path / "old" / "index.html", '<html><head><script src="/js/redirect.js"></script></head>'
        "<body><footer>f</footer></body></html>")
    pb.normalise_site_shell(tmp_path)
    old = read(tmp_path / "old" / "index.html")
    assert "<header" not in old and "<footer>f" + pb._FOOTER_CREDIT + "</footer>" in old
