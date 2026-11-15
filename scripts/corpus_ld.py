#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Facts about a corpus scenario for its schema.org Dataset markup.

generate_corpus_page.dataset_ld records one Dataset per scenario page in
scripts/corpus_pages.json, and postbuild_fix.inject_dataset_ld writes it
into the built page. Everything here is read from the scenario's own
provenance records; nothing is typed in by hand.

Google's Dataset rich result rejects a description shorter than 50 or
longer than 5000 characters; Search Console reported the scenarios
whose one-line summary fell short. It reads the catalogue a dataset
belongs to from ``includedInDataCatalog``: ``isPartOf`` expects a
CreativeWork, so the DataCatalog there was an invalid object type.
"""
from __future__ import annotations

DESCRIPTION_MIN = 50
DESCRIPTION_MAX = 5000
CATALOG = {"@type": "DataCatalog", "name": "pain001 example corpus",
           "url": "https://pain001.com/example-corpus/"}


def twin_path(rec: dict):
    """Where a record's ISO 20022 JSON twin sits next to its XML."""
    return rec["_xml"].with_name(rec["_xml"].name.replace(".xml", ".iso.json"))


def message_name(recs: list[dict]) -> str:
    """The message a scenario ships, ``pain.001`` or ``pain.008``."""
    return str(recs[0].get("message_type", "pain.001"))[:8]


def has_twins(recs: list[dict]) -> bool:
    """True when every edition of the scenario has a JSON twin."""
    return all(twin_path(r).exists() for r in recs)


def dataset_description(recs: list[dict], country: str) -> str:
    """The scenario summary, then what the files are: message, country,
    rail, editions and sidecars, so even a one-line summary clears the
    50-character floor with facts from the records."""
    first = recs[0]
    editions = ", ".join(r["message_type"] for r in recs)
    sidecars = "an ISO 20022 JSON twin and a provenance record" if has_twins(recs) else "a provenance record"
    text = (f"{str(first.get('description', '')).strip()} A synthetic ISO 20022 "
            f"{message_name(recs)} sample for {country} on the {first.get('family', '')} rail, "
            f"built from the public scheme rulebooks and checked by pain001, in {editions}; "
            f"each file comes with {sidecars}.")
    return text.strip()[:DESCRIPTION_MAX]


META_MAX = 160


def page_description(t: dict, recs: list[dict], desc: str, country: str) -> str:
    """A scenario page's meta description in the strings ``t`` of its locale.

    It names the message the files carry and, only when every edition has
    one, the JSON twin. Search results cut a description near 160
    characters, so when the summary is long the sidecar clause goes first."""
    fields = {"desc": desc, "msg": message_name(recs), "country": country,
              "family": recs[0].get("family", "")}
    text = t["meta_desc"].format(files=t["files_twin"] if has_twins(recs) else t["files_prov"], **fields)
    if len(text) > META_MAX:
        text = t["meta_desc"].format(files="", **fields)
    return " ".join(text.split())
