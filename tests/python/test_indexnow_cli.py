# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/indexnow.py's live sitemap read and CLI modes.

Pins the cache-busting query on a live sitemap URL, the default sitemap,
the empty-sitemap message, and that --dry-run submits nothing.
"""

from __future__ import annotations

import io

import indexnow

KEY = "0123456789abcdef0123456789abcdef"
SITEMAP = "<urlset><url><loc>https://pain001.com/</loc></url><url><loc>https://pain001.com/a/</loc></url></urlset>"


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _fake_urlopen(seen):
    def fake(request, timeout):
        seen.append((request.full_url, request.get_header("User-agent"), timeout))
        return _Response(SITEMAP.encode("utf-8"))

    return fake


def test_live_sitemap_gets_a_cache_buster(monkeypatch):
    seen = []
    monkeypatch.setattr(indexnow.urllib.request, "urlopen", _fake_urlopen(seen))
    monkeypatch.setattr(indexnow.time, "time", lambda: 1700000000.7)
    assert indexnow.read_sitemap("https://pain001.com/sitemap.xml") == SITEMAP
    assert indexnow.read_sitemap("http://x.test/s.xml?v=1") == SITEMAP
    assert seen == [("https://pain001.com/sitemap.xml?cb=1700000000", indexnow.USER_AGENT, 30),
                    ("http://x.test/s.xml?v=1&cb=1700000000", indexnow.USER_AGENT, 30)]


def test_default_sitemap_is_the_live_one(monkeypatch, capsys):
    seen = []
    monkeypatch.setattr(indexnow.urllib.request, "urlopen", _fake_urlopen(seen))
    monkeypatch.setattr(indexnow, "find_key", lambda: KEY)
    assert indexnow.main(["--dry-run"]) == 0
    assert seen[0][0].startswith(indexnow.DEFAULT_SITEMAP + "?cb=")
    assert capsys.readouterr().out == "[indexnow] dry run: batch 1 would submit 2 URL(s)\n"


def test_dry_run_submits_nothing(tmp_path, monkeypatch, capsys):
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(SITEMAP, encoding="utf-8")
    monkeypatch.setattr(indexnow, "find_key", lambda: KEY)
    monkeypatch.setattr(indexnow, "BATCH", 1)
    monkeypatch.setattr(indexnow.batches, "__defaults__", (1,))
    monkeypatch.setattr(indexnow, "submit", lambda body: (_ for _ in ()).throw(AssertionError("submitted")))
    assert indexnow.main(["--sitemap", str(sitemap), "--dry-run"]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "[indexnow] dry run: batch 1 would submit 1 URL(s)",
        "[indexnow] dry run: batch 2 would submit 1 URL(s)",
    ]


def test_a_sitemap_without_host_urls_submits_nothing(tmp_path, monkeypatch, capsys):
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text("<urlset><url><loc>https://other.test/</loc></url></urlset>", encoding="utf-8")
    monkeypatch.setattr(indexnow, "find_key", lambda: KEY)
    assert indexnow.main(["--sitemap", str(sitemap)]) == 0
    assert capsys.readouterr().out == f"[indexnow] no pain001.com URLs in {sitemap}; nothing submitted\n"
