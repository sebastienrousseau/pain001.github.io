#!/usr/bin/env python3
"""Extract the translatable strings of /try/ (plus shared chrome labels)
into scripts/try_i18n/en.json. Keys are exact HTML fragments as they
appear in the built page; translators replace only the values.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
site = ROOT / "docs"
html = (site / "try" / "index.html").read_text(encoding="utf-8")

main = html[html.find("<main"):html.find("</main>")]
# The status strip is translated separately (STATUS_STRIP table).
main = re.sub(r"<section[^>]*\bstatus-strip\b[^>]*>.*?</section>", "", main, flags=re.S)
# Skip code blocks and scripts entirely; inline <code> stays part of
# its fragment so keys match the built page byte-for-byte.
main = re.sub(r"<(pre|script|style)\b[^>]*>.*?</\1>", "", main, flags=re.S)

text, aria = {}, {}
for m in re.finditer(
        r"<(h[123]|p|li|button|label|th|strong|summary|option|figcaption|caption|dt|dd)\b[^>]*>(.*?)</\1>",
        main, re.S):
    inner = m.group(2).strip()
    if not inner or "<h" in inner or "<p" in inner or "<li" in inner:
        continue  # keep leaf fragments only
    plain = re.sub(r"<[^>]+>", "", inner).strip()
    if not plain or not re.search(r"[A-Za-z]{3}", plain):
        continue
    if plain.startswith(("pip ", "pain001 ", "v0.")):
        continue
    text[inner] = inner

for m in re.finditer(r'aria-label="([^"]{3,120})"', main):
    if re.search(r"[A-Za-z]{3}", m.group(1)):
        aria[m.group(1)] = m.group(1)

title = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
desc = re.search(r'name="?description"? content="([^"]+)"', html)
if not desc:
    desc = re.search(r'content="([^"]+)" name="?description"?', html)

chrome_text = [
    "Who it&rsquo;s for", "Executive brief", "Comparison vs commercial tools",
    "Installation &amp; Docker", "Glossary", "FAQs", "pain.002 reason codes",
    "AI agent tools (MCP)", "Editor integration (LSP)", "MT101 loader",
    "Excel loader", "Architecture &amp; security", "2026 briefing",
    "ISO 20022 roadmap", "Cross-border guide", "In 34 languages",
    "Documentation", "Ecosystem", "Try it in your browser",
    "Technical reference", "Payment pipelines", "pain001-mcp · AI agents",
    "pain001-lsp · editors", "Cross-Border Guide",
    "Architecture &amp; patents", "Trust Centre", "Compatibility matrix",
    "Accessibility", "RSS feed",
]
chrome_aria = [
    "Toggle Why Pain001 submenu", "Toggle Docs submenu",
    "Toggle Suite submenu", "Toggle Research submenu",
]

# NOTE: exact forms were verified against a pristine (untranslated)
# build once; the landing pages are translated in place afterwards, so
# no existence filter is possible on later runs.
chrome = {s: s for s in chrome_text}
missing = []
c_aria = {s: s for s in chrome_aria}

out = {
    "meta": {"title": title, "description": desc.group(1) if desc else ""},
    "text": text,
    "aria": aria,
    "chrome": chrome,
    "chrome_aria": c_aria,
}
dest = ROOT / "scripts" / "try_i18n"
dest.mkdir(exist_ok=True)
(dest / "en.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"text={len(text)} aria={len(aria)} chrome={len(chrome)} "
      f"chrome_aria={len(c_aria)}")
if missing:
    print("chrome strings NOT found on /fr/ (check exact form):", missing, file=sys.stderr)
