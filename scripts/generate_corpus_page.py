#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
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

import json
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
from corpus_l10n import CORPUS_LOCALES, STRINGS as L10N  # noqa: E402
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


DEFAULT_LIB = Path(os.environ["PAIN001_LIB"]) if os.environ.get("PAIN001_LIB") else None
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


def zip_holds(target: Path, entries: list[tuple[str, bytes]]) -> bool:
    """True when ``target`` is a zip of exactly ``entries`` as write_zip writes them."""
    if not target.is_file():
        return False
    try:
        with zipfile.ZipFile(target) as old:
            listed = [(i.filename, i.date_time, i.external_attr, i.compress_type)
                      for i in old.infolist()]
            wanted = [(name, ZIP_TIME, 0o644 << 16, zipfile.ZIP_DEFLATED) for name, _ in entries]
            return listed == wanted and all(old.read(name) == data for name, data in entries)
    except zipfile.BadZipFile:
        # A damaged or truncated zip does not hold the entries; write_zip
        # replaces it.
        return False


def write_zip(target: Path, entries: list[tuple[str, bytes]]) -> None:
    """Write ``entries`` as a zip, unless ``target`` already holds exactly them.

    The fixed timestamp makes a zip reproducible on one machine, but DEFLATE
    output depends on the zlib build: the same bytes compress differently
    on the macOS and Linux runners, so a regeneration that changed nothing
    still rewrote five zips. When the existing file has the same members,
    metadata and uncompressed bytes, it is kept as it is.
    """
    if zip_holds(target, entries):
        return
    with zipfile.ZipFile(target, "w") as zf:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)


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
        twin = record["_xml"].with_name(record["_xml"].name.replace(".xml", ".iso.json"))
        if twin.exists():
            dst.with_name(twin.name).write_bytes(twin.read_bytes())


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
    archives: dict[str, list[tuple[str, bytes]]] = {}
    full: list[tuple[str, bytes]] = []
    for record in files:
        full.append(("market/" + record["_rel"], record["_xml"].read_bytes()))
        full.append(("market/" + record["_rel"].replace(".xml", ".provenance.yaml"),
                     record["_public_sidecar"].encode("utf-8")))
    for edition in editions:
        for src in [edition["_dir"] / "coverage.json", *edition["_files"]]:
            full.append(("coverage/" + src.relative_to(data / "coverage").as_posix(), src.read_bytes()))
    archives[f"pain001-example-corpus-{version}.zip"] = full
    for edition in editions:
        archives[f"pain001-coverage-{edition['message_type']}-{version}.zip"] = [
            (src.name, src.read_bytes())
            for src in [edition["_dir"] / "coverage.json", *edition["_files"]]
        ]
    for old in STATIC.glob("*.zip"):
        if old.name not in archives:
            old.unlink()
    sizes: dict[str, int] = {}
    for name, entries in archives.items():
        write_zip(STATIC / name, entries)
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
        ("The provenance record answers the questions you would otherwise "
        "have to ask us:"),
        "",
        f"- **Where does the content come from?** {'; '.join(sources)}.",
        (f"- **How much can I trust it?** Confidence `{prov.get('confidence', '?')}`: "
        f"{confidence_note(prov.get('confidence', ''))}."),
        (f"- **How was it checked?** By the library, against the schema, the "
        f"ISO rules and the {profiles} profile{'s' if ',' in profiles else ''}; "
        "the record lists every finding, including warnings."),
        "- **Is it exactly this file?** Its SHA-256 is in the record.",
        "",
        ("What the record does not tell you is what *your* bank requires. "
        "That is the subject of the next section."),
        "",
    ]
    return lines


def scenario_slug(sid: str) -> str:
    """The page slug for a scenario id: dots become hyphens, prefixed."""
    return "corpus-" + sid.replace(".", "-")


def load_try_samples() -> dict[str, dict]:
    """The demo's corpus samples by scenario id, when the file exists."""
    path = STATIC / "try-samples.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {s["id"]: s for s in data.get("samples", [])}


