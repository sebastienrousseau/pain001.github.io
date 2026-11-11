# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_links.py.

Every internal href/src on a built page must resolve to a file in the
site tree, every #anchor must exist on its target page (the demo's
#sample= deep link excepted), absolute pain001.com links count as
internal, and a locale page must not link the English /try/ demo.
External links are only counted, unless --external asks curl for each.

The script works at module level and finds the locale tables next to
itself, so the tests run its real source with ``__file__`` pointing into
a temporary directory holding a try_i18n/ table. The stand-in file name
differs from the script's, which makes coverage attribute the lines to
the compiled source path, scripts/.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "validate_links.py"


def _write(site: Path, rel: str, body: str) -> None:
    path = site / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"<html><body>{body}</body></html>", encoding="utf-8")


def _run(tmp_path: Path, monkeypatch, capsys, site: Path, *flags: str) -> tuple[int, str]:
    (tmp_path / "try_i18n").mkdir(exist_ok=True)
    (tmp_path / "try_i18n" / "fr.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(site), *flags])
    code = compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")
    with pytest.raises(SystemExit) as exc:
        exec(code, {"__name__": "__main__", "__file__": str(tmp_path / "harness.py")})
    return exc.value.code, capsys.readouterr().out


@pytest.fixture
def site(tmp_path) -> Path:
    root = tmp_path / "site"
    _write(root, "index.html", '<h1 id="top">Home</h1><a href="#top">up</a><a href="#">none</a>'
           '<a href="#top">again, from the id cache</a>')
    _write(root, "why/index.html", '<h2 id=case>Case</h2><a href="/">home</a>')
    _write(root, "try/index.html", '<div id="demo"></div>')
    _write(root, "about/index.html", "About")
    (root / "style.css").write_text("body{}", encoding="utf-8")
    return root


def test_a_clean_site_passes(tmp_path, monkeypatch, capsys, site):
    _write(site, "news/index.html", " ".join([
        '<a href="/why/#case">why</a>', "<a href=/about>about</a>",
        '<link href="/style.css">', '<a href="https://pain001.com">home</a>',
        '<a href="https://pain001.com/why/">why</a>', '<a href="https://example.org/a">ext</a>',
        '<a href="http://example.org/a">ext</a>', '<a href="mailto:a@b.c">mail</a>',
        '<a href=" ">blank</a>', '<a href="/try/#sample=corpus:fr-1">demo</a>',
        '<a href="/try/#demo">demo</a>',
    ]))
    code, out = _run(tmp_path, monkeypatch, capsys, site)
    assert code == 0
    assert out == "pages scanned: 5\nunique external links: 2\nresult: CLEAN\n"


def test_broken_links_and_anchors_are_reported(tmp_path, monkeypatch, capsys, site):
    _write(site, "news/index.html", " ".join([
        '<a href="/gone/">gone</a>', '<a href="/why/#nope">bad anchor</a>',
        '<a href="#missing">bad local</a>', '<a href="/about/#sample=x">not the demo</a>',
    ]))
    code, out = _run(tmp_path, monkeypatch, capsys, site)
    assert code == 1
    assert "BROKEN  /news/index.html  ->  /gone/" in out
    assert "ANCHOR  /news/index.html  ->  /why/#nope" in out
    assert "ANCHOR  /news/index.html  ->  #missing" in out
    assert "ANCHOR  /news/index.html  ->  /about/#sample=x" in out
    assert out.endswith("result: 4 problem(s)\n")


def test_a_locale_page_must_not_link_the_english_demo(tmp_path, monkeypatch, capsys, site):
    _write(site, "fr/index.html", '<a href="/fr/try/">Essayer</a>')
    _write(site, "fr/try/index.html", '<a href="/try/">English</a>')
    _write(site, "fr/why/index.html", "Pourquoi")
    # Not locale pages: no table for "de", no home page for "es", an
    # excluded top-level directory, and a single-segment path.
    _write(site, "de/index.html", '<a href="/try/">Try</a>')
    _write(site, "de/x/index.html", '<a href="/try/">Try</a>')
    _write(site, "es/x/index.html", '<a href="/try/">Try</a>')
    _write(site, "tags/x/index.html", '<a href="/try/">Try</a>')
    (tmp_path / "try_i18n").mkdir()
    (tmp_path / "try_i18n" / "es.json").write_text("{}", encoding="utf-8")
    code, out = _run(tmp_path, monkeypatch, capsys, site)
    assert code == 1
    assert "LOCALE  /fr/try/index.html  links English /try/" in out
    assert out.count("LOCALE") == 1
    assert out.endswith("result: 1 problem(s)\n")


def test_external_links_are_checked_with_curl_on_request(tmp_path, monkeypatch, capsys, site):
    _write(site, "news/index.html", '<a href="https://ok.example/">a</a><a href="https://down.example/">b</a>')
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        code = "404" if "down" in cmd[-1] else "301"
        return subprocess.CompletedProcess(cmd, 0, stdout=f"{code}\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    code, out = _run(tmp_path, monkeypatch, capsys, site, "--external")
    assert [c[-1] for c in calls] == ["https://down.example/", "https://ok.example/"]
    assert calls[0][:2] == ["curl", "-s"]
    assert "EXT-FAIL 404  https://down.example/" in out
    assert "ok.example" not in out.split("unique external links")[1]
    # External failures are reported but do not fail the gate.
    assert code == 0
