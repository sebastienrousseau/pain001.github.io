# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/audit_deps.py, the npm advisory gate.

Pins that an advisory at or above the floor fails unless it is excepted
with a reason and an unexpired date, that an exception which no longer
matches anything fails, and that an empty `npm audit` answer is an error.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess

import pytest

import audit_deps

GHSA_ID = "GHSA-abcd-efgh-ijkl"
REPORT = {
    "vulnerabilities": {
        "extract-zip": {
            "severity": "high",
            "via": [
                "yauzl",
                {"url": f"https://github.com/advisories/{GHSA_ID.lower()}", "title": "zip slip"},
                {"url": None, "source": 1234, "title": "no url"},
            ],
        },
        "low-pkg": {"severity": "low", "via": [{"url": "", "source": 1, "title": "minor"}]},
        "odd-pkg": {"severity": "unknown", "via": [{"source": 2}]},
    }
}


def _proc(stdout: str, stderr: str = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(["npm"], 1, stdout=stdout, stderr=stderr)


def test_findings_keep_only_advisories_at_or_above_the_floor():
    assert audit_deps.findings(REPORT, "high") == [
        (GHSA_ID.upper(), "extract-zip", "high", "zip slip"),
        ("NPM:1234", "extract-zip", "high", "no url"),
    ]
    assert len(audit_deps.findings(REPORT, "low")) == 3
    assert audit_deps.findings({}, "info") == []


def test_run_audit_parses_npm_json(monkeypatch):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return _proc(json.dumps(REPORT))

    monkeypatch.setattr(audit_deps.subprocess, "run", fake_run)
    assert audit_deps.run_audit() == REPORT
    assert calls == [["npm", "audit", "--json"]]


def test_run_audit_with_no_output_exits(monkeypatch, capsys):
    monkeypatch.setattr(audit_deps.subprocess, "run", lambda *a, **k: _proc("  \n", "npm ERR! boom"))
    with pytest.raises(SystemExit) as exc:
        audit_deps.run_audit()
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "npm audit produced no output" in err and "npm ERR! boom" in err


@pytest.fixture
def config(tmp_path, monkeypatch):
    path = tmp_path / "exceptions.json"
    monkeypatch.setattr(audit_deps, "EXCEPTIONS_PATH", path)

    def write(exceptions, report, floor="high"):
        path.write_text(json.dumps({"severityFloor": floor, "exceptions": exceptions}), encoding="utf-8")
        monkeypatch.setattr(audit_deps, "run_audit", lambda: report)

    return write


def test_missing_exceptions_file_fails(config, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(audit_deps, "EXCEPTIONS_PATH", tmp_path / "absent.json")
    assert audit_deps.main() == 1
    assert "is missing" in capsys.readouterr().err


def test_clean_report_passes(config, capsys):
    config([], {"vulnerabilities": {}})
    assert audit_deps.main() == 0
    assert "no unexcepted advisories at severity >= high (0 documented" in capsys.readouterr().out


def test_fully_excepted_report_passes(config, capsys):
    future = (dt.date.today() + dt.timedelta(days=30)).isoformat()
    report = {"vulnerabilities": {"extract-zip": {"severity": "critical", "via": [REPORT["vulnerabilities"]["extract-zip"]["via"][1]]}}}
    config([{"advisory": GHSA_ID.lower(), "reason": "no fix", "expires": future}], report)
    assert audit_deps.main() == 0
    assert "(1 documented exception(s))" in capsys.readouterr().out


def test_every_kind_of_problem_is_reported(config, capsys):
    past = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    future = (dt.date.today() + dt.timedelta(days=1)).isoformat()
    config([
        {"advisory": GHSA_ID, "reason": "old", "expires": past},
        {"advisory": "GHSA-zzzz-zzzz-zzzz", "reason": "gone", "expires": future},
        {"reason": "nameless"},
        {"advisory": "GHSA-noex-piry-0000", "reason": "x"},
        {"advisory": "GHSA-badd-date-0000", "reason": "x", "expires": "soon"},
        {"advisory": "GHSA-nore-ason-0000", "expires": future},
    ], REPORT)
    assert audit_deps.main() == 1
    err = capsys.readouterr().err
    assert "[deps] 7 problem(s) at severity >= high" in err
    for text in ("exception <unnamed> lacks", "exception GHSA-NOEX-PIRY-0000 lacks",
                 "exception GHSA-BADD-DATE-0000 lacks", "exception GHSA-NORE-ASON-0000 lacks",
                 f"exception for {GHSA_ID.upper()} expired on {past}",
                 "[NPM:1234] not excepted",
                 "exception GHSA-ZZZZ-ZZZZ-ZZZZ no longer matches any advisory"):
        assert text in err


def test_an_npm_source_advisory_can_be_excepted(config, capsys):
    """Regression: exception ids are upper-cased, so a finding id of the
    form npm:<source> must be too, or its exception never matches and the
    gate reports both the advisory and a stale exception."""
    later = (dt.date.today() + dt.timedelta(days=30)).isoformat()
    report = {"vulnerabilities": {"pkg": {"severity": "high", "via": [{"url": None, "source": 1234, "title": "no url"}]}}}
    config([{"advisory": "npm:1234", "reason": "dev only", "expires": later}], report)
    assert audit_deps.main() == 0, capsys.readouterr()
