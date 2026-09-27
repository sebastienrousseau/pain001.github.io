# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/seo_scoreboard.py, with a fake Search Console API."""

import datetime as dt

import seo_scoreboard as sb

TODAY = dt.date(2026, 9, 27)
CURRENT = ("2026-08-28", "2026-09-24")
PREVIOUS = ("2026-07-31", "2026-08-27")

DATA = {
    CURRENT: {
        None: [{"clicks": 900, "impressions": 20000, "ctr": 0.045, "position": 6.0}],
        "query": [
            {"keys": ["pain.001"], "clicks": 40, "impressions": 1000, "ctr": 0.04, "position": 6.0},
            {"keys": ["pain001"], "clicks": 50, "impressions": 900, "ctr": 0.0556, "position": 1.8},
            {"keys": ["unrelated"], "clicks": 1, "impressions": 5, "ctr": 0.2, "position": 30.0},
        ],
        "page": [
            {"keys": ["https://pain001.com/pain-001/"], "clicks": 30, "impressions": 800, "ctr": 0.0375,
             "position": 5.0},
            {"keys": ["https://pain001.com/"], "clicks": 60, "impressions": 3000, "ctr": 0.02, "position": 7.0},
        ],
        "country": [{"keys": ["deu"], "clicks": 170, "impressions": 3294, "ctr": 0.05, "position": 5.0}],
    },
    PREVIOUS: {
        None: [{"clicks": 800, "impressions": 18000, "ctr": 0.044, "position": 6.5}],
        "query": [
            {"keys": ["pain.001"], "clicks": 14, "impressions": 983, "ctr": 0.014, "position": 15.0},
        ],
        "page": [{"keys": ["https://pain001.com/"], "clicks": 50, "impressions": 2800, "ctr": 0.018,
                  "position": 8.0}],
        "country": [{"keys": ["deu"], "clicks": 150, "impressions": 3000, "ctr": 0.05, "position": 5.5}],
    },
}


def fake_post(body):
    span = (body["startDate"], body["endDate"])
    dimension = (body.get("dimensions") or [None])[0]
    return {"rows": DATA[span][dimension]}


def test_windows_are_28_days_ending_three_days_ago():
    assert sb.windows(TODAY) == (CURRENT, PREVIOUS)


def test_report_lists_every_tracked_query_even_without_data():
    md = sb.render(sb.collect(fake_post, TODAY))
    for q in sb.TRACKED:
        assert f"| `{q}` |" in md
    assert "`unrelated`" not in md


def test_cells_show_value_and_change():
    md = sb.render(sb.collect(fake_post, TODAY))
    # pain.001: 40 clicks (+26), 1,000 impressions (+17), 4.0% CTR (+2.6 pt),
    # position 6.0, nine places higher than 15.0.
    assert "| `pain.001` | 40 (+26) | 1,000 (+17) | 4.0% (+2.6 pt) | 6.0 (+9.0) |" in md
    # pain001 had no rows before: the change reads "new".
    assert "| `pain001` | 50 (new) |" in md
    # A tracked query with no data at all shows dashes.
    assert "| `pain.002` | – (–) | – (–) | – (–) | – (–) |" in md


def test_pages_are_ranked_by_clicks_and_shown_as_paths():
    md = sb.render(sb.collect(fake_post, TODAY))
    pages = md.split("## Top pages")[1].split("## Top countries")[0]
    assert pages.index("| / |") < pages.index("| /pain-001/ |")


def test_not_configured_exits_zero(monkeypatch, capsys):
    monkeypatch.delenv("GSC_SERVICE_ACCOUNT_JSON", raising=False)
    assert sb.main([]) == 0
    assert "not configured" in capsys.readouterr().out


def test_report_is_written_to_the_job_summary(tmp_path, monkeypatch):
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    assert sb.main([], today=TODAY, post=fake_post) == 0
    assert summary.read_text(encoding="utf-8").startswith("# pain001.com Search Console scoreboard")


def test_the_api_is_asked_for_final_data_by_dimension():
    seen = []
    sb.collect(lambda body: seen.append(body) or fake_post(body), TODAY)
    assert {tuple(b.get("dimensions", [])) for b in seen} == {(), ("query",), ("page",), ("country",)}
    assert all(b["dataState"] == "final" for b in seen)
