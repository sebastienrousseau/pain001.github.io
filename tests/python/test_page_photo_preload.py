# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The hero image must be discoverable before blocking stylesheets."""

import json
from html.parser import HTMLParser

import postbuild_fix as build


class Tags(HTMLParser):
    """Collect attributes without depending on generated whitespace."""

    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def test_responsive_hero_preload_matches_picture(tmp_path, monkeypatch):
    """Reuse the picture's exact candidates for English and translated pages."""
    mapping = tmp_path / "photos.json"
    mapping.write_text(json.dumps({"pages": {"try": "test-photo"}}))
    monkeypatch.setattr(build, "PAGE_PHOTO_MAP", mapping)
    monkeypatch.setattr(build, "band_path", lambda photo: "/img/" + photo)
    for route in ("try", "fr/try"):
        page = tmp_path / route / "index.html"
        page.parent.mkdir(parents=True)
        page.write_text('<html><head><link rel="stylesheet" href="/site.css">'
                        '</head><body><section class="page-hero"></section></body></html>')
    build.add_page_photos(tmp_path)
    for page in tmp_path.rglob("index.html"):
        tags = Tags()
        tags.feed(page.read_text())
        preloads = [a for t, a in tags.tags if t == "link" and a.get("as") == "image"]
        assert len(preloads) == 1
        preload = preloads[0]
        picture_source = next(a for t, a in tags.tags if t == "source")
        assert preload["rel"] == "preload"
        assert preload["type"] == picture_source["type"] == "image/avif"
        assert preload["imagesrcset"] == picture_source["srcset"]
        assert preload["imagesizes"] == picture_source["sizes"]
        assert preload["fetchpriority"] == "high"
        assert tags.tags.index(("link", preload)) < next(
            i for i, (t, a) in enumerate(tags.tags)
            if t == "link" and a.get("rel") == "stylesheet"
        )
        original = page.read_text()
        build.add_page_photos(tmp_path)
        assert page.read_text() == original
