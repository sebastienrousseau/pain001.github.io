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

ROOT = Path(__file__).resolve().parent.parent
site = ROOT / "docs"
PAGES = ("why", "solutions", "executive-brief")

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
    for m in re.finditer(
            r"<(h[123]|p|li|th|td|button|label|strong|summary|option|"
            r"figcaption|caption|blockquote|dt|dd)\b[^>]*>(.*?)</\1>",
            main, re.S):
        inner = m.group(2).strip()
        if not inner or re.search(r"<(h[123]|p|li|div|section)\b", inner):
            continue
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        if not plain or not re.search(r"[A-Za-z]{3}", plain):
            continue
        if plain in (meta["title"], meta["eyebrow"], meta["deck"]):
            continue
        if plain.startswith(("pip ", "pain001 ", "v0.")):
            continue
        text[inner] = inner
    for m in re.finditer(r'aria-label="([^"]{3,120})"', main):
        if re.search(r"[A-Za-z]{3}", m.group(1)):
            aria[m.group(1)] = m.group(1)

    out[page] = {"meta": meta, "text": text, "aria": aria}
    words = sum(len(re.sub(r"<[^>]+>", " ", k).split()) for k in text)
    print(f"{page}: text={len(text)} aria={len(aria)} words={words}")

dest = ROOT / "scripts" / "pages_i18n"
dest.mkdir(exist_ok=True)
(dest / "en.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote scripts/pages_i18n/en.json")
