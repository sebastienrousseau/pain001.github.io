# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/carry_forward_assets.py's default site.

Pins that without --site the live pages are read from
https://pain001.com, and that the output directory defaults to site/.
"""

from __future__ import annotations

import carry_forward_assets as cf


def test_default_site_is_production(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    monkeypatch.chdir(tmp_path)
    seen = []
    pages = {"https://pain001.com/": (b'<link href="/_csp/0123abcd.css">', "text/html")}

    def fake_fetch(url):
        seen.append(url)
        if url.endswith(".css"):
            return b"body{}", "text/css"
        return pages.get(url)

    monkeypatch.setattr(cf, "fetch", fake_fetch)
    monkeypatch.setattr(cf.sys, "argv", ["carry_forward_assets.py"])
    assert cf.main() == 0
    assert seen[:4] == ["https://pain001.com" + p for p in cf.PAGES]
    assert seen[4] == "https://pain001.com/_csp/0123abcd.css"
    assert (tmp_path / "site" / "_csp" / "0123abcd.css").read_bytes() == b"body{}"
    assert "1 live asset(s) referenced, 1 carried into site, 0 skipped" in capsys.readouterr().out
