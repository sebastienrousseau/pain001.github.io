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
import datetime as _dt  # noqa: E402


def stamp_date(frontmatter: str) -> str:
    """Set the page date to today, in the template's two formats."""
    today = _dt.date.today()
    iso = today.strftime('%Y-%m-%dT08:00:00+00:00')
    rfc = today.strftime('%a, %d %b %Y 08:00:00 +0000')
    frontmatter = re.sub(r'^date: "[^"]*"', f'date: "{iso}"', frontmatter, flags=re.M)
    for key in ('item_pub_date', 'last_build_date', 'pub_date'):
        frontmatter = re.sub(rf'^{key}: "[^"]*"', f'{key}: "{rfc}"', frontmatter, flags=re.M)
    return frontmatter


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


BANK_MARKERS = re.compile(r"hsbc|restricted|usage guideline", re.I)
BANK_NAME = re.compile(r"hsbc", re.I)


def public_record(record: dict) -> dict:
    """The sidecar with bank-specific material removed.

    Bank usage guidelines are client documentation. The site publishes
    the generic files and the public sources behind them only: sources
    that cite a restricted guideline, the bank-variant block and any
    bank overlay verdict are dropped before the record is copied.
    """
    clean = {k: v for k, v in record.items() if not k.startswith("_")}
    clean.pop("variant", None)
    prov = dict(clean.get("provenance") or {})
    prov["sources"] = [
        s for s in prov.get("sources", [])
        if not BANK_MARKERS.search(str(s.get("title", "")))
    ]
    clean["provenance"] = prov
    validation = dict(clean.get("validation") or {})
    validation["overlays"] = {
        k: v for k, v in (validation.get("overlays") or {}).items()
        if not BANK_NAME.search(k)
    }
    clean["validation"] = validation
    return clean


def collect_market(data: Path) -> list[dict]:
    """Every generic market file; bank variants stay in the library."""
    files = []
    for sidecar in sorted((data / "market").rglob("*.provenance.yaml")):
        if "__" in sidecar.name:
            continue
        record = yaml.safe_load(sidecar.read_text(encoding="utf-8"))
        xml = sidecar.with_name(sidecar.name.replace(".provenance.yaml", ".xml"))
        record["_xml"] = xml
        record["_sidecar"] = sidecar
        record["_rel"] = xml.relative_to(data / "market").as_posix()
        record["_public_sidecar"] = yaml.safe_dump(
            public_record(record), sort_keys=False, allow_unicode=True
        )
        for text in (xml.read_text(encoding="utf-8"), record["_public_sidecar"]):
            if BANK_NAME.search(text):
                raise SystemExit(f"bank name in {xml.name}; not publishing")
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


def _clear(target: Path) -> None:
    if target.exists():
        for old in sorted(target.rglob("*"), reverse=True):
            old.unlink() if old.is_file() else old.rmdir()


def copy_market(files: list[dict], data: Path) -> None:
    target = STATIC / "market"
    _clear(target)
    for record in files:
        dst = target / record["_xml"].relative_to(data / "market")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(record["_xml"].read_bytes())
        dst.with_name(record["_sidecar"].name).write_text(
            record["_public_sidecar"], encoding="utf-8"
        )


def copy_coverage(editions: list[dict], data: Path) -> None:
    target = STATIC / "coverage"
    _clear(target)
    for edition in editions:
        for src in [edition["_dir"] / "coverage.json", *edition["_files"]]:
            dst = target / src.relative_to(data / "coverage")
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
            add_to_zip(zf, record["_xml"], "market/" + record["_rel"])
            info = zipfile.ZipInfo(
                "market/" + record["_rel"].replace(".xml", ".provenance.yaml"),
                date_time=ZIP_TIME,
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, record["_public_sidecar"].encode("utf-8"))
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


COVERAGE_SLUG = "example-corpus-coverage"
EXAMPLE_SCENARIO = "gb.chaps.property-purchase"

RUNGS = [
    ("Schema", "well-formed and valid against the edition's official ISO "
     "20022 XSD"),
    ("ISO rules", "the cross-element rules of the ISO message definition "
     "report, such as a cheque never carrying a creditor account"),
    ("Scheme profile", "the public rulebook of the rail: service levels, "
     "national identifiers, reference formats, amount limits"),
    ("Public overlay", "what a scheme body or regulator requires on top, "
     "where one has published it"),
]


