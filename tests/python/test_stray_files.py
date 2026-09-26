# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests for postbuild_fix.remove_stray_per_page_files.

ssg writes news-sitemap.xml, sitemap.xml, robots.txt, rss.xml and
manifest.json into every page directory. Search Console showed the
effects: invalid per-page sitemaps, a /404/ page served with 200 (a soft
404), and builds that differed on every run. Only the root copies and
/404.html may survive the post-build pass.
"""

import postbuild_fix as pb


def _site(tmp_path):
    site = tmp_path / "site"
    for page in ("", "why/", "fr/why/", "404/"):
        d = site / page
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text("<html></html>", encoding="utf-8")
        for name in pb.STRAY_PER_PAGE_FILES:
            (d / name).write_text("x", encoding="utf-8")
    (site / "404.html").write_text("<html>not found</html>", encoding="utf-8")
    return site


def test_root_copies_are_kept(tmp_path):
    site = _site(tmp_path)
    pb.remove_stray_per_page_files(site)
    for name in pb.STRAY_PER_PAGE_FILES:
        assert (site / name).is_file(), name


def test_every_per_page_copy_is_removed(tmp_path):
    site = _site(tmp_path)
    pb.remove_stray_per_page_files(site)
    for name in pb.STRAY_PER_PAGE_FILES:
        assert [p for p in site.rglob(name) if p.parent != site] == [], name
    assert (site / "why" / "index.html").is_file()
    assert (site / "fr" / "why" / "index.html").is_file()


def test_the_404_copy_goes_but_404_html_stays(tmp_path):
    site = _site(tmp_path)
    pb.remove_stray_per_page_files(site)
    assert not (site / "404").exists()
    assert (site / "404.html").is_file()


def test_404_directory_is_kept_without_404_html(tmp_path):
    # Without /404.html the not-found page would vanish entirely, so the
    # directory is only removed once its replacement exists.
    site = _site(tmp_path)
    (site / "404.html").unlink()
    pb.remove_stray_per_page_files(site)
    assert (site / "404" / "index.html").is_file()
