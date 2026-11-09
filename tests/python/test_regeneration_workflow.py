# SPDX-FileCopyrightText: 2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regeneration exports review evidence without writing repository history."""

import hashlib
import os
from pathlib import Path
import subprocess
import textwrap


WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/regenerate.yml"


def test_regeneration_cannot_push_or_open_a_second_iteration_pr():
    """CI must leave SSH-signed commits on the maintainer's single branch."""
    source = WORKFLOW.read_text()
    for forbidden in ("contents: write", "pull-requests: write", "actions: write", "git push", "git commit", "gh pr "):
        assert forbidden not in source
    assert "release/pain001-" not in source


def test_regeneration_uploads_a_review_patch_and_checksum():
    """A generated update remains concrete and reviewable without a bot PR."""
    source = WORKFLOW.read_text()
    assert "name: Export review patch" in source
    assert "actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9" in source
    assert "pain001-update.patch.sha256" in source


def test_exported_patch_includes_new_sources_and_excludes_library_clone(tmp_path):
    """Execute the workflow's actual export against a synthetic repository."""
    source = WORKFLOW.read_text()
    assert "      - name: Export review patch\n" in source
    step = source.split("      - name: Export review patch\n", 1)[1].split("\n      -", 1)[0]
    script = textwrap.dedent(step.split("        run: |\n", 1)[1])
    repository = tmp_path / "repository"
    repository.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    (repository / "new-source.md").write_text("Synthetic source update\n")
    clone = repository / ".pain001"
    clone.mkdir()
    (clone / "not-a-website-source.txt").write_text("Synthetic clone\n")
    patch = tmp_path / "pain001-update.patch"
    environment = dict(
        os.environ,
        REVIEW_PATCH=str(patch),
        RUNNER_TEMP=str(tmp_path),
        GITHUB_STEP_SUMMARY=str(tmp_path / "summary"),
        VERSION="0.0.84",
    )
    subprocess.run(["bash", "-e", "-c", script], cwd=repository, env=environment, check=True)
    assert "new-source.md" in patch.read_text()
    assert ".pain001" not in patch.read_text()
    checksum = (tmp_path / "pain001-update.patch.sha256").read_text().split()
    assert checksum == [hashlib.sha256(patch.read_bytes()).hexdigest(), "pain001-update.patch"]
