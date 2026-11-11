# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""generate_try_samples.py offers the demo only samples that run clean.

The script needs the pain001 library, which the site's test environment
does not install, so a small fake of `pain001`, `pain001.corpus.api` and
`pain001.twins.records` stands in for it. The tests pin which corpus
files become samples (the demo edition, no bank variant, a twin with no
gap, no missing column and at least one row), the rail preselected for
each, the CSV columns kept, and the JSON and summary written.
"""

import csv
import importlib
import io
import json
import sys
import types
from types import SimpleNamespace

import pytest

EDITION = "pain.001.001.09"


def _entry(sid, country="GB", version=EDITION, variant="", family="chaps"):
    return SimpleNamespace(scenario_id=sid, country=country, version=version,
                           variant=variant, family=family)


ENTRIES = [
    _entry("gb.ok", family="uk-chaps"),
    _entry("de.ok", country="DE", family="sepa"),
    _entry("gb.old", version="pain.001.001.03"),
    _entry("gb.bank", variant="hsbc"),
    _entry("fr.gap", country="FR"),
    _entry("fr.missing", country="FR"),
    _entry("fr.empty", country="FR"),
]
TWINS = {
    "gb.ok": SimpleNamespace(gap=[], missing_required=[], rows=[
        {"name": "A", "unused": "", "amount": "1.00"},
        {"name": "B", "unused": " ", "amount": ""},
    ]),
    "de.ok": SimpleNamespace(gap=[], missing_required=[], rows=[{"name": "C"}]),
    "fr.gap": SimpleNamespace(gap=["a", "b", "c"], missing_required=[], rows=[{"x": 1}]),
    "fr.missing": SimpleNamespace(gap=[], missing_required=["p", "q", "r", "s"], rows=[{"x": 1}]),
    "fr.empty": SimpleNamespace(gap=[], missing_required=[], rows=[]),
}
PROVENANCE = {
    "gb.ok": {"description": "  CHAPS payment \n",
              "validation": {"profiles": {"anti-duplicate-x": {}, "uk-chaps": {}, "uk-fps": {}}}},
    "de.ok": {"validation": None},
}


@pytest.fixture
def gts(monkeypatch, tmp_path):
    """The script imported against a fake pain001 library, writing to tmp_path."""
    calls = []
    api = types.ModuleType("pain001.corpus.api")

    def list_files(kind):
        calls.append(kind)
        return list(reversed(ENTRIES))

    api.list_files = list_files
    api.get_file = lambda sid, version: f"<xml id='{sid}' v='{version}'/>"
    api.provenance = lambda sid, version: PROVENANCE[sid]
    corpus = types.ModuleType("pain001.corpus")
    corpus.api = api
    records = types.ModuleType("pain001.twins.records")
    records.to_records = lambda xml, version: TWINS[xml.split("'")[1]]
    pain001 = types.ModuleType("pain001")
    pain001.__version__ = "9.9.9"
    pain001.corpus = corpus
    for name, module in (("pain001", pain001), ("pain001.corpus", corpus),
                         ("pain001.corpus.api", api), ("pain001.twins", types.ModuleType("pain001.twins")),
                         ("pain001.twins.records", records)):
        monkeypatch.setitem(sys.modules, name, module)
    monkeypatch.delitem(sys.modules, "generate_try_samples", raising=False)
    module = importlib.import_module("generate_try_samples")
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "OUT", tmp_path / "static" / "corpus" / "try-samples.json")
    (tmp_path / "static" / "corpus").mkdir(parents=True)
    module.calls = calls
    yield module
    sys.modules.pop("generate_try_samples", None)


def test_rails_of_reads_profiles_in_order(gts):
    rails_of = gts.rails_of
    assert rails_of({"validation": {"profiles": {"b": {}, "a": {}}}}) == ["b", "a"]
    assert rails_of({"validation": {"profiles": None}}) == []
    assert rails_of({}) == []


def test_to_csv_keeps_only_columns_with_a_value(gts):
    text = gts.to_csv(TWINS["gb.ok"].rows)
    assert text == "name,amount\nA,1.00\nB,\n"
    assert list(csv.DictReader(io.StringIO(text))) == [
        {"name": "A", "amount": "1.00"}, {"name": "B", "amount": ""}]


def test_main_writes_only_clean_samples(gts, capsys):
    assert gts.main() == 0
    assert gts.calls == ["market"]
    data = json.loads(gts.OUT.read_text(encoding="utf-8"))
    assert data["pain001"] == "9.9.9"
    assert data["message_type"] == EDITION
    assert [s["id"] for s in data["samples"]] == ["de.ok", "gb.ok"]
    assert gts.OUT.read_text(encoding="utf-8").endswith("\n")


def test_main_writes_each_sample_with_its_rail_and_csv(gts):
    assert gts.main() == 0
    de, gb = json.loads(gts.OUT.read_text(encoding="utf-8"))["samples"]
    assert de == {"id": "de.ok", "country": "DE", "family": "sepa", "description": "",
                  "scheme": "", "records": 1, "csv": "name\nC\n"}
    assert gb["description"] == "CHAPS payment"
    assert gb["scheme"] == "uk-chaps"
    assert gb["records"] == 2


def test_main_reports_what_it_skipped(gts, capsys):
    gts.main()
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "wrote static/corpus/try-samples.json: 2 samples, 3 skipped"
    assert out[1:] == [
        "  skipped fr.empty: gap=[] missing=[]",
        "  skipped fr.gap: gap=['a', 'b'] missing=[]",
        "  skipped fr.missing: gap=[] missing=['p', 'q', 'r']",
    ]
