# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Sitemap and locale index policy in postbuild_fix.

Pins how the sitemap is rebuilt: which built pages are listed (no API,
CSP, dot, utility, translated corpus or unindexed-locale pages), how each
lastmod comes from the git history of the page's sources (falling back
to the build date when the history is shallow or git fails), and how
decision D4 marks unindexed locales noindex and removes alternates that
point at them.
"""

import subprocess
from datetime import date
from types import SimpleNamespace

import postbuild_fix as pb


def put(path, text=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8")


def fake_git(shallow="false", log="", error=None):
    calls = []

    def run(cmd, **kwargs):
        calls.append(cmd)
        if error is not None:
            raise error
        out = shallow + "\n" if "rev-parse" in cmd else log
        return SimpleNamespace(stdout=out)

    return run, calls


def test_source_dates_reads_newest_commit_per_file(tmp_path, monkeypatch):
    log = "@2026-11-10\n\n_posts/why.md\nscripts/x.py\n@2026-10-01\n\n_posts/why.md\n_posts/old.md\n"
    run, calls = fake_git(log=log)
    monkeypatch.setattr(subprocess, "run", run)
    assert pb.source_dates(tmp_path) == {
        "_posts/why.md": "2026-11-10", "scripts/x.py": "2026-11-10", "_posts/old.md": "2026-10-01"}
    assert calls[1][:2] == ["git", "log"]


def test_source_dates_none_for_shallow_or_failed_git(tmp_path, monkeypatch):
    monkeypatch.setattr(subprocess, "run", fake_git(shallow="true")[0])
    assert pb.source_dates(tmp_path) is None
    monkeypatch.setattr(subprocess, "run", fake_git(error=OSError("no git"))[0])
    assert pb.source_dates(tmp_path) is None
    monkeypatch.setattr(subprocess, "run", fake_git(error=subprocess.CalledProcessError(128, "git"))[0])
    assert pb.source_dates(tmp_path) is None


def make_root(root):
    put(root / "_posts" / "why.md", "---\nlayout: page\n---\n")
    put(root / "_posts" / "index.md", "no layout here\n")
    put(root / "_posts" / "orphan.md", 'layout: "missing"\n')
    put(root / "_posts" / "docs-ci.md", "x")
    put(root / "_posts" / "fr-corpus-x.md", "x")
    put(root / "_layouts" / "page.html")
    put(root / "scripts" / "pages_i18n" / "fr.json", "{}")
    put(root / "scripts" / "try_i18n" / "pt-br.json", "{}")


def test_page_sources(tmp_path):
    make_root(tmp_path)
    assert pb.page_sources(tmp_path, ".") == ["_posts/index.md"]
    assert pb.page_sources(tmp_path, "why") == ["_posts/why.md", "_layouts/page.html"]
    assert pb.page_sources(tmp_path, "orphan") == ["_posts/orphan.md"]
    assert pb.page_sources(tmp_path, "docs/ci") == ["_posts/docs-ci.md"]
    assert pb.page_sources(tmp_path, "fr/why") == [
        "_posts/why.md", "_layouts/page.html", "scripts/pages_i18n/fr.json"]
    assert pb.page_sources(tmp_path, "fr/corpus-x") == ["_posts/fr-corpus-x.md", "scripts/pages_i18n/fr.json"]
    assert pb.page_sources(tmp_path, "pt-br/nothing") == ["scripts/try_i18n/pt-br.json"]
    assert pb.page_sources(tmp_path, "fr") == []


def test_page_lastmod(tmp_path):
    make_root(tmp_path)
    dates = {"_posts/why.md": "2026-01-01", "_layouts/page.html": "2026-03-01"}
    assert pb.page_lastmod(tmp_path, "why", None, "today") == "today"
    assert pb.page_lastmod(tmp_path, "why", dates, "today") == "2026-03-01"
    assert pb.page_lastmod(tmp_path, "orphan", dates, "today") == "today"


class FixedDate(date):
    @classmethod
    def today(cls):
        return cls(2026, 11, 11)


def test_regen_sitemap(tmp_path, monkeypatch, capsys):
    make_root(tmp_path)
    monkeypatch.setattr(pb, "__file__", str(tmp_path / "scripts" / "postbuild_fix.py"))
    monkeypatch.setattr(pb, "date", FixedDate)
    monkeypatch.setattr(pb, "source_dates", lambda root: {"_posts/why.md": "2026-05-05"})
    site = tmp_path / "site"
    for rel in (".", "why", "api/v1", "_csp/x", ".well-known/x", "404", "de/corpus-de-x", "uk", "uk/why", "fr"):
        put(site / rel / "index.html")
    pb.regen_sitemap(site)
    body = read(site / "sitemap.xml")
    locs = [line.strip()[5:-6] for line in body.splitlines() if "<loc>" in line]
    assert locs == ["https://pain001.com/fr/", "https://pain001.com/", "https://pain001.com/why/"]
    assert "<lastmod>2026-05-05</lastmod>" in body and "<lastmod>2026-11-11</lastmod>" in body
    assert body.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<urlset')
    assert "3 URLs, lastmod from commit dates" in capsys.readouterr().out
    monkeypatch.setattr(pb, "source_dates", lambda root: None)
    pb.regen_sitemap(site)
    assert "2026-05-05" not in read(site / "sitemap.xml")
    assert "the build date (shallow history)" in capsys.readouterr().out


ALTS = ('<head><link rel="alternate" hreflang="uk" href="/uk/" />'
        '<link rel="alternate" hreflang="fr" href="/fr/" /><link rel="canonical" href="/x/"></head>')


def test_apply_locale_index_policy(tmp_path, capsys):
    assert pb.is_noindexed_locale("uk/why") and not pb.is_noindexed_locale("fr/why")
    assert not pb.is_noindexed_locale("why")
    put(tmp_path / "uk" / "index.html", ALTS)
    put(tmp_path / "index.html", ALTS)
    put(tmp_path / "why.html", "<head></head>")
    pb.apply_locale_index_policy(tmp_path)
    assert read(tmp_path / "uk" / "index.html") == '<head><meta name="robots" content="noindex, follow" /></head>'
    assert read(tmp_path / "index.html") == (
        '<head><link rel="alternate" hreflang="fr" href="/fr/" /><link rel="canonical" href="/x/"></head>')
    assert read(tmp_path / "why.html") == "<head></head>"
    assert "1 page(s) noindex, 1 page(s) lost alternates" in capsys.readouterr().out
