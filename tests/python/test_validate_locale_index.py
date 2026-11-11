# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_locale_index.py's command line and edges.

Pins that an indexed-locale page which is itself noindex is not checked
for links, that a site without a sitemap is accepted, and the exit codes
and FAIL lines of the command.
"""

from __future__ import annotations

import sys

import validate_locale_index as v

SLUG = sorted(v.UNINDEXED)[0]
NOINDEX = '<meta name="robots" content="noindex, follow">'


def _site(tmp_path, pages):
    site = tmp_path / "site"
    for rel, body in pages.items():
        path = site / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return site


def test_a_noindex_page_may_link_anywhere_and_no_sitemap_is_fine(tmp_path):
    site = _site(tmp_path, {"404.html": f'{NOINDEX}<a href="/{SLUG}/">x</a>',
                            f"{SLUG}/index.html": NOINDEX})
    assert v.problems(site) == []


def test_main_missing_build_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["validate_locale_index.py"])
    monkeypatch.setattr(v, "ROOT", tmp_path)
    assert v.main() == 1
    assert capsys.readouterr().out == f"error: {tmp_path / 'site'}/index.html not found; run the build first\n"


def test_main_passes_a_clean_site(tmp_path, monkeypatch, capsys):
    site = _site(tmp_path, {"index.html": '<a href="/about/">a</a>'})
    monkeypatch.setattr(sys, "argv", ["validate_locale_index.py", str(site)])
    assert v.main() == 0
    assert capsys.readouterr().out.startswith("validate_locale_index: 0 problem(s); indexed: en, ")


def test_main_prints_each_failure(tmp_path, monkeypatch, capsys):
    site = _site(tmp_path, {"index.html": f'<a href="/{SLUG}/">x</a>',
                            "sitemap.xml": f"<loc>https://pain001.com/{SLUG}/</loc>"})
    monkeypatch.setattr(sys, "argv", ["validate_locale_index.py", str(site)])
    assert v.main() == 1
    lines = capsys.readouterr().out.splitlines()
    assert lines[:2] == [f"FAIL index.html: links to unindexed locale(s) {SLUG}",
                         f"FAIL sitemap.xml lists unindexed locale(s) {SLUG}"]
    assert lines[2].startswith("validate_locale_index: 2 problem(s)")
