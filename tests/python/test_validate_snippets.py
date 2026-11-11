# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/validate_snippets.py.

Python snippets in _posts/ must name real pain001 API: every
``from pain001... import X`` resolves, every method called on an imported
class exists, every call passes no more positional arguments than the
signature accepts, and every documented VersionMapper migration path is
one the mapper supports. A page declaring a newer ``min_pain001`` than
the installed version reports its failures as pending, not broken, and
the gate skips when pain001 is not importable.

pain001 is not installed in the test environment, so each test stubs it
in sys.modules with a small fake package.
"""

from __future__ import annotations

import sys
import types

import pytest

import validate_snippets as gate


class OddCallable:
    """Callable whose signature inspect cannot read."""

    __signature__ = "not a signature"

    def __call__(self):
        return None


class Mapper:
    LIMIT = 5
    odd = OddCallable()

    def __init__(self, a):
        self.a = a

    def run(self, x):
        return x

    def many(self, *rows):
        return rows

    @staticmethod
    def bare():
        return None

    @staticmethod
    def free(x, y):
        return x, y


def helper(x):
    return x


class VersionMapper:
    def load_mapping(self, src, dst):
        if dst.endswith(".99"):
            raise LookupError(dst)


@pytest.fixture
def posts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "_posts").mkdir()
    pkg = types.ModuleType("pain001")
    pkg.__version__ = "0.0.85"
    pkg.generate = helper
    core = types.ModuleType("pain001.core")
    core.Mapper, core.helper = Mapper, helper
    monkeypatch.setitem(sys.modules, "pain001", pkg)
    monkeypatch.setitem(sys.modules, "pain001.core", core)
    return tmp_path / "_posts"


def _with_migration(monkeypatch):
    migration = types.ModuleType("pain001.migration")
    migration.VersionMapper = VersionMapper
    monkeypatch.setitem(sys.modules, "pain001.migration", migration)


def _page(posts, name: str, *blocks: str, front: str = "") -> None:
    body = "".join(f"```python\n{b}\n```\n" for b in blocks)
    (posts / name).write_text(f"---\n{front}---\n{body}", encoding="utf-8")


def test_skips_when_pain001_is_not_importable(monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, "pain001", None)
    assert gate.main() == 0
    assert capsys.readouterr().out == "pain001 not importable (ModuleNotFoundError); skipping.\n"


def test_valid_snippets_pass(posts, monkeypatch, capsys):
    _with_migration(monkeypatch)
    _page(posts, "a.md", "\n".join([
        "from pain001.core import Mapper, helper as h",
        "from pain001 import generate",
        "from pain001_loader_xlsx import load",
        "from os import path",
        "from . import sibling",
        "m = Mapper(1)",
        "m2 = Mapper(1).run(2)",
        "Mapper.bare()", "Mapper.free(1, 2)", "Mapper.many(1, 2, 3)",
        "Mapper.LIMIT()", "Mapper.odd()",
        "h(1)", "h.attr()", "generate(1)", "print(1)",
        "other.method()", "obj.a().b()", "x[0]()",
        'VersionMapper().migrate_rows(rows, "pain.001.001.03", "pain.001.001.09")',
    ]))
    (posts / "notes.txt").write_text("```python\nfrom pain001.gone import X\n```\n", encoding="utf-8")
    assert gate.main() == 0
    assert capsys.readouterr().out == (
        "checked 1 python snippet(s) in _posts/ against pain001 0.0.85\nresult: CLEAN\n")


def test_unknown_api_and_wrong_arity_fail(posts, capsys):
    _page(posts, "b.md", "def broken(:", "\n".join([
        "from pain001.core import Mapper, Missing",
        "from pain001.nothere import X",
        "Mapper(1, 2)",
        "Mapper(1).run(1, 2)",
        "Mapper.nope()",
    ]))
    assert gate.main() == 1
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "checked 1 python snippet(s) in _posts/ against pain001 0.0.85"
    fails = out[1:-1]
    assert fails[0].startswith("FAIL _posts/b.md: snippet does not parse")
    assert fails[1] == "FAIL _posts/b.md: pain001.core has no 'Missing'"
    assert fails[2].startswith("FAIL _posts/b.md: cannot import pain001.nothere")
    assert fails[3:] == [
        "FAIL _posts/b.md: Mapper() called with 2 positional arg(s) but accepts at most 1",
        "FAIL _posts/b.md: Mapper.run() called with 2 positional arg(s) but accepts at most 1",
        "FAIL _posts/b.md: Mapper has no method 'nope'",
    ]
    assert out[-1] == "result: 6 problem(s)"


def test_unsupported_migration_paths_fail(posts, monkeypatch, capsys):
    _with_migration(monkeypatch)
    _page(posts, "c.md", 'mapper.migrate_file(path, "pain.001.001.09", "pain.001.001.99")')
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert ("FAIL _posts/c.md: documented migration pain.001.001.09 -> pain.001.001.99 "
            "is not supported (LookupError)") in out


def test_a_page_needing_a_newer_release_is_pending(posts, capsys):
    snippet = "from pain001.core import Future"
    _page(posts, "new.md", snippet, front='min_pain001: "0.0.90"\n')
    _page(posts, "old.md", snippet, front="min_pain001: 0.0.10\n")
    assert gate.main() == 1
    out = capsys.readouterr().out.splitlines()
    assert "FAIL _posts/old.md: pain001.core has no 'Future'" in out
    assert "PENDING v0.0.90 _posts/new.md: pain001.core has no 'Future'" in out
    assert "1 snippet issue(s) await a release; each page declares the version it needs and says so to readers." in out
    assert out[-1] == "result: 1 problem(s)"


def test_only_pending_issues_leave_the_gate_clean(posts, capsys):
    _page(posts, "new.md", "from pain001.core import Future", front='min_pain001: "0.1.0"\n')
    assert gate.main() == 0
    assert capsys.readouterr().out.splitlines()[-1] == "result: CLEAN"


def test_the_installed_version_defaults_to_zero(posts, capsys):
    del sys.modules["pain001"].__version__
    assert gate.main() == 0
    assert "against pain001 0\n" in capsys.readouterr().out
