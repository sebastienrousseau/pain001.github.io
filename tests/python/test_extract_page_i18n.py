# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/extract_page_i18n.py: which fragments of a built
page become translation keys (leaf prose only, no commands, no code
blocks, no title/eyebrow/deck repeats), the meta block, aria labels, and
the default and named output tables.

The script works at module level and resolves the site from its own
location, so each test runs the real file with ``runpy`` (which keeps
coverage attributed to it) while ``Path.resolve`` maps that one path
into ``tmp_path``.
"""

import json
import runpy
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "extract_page_i18n.py"

PAGE = """<html><head><title> Why Pain001 </title>
<meta name="description" content="Why it exists.">
</head><body><p class="eyebrow"> Overview </p><p class="deck">The deck line</p>
<main id="main">
<h1>Overview</h1>
<p>The deck line</p>
<h2>Plain <a href="/x/">linked</a> heading</h2>
<p></p>
<p>   </p>
<li><p>Nested paragraph text</p></li>
<p><span></span></p>
<p>12 34</p>
<li><code>pain001 --help</code></li>
<li><code>pip install pain001</code> then read the guide</li>
<p>pip install pain001</p>
<p>v0.0.86 notes</p>
<td><code>abc</code> x</td>
<pre><p>Inside pre block</p></pre>
<script>var s = "<p>Inside script</p>";</script>
<style>p { color: red }</style>
<blockquote><p>Quoted prose here</p></blockquote>
<button aria-label="Open the menu">Menu</button>
<span aria-label="123">x</span>
<dd>Defined term text</dd>
</main><footer><p>Footer prose</p></footer></body></html>
"""


def _run(tmp_path, monkeypatch, argv):
    (tmp_path / "scripts").mkdir(exist_ok=True)
    real_resolve = Path.resolve

    def resolve(self, strict=False):
        if self == SCRIPT:
            return tmp_path / "scripts" / SCRIPT.name
        return real_resolve(self, strict)

    monkeypatch.setattr(Path, "resolve", resolve)
    monkeypatch.setattr(sys, "argv", ["extract_page_i18n.py", *argv])
    runpy.run_path(str(SCRIPT), run_name="__main__")


def _page(tmp_path, slug, html):
    path = tmp_path / "site" / slug / "index.html"
    path.parent.mkdir(parents=True)
    path.write_text(html, encoding="utf-8")


def test_named_set_extracts_leaf_prose_meta_and_aria(tmp_path, monkeypatch, capsys):
    _page(tmp_path, "glossary", PAGE)
    _run(tmp_path, monkeypatch, ["docs_i18n", "glossary"])

    out = json.loads((tmp_path / "scripts" / "docs_i18n" / "en.json").read_text(encoding="utf-8"))
    page = out["glossary"]
    assert page["meta"] == {
        "title": "Why Pain001",
        "description": "Why it exists.",
        "eyebrow": "Overview",
        "deck": "The deck line",
    }
    assert list(page["text"]) == [
        'Plain <a href="/x/">linked</a> heading',
        "<code>pip install pain001</code> then read the guide",
        "Quoted prose here",
        "Menu",
        "Defined term text",
    ]
    assert all(k == v for k, v in page["text"].items())
    assert page["aria"] == {"Open the menu": "Open the menu"}
    printed = capsys.readouterr().out
    assert "glossary: text=5 aria=1 words=17" in printed
    assert "wrote scripts/docs_i18n/en.json" in printed


def test_reversed_description_and_missing_eyebrow_and_deck(tmp_path, monkeypatch):
    html = ('<html><head><title>T</title><meta content="Swapped order" name="description">'
            "</head><main><p>Body text here</p></main></html>")
    _page(tmp_path, "faqs", html)
    _run(tmp_path, monkeypatch, ["docs_i18n", "faqs"])

    out = json.loads((tmp_path / "scripts" / "docs_i18n" / "en.json").read_text(encoding="utf-8"))
    assert out["faqs"]["meta"] == {"title": "T", "description": "Swapped order", "eyebrow": "", "deck": ""}
    assert out["faqs"]["text"] == {"Body text here": "Body text here"}


def test_default_set_is_the_four_journey_pages(tmp_path, monkeypatch, capsys):
    html = "<html><head><title>T</title></head><main><p>Shared prose</p></main></html>"
    for slug in ("why", "solutions", "executive-brief", "pain-001"):
        _page(tmp_path, slug, html)
    _run(tmp_path, monkeypatch, [])

    out = json.loads((tmp_path / "scripts" / "pages_i18n" / "en.json").read_text(encoding="utf-8"))
    assert list(out) == ["why", "solutions", "executive-brief", "pain-001"]
    assert out["why"]["meta"]["description"] == ""
    assert "wrote scripts/pages_i18n/en.json" in capsys.readouterr().out


def test_a_missing_built_page_fails_loudly(tmp_path, monkeypatch):
    with pytest.raises(FileNotFoundError):
        _run(tmp_path, monkeypatch, ["docs_i18n", "absent"])
    assert not (tmp_path / "scripts" / "docs_i18n").exists()
