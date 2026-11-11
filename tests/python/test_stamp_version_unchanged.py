# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/stamp_version.py on pages that need no change.

Pins that a page already at the target version, or naming no version, is
not rewritten and is not counted as touched.
"""

from __future__ import annotations

import os

import stamp_version


def test_current_pages_are_left_alone(tmp_path, monkeypatch):
    posts = tmp_path / "_posts"
    posts.mkdir()
    current = posts / "a.md"
    current.write_text("Install pain001 v0.0.86 today.\n", encoding="utf-8")
    plain = posts / "b.md"
    plain.write_text("No version here.\n", encoding="utf-8")
    stale = posts / "c.md"
    stale.write_text("Install 0.0.85.\n", encoding="utf-8")
    for page in (current, plain):
        os.utime(page, (1, 1))
    monkeypatch.setattr(stamp_version, "POSTS", posts)
    assert stamp_version.stamp("0.0.86") == 1
    assert stale.read_text(encoding="utf-8") == "Install 0.0.86.\n"
    assert current.stat().st_mtime == 1 and plain.stat().st_mtime == 1
