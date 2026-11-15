#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Search-result-sized descriptions for the generated message-spec pages.

A type-reference page is described by the span of type names it lists,
and the longest spans (pain.008.001.02's "AccountIdentification4Choice
– OrganisationIdentificationSchemeName1Choice") pushed the description
past the 160 characters a search result shows. The fullest sentence
that fits is used; the shortest always fits, since no span is over 90
characters.
"""
from __future__ import annotations

DESCRIPTION_MAX = 160


def types_description(span: str, version: str) -> str:
    """The description of one type-reference page of ``version``."""
    candidates = (
        f"Complex types {span} in ISO 20022 {version}: elements, cardinality and constraints "
        "from the official XSD.",
        f"Complex types {span} in ISO 20022 {version}, from the official XSD.",
    )
    return next((c for c in candidates if len(c) <= DESCRIPTION_MAX), candidates[-1])
