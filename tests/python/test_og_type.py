# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Home pages carry og:type website; other pages keep what ssg wrote.

ssg writes og:type "article" on every page, the homepage included,
whatever the front matter's `type` says.
"""

import postbuild_fix as pb

ARTICLE = '<head><meta property="og:type" content="article" /></head>'


def test_home_pages_become_website_and_articles_stay(tmp_path):
    site = tmp_path / "site"
    for rel in ("index.html", "fr/index.html", "pain-001/index.html"):
        page = site / rel
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(ARTICLE, encoding="utf-8")
    pb.fix_home_og_type(site)
    for rel in ("index.html", "fr/index.html"):
        assert 'content="website"' in (site / rel).read_text(encoding="utf-8")
    assert 'content="article"' in (site / "pain-001/index.html").read_text(encoding="utf-8")
