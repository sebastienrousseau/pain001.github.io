# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Sitemap lastmod is the last commit to a page's sources.

regen_sitemap stamped the build date on every URL, telling crawlers that
all 493 pages changed on every deploy. Each URL now carries the latest
commit date among its post, the post's layout and, for a locale copy,
that locale's translation table.
"""

import subprocess

import postbuild_fix as pb


def _repo(tmp_path):
    root = tmp_path / "repo"
    files = {
        "_posts/index.md": "---\nlayout: index\n---\n",
        "_posts/documentation.md": '---\nlayout: "page"\n---\n',
        "_layouts/index.html": "<main></main>",
        "_layouts/page.html": "<main></main>",
        "scripts/docs_i18n/fr.json": "{}",
    }
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def _git(root, *args, date=None):
    env = {"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date} if date else {}
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                   env={**__import__("os").environ, **env})


def _commit(root, paths, date):
    _git(root, "add", *paths)
    _git(root, "-c", "user.name=t", "-c", "user.email=t@example.com",
         "-c", "commit.gpgsign=false", "commit", "-q", "-m", "x", date=date)


def test_page_sources_cover_post_layout_and_locale_table(tmp_path):
    root = _repo(tmp_path)
    assert pb.page_sources(root, ".") == ["_posts/index.md", "_layouts/index.html"]
    assert pb.page_sources(root, "fr/documentation") == [
        "_posts/documentation.md", "_layouts/page.html", "scripts/docs_i18n/fr.json"]
    assert pb.page_sources(root, "missing") == []


def test_lastmod_is_the_latest_source_commit(tmp_path):
    root = _repo(tmp_path)
    _git(root, "init", "-q")
    _commit(root, ["."], "2026-01-01T00:00:00+00:00")
    (root / "scripts/docs_i18n/fr.json").write_text('{"a": 1}', encoding="utf-8")
    _commit(root, ["scripts/docs_i18n/fr.json"], "2026-03-01T00:00:00+00:00")
    dates = pb.source_dates(root)
    assert pb.page_lastmod(root, "documentation", dates, "today") == "2026-01-01"
    assert pb.page_lastmod(root, "fr/documentation", dates, "today") == "2026-03-01"
    assert pb.page_lastmod(root, "missing", dates, "today") == "today"


def test_without_history_the_build_date_is_kept(tmp_path):
    root = _repo(tmp_path)
    assert pb.source_dates(root) is None  # not a repository
    assert pb.page_lastmod(root, ".", None, "2026-11-09") == "2026-11-09"


def test_the_homepage_is_listed(tmp_path):
    """The `.` prefix filter meant for dot-directories also matched the
    homepage's own relative path, ".", so the sitemap never listed it."""
    site = tmp_path / "site"
    for rel in ("index.html", "about/index.html", ".well-known/index.html", "404/index.html"):
        page = site / rel
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text("<html></html>", encoding="utf-8")
    pb.regen_sitemap(site)
    sitemap = (site / "sitemap.xml").read_text(encoding="utf-8")
    assert "<loc>https://pain001.com/</loc>" in sitemap
    assert "<loc>https://pain001.com/about/</loc>" in sitemap
    assert ".well-known" not in sitemap and "/404/" not in sitemap
