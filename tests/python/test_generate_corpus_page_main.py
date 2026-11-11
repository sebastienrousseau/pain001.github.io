# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""generate_corpus_page.main() turns a library checkout into the corpus pages.

A small fake pain001 checkout in tmp_path (three market scenarios, a
bank variant, one coverage edition and a twin schema) runs through
main() with STATIC, HERE and the post writer redirected, so the tests
pin what is published (the files, zips, index, schemas and JSON-LD),
what is withheld (bank variants and bank-cited sources), the pages
written in every corpus locale, and the refusals for a missing
checkout or a bank name in a published file.
"""

import datetime
import json
import sys
import zipfile
from types import SimpleNamespace

import pytest
import yaml

import generate_corpus_page as gcp

GB = {
    "scenario": "gb.chaps.property-purchase", "country": "GB", "family": "chaps",
    "message_type": "pain.001.001.09", "description": "House purchase | completion",
    "sha256": "abc123", "variant": {"bank": "x"}, "_internal": 1,
    "provenance": {"confidence": "verified", "sources": [
        {"title": "CHAPS rulebook", "url": "https://example.org/chaps", "read": "2026-01-01"},
        {"title": "Bank usage guideline", "url": "https://example.org/private"},
        {"title": "Pay.UK guide", "retrieved": "2025-12-01"},
        {"title": "Notes"},
    ]},
    "validation": {"xsd": {"errors": 0}, "mdr": {"errors": 0},
                   "profiles": {"uk-chaps": {"errors": 0, "warnings": 2}, "anti-duplicate": None},
                   "overlays": {"hsbc-uk": {"errors": 1}, "boe-public": {"errors": 0}}},
}
GB03 = {**GB, "message_type": "pain.001.001.03"}
DE = {
    "scenario": "de.sepa.sct", "country": "DE", "family": "sepa",
    "message_type": "pain.001.001.09", "description": "Supplier run",
    "provenance": {"confidence": "assumed", "sources": []},
    "validation": {"xsd": {"errors": 2}, "profiles": {"sepa-sct": {"errors": 1}}},
}
ZZ = {"scenario": "zz.misc.one", "country": "ZZ", "family": "misc", "message_type": "pain.008.001.08"}
COVERAGE = {"message_type": "pain.001.001.09",
            "files": [{"name": "a-base.xml", "description": "baseline | every element"}]}
SAMPLE = {"id": "gb.chaps.property-purchase", "records": 2, "scheme": "uk-chaps", "csv": "a,b\n1,2\n"}


def _market(data, rel, record, twin=False, xml="<Document/>"):
    xml_path = data / "market" / rel
    xml_path.parent.mkdir(parents=True, exist_ok=True)
    xml_path.write_text(xml, encoding="utf-8")
    sidecar = xml_path.with_name(xml_path.name.replace(".xml", ".provenance.yaml"))
    sidecar.write_text(yaml.safe_dump(record), encoding="utf-8")
    if twin:
        xml_path.with_name(xml_path.name.replace(".xml", ".iso.json")).write_text("{}", encoding="utf-8")


def _library(root):
    lib = root / "lib"
    data = lib / "pain001" / "corpus" / "data"
    _market(data, "gb/chaps/gb-chaps.xml", GB, twin=True)
    _market(data, "gb/chaps/gb-chaps-03.xml", GB03)
    _market(data, "gb/chaps/gb-chaps__hsbc.xml", GB, xml="<HSBC/>")
    _market(data, "de/sepa/de-sepa.xml", DE)
    _market(data, "zz/misc/zz.xml", ZZ)
    edition = data / "coverage" / "pain.001.001.09"
    edition.mkdir(parents=True)
    (edition / "coverage.json").write_text(json.dumps(COVERAGE), encoding="utf-8")
    (edition / "a-base.xml").write_text("<A/>", encoding="utf-8")
    (edition / "b-RmtInf.xml").write_text("<B/>", encoding="utf-8")
    schemas = lib / "pain001" / "schemas" / "iso-json"
    schemas.mkdir(parents=True)
    (schemas / "pain.001.001.09.schema.json").write_text("{}", encoding="utf-8")
    (lib / "pyproject.toml").write_text('[tool]\nversion = "1.2.3"\n', encoding="utf-8")
    return lib


def _frontmatter(slug, title, desc, eyebrow, deck, keywords):
    return (f'---\ntitle: "{title}"\ndate: "old"\npub_date: "old"\nhreflang: "en"\n'
            f'permalink: "https://pain001.com/{slug}/"\n\n---\n\n')


@pytest.fixture
def site(tmp_path, monkeypatch):
    posts = {}
    static = tmp_path / "site" / "static" / "corpus"
    monkeypatch.setattr(gcp, "STATIC", static)
    monkeypatch.setattr(gcp, "HERE", tmp_path / "site")
    monkeypatch.setattr(gcp, "load_frontmatter", _frontmatter)
    monkeypatch.setattr(gcp, "write_post", lambda slug, fm, body: posts.__setitem__(slug, (fm, body)))
    monkeypatch.setattr(gcp, "_dt", SimpleNamespace(date=SimpleNamespace(today=lambda: datetime.date(2026, 3, 4))))
    static.mkdir(parents=True)
    (static / "try-samples.json").write_text(json.dumps({"samples": [SAMPLE]}), encoding="utf-8")
    (static / "pain001-example-corpus-0.0.1.zip").write_bytes(b"stale")
    return SimpleNamespace(lib=_library(tmp_path), static=static, posts=posts, here=tmp_path / "site")


@pytest.fixture
def ran(site):
    """The site after one successful main() run."""
    assert gcp.main([str(site.lib)]) == 0
    return site


def _index(site):
    return json.loads((site.static / "index.json").read_text(encoding="utf-8"))


def _json_ld(site):
    return json.loads((site.here / "corpus_pages.json").read_text(encoding="utf-8"))


def test_main_publishes_the_generic_market_files_only(ran):
    market = sorted(p.relative_to(ran.static / "market").as_posix()
                    for p in (ran.static / "market").rglob("*") if p.is_file())
    assert market == ["de/sepa/de-sepa.provenance.yaml", "de/sepa/de-sepa.xml",
                      "gb/chaps/gb-chaps-03.provenance.yaml", "gb/chaps/gb-chaps-03.xml",
                      "gb/chaps/gb-chaps.iso.json", "gb/chaps/gb-chaps.provenance.yaml",
                      "gb/chaps/gb-chaps.xml", "zz/misc/zz.provenance.yaml", "zz/misc/zz.xml"]
    sidecar = yaml.safe_load((ran.static / "market/gb/chaps/gb-chaps.provenance.yaml").read_text())
    assert "variant" not in sidecar and "_internal" not in sidecar
    assert [s["title"] for s in sidecar["provenance"]["sources"]] == ["CHAPS rulebook", "Pay.UK guide", "Notes"]
    assert sidecar["validation"]["overlays"] == {"boe-public": {"errors": 0}}


def test_main_publishes_the_coverage_files_zips_and_schemas(site, capsys):
    assert gcp.main([str(site.lib)]) == 0
    assert sorted(p.name for p in (site.static / "coverage" / "pain.001.001.09").iterdir()) == [
        "a-base.xml", "b-RmtInf.xml", "coverage.json"]
    assert sorted(p.name for p in site.static.glob("*.zip")) == [
        "pain001-coverage-pain.001.001.09-1.2.3.zip", "pain001-example-corpus-1.2.3.zip"]
    with zipfile.ZipFile(site.static / "pain001-coverage-pain.001.001.09-1.2.3.zip") as zf:
        assert zf.namelist() == ["coverage.json", "a-base.xml", "b-RmtInf.xml"]
    with zipfile.ZipFile(site.static / "pain001-example-corpus-1.2.3.zip") as zf:
        assert "market/gb/chaps/gb-chaps.provenance.yaml" in zf.namelist()
        assert "coverage/pain.001.001.09/b-RmtInf.xml" in zf.namelist()
    assert [p.name for p in (site.static / "schemas").iterdir()] == ["pain.001.001.09.schema.json"]
    assert capsys.readouterr().out.splitlines() == [
        "wrote 18 scenario pages, corpus/index.json, 1 twin schemas",
        "rendered example-corpus: 4 market files, 2 coverage files, 2 zips",
    ]


def test_main_writes_the_index_scenarios(ran):
    index = _index(ran)
    assert index["pain001"] == "1.2.3"
    assert [s["id"] for s in index["scenarios"]] == ["de.sepa.sct", "gb.chaps.property-purchase", "zz.misc.one"]
    de, _, zz = index["scenarios"]
    assert de["demo"] is None and de["rails"] == ["sepa-sct"] and de["confidence"] == "assumed"
    assert zz["confidence"] is None and zz["description"] == ""


def test_main_writes_the_index_editions_and_demo(ran):
    gb = _index(ran)["scenarios"][1]
    assert gb["demo"] == "https://pain001.com/try/#sample=corpus:gb.chaps.property-purchase"
    assert gb["rails"] == ["uk-chaps"]
    assert [e["message_type"] for e in gb["editions"]] == ["pain.001.001.03", "pain.001.001.09"]
    assert "twin" not in gb["editions"][0]
    assert gb["editions"][1]["twin_schema"] == "https://pain001.com/corpus/schemas/pain.001.001.09.schema.json"


def test_main_writes_the_json_ld(ran):
    ld = _json_ld(ran)
    assert len(ld) == 18
    gb_ld = ld["corpus-gb-chaps-property-purchase"]
    assert gb_ld["inLanguage"] == "en-GB" and gb_ld["dateModified"] == "2026-03-04"
    assert gb_ld["url"] == "https://pain001.com/corpus-gb-chaps-property-purchase/"
    assert [d["encodingFormat"] for d in gb_ld["distribution"]] == [
        "application/xml", "application/yaml", "application/xml", "application/json", "application/yaml"]
    assert gb_ld["keywords"] == ["ISO 20022", "pain.001", "GB", "chaps", "uk-chaps"]


def test_main_writes_localized_json_ld(ran):
    fr_ld = _json_ld(ran)["fr/corpus-gb-chaps-property-purchase"]
    assert fr_ld["inLanguage"] == "fr"
    assert fr_ld["url"] == "https://pain001.com/fr/corpus-gb-chaps-property-purchase/"


def test_main_writes_localized_scenario_pages(ran):
    fm, body = ran.posts["fr-corpus-gb-chaps-property-purchase"]
    assert 'permalink: "https://pain001.com/fr/corpus-gb-chaps-property-purchase/"' in fm
    assert 'hreflang: "fr"' in fm and 'language: "fr"' in fm and 'locale: "fr_FR"' in fm
    assert 'date: "2026-03-04T08:00:00+00:00"' in fm
    assert 'pub_date: "Wed, 04 Mar 2026 08:00:00 +0000"' in fm
    assert "> House purchase | completion" in body
    assert "](/fr/try/#sample=corpus:gb.chaps.property-purchase)" in body


def test_main_writes_english_scenario_pages_and_titles(ran):
    en_fm, en_body = ran.posts["corpus-gb-chaps-property-purchase"]
    assert 'hreflang: "en"' in en_fm and "language:" not in en_fm
    assert en_body.startswith("House purchase | completion\n")
    assert "](/try/#sample=corpus:gb.chaps.property-purchase)" in en_body
    assert 'title: "ISO-20022-pain.001-Beispiel de.sepa.sct: Deutschland (sepa)"' in ran.posts["de-corpus-de-sepa-sct"][0]
    assert 'title: "zz.misc.one: ISO 20022 pain.001 example for ZZ (misc)"' in ran.posts["corpus-zz-misc-one"][0]


def test_main_renders_the_catalogue_page(ran):
    fm, body = ran.posts["example-corpus"]
    assert fm.startswith('---\ntitle: "ISO 20022 example files')
    assert "- **3 realistic payments** across 3 countries" in body
    assert "- **2 schema coverage files** across 1 editions" in body
    assert "### United Kingdom (GB)" in body and "### ZZ (ZZ)" in body
    assert "| [`zz.misc.one`](/corpus-zz-misc-one/) |  | base rules only |" in body
    assert "House purchase \\| completion" in body
    assert "## One scenario, end to end" in body


def test_main_renders_the_coverage_page(ran):
    _, coverage = ran.posts["example-corpus-coverage"]
    assert "2 files. [Download the set](/corpus/pain001-coverage-pain.001.001.09-1.2.3.zip)" in coverage
    assert "| [a-base.xml](/corpus/coverage/pain.001.001.09/a-base.xml) | baseline \\| every element |" in coverage
    assert "| [b-RmtInf.xml](/corpus/coverage/pain.001.001.09/b-RmtInf.xml) |  |" in coverage


def test_rerun_keeps_current_zips_repairs_damaged_ones_and_clears_old_copies(site):
    gcp.main([str(site.lib)])
    zips = {p.name: p.read_bytes() for p in site.static.glob("*.zip")}
    (site.static / "market" / "stray" / "x.xml").parent.mkdir()
    (site.static / "market" / "stray" / "x.xml").write_text("old", encoding="utf-8")
    damaged = site.static / "pain001-coverage-pain.001.001.09-1.2.3.zip"
    damaged.write_bytes(zips[damaged.name][:40])

    assert gcp.main([str(site.lib)]) == 0

    assert {p.name: p.read_bytes() for p in site.static.glob("*.zip")} == zips
    assert not (site.static / "market" / "stray").exists()


def test_main_without_try_samples_links_no_demo(site):
    (site.static / "try-samples.json").unlink()
    gcp.main([str(site.lib)])
    index = json.loads((site.static / "index.json").read_text(encoding="utf-8"))
    assert all(s["demo"] is None for s in index["scenarios"])
    assert "## Run it in your browser" not in site.posts["corpus-gb-chaps-property-purchase"][1]


def test_main_refuses_a_bank_name_in_a_published_file(site):
    data = site.lib / "pain001" / "corpus" / "data"
    _market(data, "gb/chaps/gb-leak.xml", GB, xml="<Nm>HSBC UK</Nm>")
    with pytest.raises(SystemExit, match="bank name in gb-leak.xml; not publishing"):
        gcp.main([str(site.lib)])


def test_main_reads_the_checkout_from_argv(site, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["generate_corpus_page.py", str(site.lib)])
    assert gcp.main() == 0
    assert "example-corpus" in site.posts


def test_main_falls_back_to_pain001_lib(site, monkeypatch):
    monkeypatch.setattr(gcp, "DEFAULT_LIB", site.lib)
    assert gcp.main([]) == 0


def test_main_never_guesses_the_library(monkeypatch):
    monkeypatch.setattr(gcp, "DEFAULT_LIB", None)
    with pytest.raises(SystemExit, match="the library path is never guessed"):
        gcp.main([])


def test_main_reports_a_checkout_without_corpus_data(tmp_path, capsys):
    assert gcp.main([str(tmp_path)]) == 1
    assert capsys.readouterr().err == f"no corpus data at {tmp_path.resolve()}/pain001/corpus/data\n"
