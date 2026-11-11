# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The small helpers of generate_corpus_page.py, one behaviour each.

main() is pinned end to end in test_generate_corpus_page_main.py and
the zip writer in test_corpus_zips.py; this file covers what those
runs do not reach: a checkout without a version, sizes past a
megabyte, the validation ladder verdict, an unknown confidence level,
and the worked example's presence and wording.
"""

from pathlib import Path

import generate_corpus_page as gcp


def test_lib_version_reads_pyproject_or_says_unknown(tmp_path):
    (tmp_path / "pyproject.toml").write_text('name = "x"\nversion = "0.0.86"\n', encoding="utf-8")
    assert gcp.lib_version(tmp_path) == "0.0.86"
    (tmp_path / "pyproject.toml").write_text('name = "x"\n', encoding="utf-8")
    assert gcp.lib_version(tmp_path) == "unknown"


def test_kb_switches_to_megabytes():
    assert gcp.kb(10 * 1024) == "10 KB"
    assert gcp.kb(3 * 1024 * 1024 + 512 * 1024) == "3.5 MB"
    assert gcp.esc("a | b") == "a \\| b"


def test_ladder_ok_fails_on_any_error():
    assert gcp.ladder_ok({}) is True
    assert gcp.ladder_ok({"validation": {"profiles": {"p": {"errors": 0}}, "overlays": None}}) is True
    assert gcp.ladder_ok({"validation": {"xsd": {"errors": 1}}}) is False
    assert gcp.ladder_ok({"validation": {"mdr": {"errors": 2}}}) is False
    assert gcp.ladder_ok({"validation": {"overlays": {"o": {"errors": 1}}}}) is False


def test_confidence_note_passes_an_unknown_level_through():
    assert gcp.confidence_note("verified").startswith("checked against a sample")
    assert gcp.confidence_note("guessed") == "guessed"


def test_stamp_date_sets_every_date_key():
    fm = gcp.stamp_date('date: "x"\nitem_pub_date: "x"\nlast_build_date: "x"\npub_date: "x"\ntitle: "x"\n')
    lines = fm.splitlines()
    assert lines[0].startswith('date: "') and lines[0].endswith('T08:00:00+00:00"')
    assert all(line.endswith(' 08:00:00 +0000"') for line in lines[1:4])
    assert lines[4] == 'title: "x"'


def _record(profiles):
    xml = Path("/corpus/gb/chaps/gb.xml")
    return {"scenario": gcp.EXAMPLE_SCENARIO, "description": "A house.", "message_type": "pain.001.001.09",
            "_xml": xml, "_sidecar": xml.with_name("gb.provenance.yaml"), "_rel": "gb/chaps/gb.xml",
            "provenance": {"confidence": "derived", "sources": [{"title": "Rulebook"}]},
            "validation": {"profiles": profiles}}


def test_worked_example_is_absent_without_its_scenario():
    assert gcp.worked_example([{**_record({}), "scenario": "other"}]) == []


def test_worked_example_names_its_files_sources_and_profiles():
    lines = gcp.worked_example([_record({"uk-chaps": {}, "uk-fps": {}, "anti-duplicate": {}})])
    text = "\n".join(lines)
    assert lines[0] == "## One scenario, end to end"
    assert f"Take `{gcp.EXAMPLE_SCENARIO}`: A house." in lines
    assert "- [gb.xml](/corpus/market/gb/chaps/gb.xml): the payment in pain.001.001.09" in text
    assert "- **Where does the content come from?** Rulebook." in lines
    assert "Confidence `derived`: built from the public rulebook" in text
    assert "the `uk-chaps`, `uk-fps` profiles;" in text


def test_worked_example_uses_the_singular_for_one_profile():
    text = "\n".join(gcp.worked_example([_record({"uk-chaps": {}})]))
    assert "the `uk-chaps` profile;" in text