def dataset_ld(sid: str, recs: list[dict], version: str, stamp: str,
               lang: str = "en-GB", page_url: str | None = None) -> dict:
    """schema.org Dataset markup for one scenario page (English or a locale variant)."""
    first = recs[0]
    distribution = []
    for r in recs:
        base = f"https://pain001.com/corpus/market/{r['_rel']}"
        distribution.append({"@type": "DataDownload", "encodingFormat": "application/xml",
                             "name": f"{r['message_type']} XML", "contentUrl": base})
        if r["_xml"].with_name(r["_xml"].name.replace(".xml", ".iso.json")).exists():
            distribution.append({"@type": "DataDownload", "encodingFormat": "application/json",
                                 "name": f"{r['message_type']} ISO 20022 JSON twin",
                                 "contentUrl": base.replace(".xml", ".iso.json")})
        distribution.append({"@type": "DataDownload", "encodingFormat": "application/yaml",
                             "name": f"{r['message_type']} provenance record",
                             "contentUrl": base.replace(".xml", ".provenance.yaml")})
    profiles = [p for p in ((first.get("validation") or {}).get("profiles") or {}) if p != "anti-duplicate"]
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": f"{sid}: ISO 20022 pain.001 example ({first.get('country', '').upper()})",
        "description": str(first.get("description", "")).strip(),
        "url": page_url or f"https://pain001.com/{scenario_slug(sid)}/",
        "identifier": sid,
        "inLanguage": lang,
        "version": version,
        "dateModified": stamp,
        "license": "https://spdx.org/licenses/Apache-2.0.html",
        "isAccessibleForFree": True,
        "keywords": [k for k in ["ISO 20022", "pain.001", first.get("country", "").upper(), first.get("family", "")] + profiles if k],
        "creator": {"@type": "Organization", "name": "Pain001", "url": "https://pain001.com/"},
        "isPartOf": {"@type": "DataCatalog", "name": "pain001 example corpus", "url": "https://pain001.com/example-corpus/"},
        "distribution": distribution,
    }


