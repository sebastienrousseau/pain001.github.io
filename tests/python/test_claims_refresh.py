# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for the `claims.py refresh` command and its live sources.

Pins that each live figure comes from its public endpoint, that the
release count follows pages of 100, that an unreachable source keeps the
previous figure, and that refresh rewrites the register with its SPDX
header and the current VERSION.
"""

from __future__ import annotations

import io
import json

import claims

URLS = {
    f"https://api.github.com/repos/{claims.CORE}": {"stargazers_count": 321},
    "https://pypistats.org/api/packages/pain001/recent": {"data": {"last_month": 4567}},
}


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_fetch_sends_a_user_agent_and_parses_json(monkeypatch):
    seen = []

    def fake_urlopen(request, timeout):
        seen.append((request.full_url, request.get_header("User-agent"), timeout))
        return _Response(b'{"ok": true}')

    monkeypatch.setattr(claims.urllib.request, "urlopen", fake_urlopen)
    assert claims.fetch("https://x.test/a") == {"ok": True}
    assert seen == [("https://x.test/a", "pain001.com build", 30)]


def test_release_count_follows_pages(monkeypatch):
    pages = {1: [0] * 100, 2: [0] * 100, 3: [0] * 7}
    monkeypatch.setattr(claims, "fetch", lambda url: pages[int(url.rsplit("=", 1)[1])])
    assert claims.release_count() == 207


def _fake_fetch(url):
    if url in URLS:
        return URLS[url]
    raise OSError(f"unreachable {url}")


def test_live_values_keep_only_reachable_sources(monkeypatch, capsys):
    monkeypatch.setattr(claims, "fetch", _fake_fetch)
    monkeypatch.setattr(claims, "release_count", lambda: 85)
    assert claims.live_values() == {"github_stars": 321, "pypi_downloads_month": 4567, "releases_since_2023": 85}
    assert "[claims] openssf_scorecard: source unreachable (unreachable" in capsys.readouterr().out


def test_load_skips_comment_header_and_dump_restores_it(tmp_path):
    path = tmp_path / "claims.yml"
    claims.dump({"claims": [{"id": "a", "value": "é"}]}, path)
    text = path.read_text(encoding="utf-8")
    assert text.startswith(claims.HEADER) and '"é"' in text
    assert claims.load(path) == {"claims": [{"id": "a", "value": "é"}]}


def test_main_rejects_anything_but_refresh(capsys):
    assert claims.main(["claims.py"]) == 2
    assert claims.main(["claims.py", "refresh", "extra"]) == 2
    assert capsys.readouterr().out.count("usage: claims.py refresh") == 2


def test_main_refresh_rewrites_the_register(tmp_path, monkeypatch, capsys):
    register = tmp_path / "claims.yml"
    claims.dump({"claims": [
        {"id": "github_stars", "source": "live", "value": 1, "verified_in": "0.0.1"},
        {"id": "manual", "source": "manual", "value": "x", "verified_in": "0.0.1"},
    ]}, register)
    version = tmp_path / "VERSION"
    version.write_text("0.0.86\n", encoding="utf-8")
    monkeypatch.setattr(claims, "REGISTER", register)
    monkeypatch.setattr(claims, "VERSION", version)
    monkeypatch.setattr(claims.load, "__defaults__", (register,))
    monkeypatch.setattr(claims.dump, "__defaults__", (register,))
    monkeypatch.setattr(claims, "live_values", lambda: {"github_stars": 99})
    assert claims.main(["claims.py", "refresh"]) == 0
    assert "[claims] 2 claim(s) in data/claims.yml" in capsys.readouterr().out
    by = claims.by_id(claims.load(register))
    assert (by["github_stars"]["value"], by["github_stars"]["verified_in"]) == (99, "0.0.86")
    assert by["manual"]["verified_in"] == "0.0.1"
    assert json.loads(register.read_text(encoding="utf-8").split("\n", 2)[2])["claims"][1]["id"] == "manual"
