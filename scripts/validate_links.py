#!/usr/bin/env python3
"""Validate every link on every built page.

Checks, for each docs/**/*.html page:
- every internal href/src resolves to a file in the site tree
- every in-page anchor (#id) target exists on the destination page
- hreflang alternate and canonical URLs resolve to existing pages
- locale-consistency: on /<slug>/ and /<slug>/try/ pages, no plain
  href="/try/"> may remain (must stay in-locale), and language-menu
  entries must point at existing pages

External (http/https) links are collected and de-duplicated; pass
--external to HEAD-check them over the network.
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

site = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
BASE = "https://pain001.com"

pages = sorted(site.rglob("*.html"))
ids_cache: dict[Path, set] = {}

def page_ids(p: Path) -> set:
    if p not in ids_cache:
        h = p.read_text(encoding="utf-8", errors="replace")
        ids_cache[p] = set(re.findall(r'\bid="?([A-Za-z0-9_:.-]+)"?[\s>]', h))
    return ids_cache[p]

def resolve(path: str) -> Path | None:
    """Map a site-absolute path to a file under docs/."""
    path = unquote(path)
    if path.endswith("/"):
        cand = site / path.strip("/") / "index.html" if path != "/" else site / "index.html"
    else:
        cand = site / path.lstrip("/")
    if cand.exists():
        return cand
    # extensionless page refs (rare)
    alt = site / path.strip("/") / "index.html"
    return alt if alt.exists() else None

broken, anchor_bad, ext = [], [], set()
for page in pages:
    rel = "/" + page.relative_to(site).as_posix()
    h = page.read_text(encoding="utf-8", errors="replace")
    refs = re.findall(r'(?:href|src)="([^"]+)"', h)
    refs += re.findall(r"(?:href|src)=([^\s\"'>]+)", re.sub(r'(?:href|src)="[^"]*"', "", h))
    for ref in refs:
        ref = ref.strip()
        if not ref or ref.startswith(("mailto:", "tel:", "data:", "javascript:")):
            continue
        if ref.startswith(("http://", "https://")):
            if ref.startswith(BASE):
                ref = ref[len(BASE):] or "/"
            else:
                ext.add(ref)
                continue
        if ref.startswith("#"):
            frag = ref[1:]
            if frag and frag not in page_ids(page):
                anchor_bad.append((rel, ref))
            continue
        u = urlparse(ref)
        target = resolve(u.path if u.path else "/")
        if target is None:
            broken.append((rel, ref))
        elif u.fragment and u.fragment not in page_ids(target):
            anchor_bad.append((rel, ref))

# locale-consistency: locale pages must not link the English demo
locale_bad = []
for page in pages:
    rel = "/" + page.relative_to(site).as_posix()
    parts = page.relative_to(site).parts
    if len(parts) >= 2 and parts[0] not in ("tags", "api", "_csp", "try") \
            and (site / parts[0] / "index.html").exists() \
            and (Path(__file__).parent / "try_i18n" / f"{parts[0]}.json").exists():
        h = page.read_text(encoding="utf-8", errors="replace")
        if 'href="/try/">' in h:
            locale_bad.append(rel)

print(f"pages scanned: {len(pages)}")
print(f"unique external links: {len(ext)}")
for rel, ref in sorted(set(broken)):
    print(f"BROKEN  {rel}  ->  {ref}")
for rel, ref in sorted(set(anchor_bad)):
    print(f"ANCHOR  {rel}  ->  {ref}")
for rel in sorted(set(locale_bad)):
    print(f"LOCALE  {rel}  links English /try/")

if "--external" in sys.argv:
    import subprocess
    for url in sorted(ext):
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                            "-A", "Mozilla/5.0", "-m", "20", "-L", url],
                           capture_output=True, text=True)
        code = r.stdout.strip()
        mark = "OK" if code.startswith(("2", "3")) else "EXT-FAIL"
        if mark != "OK":
            print(f"{mark} {code}  {url}")

n_bad = len(set(broken)) + len(set(anchor_bad)) + len(set(locale_bad))
print(f"result: {'CLEAN' if n_bad == 0 else str(n_bad) + ' problem(s)'}")
sys.exit(1 if n_bad else 0)
