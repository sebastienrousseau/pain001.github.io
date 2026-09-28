# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_security_txt.py (issue #60).

The validator checks that both /security.txt and /.well-known/security.txt
exist, are non-empty and identical, declare at least one Contact field,
exactly one Expires field within the next year, and the expected Canonical URL.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

import validate_security_txt as gate

CANONICAL = "https://pain001.com/.well-known/security.txt"


def make_security_txt(
    contact: str | None = "https://github.com/sebastienrousseau/pain001/security/advisories/new",
    expires: str | list[str] | None = None,
    canonical: str | None = CANONICAL,
    extra: str = "",
) -> str:
    """Build a security.txt payload."""
    if expires is None:
        future = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=180)
        expires = [future.strftime("%Y-%m-%dT%H:%M:%SZ")]
    elif isinstance(expires, str):
        expires = [expires]

    lines = ["# Security contact for pain001.com (RFC 9116)"]
    if contact:
        lines.append(f"Contact: {contact}")
    for exp in expires:
        lines.append(f"Expires: {exp}")
    if canonical:
        lines.append(f"Canonical: {canonical}")
    if extra:
        lines.append(extra)
    return "\n".join(lines) + "\n"


@pytest.fixture
def site(tmp_path: Path):
    """Factory creating a fake site/ tree with security.txt files."""
    def _create(well_known_body: str | bytes | None, root_body: str | bytes | None = None) -> Path:
        if root_body is None and well_known_body is not None:
            root_body = well_known_body
        wk = tmp_path / ".well-known" / "security.txt"
        root = tmp_path / "security.txt"
        if well_known_body is not None:
            wk.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(well_known_body, bytes):
                wk.write_bytes(well_known_body)
            else:
                wk.write_text(well_known_body, encoding="utf-8")
        if root_body is not None:
            root.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(root_body, bytes):
                root.write_bytes(root_body)
            else:
                root.write_text(root_body, encoding="utf-8")
        return tmp_path

    return _create


def test_valid_file_passes(site, capsys):
    content = make_security_txt()
    s = site(content, content)
    assert gate.main(s) == 0
    assert "result: CLEAN" in capsys.readouterr().out


def test_missing_well_known_security_txt_fails(site, capsys):
    content = make_security_txt()
    s = site(None, content)
    assert gate.main(s) == 1
    out = capsys.readouterr().out
    assert ".well-known/security.txt: missing or empty" in out
    assert "result: FAIL" in out


def test_empty_well_known_security_txt_fails(site, capsys):
    content = make_security_txt()
    s = site("", content)
    assert gate.main(s) == 1
    out = capsys.readouterr().out
    assert ".well-known/security.txt: missing or empty" in out
    assert "result: FAIL" in out


def test_two_copies_differ_fails(site, capsys):
    s = site(make_security_txt(extra="# copy A"), make_security_txt(extra="# copy B"))
    assert gate.main(s) == 1
    out = capsys.readouterr().out
    assert "the two security.txt copies differ" in out
    assert "result: FAIL" in out


def test_no_contact_line_fails(site, capsys):
    content = make_security_txt(contact=None)
    s = site(content, content)
    assert gate.main(s) == 1
    out = capsys.readouterr().out
    assert "no Contact field" in out
    assert "result: FAIL" in out


def test_two_expires_lines_fail(site, capsys):
    now = dt.datetime.now(dt.timezone.utc)
    exp1 = (now + dt.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    exp2 = (now + dt.timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = make_security_txt(expires=[exp1, exp2])
    s = site(content, content)
    assert gate.main(s) == 1
    out = capsys.readouterr().out
    assert "expected exactly one Expires field, found 2" in out
    assert "result: FAIL" in out


def test_expired_date_fails(site, capsys):
    past = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = make_security_txt(expires=past)
    s = site(content, content)
    assert gate.main(s) == 1
    out = capsys.readouterr().out
    assert f"Expires {past} is in the past" in out
    assert "result: FAIL" in out


def test_expires_date_more_than_a_year_away_fails(site, capsys):
    far = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=400)).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = make_security_txt(expires=far)
    s = site(content, content)
    assert gate.main(s) == 1
    out = capsys.readouterr().out
    assert f"Expires {far} is more than a year away" in out
    assert "result: FAIL" in out
