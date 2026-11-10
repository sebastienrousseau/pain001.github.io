# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The repository tracks no symbolic links.

A worktree that links node_modules to another checkout once committed
that link: it pointed at a path on one machine, and in CI the REUSE
check followed it into node_modules and failed. A symlink in the tree
is never part of the site, so any tracked one is a mistake.
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_no_symlink_is_tracked():
    listing = subprocess.run(
        ["git", "ls-files", "--stage"], cwd=ROOT, check=True,
        capture_output=True, text=True).stdout
    links = [line.split("\t", 1)[1] for line in listing.splitlines()
             if line.startswith("120000 ")]
    assert links == []


def test_node_modules_is_ignored_as_a_link_too():
    # "node_modules/" matches directories only; a symlink must match too.
    for path in ("node_modules", "tools/a11y/node_modules"):
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT)
        assert result.returncode == 0, path
