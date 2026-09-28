#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Weekly Search Console scoreboard for pain001.com.

Compares the last 28 days with the 28 days before them, for the site as a
whole, for the queries the site's content targets, and for the top pages
and countries: clicks, impressions, click-through rate and average
position. The report is Markdown, printed and, in GitHub Actions, written
to the job summary ($GITHUB_STEP_SUMMARY).

Search Console data lags by about three days, so both windows end three
days ago.

Credentials: Google Application Default Credentials for a service account
that has been added as a user on the Search Console property, found through
GOOGLE_APPLICATION_CREDENTIALS. In CI that file is written by
google-github-actions/auth through Workload Identity Federation: GitHub's
short-lived OIDC token is exchanged for a one-hour Google token, so no key
is stored anywhere. Without credentials, the script says so and exits 0.
See DEVELOPMENT.md for the setup.

Usage: python3 scripts/seo_scoreboard.py
"""

from __future__ import annotations

import datetime as dt
import os
import sys
import urllib.parse
from typing import Callable

PROPERTY = "sc-domain:pain001.com"
API = "https://searchconsole.googleapis.com/webmasters/v3/sites/{}/searchAnalytics/query"
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
LAG_DAYS = 3
WINDOW = 28
TRACKED = (
    "pain.001", "pain001", "pain 001", "001.001", "pain.001.001.09", "pain.001.001.03",
    "pain.001.001.09 xsd", "pain.002", "pain.001 format", "pain.001 example", "pain.001 validator",
)
TOP = 10
NOT_CONFIGURED = (
    "Search Console scoreboard not configured: GOOGLE_APPLICATION_CREDENTIALS is not set "
    "(see DEVELOPMENT.md). Nothing to report."
)

Post = Callable[[dict], dict]
Metrics = dict[str, float]


def windows(today: dt.date) -> tuple[tuple[str, str], tuple[str, str]]:
    """(current, previous) date ranges, each WINDOW days, ending LAG_DAYS ago."""
    end = today - dt.timedelta(days=LAG_DAYS)
    start = end - dt.timedelta(days=WINDOW - 1)
    prev_end = start - dt.timedelta(days=1)
    prev_start = prev_end - dt.timedelta(days=WINDOW - 1)
    return (start.isoformat(), end.isoformat()), (prev_start.isoformat(), prev_end.isoformat())


def metrics(row: dict) -> Metrics:
    return {
        "clicks": float(row.get("clicks", 0)),
        "impressions": float(row.get("impressions", 0)),
        "ctr": float(row.get("ctr", 0)),
        "position": float(row.get("position", 0)),
    }


def query(post: Post, span: tuple[str, str], dimension: str | None = None, limit: int = 25000) -> dict[str, Metrics]:
    """Rows for one date span, keyed by the dimension value ("" for the total)."""
    body: dict = {"startDate": span[0], "endDate": span[1], "rowLimit": limit, "dataState": "final"}
    if dimension:
        body["dimensions"] = [dimension]
    rows = post(body).get("rows", [])
    if not dimension:
        return {"": metrics(rows[0])} if rows else {"": metrics({})}
    return {row["keys"][0]: metrics(row) for row in rows}


def collect(post: Post, today: dt.date) -> dict:
    """Everything the report needs, from as few API calls as possible."""
    current, previous = windows(today)
    report: dict = {"current": current, "previous": previous}
    report["total"] = (query(post, current)[""], query(post, previous)[""])
    for dimension in ("query", "page", "country"):
        report[dimension] = (query(post, current, dimension), query(post, previous, dimension))
    return report


def _fmt(name: str, value: float | None) -> str:
    if value is None:
        return "–"
    if name == "ctr":
        return f"{value * 100:.1f}%"
    if name == "position":
        return f"{value:.1f}"
    return f"{value:,.0f}"


def _delta(name: str, now: float | None, before: float | None) -> str:
    if now is None or before is None:
        return "new" if before is None and now is not None else "–"
    diff = now - before
    if name == "position":
        # A lower position is better; show the change as ranks gained.
        return f"{-diff:+.1f}"
    if name == "ctr":
        return f"{diff * 100:+.1f} pt"
    return f"{diff:+,.0f}"


def _row(label: str, now: Metrics | None, before: Metrics | None) -> str:
    cells = [label]
    for name in ("clicks", "impressions", "ctr", "position"):
        a = now.get(name) if now else None
        b = before.get(name) if before else None
        cells.append(f"{_fmt(name, a)} ({_delta(name, a, b)})")
    return "| " + " | ".join(cells) + " |"


HEADER = "| {} | Clicks | Impressions | CTR | Avg. position |\n| --- | ---: | ---: | ---: | ---: |"


def render(report: dict) -> str:
    """The Markdown report. Each cell reads "current (change)"; a position
    change is ranks gained, so +2.0 means two places higher."""
    cur, prev = report["current"], report["previous"]
    lines = [
        "# pain001.com Search Console scoreboard",
        "",
        f"Last 28 days ({cur[0]} to {cur[1]}) against the previous 28 ({prev[0]} to {prev[1]}). "
        "Each cell is the current value and its change; a position change is ranks gained.",
        "",
        HEADER.format("Site"),
        _row("All queries", *report["total"]),
        "",
        "## Tracked queries",
        "",
        HEADER.format("Query"),
    ]
    now_q, before_q = report["query"]
    for q in TRACKED:
        lines.append(_row(f"`{q}`", now_q.get(q), before_q.get(q)))
    for title, key, label in (("Top pages", "page", "Page"), ("Top countries", "country", "Country")):
        now, before = report[key]
        top = sorted(now, key=lambda k: now[k]["clicks"], reverse=True)[:TOP]
        lines += ["", f"## {title}", "", HEADER.format(label)]
        lines += [_row(k.replace("https://pain001.com", "") or "/", now[k], before.get(k)) for k in top]
    return "\n".join(lines) + "\n"


def authorized_post() -> Post:
    """A POST function authenticated with Application Default Credentials."""
    import google.auth
    from google.auth.transport.requests import AuthorizedSession

    credentials, _ = google.auth.default(scopes=[SCOPE])
    session = AuthorizedSession(credentials)
    url = API.format(urllib.parse.quote(PROPERTY, safe=""))

    def post(body: dict) -> dict:
        response = session.post(url, json=body, timeout=60)
        response.raise_for_status()
        return response.json()

    return post


def main(argv: list[str] | None = None, today: dt.date | None = None, post: Post | None = None) -> int:
    if post is None:
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip():
            print(NOT_CONFIGURED)
            return 0
        post = authorized_post()
    markdown = render(collect(post, today or dt.date.today()))
    print(markdown)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