def confidence_note(level: str) -> str:
    return {
        "verified": "checked against a sample the scheme itself published",
        "derived": "built from the public rulebook or implementation guide; "
        "no published sample was available to compare",
        "assumed": "one detail rests on an assumption the record names; "
        "treat that detail with care",
    }.get(level, level)


def worked_example(files: list[dict]) -> list[str]:
    recs = [r for r in files if r["scenario"] == EXAMPLE_SCENARIO]
    if not recs:
        return []
    first = recs[0]
    prov = public_record(first).get("provenance") or {}
    sources = [s.get("title", "") for s in prov.get("sources", [])][:3]
    profiles = ", ".join(
        f"`{p}`" for p in ((first.get("validation") or {}).get("profiles") or {})
        if p != "anti-duplicate"
    )
    lines = [
        "## One scenario, end to end",
        "",
        f"Take `{EXAMPLE_SCENARIO}`: {first.get('description', '')}",
        "",
        "It ships as these files:",
        "",
    ]
    for r in recs:
        lines.append(
            f"- [{r['_xml'].name}](/corpus/market/{r['_rel']}): the payment in "
            f"{r['message_type']}, and beside it "
            f"[{r['_sidecar'].name}](/corpus/market/{r['_rel'].replace('.xml', '.provenance.yaml')}), "
            "its provenance record."
        )
    lines += [
        "",
        "The provenance record answers the questions you would otherwise "
        "have to ask us:",
        "",
        f"- **Where does the content come from?** {'; '.join(sources)}.",
        f"- **How much can I trust it?** Confidence `{prov.get('confidence', '?')}`: "
        f"{confidence_note(prov.get('confidence', ''))}.",
        f"- **How was it checked?** By the library, against the schema, the "
        f"ISO rules and the {profiles} profile{'s' if ',' in profiles else ''}; "
        "the record lists every finding, including warnings.",
        "- **Is it exactly this file?** Its SHA-256 is in the record.",
        "",
        "What the record does not tell you is what *your* bank requires. "
        "That is the subject of the next section.",
        "",
    ]
    return lines


