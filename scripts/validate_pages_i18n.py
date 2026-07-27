#!/usr/bin/env python3
"""Validate scripts/pages_i18n/<slug>.json against en.json:
page/section/key parity, HTML-tag preservation, untranslated warnings."""
import json
import re
import sys
from pathlib import Path

d = Path(__file__).parent / "pages_i18n"
en = json.loads((d / "en.json").read_text(encoding="utf-8"))
fail = 0

def tags(s):
    return sorted(re.findall(r"<[^>]+>", s))

for path in sorted(d.glob("*.json")):
    slug = path.stem
    if slug == "en":
        continue
    try:
        t = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"FAIL {slug}: invalid JSON ({e})")
        fail += 1
        continue
    errs, same = [], 0
    if set(t) != set(en):
        errs.append(f"pages: {sorted(set(en) ^ set(t))}")
    for page in en:
        for sec in ("meta", "text", "aria"):
            if set(t.get(page, {}).get(sec, {})) != set(en[page][sec]):
                errs.append(f"{page}.{sec}: key mismatch")
        for k, v in t.get(page, {}).get("text", {}).items():
            if k in en[page]["text"] and tags(k) != tags(v):
                errs.append(f"{page}: tag mismatch {k[:50]!r}")
            if v == k and len(re.sub(r"<[^>]+>", "", k).split()) > 2:
                same += 1
    if errs:
        print(f"FAIL {slug}: " + "; ".join(errs[:4]))
        fail += 1
    else:
        note = f" (untranslated-looking: {same})" if same else ""
        print(f"OK {slug}{note}")

sys.exit(1 if fail else 0)
