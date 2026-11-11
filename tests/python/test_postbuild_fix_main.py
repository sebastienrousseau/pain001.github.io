# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The postbuild_fix command line: its three passes.

build.sh runs the script three times: the main pass over the ssg output,
--optimise-assets for the CSS bundle and stripped scripts, and
--stamp-sw once static/ has been copied in. These tests run main() on a
minimal fixture site for each, with git, the claims register, the photo
map and locale_strings replaced by small fakes, and check that each pass
does its own work and nothing from the others.
"""

import sys
import types

import pytest

import postbuild_fix as pb


def put(path, text=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8")


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pb, "__file__", str(tmp_path / "scripts" / "postbuild_fix.py"))
    photos = tmp_path / "page_photos.json"
    photos.write_text('{"pages": {}}', encoding="utf-8")
    monkeypatch.setattr(pb, "PAGE_PHOTO_MAP", photos)
    monkeypatch.setattr(pb, "source_dates", lambda root: None)
    claims = types.ModuleType("claims")
    claims.load = dict
    claims.fill = lambda html, register: html
    monkeypatch.setitem(sys.modules, "claims", claims)
    strings = types.ModuleType("locale_strings")
    strings.STRINGS, strings.STATUS_STRIP = {}, {}
    monkeypatch.setitem(sys.modules, "locale_strings", strings)
    return tmp_path


def run_default_pass(isolated, monkeypatch):
    """Build a minimal ssg output in ./Pain001 and run the main pass on it."""
    site = isolated / "Pain001"
    put(site / "index.html", '<html><head><title>Home</title>&lt;meta name="a" content="b"&gt;'
        '<meta property="og:type" content="article" /></head>'
        '<body><header class="site-header">nav</header><main></main>'
        '<footer class="site-footer"><p class="footer-credit">c</p></footer></body></html>')
    put(site / "docs-bank-profiles" / "index.html", "<html><head><title>B</title></head><body></body></html>")
    put(site / "developers-ci" / "index.html", "<html><head><title>C</title></head><body></body></html>")
    put(site / "404" / "index.html", "<html><head><title>404</title></head><body></body></html>")
    put(site / "why" / "sitemap.xml", "stray")
    put(site / "fr" / "index.html", "<html><head><title>Accueil</title></head><body></body></html>")
    monkeypatch.setattr(sys, "argv", ["postbuild_fix.py"])
    pb.main()
    return site


def test_main_pass_with_default_site_dir(isolated, monkeypatch, capsys):
    site = run_default_pass(isolated, monkeypatch)
    out = capsys.readouterr().out
    assert "unescaped head/body markup on 1 page(s)" in out
    home = read(site / "index.html")
    assert '<meta name="a" content="b">' in home and pb.CSP_META in home
    assert '<meta property="og:type" content="website" />' in home and "article" not in home
    assert "og:type website on 1 home page(s)" in out
    assert '<meta property="og:type" content="website" />' in read(site / "fr" / "index.html")


def test_main_pass_moves_pages_and_writes_the_sitemap(isolated, monkeypatch):
    site = run_default_pass(isolated, monkeypatch)
    assert (site / "docs" / "bank-profiles" / "index.html").is_file()
    assert (site / "enterprise" / "index.html").is_file()
    assert (site / "404.html").is_file() and not (site / "404").exists()
    assert not (site / "why" / "sitemap.xml").exists()
    sitemap = read(site / "sitemap.xml")
    assert "<loc>https://pain001.com/docs/bank-profiles/</loc>" in sitemap
    assert "/enterprise/" not in sitemap
    assert (site / "llms.txt").is_file()


def test_main_optimise_assets(isolated, monkeypatch, capsys):
    site = isolated / "out"
    put(site / "css" / "a.css", "a { color: red; }\n")
    put(site / "p.html", '<head><link rel="stylesheet" href="/css/a.css" /></head><p>&lt;meta x&gt;</p>')
    put(site / "js" / "prism.js", "/* licence banner */\nvar a = 1;\n")
    monkeypatch.setattr(sys, "argv", ["postbuild_fix.py", "--optimise-assets", str(site)])
    pb.main()
    assert "CSS bundle(s) linked from 1 page(s)" in capsys.readouterr().out
    assert "licence banner" not in read(site / "js" / "prism.js")
    assert "var a = 1;" in read(site / "js" / "prism.js")
    assert "/css/site-" in read(site / "p.html")
    assert not (site / "sitemap.xml").exists()


def test_main_stamp_sw(isolated, monkeypatch, capsys):
    site = isolated / "out"
    put(site / "js" / "redirect.js", "var REDIRECTS = {};")
    put(site / "sw.js", 'const CACHE = "pain001-try-old";')
    monkeypatch.setattr(sys, "argv", ["postbuild_fix.py", str(site), "--stamp-sw"])
    pb.main()
    out = capsys.readouterr().out
    assert "redirect map stamped" in out and "sw.js cache version" in out
    assert '"/enterprise/": "/for-banks/"' in read(site / "js" / "redirect.js")
    assert "pain001-try-old" not in read(site / "sw.js")
    assert not (site / "sitemap.xml").exists()
