#!/usr/bin/env python3
"""Check that every English translation key still occurs in the page it
translates.

The parity validators compare locale tables against en.json, so they
stay green even when en.json itself has drifted away from the built
site. A key that matches nothing is not an error anywhere — the
substring replace simply does nothing, and the page silently ships in
English. That is how the /why/ closing paragraph and the executive
brief's print note reached production untranslated in all 34 locales:
postbuild rewrote the legacy /executive-brief-fr/ URLs inside them, and
the keys captured before that rewrite stopped matching.

Run against docs/ after a build. Fix a failure by re-running the
extractor and migrating the locale tables to the new key — never by
deleting the key, which just restores the silence.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"

# table dir -> {page slug: built page path relative to docs/}
TABLES = {
    "pages_i18n": None,   # page slugs are the directory names
    "docs_i18n": None,
    "try_i18n": {"try": "try"},
}


def page_html(slug: str) -> str | None:
    p = SITE / slug / "index.html"
    if not p.exists():
        return None
    html = p.read_text(encoding="utf-8")
    return html[html.find("<main"):html.find("</main>")] or html


def check_table(dirname: str) -> int:
    en_path = ROOT / "scripts" / dirname / "en.json"
    if not en_path.exists():
        return 0
    en = json.loads(en_path.read_text(encoding="utf-8"))
    # try_i18n is a flat table for a single page; the others are keyed
    # by page slug.
    pages = ({"try": en} if "text" in en and "meta" in en
             else {k: v for k, v in en.items() if isinstance(v, dict)})
    bad = 0
    for slug, payload in pages.items():
        main = page_html(slug)
        if main is None:
            print(f"SKIP {dirname}/{slug}: no built page")
            continue
        missing = [k for k in payload.get("text", {}) if k not in main]
        aria = [k for k in payload.get("aria", {})
                if 'aria-label="%s"' % k not in main]
        if missing or aria:
            bad += 1
            print(f"FAIL {dirname}/{slug}: {len(missing)} text key(s) and "
                  f"{len(aria)} aria key(s) match nothing on the built page")
            for k in (missing + aria)[:3]:
                print(f"      {k[:150]}")
        else:
            n = len(payload.get("text", {})) + len(payload.get("aria", {}))
            print(f"OK {dirname}/{slug}: {n} key(s) all present")
    return bad


def main() -> int:
    if not SITE.is_dir():
        print("docs/ not built; run ./build.sh first", file=sys.stderr)
        return 1
    bad = sum(check_table(d) for d in TABLES)
    if bad:
        print(f"\n{bad} page(s) carry stale keys — those strings ship in "
              f"English. Re-extract and migrate the locale tables.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
