# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/carry_forward_assets.py (issue #54, review finding SR-3).

The script copies the previous deploy's /_csp/ assets from the live site
into a new build. It now keeps a download only when it is the stylesheet
or script its name says, so a CDN challenge or error page is never
published as CSS or JavaScript. The network is replaced by a fake urlopen.
"""

import urllib.error

import pytest

import carry_forward_assets as cf

SITE = "https://pain001.test"
PAGE = b'<html><link href="/_csp/aaaaaaaa11.css"><script src="/_csp/bbbbbbbb22.js"></script></html>'


class FakeResponse:
    def __init__(self, body: bytes, content_type: str):
        self._body = body
        self.headers = {"Content-Type": content_type}

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@pytest.fixture
def serve(monkeypatch):
    """Serve `routes` {path: (body, content type)}; everything else is unreachable."""
    requested: list[str] = []

    def install(routes):
        def urlopen(request, timeout=None):
            path = request.full_url[len(SITE):]
            requested.append(path)
            if path not in routes:
                raise urllib.error.URLError("unreachable")
            return FakeResponse(*routes[path])

        monkeypatch.setattr(cf.urllib.request, "urlopen", urlopen)
        return requested

    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    return install


def run(tmp_path, capsys):
    assert cf.main([str(tmp_path), "--site", SITE]) == 0
    return capsys.readouterr().out


def test_real_css_and_js_are_carried(tmp_path, capsys, serve):
    serve({
        "/": (PAGE, "text/html; charset=utf-8"),
        "/_csp/aaaaaaaa11.css": (b"body{color:#000}", "text/css; charset=utf-8"),
        "/_csp/bbbbbbbb22.js": (b"(()=>{})();", "application/javascript; charset=utf-8"),
    })
    out = run(tmp_path, capsys)
    assert (tmp_path / "_csp/aaaaaaaa11.css").read_bytes() == b"body{color:#000}"
    assert (tmp_path / "_csp/bbbbbbbb22.js").read_bytes() == b"(()=>{})();"
    assert "2 carried" in out and "0 skipped" in out


def test_text_javascript_is_accepted_for_js(tmp_path, capsys, serve):
    serve({
        "/": (PAGE, "text/html"),
        "/_csp/bbbbbbbb22.js": (b"var a=1;", "text/javascript"),
    })
    run(tmp_path, capsys)
    assert (tmp_path / "_csp/bbbbbbbb22.js").is_file()


def test_an_html_page_served_as_css_is_not_carried(tmp_path, capsys, serve):
    serve({
        "/": (PAGE, "text/html"),
        "/_csp/aaaaaaaa11.css": (b"<!DOCTYPE html><title>Just a moment...</title>", "text/html; charset=utf-8"),
    })
    out = run(tmp_path, capsys)
    assert not (tmp_path / "_csp/aaaaaaaa11.css").exists()
    assert "skipped /_csp/aaaaaaaa11.css" in out and "1 skipped" in out


def test_an_html_body_is_refused_even_with_a_css_type(tmp_path, capsys, serve):
    serve({
        "/": (PAGE, "text/html"),
        "/_csp/aaaaaaaa11.css": (b"  \n<html><body>challenge</body></html>", "text/css"),
    })
    run(tmp_path, capsys)
    assert not (tmp_path / "_csp/aaaaaaaa11.css").exists()


@pytest.mark.parametrize("content_type", ["application/octet-stream", "text/plain", "", "text/css"])
def test_a_script_served_with_the_wrong_type_is_not_carried(tmp_path, capsys, serve, content_type):
    serve({
        "/": (PAGE, "text/html"),
        "/_csp/bbbbbbbb22.js": (b"(()=>{})();", content_type),
    })
    run(tmp_path, capsys)
    assert not (tmp_path / "_csp/bbbbbbbb22.js").exists()


def test_an_empty_response_is_not_written(tmp_path, capsys, serve):
    serve({"/": (PAGE, "text/html"), "/_csp/aaaaaaaa11.css": (b"", "text/css")})
    run(tmp_path, capsys)
    assert not (tmp_path / "_csp/aaaaaaaa11.css").exists()


def test_an_asset_already_in_the_build_is_not_fetched(tmp_path, capsys, serve):
    existing = tmp_path / "_csp/aaaaaaaa11.css"
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b"new build")
    requested = serve({"/": (PAGE, "text/html")})
    run(tmp_path, capsys)
    assert "/_csp/aaaaaaaa11.css" not in requested
    assert existing.read_bytes() == b"new build"


def test_an_unreachable_site_never_fails_the_build(tmp_path, capsys, serve):
    serve({})
    out = run(tmp_path, capsys)
    assert "0 live asset(s) referenced" in out


def test_a_reproducible_build_fetches_nothing(tmp_path, capsys, serve, monkeypatch):
    requested = serve({"/": (PAGE, "text/html")})
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1790000000")
    out = run(tmp_path, capsys)
    assert requested == []
    assert "nothing carried" in out
    assert not (tmp_path / "_csp").exists()
