# SPDX-FileCopyrightText: 2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The demo and documentation checks must use the same suite release."""

import json

import pytest
import validate_release_pins as gate


@pytest.mark.parametrize("stale", [None, "runtime", "input", "lock"])
def test_release_pins_must_agree(tmp_path, monkeypatch, capsys, stale):
    monkeypatch.setattr(gate, "ROOT", tmp_path)
    (tmp_path / "VERSION").write_text("0.0.42\n")
    runtime = tmp_path / "static/pyodide/pain001-runtime.json"
    runtime.parent.mkdir(parents=True)
    runtime.write_text(json.dumps({"pain001": "0.0.41" if stale == "runtime" else "0.0.42"}))
    requirements = tmp_path / "requirements"
    requirements.mkdir()
    for kind, suffix in (("input", "in"), ("lock", "txt")):
        version = "0.0.41" if stale == kind else "0.0.42"
        (requirements / ("snippets." + suffix)).write_text("pain001==" + version + "\n")
    assert gate.main() == (0 if stale is None else 1)
    output = capsys.readouterr().out
    assert ("does not match VERSION" in output) == (stale is not None)
