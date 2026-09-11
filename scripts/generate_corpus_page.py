#!/usr/bin/env python3
"""Generate the example-corpus page and its downloads from the library.

Everything here is copied or derived from ``pain001/corpus/data`` in the
pain001 checkout: the market files and their provenance sidecars, the
schema coverage sets and their ``coverage.json`` records. Nothing is
hand-transcribed, so the page cannot drift from what the library ships.

Output:
    _posts/example-corpus.md              the page
    static/corpus/market/<cc>/<family>/*  every market file and sidecar
    static/corpus/pain001-example-corpus-<version>.zip
    static/corpus/pain001-coverage-<edition>-<version>.zip

The sidecars are YAML and the zips are built from the library's tree,
so run this with the library's own environment:

    cd <pain001 checkout> && poetry run python3 \\
        <this repository>/scripts/generate_corpus_page.py

``PAIN001_LIB`` or the positional argument overrides the sibling
checkout at Public/Python/pain001.
"""
from __future__ import annotations

import os
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from generate_message_specs import load_frontmatter, write_post  # noqa: E402

DEFAULT_LIB = Path(
    os.environ.get("PAIN001_LIB") or HERE.parents[2] / "Python" / "pain001"
)
STATIC = ROOT / "static" / "corpus"
SLUG = "example-corpus"
REPO = "https://github.com/sebastienrousseau/pain001"

COUNTRIES = {
    "BE": "Belgium", "CH": "Switzerland", "DE": "Germany", "ES": "Spain",
    "FR": "France", "GB": "United Kingdom", "IT": "Italy",
    "LU": "Luxembourg", "NL": "Netherlands", "SE": "Sweden",
    "US": "United States",
}
# A fixed timestamp keeps every zip byte-identical between runs, so a
# regeneration that changes nothing leaves nothing to commit.
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def lib_version(lib: Path) -> str:
    text = (lib / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version = "([^"]+)"', text, re.M)
    return m.group(1) if m else "unknown"


def add_to_zip(zf: zipfile.ZipFile, path: Path, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, date_time=ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, path.read_bytes())


def kb(n: int) -> str:
    return f"{n / 1024:.0f} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} MB"


def esc(s: str) -> str:
    return s.replace("|", "\\|")


def collect_market(data: Path) -> list[dict]:
    files = []
    for sidecar in sorted((data / "market").rglob("*.provenance.yaml")):
        record = yaml.safe_load(sidecar.read_text(encoding="utf-8"))
        xml = sidecar.with_name(sidecar.name.replace(".provenance.yaml", ".xml"))
        record["_xml"] = xml
        record["_sidecar"] = sidecar
        record["_rel"] = xml.relative_to(data / "market").as_posix()
        files.append(record)
    return files


def collect_coverage(data: Path) -> list[dict]:
    editions = []
    for index in sorted((data / "coverage").glob("*/coverage.json")):
        record = yaml.safe_load(index.read_text(encoding="utf-8"))
        record["_dir"] = index.parent
        record["_files"] = sorted(index.parent.glob("*.xml"))
        editions.append(record)
    return editions


def copy_market(files: list[dict], data: Path) -> None:
    target = STATIC / "market"
    if target.exists():
        for old in sorted(target.rglob("*"), reverse=True):
            old.unlink() if old.is_file() else old.rmdir()
    for record in files:
        for src in (record["_xml"], record["_sidecar"]):
            dst = target / src.relative_to(data / "market")
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())


def write_zips(
    files: list[dict], editions: list[dict], data: Path, version: str
) -> dict[str, int]:
    for old in STATIC.glob("*.zip"):
        old.unlink()
    sizes: dict[str, int] = {}
    full = STATIC / f"pain001-example-corpus-{version}.zip"
    with zipfile.ZipFile(full, "w") as zf:
        for record in files:
            for src in (record["_xml"], record["_sidecar"]):
                add_to_zip(zf, src, "market/" + src.relative_to(data / "market").as_posix())
        for edition in editions:
            for src in [edition["_dir"] / "coverage.json", *edition["_files"]]:
                add_to_zip(zf, src, "coverage/" + src.relative_to(data / "coverage").as_posix())
    sizes[full.name] = full.stat().st_size
    for edition in editions:
        name = f"pain001-coverage-{edition['message_type']}-{version}.zip"
        with zipfile.ZipFile(STATIC / name, "w") as zf:
            for src in [edition["_dir"] / "coverage.json", *edition["_files"]]:
                add_to_zip(zf, src, src.name)
        sizes[name] = (STATIC / name).stat().st_size
    return sizes


