# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""robots.txt states the crawler policy instead of implying it.

ssg wrote two lines (a wildcard user agent and the sitemap). The site
wants citations from answer engines, so static/robots.txt, which
replaces ssg's file in the build, allows every public page and names
the AI crawlers explicitly.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROBOTS = (ROOT / "static" / "robots.txt").read_text(encoding="utf-8")


def _groups():
    groups, agents = {}, []
    for line in ROBOTS.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        if key.lower() == "user-agent":
            agents.append(value)
        elif key.lower() in ("allow", "disallow"):
            for agent in agents:
                groups.setdefault(agent, []).append((key.lower(), value))
            agents = []
    return groups


def test_every_named_ai_crawler_is_allowed_everywhere():
    groups = _groups()
    for agent in ("*", "GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"):
        assert groups.get(agent) == [("allow", "/")], agent


def test_nothing_is_disallowed_and_the_sitemap_is_linked():
    assert "disallow" not in ROBOTS.lower()
    assert "Sitemap: https://pain001.com/sitemap.xml" in ROBOTS.splitlines()
