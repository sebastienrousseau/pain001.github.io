# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Decision D4: the indexed languages, the rest noindex, follow."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import postbuild_fix as pb  # noqa: E402
import validate_locale_index as gate  # noqa: E402

HEAD = ('<head><link rel="canonical" href="https://pain001.com/uk/" />'
        '<link rel="alternate" hreflang="en" href="https://pain001.com/" />'
        '<link rel="alternate" hreflang="fr" href="https://pain001.com/fr/" />'
        '<link rel="alternate" hreflang="uk" href="https://pain001.com/uk/" />'
        '<link rel="alternate" hreflang="hi" href="https://pain001.com/hi/" /></head>')


def test_the_indexed_set_is_the_decided_one():
    assert pb.INDEXED_LOCALES[:5] == ("fr", "de", "nl", "es", "it")
    assert len(pb.INDEXED_LOCALES) == len(set(pb.INDEXED_LOCALES)) == 25
    assert not {"uk", "bn", "hi", "ro", "ha", "ta", "te", "mr", "fil"} & set(pb.INDEXED_LOCALES)
    assert set(pb.INDEXED_LOCALES) <= set(pb.LOCALES)


def test_is_noindexed_locale():
    assert pb.is_noindexed_locale("uk/index.html")
    assert pb.is_noindexed_locale("hi/try/index.html")
    assert not pb.is_noindexed_locale("fr/index.html")
    assert not pb.is_noindexed_locale("index.html")
    assert not pb.is_noindexed_locale("languages/index.html")


def _site(tmp_path):
    site = tmp_path / "site"
    for rel in ("index.html", "uk/index.html", "fr/index.html", "languages/index.html"):
        (site / rel).parent.mkdir(parents=True, exist_ok=True)
        body = '<a href="/uk/">Українська</a>' if rel in ("index.html", "languages/index.html") else ""
        (site / rel).write_text(f"<html>{HEAD}<body>{body}</body></html>", encoding="utf-8")
    return site


def test_the_policy_marks_unindexed_locales_and_trims_alternates(tmp_path):
    site = _site(tmp_path)
    pb.apply_locale_index_policy(site)
    uk = (site / "uk/index.html").read_text(encoding="utf-8")
    assert 'content="noindex, follow"' in uk
    assert "hreflang=" not in uk and 'rel="canonical"' not in uk
    home = (site / "index.html").read_text(encoding="utf-8")
    assert 'hreflang="fr"' in home and 'hreflang="uk"' not in home and 'hreflang="hi"' not in home


def test_the_gate_reports_links_alternates_and_unmarked_pages(tmp_path):
    site = _site(tmp_path)
    found = gate.problems(site)
    assert any(p.startswith("uk/index.html: unindexed locale page without robots noindex") for p in found)
    assert any(p.startswith("index.html: links to unindexed locale(s) uk") for p in found)
    assert any(p.startswith("index.html: hreflang alternate(s) for unindexed locale(s) hi, uk") for p in found)
    assert not any(p.startswith("languages/index.html: links") for p in found)


def test_the_gate_passes_once_the_policy_has_run_and_the_link_is_gone(tmp_path):
    site = _site(tmp_path)
    (site / "index.html").write_text(f"<html>{HEAD}<body></body></html>", encoding="utf-8")
    pb.apply_locale_index_policy(site)
    (site / "sitemap.xml").write_text("<loc>https://pain001.com/fr/</loc>", encoding="utf-8")
    assert gate.problems(site) == []
    (site / "sitemap.xml").write_text("<loc>https://pain001.com/uk/</loc>", encoding="utf-8")
    assert gate.problems(site) == ["sitemap.xml lists unindexed locale(s) uk"]