def render(files: list[dict], editions: list[dict], sizes: dict[str, int],
           version: str) -> str:
    scenarios: dict[str, list[dict]] = defaultdict(list)
    for record in files:
        scenarios[record["scenario"]].append(record)
    by_country: dict[str, list[str]] = defaultdict(list)
    for sid, recs in scenarios.items():
        if sid not in by_country[recs[0]["country"]]:
            by_country[recs[0]["country"]].append(sid)
    coverage_files = sum(len(e["_files"]) for e in editions)
    full_zip = next(n for n in sizes if n.startswith("pain001-example-corpus-"))

    body = [
        "If you are connecting a system to a bank, writing a parser, or "
        "testing a mapping, you need sample ISO 20022 files that are "
        "correct for your country and your rail. The ones passed around "
        "are usually old, hand-edited, or from somewhere else. This page "
        "gives you files built from the public rulebooks, with a record of "
        "where each one comes from.",
        "",
        "**What you get**",
        "",
        f"- **{len(scenarios)} realistic payments** across "
        f"{len(by_country)} countries: a UK CHAPS property purchase, a Swiss "
        "QR-bill, a Swedish Bankgiro run, a US ACH payroll, a SEPA direct "
        "debit, and more, each rendered in the message editions you are "
        "likely to meet.",
        f"- **{coverage_files} schema coverage files** across "
        f"{len(editions)} editions: deliberately exhaustive files that "
        "exercise the elements and choices of one schema edition, for "
        "testing a parser or a mapping against the whole schema rather "
        "than the usual happy path.",
        "- **A provenance record beside every payment file** saying where "
        "its content comes from, how far to trust it, and how the library "
        "checked it.",
        "",
        "**How to use it**",
        "",
        "1. Download the complete bundle below, or pick single files from "
        "the tables.",
        "2. Open the `.xml` next to your own file and diff them; open the "
        "`.provenance.yaml` to see what the differences mean.",
        "3. Get your bank's usage guideline (see below) and apply it on top: "
        "these files follow the public scheme rules, not any one bank's "
        "profile.",
        "",
        "Identifiers are synthetic: IBANs, BICs, LEIs and account numbers "
        "pass their check digits but belong to nobody, and names and "
        "addresses are invented. **Do not send these files to a bank.**",
        "",
        "## Download",
        "",
        "| Bundle | Contents | Size |",
        "| :--- | :--- | ---: |",
        f"| [Complete corpus](/corpus/{full_zip}) | "
        f"{len(files)} payment files with their provenance records, and "
        f"{coverage_files} schema coverage files across {len(editions)} "
        f"editions | {kb(sizes[full_zip])} |",
        f"| Coverage files per edition | one zip each, listed on the "
        f"[coverage page](/{COVERAGE_SLUG}/) | 9 to 12 KB |",
        "",
        f"Everything here is generated from pain001 {version}'s own corpus, "
        "which also ships inside the Python package (`pain001.corpus`) and "
        f"in the [repository]({REPO}/tree/main/pain001/corpus/data).",
        "",
        *worked_example(files),
        "## Your bank's guideline",
        "",
        "Every bank and clearing house publishes its own **message usage "
        "guideline**: which ISO 20022 elements it requires, which it "
        "ignores, and the values it accepts. Two banks on the same scheme "
        "can differ. Those guidelines are the bank's documentation, so "
        "they are not reproduced here: **download them from your bank or "
        "financial organisation**, typically from its client portal or "
        "from its collection on Swift MyStandards, and treat them as the "
        "final word.",
        "",
        "The library is built for that step. Its overlay grammar expresses "
        "a guideline as a short list of rules (an element that must be "
        "present, one that must be absent, a value that must be one of a "
        "set), `scripts/derive_overlay.py` reads a guideline's schema and "
        "drafts those rules for you, and the corpus builder can then "
        "render any scenario on this page the way your bank wants it, "
        "privately, in your own environment. The "
        f"[corpus guide]({REPO}/blob/main/docs/corpus.md) walks through it.",
        "",
        "## How the library checked these files",
        "",
        "| Step | What it checks |",
        "| :--- | :--- |",
    ]
    body += [f"| {name} | {what} |" for name, what in RUNGS]
    body += [
        "",
        "These checks are the library's own; they are not a certification, "
        "and passing them does not mean a bank will accept the file. "
        "Channel rules, onboarding profiles, cut-off times and the bank's "
        "guideline sit on top.",
        "",
        "**Reading the evidence column.** `verified` means "
        f"{confidence_note('verified')}. `derived` means "
        f"{confidence_note('derived')}. `assumed` means "
        f"{confidence_note('assumed')}.",
        "",
        "## Payment files by country",
        "",
    ]
    for cc in sorted(by_country):
        sids = by_country[cc]
        body += [
            f"### {COUNTRIES.get(cc, cc)} ({cc})",
            "",
            "| Scenario | What it shows | Checked against | Editions | Evidence |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for sid in sids:
            recs = scenarios[sid]
            first = recs[0]
            profiles = [
                p for p in ((first.get("validation") or {}).get("profiles") or {})
                if p != "anti-duplicate"
            ]
            editions_md = ", ".join(
                f"[{r['message_type']}](/corpus/market/{r['_rel']})" for r in recs
            )
            prov = first.get("provenance") or {}
            confidence = prov.get("confidence", "unknown")
            body.append(
                f"| `{sid}` | {esc(first.get('description', ''))} | "
                f"{', '.join(f'`{p}`' for p in profiles) or 'base rules only'} | "
                f"{editions_md} | {confidence} |")
        body.append("")

    body += [
        "## Schema coverage files",
        "",
        "Each edition has a small set of files built so that the elements "
        "and choice branches its schema declares each appear in at least "
        "one file. The first file is the baseline that carries every "
        "element once; each later file is named after the blocks it adds, "
        "so you can pick the one that exercises what you are testing. "
        f"The [coverage page](/{COVERAGE_SLUG}/) lists every file with what "
        "it adds and a zip per edition.",
        "",
        "| Edition | Files |",
        "| :--- | ---: |",
    ]
    for edition in editions:
        body.append(
            f"| [`{edition['message_type']}`](/{COVERAGE_SLUG}/#{edition['message_type'].replace('.', '-')}) | "
            f"{len(edition['_files'])} |")
    body += [
        "",
        "## Notes",
        "",
        "- The site publishes the generic files and their public sources. "
        "Bank-specific material stays with the banks.",
        "- The corpus is English only and grows with every release; it is "
        "generated data, not a translated page.",
        f"- The [corpus guide]({REPO}/blob/main/docs/corpus.md) explains the "
        "scenario format, the overlay grammar and how to add a country or a "
        "rail. Corrections and new scenarios are welcome there.",
        "- Regenerate this page and its downloads with "
        "`poetry run python3 scripts/generate_corpus_page.py` from the "
        "pain001 checkout after a corpus change.",
    ]
    return "\n".join(body)


def render_coverage_page(editions: list[dict], sizes: dict[str, int],
                         version: str) -> str:
    body = [
        "Schema coverage files are not realistic payments. Each set is "
        "generated from the schema itself so that the element paths and "
        "choice branches of one edition each appear in at least one of its "
        "files, and every file is valid against the schema and the ISO "
        "message definition report rules. Use them to smoke-test a parser, "
        "a mapping or a validator against the whole schema.",
        "",
        "**How to pick a file.** The first file of every set is the "
        "baseline: every element once, first branch of every choice. Each "
        "later file adds elements and choice branches the earlier files did "
        "not reach, and is named after the blocks most of that new content "
        "falls under (`RmtInf` for remittance information, `UltmtDbtr` for "
        "the ultimate debtor, `ChqInstr` for cheque instructions, and so "
        "on). The recipe in the name says what kind of payment the file is: "
        "a credit transfer, a cheque delivered to the creditor agent, a "
        "cheque with no creditor agent, or a direct debit collection.",
        "",
        "These files follow the ISO schema only. What your bank accepts is "
        "in its usage guideline; get it from your bank.",
        "",
        "The [example corpus](/example-corpus/) page has the realistic "
        "payment files and the complete download.",
        "",
    ]
    for edition in editions:
        mt = edition["message_type"]
        name = f"pain001-coverage-{mt}-{version}.zip"
        body += [
            f"## {mt}",
            "",
            f"{len(edition['_files'])} files. "
            f"[Download the set](/corpus/{name}) ({kb(sizes[name])}).",
            "",
            "| File | What it is for |",
            "| :--- | :--- |",
        ]
        infos = {f["name"]: f for f in edition.get("files", [])}
        for path in edition["_files"]:
            info = infos.get(path.name, {})
            body.append(
                f"| [{path.name}](/corpus/coverage/{mt}/{path.name}) | "
                f"{esc(info.get('description', ''))} |")
        body.append("")
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
    copy_coverage(editions, data)
    sizes = write_zips(files, editions, data, version)
    body = render(files, editions, sizes, version)
    fm = load_frontmatter(
        SLUG,
        "ISO 20022 example files — pain.001 and pain.008 samples per country and rail",
        "Download ISO 20022 pain.001 and pain.008 sample files built from "
        "the public scheme rulebooks per country and rail, each with a "
        "record of where it comes from and how it was checked, plus schema "
        "coverage files for every supported edition.",
        "Example corpus",
        f"Sample payment files for {len({r['country'] for r in files})} "
        "countries and their payment rails, plus schema coverage files for "
        "every supported edition, each traceable to its public sources.",
        "ISO 20022 example files, pain.001 sample XML, pain.008 sample, bank usage guideline, "
        "SEPA example, CHAPS example, Faster Payments example, ACH pain.001, "
        "QR-bill pain.001, Bankgiro pain.001, test corpus",
    )
    write_post(SLUG, stamp_date(fm), body)
    coverage_fm = load_frontmatter(
        COVERAGE_SLUG,
        "ISO 20022 schema coverage files — every element of every edition",
        "Generated pain.001 and pain.008 files that between them use every "
        "element path and choice branch of each supported schema edition, "
        "each named after what it adds, with a zip per edition.",
        "Example corpus",
        "One small set per edition, every file valid, every file named for "
        "the blocks it exercises.",
        "ISO 20022 schema coverage, pain.001 test files, pain.008 test files, "
        "XSD coverage, parser test corpus",
    )
    write_post(
        COVERAGE_SLUG,
        stamp_date(coverage_fm),
        render_coverage_page(editions, sizes, version),
    )
    print(f"rendered {SLUG}: {len(files)} market files, "
          f"{sum(len(e['_files']) for e in editions)} coverage files, "
          f"{len(sizes)} zips")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
