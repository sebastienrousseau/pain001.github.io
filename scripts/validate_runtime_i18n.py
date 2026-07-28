#!/usr/bin/env python3
"""Validate scripts/runtime_i18n/<slug>.json against en.json:
key parity, {placeholder} parity, untranslated warnings."""
import json
import re
import sys
from pathlib import Path

d = Path(__file__).parent / "runtime_i18n"
en = json.loads((d / "en.json").read_text(encoding="utf-8"))
fail = 0

def ph(s):
    return sorted(re.findall(r"\{\w+\}", s))

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
        errs.append(f"keys: missing={len(set(en)-set(t))} extra={len(set(t)-set(en))}")
    for k, v in t.items():
        if k in en and ph(k) != ph(v):
            errs.append(f"placeholder mismatch: {k[:50]!r}")
        if v == k and len(k.split()) > 2:
            same += 1
    if errs:
        print(f"FAIL {slug}: " + "; ".join(errs[:4]))
        fail += 1
    else:
        note = f" (untranslated-looking: {same})" if same else ""
        print(f"OK {slug} keys={len(t)}{note}")

sys.exit(1 if fail else 0)
