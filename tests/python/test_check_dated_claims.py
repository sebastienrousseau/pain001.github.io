# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/check_dated_claims.py beyond the retry logic.

Pins compressed-body decoding, the Internet Archive path (fresh capture
best effort, capture date named in the report), a missing expected
sentence, a passed review date, and the CLI report and JSON output.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import urllib.error
import zlib

import check_dated_claims as gate

PAGE = "<html><script>var x;</script><p>The release   moves to <b>November</b> &amp; stays.</p></html>"
CLAIM = {"id": "c1", "source": "https://example.org/n", "expect": ["the release moves to November"],
         "review_by": "2099-01-01", "cited_on": ["/a/", "/b/"]}


def _fake_open(answers, calls):
    def fake(url, timeout, attempts):
        calls.append((url, timeout, attempts))
        answer = answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer

    return fake


def test_get_decodes_gzip_deflate_and_plain(monkeypatch):
    calls = []
    answers = [(gzip.compress(b"gz"), "u1", ""), (zlib.compress(b"df"), "u2", "deflate"), (b"pl", "u3", "br")]
    monkeypatch.setattr(gate, "_open", _fake_open(answers, calls))
    assert [gate._get("x") for _ in range(3)] == [("u1", "gz"), ("u2", "df"), ("u3", "pl")]
    assert calls[0] == ("x", 60, gate.ATTEMPTS)


def test_visible_text_drops_markup_and_scripts():
    assert gate.visible_text(PAGE) == "The release moves to November & stays."


def test_wayback_names_the_capture_date(monkeypatch):
    calls = []
    final = "https://web.archive.org/web/20261001123456id_/https://example.org/n"
    answers = [urllib.error.URLError("refused"), (PAGE.encode(), final, "")]
    monkeypatch.setattr(gate, "_open", _fake_open(answers, calls))
    note, text = gate.fetch_wayback("https://example.org/n")
    assert note == "read from the Internet Archive capture of 2026-10-01"
    assert text.startswith("The release moves")
    assert calls[0] == (gate.WAYBACK_SAVE + "https://example.org/n", 90, 1)
    assert calls[1] == (gate.WAYBACK_RAW + "https://example.org/n", 90, gate.ATTEMPTS)


def test_wayback_with_unrecognised_final_url(monkeypatch):
    answers = [(b"saved", "s", ""), (PAGE.encode(), "https://elsewhere/", "")]
    monkeypatch.setattr(gate, "_open", _fake_open(answers, []))
    assert gate.fetch_wayback("u")[0] == "read from the Internet Archive capture of unknown date"


def test_check_uses_wayback_and_reports_drift_and_review(monkeypatch):
    monkeypatch.setattr(gate, "fetch_wayback", lambda url: ("archived", "Something else entirely"))
    claim = dict(CLAIM, via="wayback", review_by="2026-01-01", review_note="Swift said so")
    row = gate.check(claim, dt.date(2026, 6, 1))
    assert row["fetched"] == "archived" and not row["ok"]
    assert row["problems"] == ["expected sentence not found: 'the release moves to November'",
                               "review date 2026-01-01 has passed: Swift said so"]


def test_check_review_without_note_has_no_trailing_space(monkeypatch):
    monkeypatch.setattr(gate, "fetch_direct", lambda url: ("live", ""))
    row = gate.check({"id": "x", "source": "s", "review_by": "2026-01-01"}, dt.date(2026, 1, 2))
    assert row["problems"] == ["review date 2026-01-01 has passed:"]
    assert row["cited_on"] == []


def test_main_prints_report_and_writes_json(tmp_path, monkeypatch, capsys):
    claims_file = tmp_path / "dated_claims.json"
    claims_file.write_text(json.dumps({"claims": [CLAIM, dict(CLAIM, id="c2", expect=["gone"])]}), encoding="utf-8")
    monkeypatch.setattr(gate, "CLAIMS", claims_file)
    monkeypatch.setattr(gate, "fetch_direct", lambda url: ("read live", gate.visible_text(PAGE)))
    out = tmp_path / "report.json"
    assert gate.main(["--json", str(out)]) == 1
    printed = capsys.readouterr().out
    assert "ok   c1: read live" in printed
    assert "FAIL c2: read live" in printed
    assert "       - expected sentence not found: 'gone'" in printed
    assert "       pages citing it: /a/, /b/" in printed
    assert "1 of 2 dated claims hold" in printed
    report = json.loads(out.read_text(encoding="utf-8"))
    assert [r["ok"] for r in report["claims"]] == [True, False]
    assert report["date"] == dt.date.today().isoformat()


def test_main_all_hold_without_json(tmp_path, monkeypatch, capsys):
    claims_file = tmp_path / "dated_claims.json"
    claims_file.write_text(json.dumps({"claims": [CLAIM]}), encoding="utf-8")
    monkeypatch.setattr(gate, "CLAIMS", claims_file)
    monkeypatch.setattr(gate, "fetch_direct", lambda url: ("", gate.visible_text(PAGE)))
    assert gate.main([]) == 0
    assert "ok   c1: not fetched" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == [claims_file]
