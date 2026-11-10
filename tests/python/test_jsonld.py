# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Homepage structured data: the software, its owner and its version.

ssg's homepage JSON-LD had only WebSite and WebPage, so nothing told a
search or answer engine that Pain001 is free software or who maintains
it. postbuild_fix.enrich_home_ld merges SoftwareApplication and
Organization nodes into that graph; validate_jsonld checks every block.
"""

import json

import postbuild_fix as pb
import validate_jsonld as v

SSG = (
    '<head><script type="application/ld+json">'
    + json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": "https://pain001.com/#website"},
        {"@type": "WebPage", "@id": "https://pain001.com/#webpage"}]})
    + "</script></head>"
)


def _graph(html):
    return v.nodes(json.loads(v.blocks(html)[0]))


def test_the_graph_gains_software_and_organization_in_one_block():
    html = pb.enrich_home_ld(SSG, "0.0.83")
    assert len(v.blocks(html)) == 1
    types = [n["@type"] for n in _graph(html)]
    assert types == ["WebSite", "WebPage", "SoftwareApplication", "Organization"]
    site, page = _graph(html)[:2]
    assert site["publisher"] == {"@id": pb.ORG_ID}
    assert page["about"] == {"@id": pb.SOFTWARE_ID}
    assert v.home_problems(html, "0.0.83") == []


def test_enriching_twice_adds_nothing():
    once = pb.enrich_home_ld(SSG, "0.0.83")
    assert pb.enrich_home_ld(once, "0.0.83") == once


def test_without_a_version_the_page_is_unchanged():
    assert pb.enrich_home_ld(SSG, "") == SSG


def test_a_stale_version_is_reported():
    html = pb.enrich_home_ld(SSG, "0.0.82")
    assert v.home_problems(html, "0.0.83") == [
        "homepage softwareVersion '0.0.82' is not '0.0.83'"
    ]


def test_the_ssg_graph_alone_fails_the_homepage_check():
    assert v.home_problems(SSG, "0.0.83") == [
        "homepage has 0 SoftwareApplication nodes, not 1"
    ]


def test_broken_json_and_ratings_are_reported():
    broken = '<script type="application/ld+json">{"@context": </script>'
    assert v.page_problems("a.html", broken)[0].startswith("a.html: JSON-LD does not parse")
    rated = '<script type="application/ld+json">{"@context": "https://schema.org", "aggregateRating": {}}</script>'
    assert v.page_problems("b.html", rated) == ["b.html: JSON-LD claims a rating or review"]
