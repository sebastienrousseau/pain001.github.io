# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_spdx_headers.py (issue #51).

The gate fails CI when a tracked source file lacks its own copyright or
licence header. These tests pin what it accepts, what it reports, what it
exempts, and how far into a file it looks.

The header tags are assembled from pieces so that REUSE does not read the
fixtures below as this file's own licence information.
"""

import subprocess

import pytest

import validate_spdx_headers as gate

COPYRIGHT = "SPDX-File" + "CopyrightText: 2026 Example"
LICENCE = "SPDX-License" + "-Identifier: MIT"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A working directory whose `git ls-files` answer the test controls."""
    monkeypatch.chdir(tmp_path)
    listed: list[str] = []

    def fake_run(args, **kwargs):
        assert args[:2] == ["git", "ls-files"]
        return subprocess.CompletedProcess(args, 0, stdout="\n".join(listed) + "\n", stderr="")

    monkeypatch.setattr(gate.subprocess, "run", fake_run)

    def add(path: str, text: str) -> None:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        listed.append(path)

    return add


def test_a_file_with_both_tags_passes(repo, capsys):
    repo("scripts/ok.py", f"# {COPYRIGHT}\n# {LICENCE}\nprint(1)\n")
    assert gate.main() == 0
    assert "1 of 1 source files" in capsys.readouterr().out


def test_a_missing_tag_is_reported_by_name(repo, capsys):
    repo("scripts/no_licence.py", f"# {COPYRIGHT}\nprint(1)\n")
    repo("static/js/no_copyright.js", f"// {LICENCE}\n")
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert "scripts/no_licence.py: missing SPDX-License-Identifier" in out
    assert "static/js/no_copyright.js: missing SPDX-FileCopyrightText" in out
    assert "0 of 2 source files" in out


@pytest.mark.parametrize("path", [
    "static/pyodide/pyodide.js",
    "static/js/cf-beacon.min.js",
    "_posts/page.html",
    "docs/notes.yml",
    "static/corpus/data.yml",
])
def test_exempt_paths_are_skipped(repo, path):
    repo(path, "no header here\n")
    assert path not in gate.tracked()
    assert gate.main() == 0


def test_non_source_files_are_not_checked(repo):
    repo("static/img/photo.webp", "binary")
    repo("README.md", "# Readme\n")
    assert gate.tracked() == []


def test_a_tag_after_the_first_ten_lines_does_not_count(repo, capsys):
    body = "".join(f"# line {n}\n" for n in range(10))
    repo("scripts/late.py", f"{body}# {COPYRIGHT}\n# {LICENCE}\n")
    assert gate.main() == 1
    assert "scripts/late.py: missing SPDX-FileCopyrightText, SPDX-License-Identifier" in capsys.readouterr().out


def test_a_tag_on_the_tenth_line_counts(repo):
    body = "".join(f"# line {n}\n" for n in range(8))
    repo("scripts/edge.py", f"{body}# {COPYRIGHT}\n# {LICENCE}\n")
    assert gate.main() == 0
