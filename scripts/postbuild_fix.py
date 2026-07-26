#!/usr/bin/env python3
"""Post-build repairs for the ssg output, run by build.sh before publish.

Local ssg builds (0.0.47) emit two entity-escaping artifacts, the same
class of bug sebastienrousseau.github.io repairs in its postbuild:

1. Head metas: the ``{{primary}}``/partial expansion right after
   ``<title>`` ships entity-escaped (``&lt;meta ...&gt;``), which browsers
   render as visible prose and crawlers cannot read.
2. Content bodies: the rendered markdown substituted for ``{{content}}``
   ships fully escaped, gated by the ``&lt;div lang=`` marker. Code
   samples inside are double-escaped, so a single unescape yields the
   correct final HTML.

This script also:

3. Injects CSP + og:image metas into the taxonomy-generated
   ``tags/<slug>/index.html`` pages (their internal template has neither,
   failing the csp_sri and metadata audit gates).
4. Regenerates ``sitemap.xml`` from the directory tree, because the
   ssg sitemap plugin emits an empty urlset under this configuration.

Idempotent: every pass is a no-op when its artifact is absent.
"""

from __future__ import annotations

import html as _html
import re
import sys
from datetime import date
from pathlib import Path

BASE_URL = "https://pain001.com"

_ESCAPED_HEAD_TAG = re.compile(r"&lt;(?:meta|link)\b.*?(?:&gt;|>)", re.DOTALL)
_BODY_MARKER = "&lt;div lang="

# (container-open variants, container-close) pairs that may hold an
# escaped {{content}} blob. Close is searched literally: the escaped blob
# cannot contain a literal close tag, so first match ends the container.
_CONTAINERS = [
    (('<article class="content-body">', "<article class=content-body>"), "</article>"),
    (('<div class="content-body">', "<div class=content-body>"), "</div>"),
    (("<article>",), "</article>"),
]

# Byte-identical to the policy ssg emits after extracting inline assets
# (it drops 'unsafe-inline'), so the CSP-DRIFT audit sees one policy.
CSP_META = (
    "<meta content=\"default-src 'self'; base-uri 'self'; "
    "object-src 'none'; img-src 'self' https://cloudcdn.pro data:; "
    "style-src 'self' ; script-src 'self'  'wasm-unsafe-eval'; "
    "connect-src 'self'; font-src 'self'; "
    "form-action 'self' https://formspree.io\" "
    "http-equiv=Content-Security-Policy>"
)
OG_IMAGE_META = (
    '<meta property="og:image" '
    'content="https://cloudcdn.pro/pain001/v1/logos/pain001.svg" />'
    '<meta property="og:image:alt" content="Pain001 logo" />'
)


def fix_head(html: str) -> str:
    end = html.find("</head>")
    if end == -1:
        return html
    head = html[:end]
    if "&lt;meta" not in head and "&lt;link" not in head:
        return html
    head = _ESCAPED_HEAD_TAG.sub(lambda m: _html.unescape(m.group(0)), head)
    return head + html[end:]


# ssg auto-injects a second <meta name=description> synthesised from page
# text (breadcrumb prose included) and a second viewport. Keep the first
# occurrence — the authored one — and drop the rest. theme-color is left
# alone: its light/dark pair legitimately repeats with different media.
_DEDUPE_NAMES = ("description", "viewport")


def dedupe_head_metas(html: str) -> str:
    end = html.find("</head>")
    if end == -1:
        return html
    head = html[:end]
    for name in _DEDUPE_NAMES:
        pattern = re.compile(r"<meta\s+name=\"?%s\"?[^>]*>\s*" % name)
        matches = list(pattern.finditer(head))
        for m in reversed(matches[1:]):
            head = head[: m.start()] + head[m.end() :]
    return head + html[end:]


def fix_body(html: str) -> str:
    for opens, close in _CONTAINERS:
        for open_tag in opens:
            start = html.find(open_tag)
            if start == -1:
                continue
            inner_start = start + len(open_tag)
            inner_end = html.find(close, inner_start)
            if inner_end == -1:
                continue
            inner = html[inner_start:inner_end]
            if _BODY_MARKER not in inner:
                continue
            html = html[:inner_start] + _html.unescape(inner) + html[inner_end:]
    return html


