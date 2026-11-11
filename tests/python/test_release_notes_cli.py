# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/release_notes.py's gh calls and command line.

Pins the gh invocation, that the first tag asks for notes without a
previous tag, that unexpected generated notes are refused, and the
--tag, --title, --sums and --out command forms.
"""

from __future__ import annotations

import json

import pytest

import release_notes as rn

HIGHLIGHTS = "## Highlights ⭐️\n\n* **One**: A sentence.\n* **Two**: Another.\n"
BODY = "## What's Changed\n* fix by @a in https://x/pull/1\n\n**Full Changelog**: https://x/compare/v0.0.7...v0.0.8"


@pytest.fixture
def notes_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(rn, "NOTES", tmp_path)
    monkeypatch.setattr(rn, "ROOT", tmp_path.parent)
    (tmp_path / "v0.0.8.md").write_text(HIGHLIGHTS, encoding="utf-8")
    return tmp_path


def test_gh_runs_the_cli_and_returns_stdout(monkeypatch):
    seen = []

    class Done:
        stdout = "out"

    def fake_run(cmd, **kwargs):
        seen.append((cmd, kwargs))
        return Done()

    monkeypatch.setattr(rn.subprocess, "run", fake_run)
    assert rn.gh("api", "x") == "out"
    assert seen == [(["gh", "api", "x"], {"check": True, "capture_output": True, "text": True})]


def test_generated_without_previous_tag(monkeypatch):
    calls = []
    monkeypatch.setattr(rn, "gh", lambda *args: calls.append(args) or json.dumps({"body": "b"}))
    assert rn.generated("v0.0.1", None) == "b"
    assert calls == [("api", f"repos/{rn.REPO}/releases/generate-notes", "-f", "tag_name=v0.0.1")]


def test_unexpected_generated_notes_are_refused(notes_dir, monkeypatch):
    monkeypatch.setattr(rn, "previous_tag", lambda tag: "v0.0.7")
    monkeypatch.setattr(rn, "gh", lambda *args: json.dumps({"body": "## Other\n\n**Full Changelog**: https://x"}))
    with pytest.raises(SystemExit, match=r"unexpected generated notes for v0\.0\.8: '## Other'"):
        rn.compose("v0.0.8", "")


@pytest.mark.parametrize("argv", [[], ["--tag", "0.0.8"], ["--tag", "v0.0.8-rc1"]])
def test_a_bad_or_missing_tag_is_refused(argv):
    with pytest.raises(SystemExit, match=r"--tag must be a release tag such as v0\.0\.9"):
        rn.main(argv)


def test_title_mode_prints_the_title(capsys):
    assert rn.main(["--tag", "v0.0.8", "--title"]) == 0
    assert capsys.readouterr().out == "pain001.com 0.0.8\n"


def test_notes_go_to_stdout_or_a_file(notes_dir, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rn, "previous_tag", lambda tag: "v0.0.7")
    monkeypatch.setattr(rn, "gh", lambda *args: json.dumps({"body": BODY}))
    assert rn.main(["--tag", "v0.0.8"]) == 0
    printed = capsys.readouterr().out
    assert printed.startswith(HIGHLIGHTS.replace("\n\n", "\n", 1))
    assert "## Checksums" not in printed
    sums = tmp_path / "SHA256SUMS"
    sums.write_text("abc  ./a.tar.gz\n", encoding="utf-8")
    out = tmp_path / "notes.md"
    assert rn.main(["--tag", "v0.0.8", "--sums", str(sums), "--out", str(out)]) == 0
    assert capsys.readouterr().out == ""
    written = out.read_text(encoding="utf-8")
    assert "abc  a.tar.gz\n" in written
    assert written.endswith("**Full Changelog**: https://x/compare/v0.0.7...v0.0.8\n")
