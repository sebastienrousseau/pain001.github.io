# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/traction.py: the JSON fetch, the rendered table,
that an offline build keeps the published figures and exits 0, that a
page without markers fails, and that a refresh rewrites only the block."""

import datetime as dt
import io
import json
import urllib.error

import traction

PAGE = (
    "# Governance\n\nBefore.\n\n"
    "<!-- traction:start -->\nold figures\n<!-- traction:end -->\n\nAfter.\n"
)


def test_fetch_sends_a_user_agent_and_parses_json(monkeypatch):
    seen = {}

    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def fake_urlopen(request, timeout):
        seen["url"] = request.full_url
        seen["agent"] = request.get_header("User-agent")
        seen["timeout"] = timeout
        return Response(json.dumps({"ok": 1}).encode())

    monkeypatch.setattr(traction.urllib.request, "urlopen", fake_urlopen)
    assert traction.fetch("https://example.test/x") == {"ok": 1}
    assert seen == {"url": "https://example.test/x", "agent": "pain001.com build", "timeout": 30}


def test_render_formats_thousands_and_keeps_the_markers():
    table = traction.render(12345, 678, 1500, 42, "2026-11-11")
    assert table.startswith("<!-- traction:start -->\n")
    assert table.endswith("<!-- traction:end -->")
    assert "| pain001 downloads, last 30 days | 12,345 | PyPI |" in table
    assert "| pain001 downloads, last 7 days | 678 | PyPI |" in table
    assert "| GitHub stars | 1,500 | GitHub |" in table
    assert "| GitHub forks | 42 | GitHub |" in table
    assert "Refreshed 2026-11-11." in table


def _sources(monkeypatch):
    replies = {
        traction.PYPISTATS: {"data": {"last_month": 3000, "last_week": "700"}},
        traction.GITHUB: {"stargazers_count": 1234, "forks_count": 56},
    }
    monkeypatch.setattr(traction, "fetch", replies.__getitem__)


def test_unreachable_sources_keep_the_page_and_exit_zero(tmp_path, monkeypatch, capsys):
    page = tmp_path / "governance.md"
    page.write_text(PAGE, encoding="utf-8")
    monkeypatch.setattr(traction, "PAGE", page)

    def offline(url):
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(traction, "fetch", offline)
    assert traction.main() == 0
    assert page.read_text(encoding="utf-8") == PAGE
    assert "sources unreachable (<urlopen error no route>); keeping the published figures" in capsys.readouterr().out


def test_a_page_without_markers_fails(tmp_path, monkeypatch, capsys):
    page = tmp_path / "governance.md"
    page.write_text("# Governance\n\nNo table here.\n", encoding="utf-8")
    monkeypatch.setattr(traction, "PAGE", page)
    _sources(monkeypatch)
    assert traction.main() == 1
    assert page.read_text(encoding="utf-8") == "# Governance\n\nNo table here.\n"
    assert "no markers on the governance page" in capsys.readouterr().out


def test_refresh_rewrites_only_the_block(tmp_path, monkeypatch, capsys):
    page = tmp_path / "governance.md"
    page.write_text(PAGE, encoding="utf-8")
    monkeypatch.setattr(traction, "PAGE", page)
    _sources(monkeypatch)
    day = dt.date.today().isoformat()

    assert traction.main() == 0

    text = page.read_text(encoding="utf-8")
    assert text == PAGE.replace(
        "<!-- traction:start -->\nold figures\n<!-- traction:end -->",
        traction.render(3000, 700, 1234, 56, day),
    )
    assert f"traction: refreshed for {day}" in capsys.readouterr().out
