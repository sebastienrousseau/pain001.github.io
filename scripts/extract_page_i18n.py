#!/usr/bin/env python3
"""Extract translatable strings from the core journey pages
(why, solutions, executive-brief) into scripts/pages_i18n/en.json.

Structure: { "<page>": { "meta": {title, description, eyebrow, deck},
                         "text": {fragment: fragment},
                         "aria": {label: label} } }

Keys are exact HTML fragments from the built pages; translators replace
only the values. Inline <code>/<a> markup stays inside its fragment.
"""
import json
import re
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parent.parent
site = ROOT / "docs"
# default: journey pages -> pages_i18n; pass a dir name + page slugs to
# extract another set (e.g. docs_i18n documentation faqs installation glossary)
OUT_DIR = sys.argv[1] if len(sys.argv) > 2 else "pages_i18n"
PAGES = tuple(sys.argv[2:]) if len(sys.argv) > 2 else ("why", "solutions", "executive-brief")

out = {}
for page in PAGES:
    html = (site / page / "index.html").read_text(encoding="utf-8")
    main = html[html.find("<main"):html.find("</main>")]
    main = re.sub(r"<(pre|script|style)\b[^>]*>.*?</\1>", "", main, flags=re.S)

    meta = {}
    meta["title"] = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
    m = (re.search(r'name="?description"? content="([^"]+)"', html)
         or re.search(r'content="([^"]+)" name="?description"?', html))
    meta["description"] = m.group(1) if m else ""
    for key, pat in (("eyebrow", r'<p class="eyebrow">([^<]+)</p>'),
                     ("deck", r'<p class="deck">([^<]+)</p>')):
        m = re.search(pat, html)
        meta[key] = m.group(1).strip() if m else ""

    text, aria = {}, {}
    # blockquote is deliberately absent: re.finditer yields
    # non-overlapping matches, so matching the blockquote swallows the
    # <p> inside it, and that <p> is then dropped by the container
    # filter below — the fragment vanishes from the table entirely
    # rather than failing loudly. Markdown always wraps blockquote
    # content in <p>, so letting the <p> match on its own loses nothing.
    for m in re.finditer(
            r"<(h[123]|p|li|th|td|button|label|strong|summary|option|"
            r"figcaption|caption|dt|dd)\b[^>]*>(.*?)</\1>",
            main, re.S):
        inner = m.group(2).strip()
        if not inner or re.search(r"<(h[123]|p|li|div|section)\b", inner):
            continue
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        if not plain or not re.search(r"[A-Za-z]{3}", plain):
            continue
        if plain in (meta["title"], meta["eyebrow"], meta["deck"]):
            continue
        # skip fragments that are only a command, but judge that on the
        # prose left after removing <code>: a list item may open with a
        # command and continue in prose, and testing the raw text drops
        # the whole sentence along with the command that introduced it.
        prose = re.sub(r"<code\b[^>]*>.*?</code>", " ", inner, flags=re.S)
        prose = " ".join(re.sub(r"<[^>]+>", " ", prose).split())
        if not re.search(r"[A-Za-z]{2,}", prose):
            continue
        if prose.startswith(("pip ", "pain001 ", "v0.")):
            continue
        text[inner] = inner
    for m in re.finditer(r'aria-label="([^"]{3,120})"', main):
        if re.search(r"[A-Za-z]{3}", m.group(1)):
            aria[m.group(1)] = m.group(1)

    out[page] = {"meta": meta, "text": text, "aria": aria}
    words = sum(len(re.sub(r"<[^>]+>", " ", k).split()) for k in text)
    print(f"{page}: text={len(text)} aria={len(aria)} words={words}")

dest = ROOT / "scripts" / OUT_DIR
dest.mkdir(exist_ok=True)
(dest / "en.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote scripts/{OUT_DIR}/en.json")