_H2_RE = re.compile(r"<h2>(.*?)</h2>", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_ARTICLE_RE = re.compile(
    r"(<article class=\"?content-body\"?>)(.*?)(</article>)", re.DOTALL
)
_META_RE = re.compile(r"(<div class=\"?article-meta\"?>)")


def _slugify(text: str) -> str:
    text = _TAG_RE.sub("", text)
    text = _html.unescape(text)
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def add_article_furniture(html: str) -> str:
    """Heading ids + anchor links, a Contents block for long pages, and a
    reading-time entry in the article meta bar. Idempotent via the
    heading-anchor marker."""
    if "heading-anchor" in html:
        return html
    m = _ARTICLE_RE.search(html)
    if not m:
        return html
    open_tag, body, close_tag = m.groups()

    entries = []
    seen: dict[str, int] = {}

    def anchor(match: re.Match) -> str:
        inner = match.group(1)
        slug = _slugify(inner)
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        if n:
            slug = f"{slug}-{n + 1}"
        label = _TAG_RE.sub("", inner)
        entries.append((slug, label))
        return (
            f'<h2 id="{slug}">{inner}'
            f'<a class="heading-anchor" href="#{slug}" '
            f'aria-label="Link to section: {label}">#</a></h2>'
        )

    body = _H2_RE.sub(anchor, body)

    if len(entries) >= 4:
        # The TOC list already numbers entries (decimal-leading-zero), so a
        # heading's own "01. " prefix would double up — strip it here only.
        strip_num = re.compile(r"^\d{1,2}\. ")
        items = "".join(
            '<li><a href="#%s">%s</a></li>' % (slug, strip_num.sub("", label))
            for slug, label in entries
        )
        toc = (
            '<nav class="article-toc" aria-label="Contents">'
            "<h2>Contents</h2><ol>" + items + "</ol></nav>"
        )
        body = toc + body

    html = html[: m.start()] + open_tag + body + close_tag + html[m.end() :]

    words = len(_TAG_RE.sub(" ", body).split())
    minutes = max(1, round(words / 220))
    html = _META_RE.sub(
        r"\1<span>%d min read</span>" % minutes, html, count=1
    )
    return html


_TABLE_RE = re.compile(r"<table\b.*?</table>", re.DOTALL)
_THEAD_RE = re.compile(r"<thead\b.*?</thead>", re.DOTALL)
_TH_RE = re.compile(r"<th\b[^>]*>(.*?)</th>", re.DOTALL)
_TR_RE = re.compile(r"<tr\b.*?</tr>", re.DOTALL)
_CELL_RE = re.compile(r"<t([dh])\b([^>]*)>")


def stamp_table_labels(html: str) -> str:
    """Stamp data-label="<column header>" on every body td so the
    narrow-screen card layout can name each cell. Labels map by column
    position within the row (row-header th cells advance the position but
    are never stamped). Idempotent."""

    def process(match: re.Match) -> str:
        table = match.group(0)
        if "data-label" in table:
            return table
        thead = _THEAD_RE.search(table)
        if not thead:
            return table
        headers = [
            _html.unescape(_TAG_RE.sub("", h)).strip()
            for h in _TH_RE.findall(thead.group(0))
        ]
        if not headers:
            return table
        body = table[thead.end():]

        def process_row(row: re.Match) -> str:
            pos = {"i": 0}

            def stamp(cell: re.Match) -> str:
                idx = pos["i"]
                pos["i"] += 1
                if cell.group(1) == "h" or idx >= len(headers):
                    return cell.group(0)
                safe = headers[idx].replace('"', "&quot;")
                return f'<td data-label="{safe}"{cell.group(2)}>'

            return _CELL_RE.sub(stamp, row.group(0))

        body = _TR_RE.sub(process_row, body)
        return table[: thead.end()] + body

    return _TABLE_RE.sub(process, html)


# ssg's syntax highlighter nests a second <pre style="background..."> with
# inline-styled spans INSIDE the markdown <pre><code> block. The inline
# styles are blocked by the strict CSP (style-src 'self'), leaving broken
# box artifacts around every fenced code sample. Unwrap: drop the inner
# pre and all span wrappers, keeping the text; the layouts style code
# blocks with theme tokens.
_CODE_BLOCK_RE = re.compile(r"(<pre><code[^>]*>)(.*?)(</code></pre>)", re.DOTALL)
_INNER_PRE_RE = re.compile(r"</?pre[^>]*>")
_SPAN_RE = re.compile(r"</?span[^>]*>")


def fix_code_blocks(html: str) -> str:
    def unwrap(m: re.Match) -> str:
        inner = _SPAN_RE.sub("", _INNER_PRE_RE.sub("", m.group(2)))
        return m.group(1) + inner.strip("\n") + m.group(3)

    return _CODE_BLOCK_RE.sub(unwrap, html)


# ssg's markdown renderer emits presentational align attributes on table
# cells, which fail WCAG H49 (163 AAA errors across the site). CSS handles
# alignment; strip the attribute.
_ALIGN_ATTR_RE = re.compile(r"(<t[dhr]\b[^>]*?)\s+align=\"?[a-z]+\"?")


def strip_align_attrs(html: str) -> str:
    return _ALIGN_ATTR_RE.sub(r"\1", html)


_BODY_LINK_RE = re.compile(r"<link rel=\"stylesheet\"[^>]*>")


def relocate_body_stylesheets(html: str) -> str:
    """ssg's search widget injects its <link rel=stylesheet> inside <body>,
    which fails WCAG H59 (link elements belong in <head>). Move any
    body-level stylesheet links into the head, preserving SRI attributes."""
    head_end = html.find("</head>")
    if head_end == -1:
        return html
    body = html[head_end:]
    moved = _BODY_LINK_RE.findall(body)
    if not moved:
        return html
    body = _BODY_LINK_RE.sub("", body)
    return html[:head_end] + "".join(moved) + body


def fix_tag_pages(site: Path) -> None:
    for page in site.glob("tags/*/index.html"):
        html = page.read_text(encoding="utf-8")
        inject = ""
        if "Content-Security-Policy" not in html:
            inject += CSP_META
        if 'property="og:image"' not in html:
            inject += OG_IMAGE_META
        if inject:
            page.write_text(html.replace("</head>", inject + "</head>", 1), encoding="utf-8")
            print(f"[postbuild] patched CSP/og:image: {page}")


def fix_manifest(site: Path) -> None:
    """ssg emits "theme_color": null (it only understands the legacy RGB
    triple), which Chrome logs as an invalid-type warning. Pin valid hexes."""
    import json

    path = site / "manifest.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("theme_color"), str) or not data["theme_color"].startswith("#"):
        data["theme_color"] = "#0b0e14"
    if not isinstance(data.get("background_color"), str):
        data["background_color"] = "#ffffff"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("[postbuild] manifest.json theme_color fixed")


def regen_sitemap(site: Path) -> None:
    today = date.today().isoformat()
    urls = []
    for page in sorted(site.rglob("index.html")):
        rel = page.parent.relative_to(site).as_posix()
        if rel.startswith(("api/", "_csp", ".")) or rel in ("404", "offline"):
            continue
        loc = BASE_URL + "/" if rel == "." else f"{BASE_URL}/{rel}/"
        urls.append(
            "<url>\n"
            f"  <loc>{loc}</loc>\n"
            f"  <lastmod>{today}</lastmod>\n"
            "  <changefreq>weekly</changefreq>\n"
            "</url>"
        )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (site / "sitemap.xml").write_text(body, encoding="utf-8")
    print(f"[postbuild] sitemap.xml regenerated with {len(urls)} URLs")


def main() -> None:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "Pain001")
    repaired = 0
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        fixed = relocate_body_stylesheets(
            fix_code_blocks(
                strip_align_attrs(
                    stamp_table_labels(
                        add_article_furniture(
                            fix_body(dedupe_head_metas(fix_head(html)))
                        )
                    )
                )
            )
        )
        if fixed != html:
            page.write_text(fixed, encoding="utf-8")
            repaired += 1
    print(f"[postbuild] unescaped head/body markup on {repaired} page(s)")
    fix_tag_pages(site)
    fix_manifest(site)
    regen_sitemap(site)


if __name__ == "__main__":
    main()
