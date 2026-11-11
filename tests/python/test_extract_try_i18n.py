# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/extract_try_i18n.py: which fragments of the built
/try/ page become translation keys (leaf prose, classed prose spans not
already inside a fragment, aria labels), what is left out (status strip,
code blocks, commands, non-prose), the meta block and the fixed chrome
tables.

The script works at module level and resolves the site from its own
location, so each test runs the real file with ``runpy`` (which keeps
coverage attributed to it) while ``Path.resolve`` maps that one path
into ``tmp_path``.
"""

import json
import runpy
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "extract_try_i18n.py"

PAGE = """<html><head><title>
 Try pain001 </title><meta name="description" content="Run it in the browser.">
</head><body><nav><a>Glossary</a></nav>
<main id="main">
<section class="hero status-strip"><p>Status strip prose</p></section>
<h1>Try it in your browser</h1>
<p></p>
<li><p>Nested paragraph</p></li>
<p><span></span></p>
<p>12 34</p>
<p>pip install pain001</p>
<p>v0.0.86 release</p>
<p>Look <span class="hl">this sentence has more than five words</span> here</p>
<pre><p>Inside pre</p></pre>
<script>const s = "<p>Inside script</p>";</script>
<style>p { color: red }</style>
<div><span class="empty">Nothing to show yet, paste a payment file above</span></div>
<div><span class="badge">abcdefghijklmnopqrstuvwxyz</span></div>
<div><span class="num">1 2 3 4 5 6 7 8 9 10 11</span></div>
<button aria-label="Copy the output">Copy</button>
<span aria-label="123">x</span>
</main></body></html>
"""


def _relocate(tmp_path, monkeypatch):
    real_resolve = Path.resolve

    def resolve(self, strict=False):
        if self == SCRIPT:
            return tmp_path / "scripts" / SCRIPT.name
        return real_resolve(self, strict)

    monkeypatch.setattr(Path, "resolve", resolve)


def _run(tmp_path, monkeypatch, html):
    page = tmp_path / "site" / "try" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text(html, encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    _relocate(tmp_path, monkeypatch)
    runpy.run_path(str(SCRIPT), run_name="__main__")
    return json.loads((tmp_path / "scripts" / "try_i18n" / "en.json").read_text(encoding="utf-8"))


def test_leaf_prose_spans_and_aria_are_extracted(tmp_path, monkeypatch, capsys):
    out = _run(tmp_path, monkeypatch, PAGE)

    assert out["meta"] == {"title": "Try pain001", "description": "Run it in the browser."}
    assert list(out["text"]) == [
        "Try it in your browser",
        'Look <span class="hl">this sentence has more than five words</span> here',
        "Copy",
        "Nothing to show yet, paste a payment file above",
    ]
    assert all(k == v for k, v in out["text"].items())
    assert out["aria"] == {"Copy the output": "Copy the output"}
    assert len(out["chrome"]) == 29 and out["chrome"]["Glossary"] == "Glossary"
    assert out["chrome_aria"]["Toggle Docs submenu"] == "Toggle Docs submenu"
    assert len(out["chrome_aria"]) == 4
    assert capsys.readouterr().out == "text=4 aria=1 chrome=29 chrome_aria=4\n"


def test_reversed_description_attribute_order(tmp_path, monkeypatch):
    html = ('<html><head><title>T</title><meta content="Swapped order" name="description">'
            "</head><main><p>Body text</p></main></html>")
    out = _run(tmp_path, monkeypatch, html)
    assert out["meta"] == {"title": "T", "description": "Swapped order"}
    assert out["text"] == {"Body text": "Body text"}


def test_no_description_gives_an_empty_string(tmp_path, monkeypatch):
    out = _run(tmp_path, monkeypatch, "<html><title>T</title><main></main></html>")
    assert out["meta"]["description"] == ""
    assert out["text"] == {} and out["aria"] == {}


def test_a_missing_built_page_fails_loudly(tmp_path, monkeypatch):
    _relocate(tmp_path, monkeypatch)
    with pytest.raises(FileNotFoundError):
        runpy.run_path(str(SCRIPT), run_name="__main__")
    assert not (tmp_path / "scripts" / "try_i18n").exists()
