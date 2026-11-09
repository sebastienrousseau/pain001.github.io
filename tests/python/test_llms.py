# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""llms.txt states no figure the site cannot keep current.

It said the MCP server had "21 tools" from September 2026 on, a number
typed by hand; pain001-mcp 0.0.83 ships 30. Nothing on the site reads
the MCP server's tool list, so llms.txt points at the page instead of
stating a count that goes stale on the next tool.
"""

import json
import re

import postbuild_fix as pb


def test_llms_states_no_tool_count(tmp_path, monkeypatch):
    site = tmp_path / "site"
    site.mkdir()
    pb.write_llms(site)
    text = (site / "llms.txt").read_text(encoding="utf-8")
    assert not re.search(r"\d+ tools", text)
    assert "https://pain001.com/pain001-mcp/" in text
    assert json.loads((pb.Path(pb.__file__).resolve().parent.parent / "static/corpus/index.json").read_text())["pain001"] in text
