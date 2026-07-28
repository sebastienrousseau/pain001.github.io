#!/usr/bin/env python3
"""Extract message specifications from the official ISO 20022 XSDs.

Everything this produces is derived from the schemas shipped in the
pain001 library — the same files the validator uses. Nothing is
hand-transcribed, so the reference cannot drift from what the software
actually enforces, and every cardinality and code value is checkable
against ISO's own publication.

Output: scripts/message_specs/<version>.json plus an index.json holding
cross-version data (code-list coverage and element deltas).

Usage:
    python3 scripts/extract_message_specs.py [path-to-pain001-repo]
"""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

XS = "{http://www.w3.org/2001/XMLSchema}"
HERE = Path(__file__).resolve().parent
OUT = HERE / "message_specs"

DEFAULT_LIB = Path("/Users/seb/Code/Public/python/pain001")

# Schemas known to be placeholders rather than ISO publications. They
# are excluded rather than silently producing an empty specification.
PLACEHOLDER_MIN_BYTES = 10_000


def _text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return " ".join("".join(el.itertext()).split())


def parse_schema(xsd: Path) -> dict:
    """Return the message model: types, elements, and code lists."""
    root = ET.parse(xsd).getroot()
    complex_types: dict[str, dict] = {}
    simple_types: dict[str, dict] = {}

    for ct in root.findall(f"{XS}complexType"):
        name = ct.get("name")
        if not name:
            continue
        children = []
        for el in ct.iter(f"{XS}element"):
            children.append({
                "name": el.get("name"),
                "type": el.get("type"),
                "min": el.get("minOccurs", "1"),
                "max": el.get("maxOccurs", "1"),
                "doc": _text(el.find(f"{XS}annotation/{XS}documentation")),
            })
        # a choice means the children are alternatives, not a sequence
        is_choice = ct.find(f"{XS}choice") is not None
        complex_types[name] = {
            "name": name,
            "children": children,
            "kind": "choice" if is_choice else "sequence",
            "doc": _text(ct.find(f"{XS}annotation/{XS}documentation")),
        }

    for st in root.findall(f"{XS}simpleType"):
        name = st.get("name")
        if not name:
            continue
        restriction = st.find(f"{XS}restriction")
        base = restriction.get("base") if restriction is not None else None
        enums = [e.get("value") for e in st.iter(f"{XS}enumeration")]
        facets: dict[str, str] = {}
        if restriction is not None:
            for facet in ("minLength", "maxLength", "pattern", "totalDigits",
                          "fractionDigits", "minInclusive", "maxInclusive"):
                node = restriction.find(f"{XS}{facet}")
                if node is not None:
                    facets[facet] = node.get("value")
        simple_types[name] = {
            "name": name,
            "base": base,
            "codes": enums,
            "facets": facets,
            "doc": _text(st.find(f"{XS}annotation/{XS}documentation")),
        }

    root_el = root.find(f"{XS}element")
    return {
        "root_element": root_el.get("name") if root_el is not None else None,
        "root_type": root_el.get("type") if root_el is not None else None,
        "complex_types": complex_types,
        "simple_types": simple_types,
    }


def walk(model: dict, type_name: str, depth: int = 0, max_depth: int = 5,
         path: str = "", seen: tuple[str, ...] = ()) -> list[dict]:
    """Flatten the message tree into rows with XML paths and cardinality.

    Recursion is bounded and cycle-aware: ISO models are self-referential
    (a party contains an address contains a party), so an unbounded walk
    never terminates.
    """
    ct = model["complex_types"].get(type_name)
    if ct is None or depth > max_depth or type_name in seen:
        return []
    rows = []
    for child in ct["children"]:
        child_path = f"{path}/{child['name']}" if path else child["name"]
        st = model["simple_types"].get(child["type"])
        rows.append({
            "path": child_path,
            "name": child["name"],
            "type": child["type"],
            "min": child["min"],
            "max": child["max"],
            "depth": depth,
            "in_choice": ct["kind"] == "choice",
            "codes": st["codes"] if st else [],
            "facets": st["facets"] if st else {},
            "doc": child["doc"],
        })
        rows.extend(walk(model, child["type"], depth + 1, max_depth,
                         child_path, seen + (type_name,)))
    return rows


