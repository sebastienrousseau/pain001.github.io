# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""validate_no_commercial.py fails on the retired offer (decision D0)."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "scripts" / "validate_no_commercial.py"


def _run(site: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(GATE), str(site)],
                          capture_output=True, text=True, check=False)


def _site(tmp_path: Path, body: str) -> Path:
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(f"<html><body>{body}</body></html>", encoding="utf-8")
    return site


def test_a_clean_site_passes(tmp_path):
    site = _site(tmp_path, '<a href="/for-banks/">Get the evidence pack</a>')
    (site / "enterprise").mkdir()
    (site / "enterprise" / "index.html").write_text("redirect stub", encoding="utf-8")
    assert _run(site).returncode == 0


@pytest.mark.parametrize("body", [
    '<a class="btn" href="/try/">Book a briefing</a>',
    "Book an architecture briefing",
    "optional paid support",
    "No prices on this page; one form",
    "A supported release channel is available.",
    '<a href="https://github.com/sponsors/someone">Sponsor</a>',
    '<a href="/enterprise/#ask">Ask</a>',
    '<a href="/fr/thanks/">Merci</a>',
    "Trusted by HSBC",
    "/* hsbc */",
])
def test_retired_copy_fails(tmp_path, body):
    result = _run(_site(tmp_path, body))
    assert result.returncode == 1, result.stdout
    assert "FAIL index.html" in result.stdout


def test_a_missing_build_is_an_error(tmp_path):
    assert _run(tmp_path).returncode == 1
