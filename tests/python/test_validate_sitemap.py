# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_sitemap.py.

The sitemap lists only canonical, indexable pages, and no noindex page
names itself canonical (Search Console flagged both signals on the
translated corpus pages).
"""

from __future__ import annotations

from pathlib import Path

import validate_sitemap as gate

BASE = "https://pain001.com"
NOINDEX = '<meta name="robots" content="noindex, follow" />'


def _page(site: Path, rel: str, head: str) -> None:
    d = site / rel if rel else site
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(f"<html><head>{head}</head></html>", encoding="utf-8")


def _canon(url: str) -> str:
    return f'<link rel="canonical" href="{url}" />'


def _sitemap(site: Path, *urls: str) -> None:
    locs = "".join(f"<url><loc>{u}</loc></url>" for u in urls)
    (site / "sitemap.xml").write_text(
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{locs}</urlset>',
        encoding="utf-8")


def test_clean_site_passes(tmp_path):
    _page(tmp_path, "", _canon(f"{BASE}/"))
    _page(tmp_path, "why", _canon(f"{BASE}/why/"))
    _page(tmp_path, "de/corpus-x", NOINDEX)
    _page(tmp_path, "executive-brief-fr", NOINDEX + _canon(f"{BASE}/fr/executive-brief/"))
    _sitemap(tmp_path, f"{BASE}/", f"{BASE}/why/")
    assert gate.problems(tmp_path) == []


def test_sitemap_url_must_be_built_indexable_and_self_canonical(tmp_path):
    _page(tmp_path, "hidden", NOINDEX)
    _page(tmp_path, "alias", _canon(f"{BASE}/other/"))
    _sitemap(tmp_path, f"{BASE}/hidden/", f"{BASE}/alias/", f"{BASE}/gone/",
             "https://www.pain001.com/")
    found = gate.problems(tmp_path)
    assert f"{BASE}/hidden/: listed in the sitemap but noindex" in found
    assert f"{BASE}/alias/: canonical is {BASE}/other/" in found
    assert f"{BASE}/gone/: not a page in the build" in found
    assert "https://www.pain001.com/: not a page in the build" in found


def test_noindex_page_must_not_name_itself_canonical(tmp_path):
    # The shape Search Console flagged on /es/corpus-cz-sepa-sct/.
    _page(tmp_path, "", _canon(f"{BASE}/"))
    _page(tmp_path, "es/corpus-cz", NOINDEX + _canon(f"{BASE}/es/corpus-cz/"))
    _sitemap(tmp_path, f"{BASE}/")
    assert gate.problems(tmp_path) == [f"{BASE}/es/corpus-cz/: noindex yet canonical to itself"]


def test_main_reports_exit_status(tmp_path, monkeypatch, capsys):
    _page(tmp_path, "", _canon(f"{BASE}/"))
    _page(tmp_path, "x", NOINDEX + _canon(f"{BASE}/x/"))
    _sitemap(tmp_path, f"{BASE}/")
    monkeypatch.setattr(gate, "SITE", tmp_path)
    assert gate.main() == 1
    assert "1 problem(s)" in capsys.readouterr().out
    (tmp_path / "x" / "index.html").write_text(f"<head>{NOINDEX}</head>", encoding="utf-8")
    assert gate.main() == 0


def test_the_homepage_must_be_listed(tmp_path):
    # regen_sitemap's "." prefix filter dropped the homepage itself.
    _page(tmp_path, "", _canon(f"{BASE}/"))
    _page(tmp_path, "why", _canon(f"{BASE}/why/"))
    _sitemap(tmp_path, f"{BASE}/why/")
    assert gate.problems(tmp_path) == [f"{BASE}/: the homepage is not in the sitemap"]