def walk_inline(el: ET.Element, depth: int = 0, max_depth: int = 6,
                path: str = "") -> list[dict]:
    """Walk a schema authored with inline (anonymous) complex types.

    The pain.001 schemas ISO publishes use named types, so `walk` above
    resolves them by name. pain.008.001.02 as shipped nests its types
    directly inside their elements, which that lookup cannot see — it
    reported zero elements rather than failing, which is exactly the kind
    of silent empty output worth catching.
    """
    if depth > max_depth:
        return []
    rows: list[dict] = []
    ct = el.find(f"{XS}complexType")
    if ct is None:
        return rows
    container = ct.find(f"{XS}sequence")
    is_choice = False
    if container is None:
        container = ct.find(f"{XS}choice")
        is_choice = container is not None
    if container is None:
        return rows
    for child in container.findall(f"{XS}element"):
        name = child.get("name")
        if not name:
            continue
        child_path = f"{path}/{name}" if path else name
        rows.append({
            "path": child_path,
            "name": name,
            "type": child.get("type") or "(inline)",
            "min": child.get("minOccurs", "1"),
            "max": child.get("maxOccurs", "1"),
            "depth": depth,
            "in_choice": is_choice,
            "codes": [e.get("value") for e in child.iter(f"{XS}enumeration")],
            "facets": {},
            "doc": _text(child.find(f"{XS}annotation/{XS}documentation")),
        })
        rows.extend(walk_inline(child, depth + 1, max_depth, child_path))
    return rows


def main() -> int:
    lib = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LIB
    templates = lib / "pain001" / "templates"
    if not templates.is_dir():
        print(f"library templates not found at {templates}", file=sys.stderr)
        return 1

    OUT.mkdir(exist_ok=True)
    versions: dict[str, dict] = {}
    skipped: list[str] = []

    for d in sorted(templates.glob("pain.*")):
        version = d.name
        xsd = d / f"{version}.xsd"
        if not xsd.exists():
            continue
        if xsd.stat().st_size < PLACEHOLDER_MIN_BYTES:
            skipped.append(version)
            continue
        model = parse_schema(xsd)
        rows = walk(model, model["root_type"] or "Document")
        if not rows:
            # schema authored with inline types (pain.008.001.02)
            root_el = ET.parse(xsd).getroot().find(f"{XS}element")
            if root_el is not None:
                rows = walk_inline(root_el)
        code_lists = {
            n: s for n, s in model["simple_types"].items() if s["codes"]
        }
        type_index = {
            name: {
                "name": name,
                "kind": ct["kind"],
                "children": [
                    {
                        "name": c["name"], "type": c["type"],
                        "min": c["min"], "max": c["max"],
                        "codes": (model["simple_types"].get(c["type"]) or {}).get("codes", []),
                        "facets": (model["simple_types"].get(c["type"]) or {}).get("facets", {}),
                    }
                    for c in ct["children"]
                ],
            }
            for name, ct in model["complex_types"].items()
        }
        payload = {
            "version": version,
            "type_index": type_index,
            "root_element": model["root_element"],
            "element_count": len(rows),
            "complex_type_count": len(model["complex_types"]),
            "code_list_count": len(code_lists),
            "elements": rows,
            "code_lists": code_lists,
            "simple_types": model["simple_types"],
        }
        (OUT / f"{version}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        versions[version] = payload
        print(f"{version}: {len(rows)} element rows, "
              f"{len(model['complex_types'])} types, "
              f"{len(code_lists)} code lists")

    # cross-version index: element deltas and code-list coverage
    index: dict = {"versions": sorted(versions), "skipped": skipped,
                   "deltas": {}, "code_list_coverage": {}}
    # deltas only make sense within one message family: comparing
    # pain.001.001.13 to pain.008.001.02 would report the entire direct
    # debit model as "added".
    families: dict[str, list[str]] = {}
    for v in sorted(versions):
        families.setdefault(v.rsplit(".", 1)[0], []).append(v)
    ordered = [v for fam in families.values() for v in fam]
    pairs = [(a, b) for fam in families.values()
             for a, b in zip(fam, fam[1:])]
    for prev, cur in pairs:
        a = {e["path"] for e in versions[prev]["elements"]}
        b = {e["path"] for e in versions[cur]["elements"]}
        index["deltas"][f"{prev}->{cur}"] = {
            "added": sorted(b - a),
            "removed": sorted(a - b),
        }
    for v, payload in versions.items():
        for name, cl in payload["code_lists"].items():
            entry = index["code_list_coverage"].setdefault(
                name, {"versions": [], "codes": cl["codes"]})
            entry["versions"].append(v)

    (OUT / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nindexed {len(versions)} version(s); "
          f"skipped placeholders: {skipped or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
