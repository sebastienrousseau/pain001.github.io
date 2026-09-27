# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/indexnow.py: key discovery, sitemap parsing,
batching, the request body, and that a failing engine never fails CI."""

import json
import urllib.error

import indexnow

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://pain001.com/</loc></url>
<url><loc> https://pain001.com/pain-001/ </loc></url>
<url><loc>https://pain001.com/pain-001/</loc></url>
<url><loc>https://example.com/elsewhere/</loc></url>
</urlset>"""


def test_the_repository_key_file_is_found():
    key = indexnow.find_key()
    assert len(key) == 32
    assert (indexnow.ROOT / "static" / f"{key}.txt").read_text(encoding="utf-8").strip() == key


def test_a_txt_file_whose_content_differs_is_not_a_key(tmp_path):
    (tmp_path / ("a" * 32 + ".txt")).write_text("b" * 32, encoding="utf-8")
    (tmp_path / "security.txt").write_text("Contact: x", encoding="utf-8")
    try:
        indexnow.find_key(tmp_path)
    except SystemExit:
        return
    raise AssertionError("a mismatched key file was accepted")


def test_sitemap_urls_are_this_host_only_and_unique():
    assert indexnow.site_urls(SITEMAP) == ["https://pain001.com/", "https://pain001.com/pain-001/"]


def test_batches_never_exceed_ten_thousand():
    urls = [f"https://pain001.com/{i}/" for i in range(25_001)]
    sizes = [len(b) for b in indexnow.batches(urls)]
    assert sizes == [10_000, 10_000, 5_001]


def test_payload_names_host_key_and_key_location():
    body = indexnow.payload("k" * 32, ["https://pain001.com/"])
    assert body == {
        "host": "pain001.com",
        "key": "k" * 32,
        "keyLocation": "https://pain001.com/" + "k" * 32 + ".txt",
        "urlList": ["https://pain001.com/"],
    }


def test_submit_posts_json_and_returns_the_status(monkeypatch):
    seen = {}

    class Response:
        status = 202

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def fake_urlopen(request, timeout):
        seen["url"] = request.full_url
        seen["method"] = request.get_method()
        seen["body"] = json.loads(request.data)
        return Response()

    monkeypatch.setattr(indexnow.urllib.request, "urlopen", fake_urlopen)
    assert indexnow.submit(indexnow.payload("k" * 32, ["https://pain001.com/"])) == 202
    assert seen["url"] == "https://api.indexnow.org/indexnow"
    assert seen["method"] == "POST"
    assert seen["body"]["urlList"] == ["https://pain001.com/"]


def test_an_unreachable_engine_or_http_error_never_raises(monkeypatch):
    def refused(request, timeout):
        raise urllib.error.URLError("refused")

    monkeypatch.setattr(indexnow.urllib.request, "urlopen", refused)
    assert str(indexnow.submit({})).startswith("unreachable")

    def forbidden(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 403, "Forbidden", {}, None)

    monkeypatch.setattr(indexnow.urllib.request, "urlopen", forbidden)
    assert indexnow.submit({}) == 403


def test_main_exits_zero_when_the_sitemap_cannot_be_read(tmp_path, capsys):
    assert indexnow.main(["--sitemap", str(tmp_path / "missing.xml")]) == 0
    assert "skipped" in capsys.readouterr().out


def test_main_submits_every_batch(tmp_path, monkeypatch, capsys):
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(SITEMAP, encoding="utf-8")
    sent = []
    monkeypatch.setattr(indexnow, "submit", lambda body: sent.append(body) or 200)
    assert indexnow.main(["--sitemap", str(sitemap)]) == 0
    assert len(sent) == 1 and len(sent[0]["urlList"]) == 2
    assert "-> 200" in capsys.readouterr().out
