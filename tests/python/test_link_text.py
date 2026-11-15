# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""No layout link reads as one of Lighthouse's non-descriptive texts.

The SDK tile linked the Go SDK as "Go", which Lighthouse's link-text
audit lists alongside "click here" and "more"; the homepage's SEO score
fell to 92 and the CI Lighthouse gate failed.
"""

import re
from pathlib import Path

LAYOUTS = Path(__file__).resolve().parents[2] / "_layouts"
# Lighthouse's English list (core/audits/seo/link-text.js).
VAGUE = {"click here", "click this", "go", "here", "information", "learn more", "more",
         "more info", "more information", "right here", "read more", "see more", "start",
         "this", "ok"}


def test_layout_links_describe_their_target():
    vague = []
    for layout in sorted(LAYOUTS.glob("*.html")):
        for inner in re.findall(r"<a\b[^>]*>(.*?)</a>", layout.read_text(encoding="utf-8"), re.S):
            text = " ".join(re.sub(r"<[^>]+>", "", inner).split()).lower()
            if text in VAGUE:
                vague.append(f"{layout.name}: {text!r}")
    assert vague == []
