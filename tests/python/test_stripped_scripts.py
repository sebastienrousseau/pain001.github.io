# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Every script the build strips of comments still parses afterwards.

strip_js_comments copies quoted strings through but does not understand
regex literals, so a quote or "/*" inside a regex in one of these files
could corrupt it. Each stripped file is parsed with node --check.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from css_minify import strip_js_comments  # noqa: E402
from postbuild_fix import STRIPPED_SCRIPTS  # noqa: E402


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
@pytest.mark.parametrize("name", STRIPPED_SCRIPTS)
def test_a_stripped_script_still_parses(tmp_path, name):
    source = (ROOT / "static" / "js" / name).read_text(encoding="utf-8")
    stripped = strip_js_comments(source)
    assert len(stripped) <= len(source)
    # .mjs parses import/export as well as classic scripts' syntax
    out = tmp_path / (Path(name).stem + ".mjs")
    out.write_text(stripped, encoding="utf-8")
    result = subprocess.run(["node", "--check", str(out)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
