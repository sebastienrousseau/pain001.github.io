# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The type-reference pages' descriptions fit a search result.

Thirty generated message-spec pages had descriptions of 161 to 195
characters, because each names the span of type names it lists.
"""

import re
from pathlib import Path

import spec_text

POSTS = Path(spec_text.__file__).resolve().parent.parent / "_posts"


def test_a_short_span_keeps_the_full_sentence():
    assert spec_text.types_description("A – B", "pain.001.001.09") == (
        "Complex types A – B in ISO 20022 pain.001.001.09: elements, cardinality and constraints "
        "from the official XSD.")


def test_a_long_span_falls_back_to_the_short_sentence():
    span = "AccountIdentification4Choice – OrganisationIdentificationSchemeName1Choice"
    text = spec_text.types_description(span, "pain.008.001.02")
    assert text == f"Complex types {span} in ISO 20022 pain.008.001.02, from the official XSD."
    assert len(text) <= spec_text.DESCRIPTION_MAX


def test_every_generated_spec_page_fits_a_search_result():
    wrong = {}
    for post in sorted(POSTS.glob("message-spec*.md")):
        description = re.search(r'^description: "(.*)"$', post.read_text(encoding="utf-8"), re.M).group(1)
        if not 50 <= len(description) <= spec_text.DESCRIPTION_MAX:
            wrong[post.name] = len(description)
    assert wrong == {}
