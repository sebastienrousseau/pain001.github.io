# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for the validate_claims.py command line.

Pins the exit codes: 1 when the build is missing, 1 with a FAIL line per
drift, 0 when every figure matches the register for the current release.
"""

from __future__ import annotations

import sys

import claims
import validate_claims

REGISTER = {"claims": [
    {"id": "stars", "claim": "stars", "value": 1234, "format": "count", "source": "live",
     "pages": ["/", "/about.html"], "evidence_url": "https://github.com/x/y", "verified_in": "0.0.86"},
]}


def _setup(tmp_path, monkeypatch, pages):
    site = tmp_path / "site"
    site.mkdir()
    for name, body in pages.items():
        (site / name).write_text(body, encoding="utf-8")
    register = tmp_path / "claims.yml"
    claims.dump(REGISTER, register)
    version = tmp_path / "VERSION"
    version.write_text("0.0.86\n", encoding="utf-8")
    monkeypatch.setattr(validate_claims, "REGISTER", register)
    monkeypatch.setattr(validate_claims, "VERSION", version)
    monkeypatch.setattr(sys, "argv", ["validate_claims.py", str(site)])
    return site


def test_missing_build_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["validate_claims.py", str(tmp_path)])
    assert validate_claims.main() == 1
    assert f"error: {tmp_path}/index.html not found" in capsys.readouterr().out


def test_default_site_is_under_root(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["validate_claims.py"])
    monkeypatch.setattr(validate_claims, "ROOT", tmp_path)
    assert validate_claims.main() == 1
    assert f"error: {tmp_path / 'site'}/index.html not found" in capsys.readouterr().out


def test_matching_site_passes(tmp_path, monkeypatch, capsys):
    good = '<dd data-claim="stars">1,234</dd>'
    _setup(tmp_path, monkeypatch, {"index.html": good, "about.html": good})
    assert validate_claims.main() == 0
    assert capsys.readouterr().out == "validate_claims: 0 problem(s)\n"


def test_drift_is_reported_per_line(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch, {"index.html": '<dd data-claim="stars">9</dd>'})
    assert validate_claims.main() == 1
    out = capsys.readouterr().out.splitlines()
    assert out == ["FAIL /: stars shows '9', the register says '1,234'",
                   "FAIL stars: listed for /about.html but not shown there",
                   "validate_claims: 2 problem(s)"]
