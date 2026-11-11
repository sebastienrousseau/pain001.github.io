# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_security_txt.py's site selection and edges.

Pins that the site comes from the argument, then argv, then the default
site/ directory; that a site with neither copy reports both missing; and
that a wrong Canonical is reported.
"""

from __future__ import annotations

import datetime as dt
import sys

import validate_security_txt as v


def _body(canonical: str) -> str:
    expires = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=100)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"# comment\nContact: mailto:security@example.org\nExpires: {expires}\nCanonical: {canonical}\n"


def _write(site, body):
    (site / ".well-known").mkdir(parents=True)
    for path in (site / ".well-known" / "security.txt", site / "security.txt"):
        path.write_text(body, encoding="utf-8")


def test_site_from_argv(tmp_path, monkeypatch, capsys):
    _write(tmp_path, _body(v.CANONICAL))
    monkeypatch.setattr(sys, "argv", ["validate_security_txt.py", str(tmp_path)])
    assert v.main() == 0
    assert capsys.readouterr().out == "result: CLEAN\n"


def test_default_site_with_no_copies(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["validate_security_txt.py"])
    monkeypatch.setattr(v, "SITE", tmp_path)
    assert v.main() == 1
    assert capsys.readouterr().out.splitlines() == [
        "FAIL .well-known/security.txt: missing or empty",
        "FAIL security.txt: missing or empty",
        "result: FAIL",
    ]


def test_wrong_canonical_fails(tmp_path, capsys):
    _write(tmp_path, _body("https://pain001.com/security.txt"))
    assert v.main(tmp_path) == 1
    assert f"FAIL Canonical does not name {v.CANONICAL}" in capsys.readouterr().out