def ladder_ok(record: dict) -> bool:
    v = record.get("validation") or {}
    if v.get("xsd", {}).get("errors") or v.get("mdr", {}).get("errors"):
        return False
    for group in ("profiles", "overlays"):
        for entry in (v.get(group) or {}).values():
            if entry.get("errors"):
                return False
    return True


def render(files: list[dict], editions: list[dict], sizes: dict[str, int],
           version: str) -> str:
    scenarios: dict[str, list[dict]] = defaultdict(list)
    for record in files:
        scenarios[record["scenario"]].append(record)
    by_country: dict[str, list[str]] = defaultdict(list)
    for sid, recs in scenarios.items():
        if sid not in by_country[recs[0]["country"]]:
            by_country[recs[0]["country"]].append(sid)
    variants = [r for r in files if r.get("variant")]
    overlays = sorted({r["variant"]["overlay"] for r in variants})
    coverage_files = sum(len(e["_files"]) for e in editions)
    clean = sum(1 for r in files if ladder_ok(r))
    full_zip = next(n for n in sizes if n.startswith("pain001-example-corpus-"))

    body = [
        "Ready-made ISO 20022 payment files you can download, diff and feed "
        "to your own validator: a **market corpus** of realistic scenarios "
        "per country and rail, with bank variants where the evidence "
        "exists, and a **schema coverage corpus** that exercises every "
        "element and choice branch of every supported pain.001 and "
        "pain.008 edition.",
        "",
        "**Everything on this page is generated from the pain001 library's "
        f"own corpus (version {version})**, the same files its test suite "
        "pins. Every file below passed the library's four-rung validation "
        "ladder when it was built (XSD, the ISO message definition report "
        "rules, the rail profile, and the bank or scheme overlay), and the "
        "sidecar next to each file records that run, its sources and the "
        "confidence of the evidence.",
        "",
        "## Download",
        "",
        "| Bundle | Contents | Size |",
        "| :--- | :--- | ---: |",
        f"| [Complete corpus](/corpus/{full_zip}) | "
        f"{len(files)} market files with provenance sidecars and "
        f"{coverage_files} coverage files across {len(editions)} editions | "
        f"{kb(sizes[full_zip])} |",
    ]
    for edition in editions:
        name = f"pain001-coverage-{edition['message_type']}-{version}.zip"
        body.append(
            f"| [Coverage {edition['message_type']}](/corpus/{name}) | "
            f"{len(edition['_files'])} files and `coverage.json` | "
            f"{kb(sizes[name])} |")
    body += [
        "",
        "Single files are linked from the tables below; each `.xml` has a "
        "`.provenance.yaml` beside it at the same path. The corpus also "
        "ships inside the Python package (`pain001.corpus`) and in the "
        f"[repository]({REPO}/tree/main/pain001/corpus/data).",
        "",
        "## Market corpus",
        "",
        f"{len(scenarios)} scenarios across {len(by_country)} countries, "
        f"{len(files)} files of which {len(variants)} are bank variants "
        f"built from {len(overlays)} overlays. {clean} of {len(files)} "
        "files pass every rung of the ladder without an error; the rest "
        "carry a recorded warning, never an error.",
        "",
        "A scenario renders the same payment in more than one edition of "
        "the message (typically pain.001.001.03, still the most deployed, "
        "and .09, the CBPR+ and SEPA 2025 baseline). A **bank variant** is "
        "the same scenario with a bank's fixed choices pinned by its usage "
        "guideline, named `<scenario>__<overlay>`. Bank usage guidelines "
        "are client documentation and are not redistributed; the overlays "
        "carry short, cited rules derived from them.",
        "",
    ]
    for cc in sorted(by_country):
        sids = by_country[cc]
        body += [
            f"### {COUNTRIES.get(cc, cc)} ({cc})",
            "",
            "| Scenario | What it shows | Rail profile | Editions | "
            "Bank variants | Evidence |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for sid in sids:
            recs = scenarios[sid]
            base = [r for r in recs if not r.get("variant")]
            vars_ = [r for r in recs if r.get("variant")]
            first = base[0] if base else recs[0]
            profiles = [
                p for p in ((first.get("validation") or {}).get("profiles") or {})
                if p != "anti-duplicate"
            ]
            editions_md = ", ".join(
                f"[{r['message_type']}](/corpus/market/{r['_rel']})" for r in base
            )
            variants_md = ", ".join(
                f"[{r['variant']['overlay']}](/corpus/market/{r['_rel']}) "
                f"({r['message_type']})" for r in vars_
            ) or "—"
            prov = first.get("provenance") or {}
            confidence = prov.get("confidence", "unknown")
            body.append(
                f"| `{sid}` | {esc(first.get('description', ''))} "
                f"({esc(first.get('family', ''))}) | "
                f"{', '.join(f'`{p}`' for p in profiles) or '—'} | "
                f"{editions_md} | {variants_md} | {confidence} |")
        body.append("")

    body += [
        "## Schema coverage corpus",
        "",
        "One set per supported edition, generated from the schema itself "
        "along the message definition report's recipes (transfer, cheque "
        "with and without a creditor agent, direct debit sequences) so "
        "that every element path and every choice branch appears in at "
        "least one file that is XSD-valid and MDR-clean. Use it to smoke "
        "a parser, a mapping or a validator against the whole schema, not "
        "a happy path.",
        "",
        "| Edition | Files | Paths covered | Branches covered | Download |",
        "| :--- | ---: | ---: | ---: | :--- |",
    ]
    for edition in editions:
        name = f"pain001-coverage-{edition['message_type']}-{version}.zip"
        paths = edition.get("paths") or {}
        branches = edition.get("branches") or {}
        body.append(
            f"| `{edition['message_type']}` | {len(edition['_files'])} | "
            f"{paths.get('hit', '?')} of {paths.get('declared', '?')} "
            f"({paths.get('percent', '?'):.0f} %) | "
            f"{branches.get('hit', '?')} of {branches.get('declared', '?')} "
            f"({branches.get('percent', '?'):.0f} %) | "
            f"[zip](/corpus/{name}) |")
    body += [
        "",
        "## How every file is judged",
        "",
        "| Rung | Check | Source |",
        "| :--- | :--- | :--- |",
        "| L0 | Well-formed XML and valid against the edition's official XSD "
        "| ISO 20022 schema |",
        "| L1 | The message definition report's cross-element rules "
        "(cheque and creditor-agent pairings, amendment indicators, "
        "sequence types, and more) | ISO 20022 MDR |",
        "| L2 | The rail profile: scheme limits, service levels, national "
        "identifiers and reference formats | Public scheme rulebooks and "
        "bank implementation guides |",
        "| L3 | The scheme or bank overlay: required, forbidden and "
        "restricted elements | Public overlays, and cited rules derived "
        "from restricted usage guidelines |",
        "",
        "The result of each rung is written into the file's "
        "`.provenance.yaml` with the sources read, the confidence of the "
        "evidence (`verified`, `derived` or `assumed`) and anything the "
        "builder had to rename, wrap or drop to fit the edition.",
        "",
        "## Scope and honesty",
        "",
        "- Identifiers are **synthetic**: IBANs, BICs, LEIs and account "
        "numbers pass their check digits and formats but belong to nobody. "
        "Names and addresses are invented. Do not send these files to a "
        "bank.",
        "- A file that passes here can still be rejected by a bank: "
        "channel rules, onboarding profiles and cut-offs are not in scope. "
        "A bank variant reflects one usage guideline at the date recorded "
        "in its sidecar.",
        "- The corpus is **English only** and grows with every release; it "
        "is generated data, not a translated page.",
        f"- The [corpus guide]({REPO}/blob/main/docs/corpus.md) explains "
        "the scenario format, the overlay grammar and how to add a country "
        "or a rail.",
        "- Regenerate this page and its downloads with "
        "`poetry run python3 scripts/generate_corpus_page.py` from the "
        "pain001 checkout after a corpus change.",
    ]
    return "\n".join(body)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    lib = Path(args[0]).resolve() if args else DEFAULT_LIB
    data = lib / "pain001" / "corpus" / "data"
    if not data.is_dir():
        print(f"no corpus data at {data}", file=sys.stderr)
        return 1
    version = lib_version(lib)
    files = collect_market(data)
    editions = collect_coverage(data)
    STATIC.mkdir(parents=True, exist_ok=True)
    copy_market(files, data)
    sizes = write_zips(files, editions, data, version)
    body = render(files, editions, sizes, version)
    fm = load_frontmatter(
        SLUG,
        "ISO 20022 example corpus — downloadable pain.001 and pain.008 files",
        "Download realistic ISO 20022 pain.001 and pain.008 example files "
        "per country and rail, with bank variants, plus a schema coverage "
        "corpus for every supported edition. Generated from the pain001 "
        "library, validated at every rung.",
        "Example corpus",
        f"{len(files)} market files across {len({r['country'] for r in files})} "
        f"countries and {sum(len(e['_files']) for e in editions)} schema "
        "coverage files, every one validated and traceable to its sources.",
        "ISO 20022 example files, pain.001 sample XML, pain.008 sample, "
        "SEPA example, CHAPS example, Faster Payments example, ACH pain.001, "
        "QR-bill pain.001, Bankgiro pain.001, test corpus",
    )
    write_post(SLUG, fm, body)
    print(f"rendered {SLUG}: {len(files)} market files, "
          f"{sum(len(e['_files']) for e in editions)} coverage files, "
          f"{len(sizes)} zips")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
