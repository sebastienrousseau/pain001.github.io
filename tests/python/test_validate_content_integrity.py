# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_content_integrity.py.

Pins the four structural tells of content the build ate: an unknown
element in the output, an element name swallowed inside <code>, a
literal backslash escape in prose, and a double-encoded entity in the
<head>. A clean site passes and a missing site/ is an error.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import validate_content_integrity as gate


@pytest.fixture
def site(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "SITE", tmp_path)
    return tmp_path


def _page(site: Path, rel: str, html: str) -> None:
    path = site / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def test_missing_site_is_an_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gate, "SITE", tmp_path / "absent")
    assert gate.main() == 1
    assert "site/ not built" in capsys.readouterr().err


def test_clean_site_passes(site, capsys):
    _page(site, "index.html",
          "<html><head><title>A &amp; B</title></head><body>"
          "<p>text</p><code>&lt;BIC&gt;</code><pre>a\\nb</pre></body></html>")
    # A page with no </head> is scanned whole.
    _page(site, "why/index.html", "<p>plain</p>")
    assert gate.main() == 0
    out = capsys.readouterr().out
    assert "scanned 2 page(s)" in out
    assert "result: CLEAN" in out


def test_unknown_element_and_swallowed_code_fail(site, capsys):
    _page(site, "a/index.html", "<html><body><p>Set <code><BIC></code></p></body></html>")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL unknown elements in output: {'bic': 1}" in out
    assert "['a/index.html']" in out
    assert "FAIL element name eaten by the parser inside <code> on 1 page(s)" in out
    assert "result: CLEAN" not in out


def test_literal_escape_in_prose_fails(site, capsys):
    _page(site, "try/index.html", "<html><body><p>line one\\nline two</p></body></html>")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL literal \\n in rendered text on 1 page(s): ['try/index.html']" in out


def test_double_encoded_entity_in_head_fails(site, capsys):
    _page(site, "index.html",
          '<html><head><meta property="og:title" content="A &amp;amp; B"></head>'
          "<body>&amp;amp; in the body is not checked</body></html>")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "FAIL double-encoded entity in <head> on 1 page(s): ['index.html']" in out


def test_double_encoding_only_in_body_passes(site):
    _page(site, "index.html", "<html><head></head><body>&amp;lt;</body></html>")
    assert gate.main() == 0


def test_prose_drops_code_scripts_and_tags():
    markup = "<p>a</p><script>x\\n</script><code>y</code><PRE>z</PRE>b"
    assert gate.prose(markup).split() == ["a", "b"]
