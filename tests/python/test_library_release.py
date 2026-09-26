# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests for scripts/library_release.py.

Guards fix f3efab84 ("regenerate on every library release"): the site
never regenerated for a library release because the only trigger
needed a token that did not exist. The scheduled trigger regenerates
only when PyPI is ahead of the pinned wheel, and pins the new wheel.
"""

import json

import pytest

import library_release as lr

WHEEL = "pain001-{v}-py3-none-any.whl"


def _release(version, deps):
    return {
        "info": {"version": version, "requires_dist": deps},
        "urls": [
            {"packagetype": "sdist", "filename": f"pain001-{version}.tar.gz", "size": 9,
             "digests": {"sha256": "0" * 64}},
            {"packagetype": "bdist_wheel", "filename": WHEEL.format(v=version), "size": 1200,
             "digests": {"sha256": "f" * 64}},
        ],
    }


@pytest.fixture
def manifest(tmp_path, monkeypatch):
    path = tmp_path / "pain001-runtime.json"
    path.write_text(json.dumps({
        "pain001": "0.0.70",
        "pain001_source": "pypi:pain001==0.0.70",
        "wheels": [
            {"file": "defusedxml-0.7.1-py2.py3-none-any.whl", "bytes": 100, "sha256": "1" * 64, "url": "u"},
            {"file": WHEEL.format(v="0.0.70"), "bytes": 1000, "sha256": "2" * 64, "url": "old"},
        ],
        "total_bytes": 5000,
    }, indent=1) + "\n", encoding="utf-8")
    monkeypatch.setattr(lr, "MANIFEST", path)
    return path


@pytest.fixture
def pypi(monkeypatch):
    releases = {}

    def fake(version=""):
        return releases[version or "latest"]

    monkeypatch.setattr(lr, "pypi", fake)
    return releases


def test_schedule_targets_a_newer_release(manifest, pypi):
    pypi["latest"] = _release("0.0.71", [])
    assert lr.target("") == "0.0.71"


def test_schedule_does_nothing_when_current_or_behind(manifest, pypi):
    pypi["latest"] = _release("0.0.70", [])
    assert lr.target("") == ""
    pypi["latest"] = _release("0.0.9", [])  # numeric, not text, comparison
    assert lr.target("") == ""


def test_requested_version_is_used_as_given_and_validated(manifest, pypi):
    assert lr.target("0.0.71") == "0.0.71"
    with pytest.raises(SystemExit):
        lr.target("latest")


def test_pin_rewrites_the_wheel_entry_and_total(manifest, pypi, capsys):
    deps = ["click<9,>=8.5.0", 'lxml<7; extra == "fast"']
    pypi["0.0.70"] = _release("0.0.70", deps)
    pypi["0.0.71"] = _release("0.0.71", deps + ['holidays<1; extra == "rules"'])

    lr.pin("0.0.71")

    data = json.loads(manifest.read_text(encoding="utf-8"))
    wheel = data["wheels"][1]
    assert wheel == {
        "file": WHEEL.format(v="0.0.71"), "bytes": 1200, "sha256": "f" * 64,
        "url": "https://files.pythonhosted.org/packages/py3/p/pain001/" + WHEEL.format(v="0.0.71"),
    }
    assert data["wheels"][0]["file"].startswith("defusedxml")
    assert data["total_bytes"] == 5200
    assert data["pain001"] == "0.0.71"
    assert "::warning::" not in capsys.readouterr().out  # extras changed, core did not


def test_pin_warns_when_core_dependencies_change(manifest, pypi, capsys):
    pypi["0.0.70"] = _release("0.0.70", ["click<9,>=8.5.0"])
    pypi["0.0.71"] = _release("0.0.71", ["click<9,>=8.5.0", "rich>=15"])

    lr.pin("0.0.71")

    assert "::warning::pain001 0.0.71 changed its core dependencies" in capsys.readouterr().out


def test_pin_refuses_a_release_without_a_pure_python_wheel(manifest, pypi):
    release = _release("0.0.71", [])
    release["urls"] = release["urls"][:1]
    pypi["0.0.71"] = release
    with pytest.raises(SystemExit, match="no pure-Python wheel"):
        lr.pin("0.0.71")
