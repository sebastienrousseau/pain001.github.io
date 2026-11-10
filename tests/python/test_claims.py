# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The claims register drives every figure the site shows (decision D5)."""

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import claims  # noqa: E402
import validate_claims  # noqa: E402

REGISTER = {"claims": [
    {"id": "stars", "claim": "stars", "value": 1234, "format": "count", "source": "live",
     "pages": ["/"], "evidence_url": "https://github.com/x/y", "verified_in": "0.0.85"},
    {"id": "score", "claim": "score", "value": 8, "format": "score", "source": "live",
     "pages": ["/"], "evidence_url": "https://scorecard.dev/x", "verified_in": "0.0.85"},
    {"id": "cov", "claim": "coverage", "value": "100%", "format": "text", "source": "manual",
     "pages": ["/"], "evidence_url": "https://github.com/x/y/blob/main/pyproject.toml", "verified_in": "0.0.85"},
]}


def test_render_formats_counts_scores_and_text():
    by = claims.by_id(REGISTER)
    assert [claims.render(by[k]) for k in ("stars", "score", "cov")] == ["1,234", "8.0", "100%"]


def test_fill_writes_each_figure_and_leaves_unknown_ids():
    html = '<dd data-claim="stars">old</dd><span class="x" data-claim="cov"></span><b data-claim="nope">?</b>'
    assert claims.fill(html, REGISTER) == '<dd data-claim="stars">1,234</dd><span class="x" data-claim="cov">100%</span><b data-claim="nope">?</b>'


def test_refresh_stamps_only_fetched_live_figures():
    reg = copy.deepcopy(REGISTER)
    for c in reg["claims"]:
        c["verified_in"] = "0.0.84"
    claims.refresh(reg, {"stars": 99, "cov": "50%"}, "0.0.85")
    by = claims.by_id(reg)
    assert (by["stars"]["value"], by["stars"]["verified_in"]) == (99, "0.0.85")
    assert (by["score"]["value"], by["score"]["verified_in"]) == (8, "0.0.84")   # source failed
    assert (by["cov"]["value"], by["cov"]["verified_in"]) == ("100%", "0.0.84")  # manual


def _site(tmp_path, body):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(body, encoding="utf-8")
    return site


def test_a_site_that_matches_the_register_passes(tmp_path):
    site = _site(tmp_path, claims.fill('<dd data-claim="stars"></dd><i data-claim="score"></i><i data-claim="cov"></i>', REGISTER))
    assert validate_claims.problems(site, REGISTER, "0.0.85") == []


def test_each_kind_of_drift_is_reported(tmp_path):
    site = _site(tmp_path, '<dd data-claim="stars">1,000</dd><i data-claim="ghost">1</i><i data-claim="cov">100%</i>')
    reg = copy.deepcopy(REGISTER)
    claims.by_id(reg)["cov"]["evidence_url"] = ""
    found = validate_claims.problems(site, reg, "0.0.86")
    assert any("stars shows '1,000'" in p for p in found)
    assert any('"ghost" is not in' in p for p in found)
    assert any("score: listed for / but not shown" in p for p in found)
    assert any("verified in 0.0.85, the release is 0.0.86" in p for p in found)
    assert any("cov: no evidence URL" in p for p in found)


def test_the_committed_register_is_well_formed():
    reg = claims.load()
    ids = [c["id"] for c in reg["claims"]]
    assert len(ids) == len(set(ids))
    for c in reg["claims"]:
        assert c["source"] in ("live", "manual")
        assert c["format"] in ("count", "score", "text")
        assert c["evidence_url"].startswith("https://")
        assert c["pages"]
