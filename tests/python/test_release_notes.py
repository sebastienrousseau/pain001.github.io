# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests for scripts/release_notes.py.

Guards the release-page format (commit 68e9b159): every release page
has the same title, hand-written Highlights, GitHub's generated change
list, the checksums before the Full Changelog line, and a first release
lists its commits in the same shape. Before it, titles carried a "v" and
some releases (v0.0.5) shipped without their checksums in the notes.
"""

import json

import pytest

import release_notes as rn

HIGHLIGHTS = """## Highlights ⭐️

* **First thing**: A plain sentence.
* **Second thing**: Another sentence.
"""
REPO = "sebastienrousseau/pain001.github.io"
SUMS = "abc123  ./pain001-site-v0.0.8.tar.gz\ndef456  ./pain001-site-v0.0.8.cdx.json\n"


@pytest.fixture
def notes_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(rn, "NOTES", tmp_path)
    monkeypatch.setattr(rn, "ROOT", tmp_path.parent)
    return tmp_path


def _write(notes_dir, tag, text):
    (notes_dir / f"{tag}.md").write_text(text, encoding="utf-8")


def test_title_drops_the_v():
    assert rn.title("v0.0.8") == "pain001.com 0.0.8"


def test_highlights_accepts_the_format(notes_dir):
    _write(notes_dir, "v0.0.8", HIGHLIGHTS)
    assert rn.highlights("v0.0.8").startswith("## Highlights ⭐️\n* **First thing**")


@pytest.mark.parametrize("text, reason", [
    ("# pain001.com 0.0.8\n\n" + HIGHLIGHTS, "must start with"),
    (HIGHLIGHTS.replace("* **First thing**:", "* First thing:"), "bullets read"),
    ("## Highlights ⭐️\n\n* **Only one**: sentence.\n", "2 to 4"),
    (HIGHLIGHTS + "\n## What's Changed\n\n* x\n", "Highlights only"),
])
def test_highlights_rejects_what_is_out_of_format(notes_dir, text, reason):
    _write(notes_dir, "v0.0.8", text)
    with pytest.raises(SystemExit, match=reason):
        rn.highlights("v0.0.8")


def test_missing_highlights_file_fails(notes_dir):
    with pytest.raises(SystemExit, match="missing"):
        rn.highlights("v0.0.9")


def test_compose_orders_sections_and_puts_checksums_before_the_changelog(notes_dir, monkeypatch):
    _write(notes_dir, "v0.0.8", HIGHLIGHTS)
    generated = (
        "## What's Changed\n* feat: x by @someone in https://github.com/r/pull/41\n\n"
        "## New Contributors\n* @someone made their first contribution in https://github.com/r/pull/41\n\n\n"
        f"**Full Changelog**: https://github.com/{REPO}/compare/v0.0.7...v0.0.8"
    )
    monkeypatch.setattr(rn, "previous_tag", lambda tag: "v0.0.7")
    monkeypatch.setattr(rn, "gh", lambda *args: json.dumps({"body": generated}))

    body = rn.compose("v0.0.8", SUMS)

    headings = [line for line in body.splitlines() if line.startswith("## ")]
    assert headings == ["## Highlights ⭐️", "## What's Changed", "## New Contributors", "## Checksums"]
    assert body.index("## Checksums") < body.index("**Full Changelog**")
    assert "```\nabc123  ./pain001-site-v0.0.8.tar.gz\ndef456" in body
    assert body.rstrip().splitlines()[-1].startswith("**Full Changelog**: ")


def test_compose_without_checksums_has_no_checksum_section(notes_dir, monkeypatch):
    _write(notes_dir, "v0.0.8", HIGHLIGHTS)
    monkeypatch.setattr(rn, "previous_tag", lambda tag: "v0.0.7")
    monkeypatch.setattr(rn, "gh", lambda *args: json.dumps({"body": (
        "## What's Changed\n* x by @a in https://github.com/r/pull/1\n\n"
        "**Full Changelog**: https://github.com/r/compare/v0.0.7...v0.0.8")}))

    assert "## Checksums" not in rn.compose("v0.0.8", "")


def test_first_release_lists_its_commits(notes_dir, monkeypatch):
    _write(notes_dir, "v0.0.1", HIGHLIGHTS)
    commits = [
        {"sha": "b" * 40, "commit": {"message": "feat: second\n\nbody"}, "author": {"login": "maint"}},
        {"sha": "a" * 40, "commit": {"message": "Initial commit"}, "author": None},
    ]

    def fake_gh(*args):
        if "generate-notes" in args[1]:
            return json.dumps({"body": f"**Full Changelog**: https://github.com/{REPO}/commits/v0.0.1"})
        return json.dumps(commits)

    monkeypatch.setattr(rn, "previous_tag", lambda tag: None)
    monkeypatch.setattr(rn, "gh", fake_gh)

    body = rn.compose("v0.0.1", "")

    assert f"* Initial commit by @unknown in https://github.com/{REPO}/commit/{'a' * 40}" in body
    assert body.index("Initial commit") < body.index("feat: second")
    assert "## What's Changed" in body


def test_compose_refuses_notes_without_a_changelog_line(notes_dir, monkeypatch):
    _write(notes_dir, "v0.0.8", HIGHLIGHTS)
    monkeypatch.setattr(rn, "previous_tag", lambda tag: "v0.0.7")
    monkeypatch.setattr(rn, "gh", lambda *args: json.dumps({"body": "## What's Changed\n* x"}))
    with pytest.raises(SystemExit, match="Full Changelog"):
        rn.compose("v0.0.8", "")


def test_previous_tag_orders_by_semver_not_text(monkeypatch):
    class Done:
        stdout = "v0.0.9\nv0.0.10\nv0.0.2\nv0.0.1\nnot-a-tag\n"

    monkeypatch.setattr(rn.subprocess, "run", lambda *a, **k: Done())
    assert rn.previous_tag("v0.0.10") == "v0.0.9"
    assert rn.previous_tag("v0.0.1") is None


def test_check_mode_validates_every_file(notes_dir, capsys):
    _write(notes_dir, "v0.0.1", HIGHLIGHTS)
    _write(notes_dir, "v0.0.2", HIGHLIGHTS)
    assert rn.main(["--check"]) == 0
    assert "2 Highlights file(s)" in capsys.readouterr().out
