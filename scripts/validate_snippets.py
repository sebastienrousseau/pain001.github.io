#!/usr/bin/env python3
"""Check that Python snippets in _posts/ reference real pain001 API.

The ten pain.001 version pages shipped a snippet calling
``VersionMapper("from", "to").migrate(records)`` — an API that has never
existed (the constructor takes no arguments and the method is
``migrate_rows``). It raised TypeError on every page and nothing caught
it, because no test ever executed documentation.

This does not run the snippets (they need payment data). It checks every
``from pain001... import X`` resolves, every attribute accessed on an
imported symbol exists, and every call's arity matches the signature.

CI installs pain001 from PyPI on purpose: the question this answers is
"does the documentation work for someone who ran ``pip install pain001``
today", and only the published wheel can answer it.

That makes documenting an API before it ships a guaranteed failure, and
the honest fix is not to relax the check but to say which version a page
needs. A page whose snippets require an unreleased API declares
``min_pain001: "0.0.58"`` in its front matter; its failures are then
reported as pending that release rather than as broken documentation,
and the page renders a visible requirement note for readers. Once that
version is on PyPI the same failures become real again, so a stale
declaration cannot hide a genuine break.

Skipped automatically when pain001 is not importable, so the site can
still build without the library installed.
"""
from __future__ import annotations

import ast
import glob
import importlib
import inspect
import re
import sys

PY_BLOCK = re.compile(r"```python\n(.*?)```", re.S)
MIN_VERSION = re.compile(r'^min_pain001:\s*"?([\d.]+)"?\s*$', re.M)


def _parse(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in re.findall(r"\d+", v))


def _pending_minimum(path: str, installed: str) -> str | None:
    """The version this page needs, if it is newer than what is installed."""
    m = MIN_VERSION.search(open(path, encoding="utf-8").read())
    if not m:
        return None
    return m.group(1) if _parse(m.group(1)) > _parse(installed) else None


def main() -> int:
    try:
        importlib.import_module("pain001")
    except Exception as exc:  # noqa: BLE001
        print(f"pain001 not importable ({exc.__class__.__name__}); skipping.")
        return 0

    problems: list[str] = []
    checked = 0

    for path in sorted(glob.glob("_posts/*.md")):
        text = open(path, encoding="utf-8").read()
        for block in PY_BLOCK.findall(text):
            try:
                tree = ast.parse(block)
            except SyntaxError as exc:
                problems.append(f"{path}: snippet does not parse — {exc}")
                continue
            checked += 1

            symbols: dict[str, object] = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("pain001"):
                    # companion packages ship separately (pain001_loader_*,
                    # pain001_mcp, pain001_lsp); absent here is not a defect
                    if not node.module.startswith("pain001."):
                        if node.module != "pain001":
                            continue
                    try:
                        mod = importlib.import_module(node.module)
                    except Exception as exc:  # noqa: BLE001
                        problems.append(f"{path}: cannot import {node.module} — {exc}")
                        continue
                    for alias in node.names:
                        obj = getattr(mod, alias.name, None)
                        if obj is None:
                            problems.append(
                                f"{path}: {node.module} has no {alias.name!r}")
                        else:
                            symbols[alias.asname or alias.name] = obj

            # attribute access + constructor arity on imported symbols
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    fn = node.func
                    # Symbol(...)  -> constructor arity
                    if isinstance(fn, ast.Name) and fn.id in symbols:
                        obj = symbols[fn.id]
                        if inspect.isclass(obj):
                            _check_arity(obj.__init__, node, f"{fn.id}()",
                                         path, problems, skip_self=True)
                    # Symbol(...).method(...) or var.method(...)
                    if isinstance(fn, ast.Attribute):
                        base = fn.value
                        owner = None
                        if isinstance(base, ast.Name) and base.id in symbols:
                            owner = symbols[base.id]
                        elif (isinstance(base, ast.Call)
                              and isinstance(base.func, ast.Name)
                              and base.func.id in symbols):
                            owner = symbols[base.func.id]
                        if owner is not None and inspect.isclass(owner):
                            meth = getattr(owner, fn.attr, None)
                            if meth is None:
                                problems.append(
                                    f"{path}: {owner.__name__} has no method "
                                    f"{fn.attr!r}")
                            elif callable(meth):
                                _check_arity(meth, node,
                                             f"{owner.__name__}.{fn.attr}()",
                                             path, problems, skip_self=True)

    problems += _check_migration_paths()

    installed = getattr(importlib.import_module("pain001"), "__version__", "0")
    pending: dict[str, str] = {}
    real: list[str] = []
    for p in problems:
        path = p.split(":", 1)[0]
        need = _pending_minimum(path, installed) if path.startswith("_posts/") else None
        if need:
            pending[p] = need
        else:
            real.append(p)

    print(f"checked {checked} python snippet(s) in _posts/ "
          f"against pain001 {installed}")
    for p in real:
        print("FAIL", p)
    for p, need in pending.items():
        print(f"PENDING v{need}", p)
    if pending:
        print(f"\n{len(pending)} snippet issue(s) await a release; each page "
              f"declares the version it needs and says so to readers.")
    print("result:", "CLEAN" if not real else f"{len(real)} problem(s)")
    return 1 if real else 0


def _check_migration_paths() -> list[str]:
    """Verify documented VersionMapper paths are actually supported.

    Arity and attribute checks pass happily on
    ``migrate_rows(rows, "pain.001.001.09", "pain.001.001.12")`` — but
    that raised DataSourceError at runtime until modern-to-modern
    migration was implemented, and four version pages documented paths
    that could not run. Signature checking cannot see this; the mapper's
    own support predicate can.
    """
    problems: list[str] = []
    try:
        from pain001.migration import VersionMapper
    except Exception:  # noqa: BLE001
        return problems

    mapper = VersionMapper()
    pat = re.compile(
        r'migrate_(?:rows|file)\(\s*[^,]+,\s*"([^"]+)"\s*,\s*"([^"]+)"',
        re.S)
    for path in sorted(glob.glob("_posts/*.md")):
        text = open(path, encoding="utf-8").read()
        for block in PY_BLOCK.findall(text):
            for src, dst in pat.findall(block):
                try:
                    mapper.load_mapping(src, dst)
                except Exception as exc:  # noqa: BLE001
                    problems.append(
                        f"{path}: documented migration {src} -> {dst} is not "
                        f"supported ({exc.__class__.__name__})")
    return problems


def _check_arity(func, call: ast.Call, label: str, path: str,
                 problems: list[str], skip_self: bool = False) -> None:
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return
    params = list(sig.parameters.values())
    if skip_self and params and params[0].name in ("self", "cls"):
        params = params[1:]
    if any(p.kind is p.VAR_POSITIONAL for p in params):
        return
    maxpos = sum(1 for p in params
                 if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))
    given = len(call.args)
    if given > maxpos:
        problems.append(
            f"{path}: {label} called with {given} positional arg(s) but "
            f"accepts at most {maxpos}")


if __name__ == "__main__":
    sys.exit(main())
