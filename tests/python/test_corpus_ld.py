# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The Dataset markup of the corpus scenario pages.

Search Console flagged corpus-it-sepa-sct-single: "Invalid string length
in field 'description'". Google wants 50 to 5000 characters, and seven
scenarios carried only their one-line summary (30 to 48 characters) on
every locale copy. corpus_ld builds the description from the scenario's
own records; these tests pin the length on the shipped table and on the
shortest possible record.
"""

import json
from pathlib import Path

import corpus_ld

TABLE = Path(corpus_ld.__file__).resolve().parent / "corpus_pages.json"


def _rec(tmp_path, name, message_type="pain.001.001.09", twin=True, **extra):
    xml = tmp_path / f"{name}.xml"
    xml.write_text("<Document/>", encoding="utf-8")
    if twin:
        xml.with_name(f"{name}.iso.json").write_text("{}", encoding="utf-8")
    return {"message_type": message_type, "_xml": xml, "_rel": f"us/rtp/{name}.xml",
            "country": "US", "family": "instant-payment", **extra}


def test_every_shipped_dataset_description_is_within_googles_limits():
    table = json.loads(TABLE.read_text(encoding="utf-8"))
    short = {slug: len(ld["description"]) for slug, ld in table.items()
             if not corpus_ld.DESCRIPTION_MIN <= len(ld["description"]) <= corpus_ld.DESCRIPTION_MAX}
    assert short == {}


def test_a_one_line_summary_is_extended_with_facts_from_the_records(tmp_path):
    recs = [_rec(tmp_path, "a", "pain.001.001.03", description="RTP real-time payment, single."),
            _rec(tmp_path, "b")]
    text = corpus_ld.dataset_description(recs, "United States")
    assert text == (
        "RTP real-time payment, single. A synthetic ISO 20022 pain.001 sample for United States "
        "on the instant-payment rail, built from the public scheme rulebooks and checked by pain001, "
        "in pain.001.001.03, pain.001.001.09; each file comes with an ISO 20022 JSON twin and a "
        "provenance record.")


def test_a_record_without_a_summary_still_clears_the_floor(tmp_path):
    recs = [_rec(tmp_path, "c", "pain.008.001.08", twin=False)]
    text = corpus_ld.dataset_description(recs, "ZZ")
    assert text.startswith("A synthetic ISO 20022 pain.008 sample for ZZ")
    assert text.endswith("each file comes with a provenance record.")
    assert len(text) >= corpus_ld.DESCRIPTION_MIN


def test_an_overlong_summary_is_capped_at_the_ceiling(tmp_path):
    recs = [_rec(tmp_path, "d", description="x" * 6000)]
    assert len(corpus_ld.dataset_description(recs, "US")) == corpus_ld.DESCRIPTION_MAX


def test_the_message_name_follows_the_files():
    assert corpus_ld.message_name([{"message_type": "pain.008.001.02"}]) == "pain.008"
    assert corpus_ld.message_name([{}]) == "pain.001"


def test_every_shipped_dataset_names_its_catalogue_in_included_in_data_catalog():
    table = json.loads(TABLE.read_text(encoding="utf-8"))
    wrong = [slug for slug, ld in table.items()
             if ld.get("includedInDataCatalog") != corpus_ld.CATALOG or "isPartOf" in ld]
    assert wrong == []