def scenario_page(sid: str, recs: list[dict], version: str, sample: dict | None,
                  locale: str = "en") -> str:
    """The body of one scenario's page: what it is, its files, how it was checked, where it comes from.

    ``locale`` picks the fixed strings (scripts/corpus_l10n.py). The record's own
    prose (description, source titles) is quoted in English and labelled as such
    on the locale variants; the demo link points at that locale's /try/ page."""
    t = L10N[locale]
    first = recs[0]
    country = first.get("country", "").upper()
    country_name = t["countries"].get(first.get("country", ""), country)
    prov = public_record(first).get("provenance") or {}
    validation = first.get("validation") or {}
    profiles = {p: v for p, v in (validation.get("profiles") or {}).items()}
    sources = prov.get("sources", [])
    editions = ", ".join(f"`{r['message_type']}`" for r in recs)
    desc = str(first.get("description", "")).strip()
    lines = []
    if t["desc_label"]:
        lines += [t["desc_label"], "", f"> {desc}"]
    else:
        lines.append(desc)
    lines += [
        "",
        t["intro"].format(country=country_name, family=first.get("family", ""),
                          editions=editions, version=version),
        "",
        f"## {t['h_files']}",
        "",
        f"| {t['th_edition']} | {t['th_file']} | {t['th_twin']} | {t['th_prov']} |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for r in recs:
        rel = r["_rel"]
        has_twin = r["_xml"].with_name(r["_xml"].name.replace(".xml", ".iso.json")).exists()
        twin_md = (f"[{r['_xml'].name.replace('.xml', '.iso.json')}](/corpus/market/{rel.replace('.xml', '.iso.json')})"
                   if has_twin else t["no_twin"])
        lines.append(
            f"| `{r['message_type']}` | [{r['_xml'].name}](/corpus/market/{rel}) | {twin_md} | "
            f"[{r['_sidecar'].name}](/corpus/market/{rel.replace('.xml', '.provenance.yaml')}) |"
        )
    if any(r["_xml"].with_name(r["_xml"].name.replace(".xml", ".iso.json")).exists() for r in recs):
        schema_links = ", ".join(
            f"[{r['message_type']}](/corpus/schemas/{r['message_type']}.schema.json)"
            for r in recs if r["_xml"].with_name(r["_xml"].name.replace(".xml", ".iso.json")).exists()
        )
        lines += ["", t["twin_para"].format(schemas=schema_links), ""]
    else:
        lines.append("")
    if sample:
        # A fragment, not a query string: Search Console listed 41
        # /try/?sample=… variants as alternates of /try/; a fragment is
        # the same URL to a crawler and the demo reads either.
        demo = f"/try/#sample=corpus:{sid}" if locale == "en" else f"/{locale}/try/#sample=corpus:{sid}"
        lines += [
            f"## {t['h_run']}",
            "",
            t["run_para"].format(url=demo, n=sample["records"], scheme=sample["scheme"]),
            "",
            t["flat_records"],
            "",
            "```csv",
            sample["csv"].strip(),
            "```",
            "",
        ]
    lines += [f"## {t['h_checked']}", ""]
    xsd = (validation.get("xsd") or {}).get("errors", 0)
    mdr = (validation.get("mdr") or {}).get("errors", 0)

    def verdict(errs: int) -> str:
        return t["passed"] if not errs else t["errors"].format(n=errs)

    lines.append(f"- **{t['xsd']}**: {verdict(xsd)}.")
    lines.append(f"- **{t['mdr']}**: {verdict(mdr)}.")
    for name, v in profiles.items():
        errs = (v or {}).get("errors", 0)
        warns = (v or {}).get("warnings", 0)
        lines.append(f"- **{t['profile']} `{name}`**: {verdict(errs)}"
                     + (", " + t["warnings"].format(n=warns) if warns else "") + ".")
    conf = prov.get("confidence", "unknown")
    lines += ["", t["confidence"].format(level=t["levels"].get(conf, conf),
                                         note=t["notes"].get(conf, conf)), "",
              f"## {t['h_sources']}", ""]
    if sources:
        for src in sources:
            title = str(src.get("title", "")).strip()
            read = src.get("read") or src.get("retrieved") or ""
            url = src.get("url") or ""
            item = f"[{title}]({url})" if url else title
            lines.append(f"- {item}" + (" " + t["read"].format(date=read) if read else ""))
    else:
        lines.append(f"- {t['public_only']}")
    lines += ["", t["sha_para"], "",
              f"[{t['back']}](/example-corpus/) · [{t['all_by_country']}](/example-corpus/#payment-files-by-country)"]
    return "\n".join(lines)


def copy_schemas(lib: Path) -> int:
    """Serve the twin JSON Schemas the library bundles, one per edition."""
    src = lib / "pain001" / "schemas" / "iso-json"
    target = STATIC / "schemas"
    _clear(target)
    target.mkdir(parents=True, exist_ok=True)
    n = 0
    for path in sorted(src.glob("*.schema.json")):
        (target / path.name).write_bytes(path.read_bytes())
        n += 1
    return n


def write_index(files: list[dict], version: str) -> None:
    """A machine-readable index of the corpus: one entry per scenario, every URL absolute."""
    base = "https://pain001.com"
    scenarios: dict[str, list[dict]] = defaultdict(list)
    for record in files:
        scenarios[record["scenario"]].append(record)
    samples = load_try_samples()
    entries = []
    for sid, recs in sorted(scenarios.items()):
        first = recs[0]
        editions = []
        for r in recs:
            rel = r["_rel"]
            entry = {
                "message_type": r["message_type"],
                "xml": f"{base}/corpus/market/{rel}",
                "provenance": f"{base}/corpus/market/{rel.replace('.xml', '.provenance.yaml')}",
                "sha256": r.get("sha256"),
            }
            if r["_xml"].with_name(r["_xml"].name.replace(".xml", ".iso.json")).exists():
                entry["twin"] = f"{base}/corpus/market/{rel.replace('.xml', '.iso.json')}"
                entry["twin_schema"] = f"{base}/corpus/schemas/{r['message_type']}.schema.json"
            editions.append(entry)
        entries.append({
            "id": sid,
            "country": first.get("country"),
            "family": first.get("family"),
            "description": str(first.get("description", "")).strip(),
            "page": f"{base}/{scenario_slug(sid)}/",
            "confidence": (first.get("provenance") or {}).get("confidence"),
            "rails": [p for p in ((first.get("validation") or {}).get("profiles") or {}) if p != "anti-duplicate"],
            "demo": f"{base}/try/#sample=corpus:{sid}" if sid in samples else None,
            "editions": editions,
        })
    (STATIC / "index.json").write_text(json.dumps({
        "pain001": version,
        "catalog": f"{base}/example-corpus/",
        "license": "Apache-2.0 OR MIT",
        "scenarios": entries,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def _locale_frontmatter(fm: str, loc: str, slug: str) -> str:
    """Retarget a cloned English front matter at /<loc>/<slug>/ in that locale."""
    lang, posix = CORPUS_LOCALES[loc]
    fm = fm.replace(f"https://pain001.com/{loc}-{slug}/", f"https://pain001.com/{loc}/{slug}/")
    for key, value in (("hreflang", lang), ("language", lang), ("locale", posix)):
        fm, n = re.subn(rf'^{key}: .*$', f'{key}: "{value}"', fm, flags=re.M)
        if not n:
            fm = fm.replace("\n\n---\n\n", f'\n{key}: "{value}"\n\n---\n\n', 1)
    return fm


def write_scenario_pages(files: list[dict], version: str) -> int:
    """One page per scenario in English plus one per corpus locale; returns how
    many were written. Also records the JSON-LD for post-build injection, keyed
    by the page's final path (the locale variants are built at /<loc>-<slug>/
    and moved under /<loc>/ by postbuild_fix.relocate_corpus_locales)."""
    scenarios: dict[str, list[dict]] = defaultdict(list)
    for record in files:
        scenarios[record["scenario"]].append(record)
    samples = load_try_samples()
    stamp = _dt.date.today().isoformat()
    ld: dict[str, dict] = {}
    for sid, recs in sorted(scenarios.items()):
        first = recs[0]
        slug = scenario_slug(sid)
        desc = str(first.get("description", "")).strip()
        family = first.get("family", "")
        for loc in ("en", *CORPUS_LOCALES):
            t = L10N[loc]
            country = t["countries"].get(first.get("country", ""), first.get("country", "").upper())
            post_slug = slug if loc == "en" else f"{loc}-{slug}"
            fm = load_frontmatter(
                post_slug,
                t["title"].format(sid=sid, country=country, family=family),
                t["meta_desc"].format(desc=desc, country=country, family=family),
                t["eyebrow"],
                desc,
                t["keywords"].format(sid=sid, country=country, family=family),
            )
            if loc != "en":
                fm = _locale_frontmatter(fm, loc, slug)
            write_post(post_slug, stamp_date(fm), scenario_page(sid, recs, version, samples.get(sid), loc))
            if loc == "en":
                ld[slug] = dataset_ld(sid, recs, version, stamp)
            else:
                ld[f"{loc}/{slug}"] = dataset_ld(sid, recs, version, stamp, CORPUS_LOCALES[loc][0],
                                                 f"https://pain001.com/{loc}/{slug}/")
    (HERE / "corpus_pages.json").write_text(json.dumps(ld, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(ld)


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
        ("If you are connecting a system to a bank, writing a parser, or "
        "testing a mapping, you need sample ISO 20022 files that are "
        "correct for your country and your rail. The ones passed around "
        "are usually old, hand-edited, or from somewhere else. This page "
        "gives you files built from the public rulebooks, with a record of "
        "where each one comes from."),
        "",
        "**What you get**",
        "",
        (f"- **{len(scenarios)} realistic payments** across "
        f"{len(by_country)} countries: a UK CHAPS property purchase, a Swiss "
        "QR-bill, a Swedish Bankgiro run, a US ACH payroll, a SEPA direct "
        "debit, and more, each rendered in the message editions you are "
        "likely to meet."),
        (f"- **{coverage_files} schema coverage files** across "
        f"{len(editions)} editions: deliberately exhaustive files that "
        "exercise the elements and choices of one schema edition, for "
        "testing a parser or a mapping against the whole schema rather "
        "than the usual happy path."),
        ("- **A provenance record beside every payment file** saying where "
        "its content comes from, how far to trust it, and how the library "
        "checked it."),
        "",
        "**How to use it**",
        "",
        ("1. Download the complete bundle below, or pick single files from "
        "the tables."),
        ("2. Open the `.xml` next to your own file and diff them; open the "
        "`.provenance.yaml` to see what the differences mean."),
        ("3. Get your bank's usage guideline (see below) and apply it on top: "
        "these files follow the public scheme rules, not any one bank's "
        "profile."),
        "",
        ("Identifiers are synthetic: IBANs, BICs, LEIs and account numbers "
        "pass their check digits but belong to nobody, and names and "
        "addresses are invented. **Do not send these files to a bank.**"),
        "",
        "## Download",
        "",
        "| Bundle | Contents | Size |",
        "| :--- | :--- | ---: |",
        (f"| [Complete corpus](/corpus/{full_zip}) | "
        f"{len(files)} payment files with their provenance records, and "
        f"{coverage_files} schema coverage files across {len(editions)} "
        f"editions | {kb(sizes[full_zip])} |"),
        (f"| Coverage files per edition | one zip each, listed on the "
        f"[coverage page](/{COVERAGE_SLUG}/) | 9 to 12 KB |"),
        "",
        (f"Everything here is generated from pain001 {version}'s own corpus, "
        "which also ships inside the Python package (`pain001.corpus`) and "
        f"in the [repository]({REPO}/tree/main/pain001/corpus/data)."),
        "",
        *worked_example(files),
        "## Your bank's guideline",
        "",
        ("Every bank and clearing house publishes its own **message usage "
        "guideline**: which ISO 20022 elements it requires, which it "
        "ignores, and the values it accepts. Two banks on the same scheme "
        "can differ. Those guidelines are the bank's documentation, so "
        "they are not reproduced here: **download them from your bank or "
        "financial organisation**, typically from its client portal or "
        "from its collection on Swift MyStandards, and treat them as the "
        "final word."),
        "",
        ("The library is built for that step. Its overlay grammar expresses "
        "a guideline as a short list of rules (an element that must be "
        "present, one that must be absent, a value that must be one of a "
        "set), `scripts/derive_overlay.py` reads a guideline's schema and "
        "drafts those rules for you, and the corpus builder can then "
        "render any scenario on this page the way your bank wants it, "
        "privately, in your own environment. The "
        f"[corpus guide]({REPO}/blob/main/docs/corpus.md) walks through it."),
        "",
        "## How the library checked these files",
        "",
        "| Step | What it checks |",
        "| :--- | :--- |",
    ]
    body += [f"| {name} | {what} |" for name, what in RUNGS]
    body += [
        "",
        ("These checks are the library's own; they are not a certification, "
        "and passing them does not mean a bank will accept the file. "
        "Channel rules, onboarding profiles, cut-off times and the bank's "
        "guideline sit on top."),
        "",
        ("**Reading the evidence column.** `verified` means "
        f"{confidence_note('verified')}. `derived` means "
        f"{confidence_note('derived')}. `assumed` means "
        f"{confidence_note('assumed')}."),
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
                f"| [`{sid}`](/{scenario_slug(sid)}/) | {esc(first.get('description', ''))} | "
                f"{', '.join(f'`{p}`' for p in profiles) or 'base rules only'} | "
                f"{editions_md} | {confidence} |")
        body.append("")

    body += [
        "## Schema coverage files",
        "",
        ("Each edition has a small set of files built so that the elements "
        "and choice branches its schema declares each appear in at least "
        "one file. The first file is the baseline that carries every "
        "element once; each later file is named after the blocks it adds, "
        "so you can pick the one that exercises what you are testing. "
        f"The [coverage page](/{COVERAGE_SLUG}/) lists every file with what "
        "it adds and a zip per edition."),
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
        ("- The site publishes the generic files and their public sources. "
        "Bank-specific material stays with the banks."),
        ("- The corpus is English only and grows with every release; it is "
        "generated data, not a translated page."),
        (f"- The [corpus guide]({REPO}/blob/main/docs/corpus.md) explains the "
        "scenario format, the overlay grammar and how to add a country or a "
        "rail. Corrections and new scenarios are welcome there."),
        ("- Regenerate this page and its downloads with "
        "`poetry run python3 scripts/generate_corpus_page.py` from the "
        "pain001 checkout after a corpus change."),
    ]
    return "\n".join(body)


def render_coverage_page(editions: list[dict], sizes: dict[str, int],
                         version: str) -> str:
    body = [
        ("Schema coverage files are not realistic payments. Each set is "
        "generated from the schema itself so that the element paths and "
        "choice branches of one edition each appear in at least one of its "
        "files, and every file is valid against the schema and the ISO "
        "message definition report rules. Use them to smoke-test a parser, "
        "a mapping or a validator against the whole schema."),
        "",
        ("**How to pick a file.** The first file of every set is the "
        "baseline: every element once, first branch of every choice. Each "
        "later file adds elements and choice branches the earlier files did "
        "not reach, and is named after the blocks most of that new content "
        "falls under (`RmtInf` for remittance information, `UltmtDbtr` for "
        "the ultimate debtor, `ChqInstr` for cheque instructions, and so "
        "on). The recipe in the name says what kind of payment the file is: "
        "a credit transfer, a cheque delivered to the creditor agent, a "
        "cheque with no creditor agent, or a direct debit collection."),
        "",
        ("These files follow the ISO schema only. What your bank accepts is "
        "in its usage guideline; get it from your bank."),
        "",
        ("The [example corpus](/example-corpus/) page has the realistic "
        "payment files and the complete download."),
        "",
    ]
    for edition in editions:
        mt = edition["message_type"]
        name = f"pain001-coverage-{mt}-{version}.zip"
        body += [
            f"## {mt}",
            "",
            (f"{len(edition['_files'])} files. "
            f"[Download the set](/corpus/{name}) ({kb(sizes[name])})."),
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
    if lib is None:
        sys.exit(
            "usage: generate_corpus_page.py <pain001 checkout>  "
            "(or set PAIN001_LIB); the library path is never guessed"
        )
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
    pages = write_scenario_pages(files, version)
    write_index(files, version)
    schemas = copy_schemas(lib)
    fm = load_frontmatter(
        SLUG,
        "ISO 20022 example files: pain.001 and pain.008 samples per country and rail",
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
    print(f"wrote {pages} scenario pages, corpus/index.json, {schemas} twin schemas")
    coverage_fm = load_frontmatter(
        COVERAGE_SLUG,
        "ISO 20022 schema coverage files: every element of every edition",
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
