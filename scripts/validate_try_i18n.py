#!/usr/bin/env python3
"""Validate the per-locale try_i18n tables against en.json:
key parity per section, HTML-tag preservation, and a warning for
values left identical to the English source."""
import json
import re
import sys
from pathlib import Path

d = Path(__file__).parent / "try_i18n"
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
    for sec in ("meta", "text", "aria", "chrome", "chrome_aria"):
        if set(t.get(sec, {})) != set(en.get(sec, {})):
            missing = set(en.get(sec, {})) - set(t.get(sec, {}))
            extra = set(t.get(sec, {})) - set(en.get(sec, {}))
            errs.append(f"{sec}: missing={len(missing)} extra={len(extra)}"
                        + (f" e.g. {list(missing)[:1]}" if missing else ""))
    for k, v in t.get("text", {}).items():
        if k in en["text"] and tags(k) != tags(v):
            errs.append(f"tag mismatch: {k[:60]!r}")
        if v == k and len(re.sub(r'<[^>]+>', '', k).split()) > 2:
            same += 1
    if errs:
        print(f"FAIL {slug}: " + "; ".join(errs[:4]))
        fail += 1
    else:
        note = f" (untranslated-looking: {same})" if same else ""
        print(f"OK {slug} text={len(t['text'])}{note}")

sys.exit(1 if fail else 0)
