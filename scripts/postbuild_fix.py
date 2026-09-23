#!/usr/bin/env python3
"""Post-build repairs for the ssg output, run by build.sh before publish.

Local ssg builds (0.0.63) emit two entity-escaping artifacts, the same
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

import hashlib
import base64
import html as _html
import json
import re
import sys
from datetime import date
from pathlib import Path

from css_minify import minify_css, strip_js_comments  # sibling module; scripts/ is on sys.path
from import_photos import band_path  # the band folder names the licence

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
    "object-src 'none'; img-src 'self' data:; "
    "style-src 'self'  'unsafe-hashes' 'sha256-+naa4DVyLB6dFJG6pe9ePhWQvc+IemcuXsxc1C9yQdg='; "
    "script-src 'self' 'sha256-%s' 'wasm-unsafe-eval'; "
    "connect-src 'self' https://cloudflareinsights.com; font-src 'self'; "
    "form-action 'self' https://formspree.io\" "
    "http-equiv=Content-Security-Policy>"
)
# The theme script must run before first paint, and as a separate file it
# was a render-blocking request on every page: Lighthouse put a third of
# the mobile first paint on it and scored 99 on the tablet and locale
# home pages. It is inlined instead, allowed by the hash above, and the
# file under /js/ stays as the source of truth.
_THEME_INIT_SRC = Path(__file__).resolve().parent.parent / "static" / "js" / "prism-theme-init.js"
_THEME_INIT_JS = strip_js_comments(_THEME_INIT_SRC.read_text(encoding="utf-8")).strip()
assert "</script" not in _THEME_INIT_JS.lower()
_THEME_INIT_TAG = "<script>%s</script>" % _THEME_INIT_JS
_THEME_INIT_LINK = '<script src="/js/prism-theme-init.js"></script>'
CSP_META = CSP_META % base64.b64encode(
    hashlib.sha256(_THEME_INIT_JS.encode("utf-8")).digest()).decode("ascii")
OG_IMAGE_META = (
    '<meta property="og:image" '
    'content="https://pain001.com/og/pain001-card.jpg" />'
    '<meta property="og:image:alt" content="Pain001 catches payment-file errors before your bank does" />'
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
        # ssg re-emits metas with attributes in arbitrary order
        # (``<meta content=... name=viewport>``), so anchoring on
        # ``name=`` first silently matched only one of the pair and
        # deduped nothing. Match any <meta> carrying the name instead.
        pattern = re.compile(
            r'<meta\b(?=[^>]*\bname=["\']?%s["\']?[\s>])[^>]*>\s*' % name)
        matches = list(pattern.finditer(head))
        for m in reversed(matches[1:]):
            head = head[: m.start()] + head[m.end():]
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


_PRE_BLOCK_RE = re.compile(r"<pre\b.*?</pre>", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"(<code\b[^>]*>)(.*?)(</code>)", re.DOTALL)


def escape_inline_code(html: str) -> str:
    """Re-escape angle brackets inside inline ``<code>`` spans.

    ``fix_body`` unescapes the whole content blob because ssg
    double-escapes it. Block code survives that (it was escaped twice),
    but inline code was escaped once, so a single pass strips it bare:
    markdown's ``` `<BIC>` ``` became a literal ``<code><BIC></code>``
    and the browser parsed ``<BIC>`` as an element. The element name
    disappeared from the page entirely — 184 times across 84 pages, on
    a site whose subject is ISO 20022 element names. Readers saw an
    empty code chip where ``<BIC>`` should be.

    ``<pre>`` blocks are excluded: their contents are legitimately
    marked up with syntax-highlighting spans, and escaping those would
    show the markup as text.
    """
    spans: list[str] = []

    def stash(m: re.Match) -> str:
        spans.append(m.group(0))
        return "\x00PRE%d\x00" % (len(spans) - 1)

    body = _PRE_BLOCK_RE.sub(stash, html)

    def fix(m: re.Match) -> str:
        inner = m.group(2)
        if "<" not in inner and ">" not in inner:
            return m.group(0)
        inner = inner.replace("<", "&lt;").replace(">", "&gt;")
        return m.group(1) + inner + m.group(3)

    body = _INLINE_CODE_RE.sub(fix, body)
    return re.sub(r"\x00PRE(\d+)\x00", lambda m: spans[int(m.group(1))], body)


_H2_RE = re.compile(r"<h2>(.*?)</h2>", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_ARTICLE_RE = re.compile(
    r'(<article class="[^"]*\bcontent-body\b[^"]*">)(.*?)(</article>)',
    re.DOTALL,
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

    # Two sections are enough to earn the rail: from 72rem it is what
    # fills the right of the container beside the 68ch text column, and
    # without it a short reference page read as a squashed left column.
    if len(entries) >= 2:
        # The TOC list already numbers entries (decimal-leading-zero), so a
        # heading's own "01. " prefix would double up — strip it here only.
        strip_num = re.compile(r"^\d{1,2}\. ")
        items = "".join(
            '<li><a href="#%s">%s</a></li>' % (slug, strip_num.sub("", label))
            for slug, label in entries
        )
        toc = (
            '<nav class="article-toc" aria-label="Contents" data-local-nav>'
            '<div class="toc-inner"><h2>Contents</h2><ol>' + items + "</ol></div></nav>"
        )
        body = toc + body

    html = html[: m.start()] + open_tag + body + close_tag + html[m.end() :]

    words = len(_TAG_RE.sub(" ", body).split())
    minutes = max(1, round(words / 220))
    html = _META_RE.sub(
        r"\1<span>%d min read</span>" % minutes, html, count=1
    )
    return html


_TABLE_BLOCK_RE = re.compile(r"<table\b.*?</table>", re.DOTALL)


def wrap_tables(html: str) -> str:
    """Put every article table in a scrollable, breakout-capable box.

    Markdown emits a bare ``<table>``, so 1136 of the site's 1261 tables
    had no wrapper: a table wider than the 68ch reading measure was
    simply clipped, with no way to reach the hidden columns. Only the
    125 hand-authored ones were wrapped.

    The wrapper is what the stylesheet targets to let wide tables escape
    the prose measure on large screens and to scroll on small ones, so
    this is what makes the CSS fix apply site-wide rather than to the
    handful someone remembered to wrap.

    Idempotent: a table already preceded by the wrapper is left alone,
    which also means a second postbuild pass is a no-op.
    """
    start, end = html.find("<main"), html.find("</main>")
    if start == -1 or end == -1:
        return html
    body = html[start:end]
    out, pos, wrapped = [], 0, 0
    for m in _TABLE_BLOCK_RE.finditer(body):
        # A nested table would break the non-greedy match; none exist
        # today, and saying so beats silently mangling one later.
        if "<table" in m.group(0)[6:]:
            print("[postbuild] WARNING: nested table left unwrapped")
            continue
        before = body[max(0, m.start() - 200):m.start()]
        # Already wrapped, by us or by ssg's own scroll region: a second
        # box inside ssg's region duplicated its landmark.
        if "table-responsive" in before[-80:] or "ssg-table-scroll" in before:
            continue
        out.append(body[pos:m.start()])
        out.append('<div class="table-responsive">')
        out.append(m.group(0))
        out.append("</div>")
        pos = m.end()
        wrapped += 1
    if not wrapped:
        return html
    out.append(body[pos:])
    return html[:start] + "".join(out) + html[end:]


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
_ESCAPED_CODE_BLOCK_RE = re.compile(
    r"<pre>(&lt;code\b.*?&gt;)(.*?)&lt;/code&gt;&lt;/pre&gt;", re.DOTALL
)
_ESCAPED_CODE_RE = re.compile(
    r"&lt;code(.*?)&gt;(.*?)&lt;/code&gt;", re.DOTALL
)
_INNER_PRE_RE = re.compile(r"</?pre[^>]*>")
_SPAN_RE = re.compile(r"</?span[^>]*>")


def fix_code_blocks(html: str) -> str:
    # ssg 0.0.63 can leave the structural code/pre delimiters encoded one
    # level deeper than the syntax-highlight spans. Restore only those
    # delimiters; code samples such as <BIC> must remain escaped text.
    def restore(m: re.Match) -> str:
        opening = _html.unescape(m.group(1))
        inner = _INNER_PRE_RE.sub("", m.group(2)).strip("\n")
        return f"<pre>{opening}{inner}</code></pre>"

    html = _ESCAPED_CODE_BLOCK_RE.sub(restore, html)

    def unwrap(m: re.Match) -> str:
        inner = _SPAN_RE.sub("", _INNER_PRE_RE.sub("", m.group(2)))
        return m.group(1) + inner.strip("\n") + m.group(3)

    return _CODE_BLOCK_RE.sub(unwrap, html)


def restore_encoded_code(html: str) -> str:
    """Restore encoded code delimiters while leaving their payload escaped.

    SSG 0.0.63 emits both inline and fenced code delimiters one entity level
    deeper than the surrounding Markdown.  Unescaping only the delimiters
    preserves examples such as ``<BIC>`` as text instead of creating unknown
    HTML elements.
    """
    def restore(m: re.Match) -> str:
        attrs = _html.unescape(m.group(1))
        return f"<code{attrs}>{m.group(2)}</code>"

    return _ESCAPED_CODE_RE.sub(restore, html)


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


# ---- Localization -------------------------------------------------------
# Locale landing pages (slug -> hreflang code). English is the x-default.
LOCALES = {
    "ar": "ar", "bn": "bn", "cs": "cs", "de": "de", "el": "el", "es": "es",
    "fa": "fa", "fil": "fil", "fr": "fr", "ha": "ha", "he": "he", "hi": "hi",
    "hu": "hu", "id": "id", "it": "it", "ja": "ja", "ko": "ko", "mr": "mr",
    "ms": "ms", "nl": "nl", "pl": "pl", "pt-br": "pt-BR", "ro": "ro",
    "ru": "ru", "sv": "sv", "ta": "ta", "te": "te", "th": "th", "tr": "tr",
    "uk": "uk", "vi": "vi", "yo": "yo", "zh-hans": "zh-Hans",
    "zh-hant": "zh-Hant",
}
RTL_LANGS = {"ar", "fa", "he"}

_HTML_TAG_RE = re.compile(r"<html\b([^>]*)>")


def add_rtl_dir(html: str, slug: str) -> str:
    """Right-to-left languages need dir=rtl on the root element."""
    if slug not in RTL_LANGS:
        return html
    return _HTML_TAG_RE.sub(
        lambda m: "<html" + m.group(1) + ' dir="rtl">'
        if "dir=" not in m.group(1) else m.group(0),
        html, count=1)


def hreflang_cluster(self_lang: str) -> str:
    """Reciprocal alternate links for the locale cluster + x-default.

    Google honours hreflang only when every page in the cluster links
    every other page; partial clusters are ignored."""
    links = ['<link rel="alternate" hreflang="en" href="%s/" />' % BASE_URL,
             '<link rel="alternate" hreflang="x-default" href="%s/" />' % BASE_URL]
    for slug, code in sorted(LOCALES.items()):
        links.append('<link rel="alternate" hreflang="%s" href="%s/%s/" />'
                     % (code, BASE_URL, slug))
    return "".join(l for l in links if 'hreflang="%s"' % self_lang not in l)


def translate_chrome(html: str, s: list) -> str:
    """Localise the layout chrome around a translated body: nav labels,
    controls, breadcrumb, article meta, footer. Replacements are anchored
    to exact chrome markup so translated body text is never touched."""
    (home, skip, minread, lastrev, contents, trydemo, why, see, docs,
     suite, research, tagline, fres, privacy, terms, contact, langline,
     tognav, swdark, swlight, srch, chlang) = s
    pairs = [
        ('>Skip to main content<', '>%s<' % skip),
        ('aria-label="Toggle navigation"', 'aria-label="%s"' % tognav),
        ('>Why Pain001</a>', '>%s</a>' % why),
        ('>See it live</a>', '>%s</a>' % see),
        ('>Docs</a>', '>%s</a>' % docs),
        ('>Suite</a>', '>%s</a>' % suite),
        ('>Research</a>', '>%s</a>' % research),
        ('aria-label="Switch to dark theme"',
         'aria-label="%s" data-label-dark="%s" data-label-light="%s"'
         % (swdark, swdark, swlight)),
        ('title="Switch theme"', 'title="%s"' % swdark),
        ('aria-label="Search (Cmd or Ctrl + K)"', 'aria-label="%s (Cmd/Ctrl + K)"' % srch),
        ('title="Search (⌘K)"', 'title="%s (⌘K)"' % srch),
        ('aria-label="Change language"', 'aria-label="%s"' % chlang),
        ('title="Change language"', 'title="%s"' % chlang),
        ('>Try the demo&nbsp;&rsaquo;<', '>%s&nbsp;&rsaquo;<' % trydemo),
        ('>Try the demo ›<', '>%s ›<' % trydemo),
        ('>Home</a>', '>%s</a>' % home),
        ('"name": "Home"', '"name": "%s"' % home),
        (' min read<', ' %s<' % minread),
        ('>Last reviewed <', '>%s <' % lastrev),
        ('>Contents</h2>', '>%s</h2>' % contents),
        ('>26 July 2026<', '>2026-07-26<'),
        ('Open-source ISO 20022 payment initiation. Validated files, local processing, no lock-in.', tagline),
        ('>Research &amp; trust</h2>', '>%s</h2>' % fres),
        ('>Privacy</a>', '>%s</a>' % privacy),
        ('>Terms</a>', '>%s</a>' % terms),
        ('>Contact</a>', '>%s</a>' % contact),
        ('>This overview in 34 languages<', '>%s<' % langline),
    ]
    for old, new in pairs:
        html = html.replace(old, new)
    return html


def status_strip_values(site: Path) -> dict | None:
    """Parse the homepage status strip so locale strips share its values
    and cannot drift when a release or review date changes."""
    home = site / "index.html"
    if not home.exists():
        return None
    html = home.read_text(encoding="utf-8")
    vals = {}
    for key, label in (("milestone", "Next CBPR+ milestone:"),
                       ("relay", "Relay version:"),
                       ("release", "Latest release:"),
                       ("msgdefs", "Message definitions:"),
                       ("reviewed", "Reviewed:")):
        m = re.search(re.escape(label) + r"</strong>\s*([^<]+?)</a>", html)
        if not m:
            return None
        vals[key] = m.group(1).strip()
    # Locale chrome uses ISO dates ("14 Nov 2026" -> "2026-11-14").
    months = {m: i for i, m in enumerate(
        "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
    m = re.fullmatch(r"(\d{1,2}) (\w{3}) (\d{4})", vals["milestone"])
    if m and m.group(2) in months:
        vals["milestone"] = "%s-%02d-%02d" % (
            m.group(3), months[m.group(2)], int(m.group(1)))
    return vals


def status_strip_html(s: list, vals: dict) -> str:
    aria, milestone, addr, addr_v, relay, release, msgdefs, reviewed = s
    row = '<a href="%s"%s><strong>%s</strong> %s</a>'
    items = [
        row % ("/iso20022-roadmap/", "", milestone, vals["milestone"]),
        row % ("/2026-iso20022-migration-trends/", "", addr, addr_v),
        row % ("/pain.001.001.09/", "", relay, vals["relay"]),
        row % ("https://pypi.org/project/pain001/", ' rel="external"',
               release, vals["release"]),
        row % ("/compatibility/", "", msgdefs, vals["msgdefs"]),
        row % ("/iso20022-roadmap/", "", reviewed, vals["reviewed"]),
    ]
    return ('<section class="status-strip" aria-label="%s">'
            '<div class="wrap status-strip-inner">%s</div></section>'
            % (aria, "".join(items)))


def fix_try_strip(site: Path) -> None:
    """Mirror the homepage status strip onto /try/, copying the section
    verbatim so a release bump can never drift between the two pages."""
    home, page = site / "index.html", site / "try" / "index.html"
    if not (home.exists() and page.exists()):
        return
    m = re.search(r"<section[^>]*\bstatus-strip\b[^>]*>.*?</section>",
                  home.read_text(encoding="utf-8"), re.S)
    if not m:
        return
    html = page.read_text(encoding="utf-8")
    if "status-strip" in html:
        return
    html = re.sub(r'<main id="?main-content"?>',
                  lambda mm: mm.group(0) + m.group(0), html, count=1)
    page.write_text(html, encoding="utf-8")
    print("[postbuild] status strip mirrored onto /try/")


def load_try_i18n(slug: str) -> dict | None:
    """Per-locale translation table (scripts/try_i18n/<slug>.json)."""
    return _load_i18n("try_i18n", slug)


def load_pages_i18n(slug: str) -> dict | None:
    """Per-locale journey-page table (scripts/pages_i18n/<slug>.json)."""
    return _load_i18n("pages_i18n", slug)


def _load_i18n(dirname: str, slug: str) -> dict | None:

    path = Path(__file__).parent / dirname / f"{slug}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        print(f"[postbuild] WARNING: invalid JSON in {path}", file=sys.stderr)
        return None


def apply_chrome_extra(html: str, d: dict) -> str:
    """Submenu, footer and toggle-aria labels from the i18n table."""
    for k in sorted(d.get("chrome", {}), key=len, reverse=True):
        html = html.replace(">%s<" % k, ">%s<" % d["chrome"][k])
    for k, v in d.get("chrome_aria", {}).items():
        html = html.replace('aria-label="%s"' % k, 'aria-label="%s"' % v)
    return html


def lang_badge(html: str, slug: str) -> str:
    """The globe button shows the current language code, not EN."""
    return html.replace('class="ap-lang-current">EN<',
                        'class="ap-lang-current">%s<'
                        % slug.split("-")[0].upper())


def retag_body_lang(html: str, code: str) -> str:
    """Point the body wrapper's lang at the locale it now contains.

    ssg wraps every page body in ``<div lang="…">`` taken from the
    source front matter, which is always ``en``. Locale pages are made
    by translating that English build in place, so the wrapper kept
    claiming English around Arabic or Japanese text — a WCAG 3.1.2
    (Language of Parts) failure, and one a screen reader makes audible:
    it reads the whole page in an English voice. ``<html lang>`` was
    already correct, so the inner wrapper was overriding it.

    Only ``<div lang="en">`` is touched. The language menu carries
    ``lang="en"`` on its English <a>, and that one is genuinely English.
    No ``dir`` is set here: ``<html dir="rtl">`` already covers the RTL
    locales and direction inherits.
    """
    return html.replace('<div lang="en">', '<div lang="%s">' % code)


def retag_html_lang(html: str, code: str, rtl: bool = False) -> str:
    """Set the document language without assuming `<html>` has no class.

    PRISM carries `class="no-js"` on the root element, so the former exact
    `<html lang="en-GB">` replacement no longer matched localized copies.
    """
    direction = ' dir="rtl"' if rtl else ""
    return re.sub(
        r'<html\b([^>]*?)\blang="en-GB"([^>]*)>',
        lambda m: '<html' + m.group(1) + 'lang="%s"' % code
        + m.group(2) + direction + '>',
        html, count=1)


def translate_status_strip(html: str, s: list) -> str:
    aria, milestone, addr, addr_v, relay, release, msgdefs, reviewed = s
    pairs = [
        ('aria-label="Current standards and project status"',
         'aria-label="%s"' % aria),
        (">Next CBPR+ milestone:<", ">%s<" % milestone),
        (">Address rule:<", ">%s<" % addr),
        ("</strong> structured or hybrid<", "</strong> %s<" % addr_v),
        (">Relay version:<", ">%s<" % relay),
        (">Latest release:<", ">%s<" % release),
        (">Message definitions:<", ">%s<" % msgdefs),
        (">Reviewed:<", ">%s<" % reviewed),
        ("</strong> 14 Nov 2026<", "</strong> 2026-11-14<"),
    ]
    for old, new in pairs:
        html = html.replace(old, new)
    return html


def path_hreflang_cluster(path: str, self_lang: str) -> str:
    """Reciprocal alternates for a localized page cluster at /<path>."""
    links = ['<link rel="alternate" hreflang="en" href="%s/%s" />'
             % (BASE_URL, path),
             '<link rel="alternate" hreflang="x-default" href="%s/%s" />'
             % (BASE_URL, path)]
    for slug, code in sorted(LOCALES.items()):
        links.append('<link rel="alternate" hreflang="%s" href="%s/%s/%s" />'
                     % (code, BASE_URL, slug, path))
    return "".join(l for l in links if 'hreflang="%s"' % self_lang not in l)


def try_hreflang_cluster(self_lang: str) -> str:
    return path_hreflang_cluster("try/", self_lang)


def retarget_lang_menu(html: str, path: str) -> str:
    """On localized pages the language menu switches between the
    same page's locale variants (path e.g. "try/" or "why/")."""
    html = html.replace('class="ap-lang-item" href="/" hreflang="en"',
                        'class="ap-lang-item" href="/%s" hreflang="en"' % path)
    for slug in LOCALES:
        html = html.replace(
            'class="ap-lang-item" href="/%s/" hreflang=' % slug,
            'class="ap-lang-item" href="/%s/%s" hreflang=' % (slug, path))
    return html


def retarget_lang_menu_to_try(html: str) -> str:
    return retarget_lang_menu(html, "try/")


JOURNEY_PAGES = ("why", "solutions", "executive-brief")
DOCS_PAGES = ("documentation", "faqs", "installation", "glossary")

# Submenu targets that exist only in English get a visible cue on
# localized pages, so the language jump is expected instead of surprising.
EN_ONLY_SUB = (
    "/competitors-comparison/", "/message-specs/", "/example-corpus/",
    "/pain002-reason-codes/", "/pain001-mcp/", "/pain001-lsp/",
    "/pain001-loader-mt101/", "/pain001-loader-xlsx/",
    "/architecture-and-patents/", "/2026-iso20022-migration-trends/",
    "/iso20022-roadmap/",
    "/iso-20022-payment-initiation-for-cross-border-payments/", "/languages/",
)


def retarget_journey_nav(html: str, slug: str) -> str:
    """Nav/footer/body links to localized pages stay in-locale.

    The language menu's English entry is the one link that must leave the
    locale: rewriting it too sent "English" on /fr/documentation/ back to
    /fr/documentation/ (and gave WAVE two adjacent links to one URL)."""
    for p in JOURNEY_PAGES + DOCS_PAGES:
        html = re.sub(r'href="/%s/"(?! hreflang="en")' % re.escape(p),
                      'href="/%s/%s/"' % (slug, p), html)
    return html


def mark_english_submenu(html: str) -> str:
    """Tag English-only submenu items with hreflang and an (EN) suffix."""
    def tag_region(m):
        region = m.group(0)
        for t in EN_ONLY_SUB:
            region = re.sub(
                r'(<a href="%s")(>)([^<]*?)(</a>)' % re.escape(t),
                lambda mm: mm.group(0) if mm.group(3).endswith("(EN)")
                else mm.group(1) + ' hreflang="en"' + mm.group(2)
                + mm.group(3) + " (EN)" + mm.group(4),
                region)
        return region
    return re.sub(r'<ul id="sub-[a-z]+" class="ap-sub">.*?</ul>',
                  tag_region, html, flags=re.S)


def gen_try_locales(site: Path) -> None:
    """Generate /<slug>/try/ for every locale with a translation table:
    translated chrome + demo copy, correct lang/dir, self-canonical URLs
    and a reciprocal hreflang cluster across all try variants."""
    try:
        from locale_strings import STRINGS, STATUS_STRIP
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from locale_strings import STRINGS, STATUS_STRIP
    src = site / "try" / "index.html"
    if not src.exists():
        return
    base = src.read_text(encoding="utf-8")

    # The English page joins the cluster and its language menu switches
    # between try variants.
    en = base
    if 'hreflang="x-default" href="%s/try/"' % BASE_URL not in en:
        en = en.replace("</head>", try_hreflang_cluster("en") + "</head>", 1)
    en = retarget_lang_menu_to_try(en)
    src.write_text(en, encoding="utf-8")

    en_meta = (load_try_i18n("en") or {}).get("meta", {})
    n = 0
    for slug, code in LOCALES.items():
        d = load_try_i18n(slug)
        if not d or slug not in STRINGS:
            continue
        html = base
        # lang + direction
        html = retag_html_lang(html, code, slug in RTL_LANGS)
        html = html.replace('"inLanguage": "en-GB"',
                            '"inLanguage": "%s"' % code)
        # metadata: title/description everywhere they appear, then URLs
        meta = d.get("meta", {})
        for key in ("title", "description"):
            if en_meta.get(key) and meta.get(key):
                html = html.replace(en_meta[key], meta[key])
        html = html.replace("https://pain001.com/try/",
                            "https://pain001.com/%s/try/" % slug)
        html = html.replace("</head>",
                            try_hreflang_cluster(code) + "</head>", 1)
        # demo copy, longest fragment first so substrings cannot clash;
        # fragments padded by whitespace inside their tag miss the >k<
        # anchor, so long keys fall back to raw substring replacement
        for k in sorted(d.get("text", {}), key=len, reverse=True):
            v = d["text"][k]
            apostrophe_k = k.replace("&#x27;", "'").replace("&#39;", "'")
            apostrophe_v = v.replace("&#x27;", "'").replace("&#39;", "'")
            if ">%s<" % k in html:
                html = html.replace(">%s<" % k, ">%s<" % v)
            elif apostrophe_k in html:
                html = html.replace(apostrophe_k, apostrophe_v)
            elif _html.unescape(k) in html:
                html = html.replace(_html.unescape(k), _html.unescape(v))
            elif len(k) >= 30:
                html = html.replace(k, v)
        for k, v in d.get("aria", {}).items():
            html = html.replace('aria-label="%s"' % k, 'aria-label="%s"' % v)
        html = apply_chrome_extra(html, d)
        html = translate_chrome(html, STRINGS[slug])
        html = translate_status_strip(html, STATUS_STRIP[slug])
        html = retarget_lang_menu_to_try(html)
        # nav/CTA/footer demo links stay in this locale; the language
        # menu's English entry (href="/try/" hreflang="en") is untouched
        # because its href is not followed directly by ">".
        html = html.replace('href="/try/">', 'href="/%s/try/">' % slug)
        html = retarget_journey_nav(html, slug)
        html = mark_english_submenu(html)
        html = lang_badge(html, slug)
        html = retag_body_lang(html, code)
        rd = _load_i18n("runtime_i18n", slug)
        if rd:
            import json as _json

            # non-executable JSON table read by try-page.js; <
            # escaping keeps "</script>" impossible inside the payload
            payload = _json.dumps(rd, ensure_ascii=False).replace("<", "\\u003c")
            html = html.replace(
                "</body>",
                '<script id="try-i18n" type="application/json">%s</script>'
                "</body>" % payload, 1)
        dest = site / slug / "try"
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.html").write_text(html, encoding="utf-8")
        n += 1
    print(f"[postbuild] generated {n} locale /try/ page(s)")


def gen_journey_locales(site: Path) -> None:
    _gen_localized_pages(site, JOURNEY_PAGES, "pages_i18n")
    _gen_localized_pages(site, DOCS_PAGES, "docs_i18n")


def _gen_localized_pages(site: Path, pages: tuple, table_dir: str) -> None:
    """Generate /<slug>/<page>/ for every locale with a translation
    table — same mechanics as the /try/ variants."""
    try:
        from locale_strings import STRINGS
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from locale_strings import STRINGS
    en_all = _load_i18n(table_dir, "en") or {}
    for page_name in pages:
        src = site / page_name / "index.html"
        if not src.exists():
            continue
        base = src.read_text(encoding="utf-8")
        en = base
        if ('hreflang="x-default" href="%s/%s/"' % (BASE_URL, page_name)
                not in en):
            en = en.replace("</head>",
                            path_hreflang_cluster(page_name + "/", "en")
                            + "</head>", 1)
        en = retarget_lang_menu(en, page_name + "/")
        src.write_text(en, encoding="utf-8")

        en_meta = en_all.get(page_name, {}).get("meta", {})
        n = 0
        for slug, code in LOCALES.items():
            d = _load_i18n(table_dir, slug)
            if not d or page_name not in d or slug not in STRINGS:
                continue
            pd = d[page_name]
            html = base
            html = retag_html_lang(html, code, slug in RTL_LANGS)
            html = html.replace('"inLanguage": "en-GB"',
                                '"inLanguage": "%s"' % code)
            # anchored meta swaps only — a raw global replace of the
            # short eyebrow once corrupted og:image:alt mid-string
            meta = pd.get("meta", {})
            for key in sorted(en_meta, key=lambda k: -len(en_meta[k] or "")):
                ev, tv = en_meta.get(key), meta.get(key)
                if not (ev and tv):
                    continue
                for pat in ("<title>%s</title>", 'content="%s"',
                            ">%s<", '": "%s"'):
                    html = html.replace(pat % ev, pat % tv)
            html = html.replace("https://pain001.com/%s/" % page_name,
                                "https://pain001.com/%s/%s/" % (slug, page_name))
            html = html.replace("</head>",
                                path_hreflang_cluster(page_name + "/", code)
                                + "</head>", 1)
            for k in sorted(pd.get("text", {}), key=len, reverse=True):
                v = pd["text"][k]
                apostrophe_k = k.replace("&#x27;", "'").replace("&#39;", "'")
                apostrophe_v = v.replace("&#x27;", "'").replace("&#39;", "'")
                if ">%s<" % k in html:
                    html = html.replace(">%s<" % k, ">%s<" % v)
                elif apostrophe_k in html:
                    html = html.replace(apostrophe_k, apostrophe_v)
                elif _html.unescape(k) in html:
                    html = html.replace(_html.unescape(k), _html.unescape(v))
                elif len(k) >= 30:
                    html = html.replace(k, v)
            for k, v in pd.get("aria", {}).items():
                html = html.replace('aria-label="%s"' % k,
                                    'aria-label="%s"' % v)
            td = load_try_i18n(slug)
            if td:
                html = apply_chrome_extra(html, td)
            html = translate_chrome(html, STRINGS[slug])
            html = retarget_lang_menu(html, page_name + "/")
            html = retarget_journey_nav(html, slug)
            html = html.replace('href="/try/">', 'href="/%s/try/">' % slug)
            html = mark_english_submenu(html)
            html = lang_badge(html, slug)
            html = retag_body_lang(html, code)
            # legacy localized-brief URLs map onto the new scheme
            for old in ("fr", "de", "es"):
                html = html.replace("/executive-brief-%s/" % old,
                                    "/%s/executive-brief/" % old)
            dest = site / slug / page_name
            dest.mkdir(parents=True, exist_ok=True)
            (dest / "index.html").write_text(html, encoding="utf-8")
            n += 1
        print(f"[postbuild] generated {n} locale /{page_name}/ page(s)")


def localise_pages(site: Path) -> None:
    try:
        from locale_strings import STRINGS, STATUS_STRIP
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from locale_strings import STRINGS, STATUS_STRIP
    strip_vals = status_strip_values(site)
    n = 0
    for slug in LOCALES:
        page = site / slug / "index.html"
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        if "x-default" not in html:
            html = html.replace("</head>",
                                hreflang_cluster(LOCALES[slug]) + "</head>", 1)
        html = add_rtl_dir(html, slug)
        if slug in STRINGS:
            html = translate_chrome(html, STRINGS[slug])
        if (strip_vals and slug in STATUS_STRIP
                and "status-strip" not in html):
            strip = status_strip_html(STATUS_STRIP[slug], strip_vals)
            html = re.sub(r'<main id="?main-content"?>',
                          lambda m: m.group(0) + strip, html, count=1)
        d = load_try_i18n(slug)
        if d:
            html = apply_chrome_extra(html, d)
            html = lang_badge(html, slug)
            html = retag_body_lang(html, LOCALES[slug])
            html = html.replace('href="/try/"', 'href="/%s/try/"' % slug)
        if load_pages_i18n(slug):
            html = retarget_journey_nav(html, slug)
            html = mark_english_submenu(html)
        page.write_text(html, encoding="utf-8")
        n += 1
    home = site / "index.html"
    if home.exists():
        html = home.read_text(encoding="utf-8")
        if "x-default" not in html:
            html = html.replace("</head>", hreflang_cluster("en") + "</head>", 1)
            home.write_text(html, encoding="utf-8")
    print(f"[postbuild] hreflang cluster on {n} locale page(s) + home; "
          f"RTL dir on {len(RTL_LANGS & set(LOCALES))}")


_DESC_RE = re.compile(
    r'<meta\b(?=[^>]*\bname=["\']?description["\']?[\s>])[^>]*\bcontent="([^"]*)"[^>]*>')


def fix_social_descriptions(site: Path) -> None:
    """Point og:description and twitter:description at the authored
    description.

    ssg synthesises the social descriptions from visible page text, which
    on the homepage means the status strip — shared links read "Next
    CBPR+ milestone: ... Reviewed:" and truncate mid-label. The authored
    <meta name=description> is the human-written one, so mirror it."""
    fixed = 0
    for page in site.rglob("index.html"):
        html = page.read_text(encoding="utf-8")
        m = _DESC_RE.search(html[:html.find("</head>")])
        if not m:
            continue
        desc = m.group(1).strip()
        if not desc:
            continue
        out = html
        for prop, attr in (("og:description", "property"),
                           ("twitter:description", "name")):
            pat = re.compile(
                r'(<meta\b(?=[^>]*\b%s=["\']?%s["\']?[\s>])[^>]*\bcontent=")'
                r'([^"]*)(")' % (attr, re.escape(prop)))
            def repl(mm, d=desc):
                return mm.group(1) + d + mm.group(3)
            out = pat.sub(repl, out)
        if out != html:
            page.write_text(out, encoding="utf-8")
            fixed += 1
    print(f"[postbuild] social descriptions aligned on {fixed} page(s)")


def stamp_sw_cache_version(site: Path) -> str | None:
    """Derive the service worker's cache name from what it caches.

    sw.js is cache-first for /try/ and every /<locale>/try/, so a
    returning visitor keeps the old page until the CACHE constant
    changes. Bumping it by hand has been forgotten three times — most
    recently the layer-summary translations, which shipped to all 34
    locales while returning visitors kept the English original. CI was
    green every time, because nothing was wrong with the build.

    Hashing the cached content removes the human step: the constant
    changes exactly when the cached bytes change, and never otherwise
    (so a no-op rebuild does not evict everyone's Pyodide download).
    Large binaries contribute name+size rather than content — they are
    versioned wheels, and rewriting one without changing its size is
    not a case worth paying 30 MB per build to catch.
    """
    sw = site / "sw.js"
    if not sw.exists():
        return None
    h = hashlib.sha256()
    for page in sorted(site.glob("*/try/index.html")) + [
            site / "try" / "index.html"]:
        if page.exists():
            h.update(page.read_bytes())
    for js in sorted((site / "js").glob("try-*.js")):
        h.update(js.read_bytes())
    for sample in sorted((site / "samples").glob("*")):
        h.update(sample.read_bytes())
    for asset in sorted((site / "pyodide").glob("*")):
        h.update(asset.name.encode())
        h.update(str(asset.stat().st_size).encode())
    digest = h.hexdigest()[:12]
    text = sw.read_text(encoding="utf-8")
    new, n = re.subn(r'const CACHE = "pain001-try-[^"]+";',
                     'const CACHE = "pain001-try-%s";' % digest, text, count=1)
    if not n:
        print("[postbuild] WARNING: sw.js CACHE constant not found")
        return None
    if new != text:
        sw.write_text(new, encoding="utf-8")
    print(f"[postbuild] sw.js cache version pain001-try-{digest}")
    return digest


def add_version_requirements(site: Path) -> None:
    """Render a visible "needs version X" note on pages that document an
    API newer than the current PyPI release.

    Documentation that describes an unreleased API is a claim that is not
    yet true: a reader who runs ``pip install pain001`` and follows the
    page gets an ImportError with nothing to explain it. The front-matter
    ``min_pain001`` that scripts/validate_snippets.py reads to defer its
    failures has to be visible to readers too, or the site is keeping the
    caveat to itself.

    The note is emitted from the same field the validator reads, so the
    two cannot disagree.
    """
    posts = Path("_posts")
    if not posts.is_dir():
        return
    pat = re.compile(r'^min_pain001:\s*"?([\d.]+)"?\s*$', re.M)
    url_pat = re.compile(r'^id:\s*"([^"]+)"\s*$', re.M)
    n = 0
    for md in sorted(posts.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        m, u = pat.search(text), url_pat.search(text)
        if not (m and u):
            continue
        version = m.group(1)
        path = u.group(1).replace(BASE_URL, "").strip("/")
        page = site / path / "index.html" if path else site / "index.html"
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        if "version-requirement" in html:
            continue
        # Worded to stay true before and after v%s reaches PyPI. Saying
        # "upgrade with pip" would be its own false claim while the
        # version is still unreleased, which is the problem this note
        # exists to solve.
        note = (
            '<p class="version-requirement"><strong>Requires Pain001 '
            "v%s or later.</strong> Earlier versions do not carry the API "
            "shown on this page. Check what you have with "
            '<code class="tt-mono">pain001 --version</code>, and see '
            '<a href="https://github.com/sebastienrousseau/pain001/releases">'
            "the releases page</a> for what is published.</p>" % version
        )
        for anchor in ('<article class="content-body">',
                       "<article class=content-body>"):
            if anchor in html:
                html = html.replace(anchor, anchor + note, 1)
                page.write_text(html, encoding="utf-8")
                n += 1
                break
    print(f"[postbuild] version-requirement note on {n} page(s)")


TAXONOMY_CSS = '<link rel="stylesheet" href="/css/taxonomy.css" />'
# The layouts carry these; the taxonomy pages did not, so every visit
# to a tag page requested /favicon.ico and got a 404.
TAXONOMY_ICONS = ('<link rel="icon" type="image/svg+xml" href="/img/pain001.svg" sizes="any" />'
                  '<link rel="apple-touch-icon" href="/img/pain001.svg" />')
BEACON_TAG = '<script defer src="/js/pain001-analytics.js" data-cf-token="7e7c74d9aa9046ff8d3bf7c56e5a510d"></script>'
TAXONOMY_VIEWPORT = (
    '<meta name="viewport" content="width=device-width, initial-scale=1" />'
)


_DOUBLE_ENC_RE = re.compile(r"&amp;(amp|lt|gt|quot|#\d+|#x[0-9a-fA-F]+);")


def fix_double_encoded_meta(site: Path) -> None:
    """Undo ssg's second escaping pass on social metadata.

    A title containing a plain ``&`` in the front matter is escaped once
    for ``<title>`` (correct) and twice for og:title/twitter:title, so
    "Release & Support Policy" reached Twitter and LinkedIn as
    "Release &amp; Support Policy" — visible mojibake in every share
    card. Only the head is touched, and only the doubled form, so a
    correctly escaped entity is left alone.
    """
    n = 0
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        end = html.find("</head>")
        if end == -1:
            continue
        head = html[:end]
        fixed = _DOUBLE_ENC_RE.sub(lambda m: "&" + m.group(1) + ";", head)
        if fixed != head:
            page.write_text(fixed + html[end:], encoding="utf-8")
            n += 1
    print(f"[postbuild] un-double-encoded head metadata on {n} page(s)")


def fix_tag_pages(site: Path) -> None:
    """The taxonomy plugin emits pages outside _layouts/, so they arrive
    with no stylesheet and no viewport meta: an 8px browser-default
    gutter, a link list running the full 1424px of a 1440px screen, and
    no mobile scaling at all. Link the shell stylesheet and give them a
    viewport, alongside the CSP and og:image the audit gates want.

    Linked rather than inlined because the CSP allows style-src 'self',
    so a same-origin file needs no hash bookkeeping."""
    for page in site.glob("tags/*/index.html"):
        html = page.read_text(encoding="utf-8")
        inject = ""
        if "Content-Security-Policy" not in html:
            inject += CSP_META
        if 'property="og:image"' not in html:
            inject += OG_IMAGE_META
        if "css/taxonomy.css" not in html:
            inject += TAXONOMY_CSS
        if 'name="viewport"' not in html:
            inject += TAXONOMY_VIEWPORT
        if 'rel="icon"' not in html:
            inject += TAXONOMY_ICONS
        if inject:
            page.write_text(html.replace("</head>", inject + "</head>", 1), encoding="utf-8")
            print(f"[postbuild] patched tag page: {page}")
        html = page.read_text(encoding="utf-8")
        if "pain001-analytics.js" not in html and "</body>" in html:
            # the same page-view beacon the layouts carry (see METRICS.md)
            page.write_text(html.replace("</body>", BEACON_TAG + "</body>", 1), encoding="utf-8")


def fix_manifest(site: Path) -> None:
    """ssg emits "theme_color": null (it only understands the legacy RGB
    triple), which Chrome logs as an invalid-type warning. Pin valid hexes."""

    path = site / "manifest.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("theme_color"), str) or not data["theme_color"].startswith("#"):
        data["theme_color"] = "#0b0e14"
    if not isinstance(data.get("background_color"), str):
        data["background_color"] = "#ffffff"
    for icon in data.get("icons", []):
        if isinstance(icon, dict) and str(icon.get("src", "")).startswith(BASE_URL + "/"):
            icon["src"] = icon["src"][len(BASE_URL):]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("[postbuild] manifest.json theme_color fixed")


_STYLESHEET_RE = re.compile(
    r'<link\b(?=[^>]*\brel="stylesheet")(?=[^>]*\bhref="([^"]+)")[^>]*>'
)


def bundle_stylesheets(site: Path) -> None:
    """Collapse each page's local CSS chain into one immutable SRI asset.

    The authored PRISM, adapter, and layout styles remain separate
    in the repository.  The published bundle removes four render-blocking
    round trips on mobile without weakening the CSP or changing the cascade.
    """
    output = site / "css"
    output.mkdir(exist_ok=True)
    bundles: dict[tuple[str, ...], tuple[str, str]] = {}
    pages = 0
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        matches = list(_STYLESHEET_RE.finditer(html))
        hrefs = tuple(m.group(1) for m in matches)
        if not hrefs or any(h.startswith(("http:", "https:", "//")) for h in hrefs):
            continue
        paths = [site / h.lstrip("/") for h in hrefs]
        # SSG 0.0.63 fingerprints its generated syntax-highlighter asset but
        # leaves the authored ``/highlight.css`` URL in HTML. Resolve that
        # single generated file while assembling the final page bundle; the
        # stale URL is then removed with the other individual stylesheet
        # links instead of becoming a site-wide 404.
        for index, (href, path) in enumerate(zip(hrefs, paths)):
            if path.is_file() or href != "/highlight.css":
                continue
            candidates = sorted(site.glob("highlight.*.css"))
            if len(candidates) == 1:
                paths[index] = candidates[0]
        if not all(path.is_file() for path in paths):
            continue
        if hrefs not in bundles:
            payload = (minify_css("\n".join(path.read_text(encoding="utf-8") for path in paths)) + "\n").encode()
            digest = hashlib.sha256(payload).hexdigest()[:16]
            sri = base64.b64encode(hashlib.sha384(payload).digest()).decode()
            name = f"site-{digest}.css"
            (output / name).write_bytes(payload)
            bundles[hrefs] = (f"/css/{name}", sri)
        href, sri = bundles[hrefs]
        replacement = (
            f'<link rel="stylesheet" href="{href}" integrity="sha384-{sri}" '
            'crossorigin="anonymous" />'
        )
        # Stylesheet links are interleaved with metadata in SSG's generated
        # head. Replace links individually; replacing the whole first-to-last
        # span would silently delete canonical, Open Graph, and feed tags.
        parts: list[str] = []
        cursor = 0
        for index, match in enumerate(matches):
            parts.append(html[cursor : match.start()])
            if index == 0:
                parts.append(replacement)
            cursor = match.end()
        parts.append(html[cursor:])
        html = "".join(parts)
        page.write_text(html, encoding="utf-8")
        pages += 1
    print(f"[postbuild] {len(bundles)} CSS bundle(s) linked from {pages} page(s)")


def ensure_social_metadata(site: Path) -> None:
    """Give every authored and generated page the minimum social card set."""
    changed = 0
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        title_match = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
        if not title_match or "</head>" not in html:
            continue
        title = _html.escape(_html.unescape(_TAG_RE.sub("", title_match.group(1))).strip(), quote=True)
        tags = []
        if not re.search(r'<meta\s+property=["\']og:title["\']', html, re.IGNORECASE):
            tags.append(f'<meta property="og:title" content="{title}" />')
        if not re.search(r'<meta\s+property=["\']og:type["\']', html, re.IGNORECASE):
            tags.append('<meta property="og:type" content="website" />')
        if not re.search(r'<meta\s+name=["\']twitter:card["\']', html, re.IGNORECASE):
            tags.append('<meta name="twitter:card" content="summary_large_image" />')
        if not tags:
            continue
        html = html.replace("</head>", "".join(tags) + "</head>", 1)
        page.write_text(html, encoding="utf-8")
        changed += 1
    print(f"[postbuild] social card metadata on {changed} page(s)")


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


# Corpus scenario pages exist in English and in the five locales whose
# market packs the corpus covers (scripts/corpus_l10n.py). The generator
# writes them as /<loc>-corpus-<id>/ posts (ssg names output after the
# post file); this pass moves them under /<loc>/ and localises the chrome
# the same way the /try/ and journey pages are. The hreflang cluster is
# the six-language one, never the 35-locale site cluster: Google ignores
# a cluster whose members do not all exist.
CORPUS_LOCALES = ("de", "fr", "es", "it", "nl")
_EN_DATE_RE = re.compile(
    r">(\d{1,2}) (January|February|March|April|May|June|July|August|"
    r"September|October|November|December) (\d{4})<")
_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December")


def corpus_hreflang_cluster(slug: str, self_lang: str) -> str:
    links = ['<link rel="alternate" hreflang="en" href="%s/%s/" />' % (BASE_URL, slug),
             '<link rel="alternate" hreflang="x-default" href="%s/%s/" />' % (BASE_URL, slug)]
    for loc in CORPUS_LOCALES:
        links.append('<link rel="alternate" hreflang="%s" href="%s/%s/%s/" />'
                     % (LOCALES[loc], BASE_URL, loc, slug))
    return "".join(l for l in links if 'hreflang="%s"' % self_lang not in l)


def retarget_lang_menu_corpus(html: str, slug: str) -> str:
    """The globe menu switches between this scenario's six variants; the
    other locales keep pointing at their home page, which is what exists."""
    html = html.replace('class="ap-lang-item" href="/" hreflang="en"',
                        'class="ap-lang-item" href="/%s/" hreflang="en"' % slug)
    for loc in CORPUS_LOCALES:
        html = html.replace('class="ap-lang-item" href="/%s/" hreflang=' % loc,
                            'class="ap-lang-item" href="/%s/%s/" hreflang=' % (loc, slug))
    return html


def iso_english_dates(html: str) -> str:
    """A locale page must not carry an English month name in its chrome."""
    return _EN_DATE_RE.sub(
        lambda m: ">%s-%02d-%02d<" % (m.group(3), _MONTHS.index(m.group(2)) + 1, int(m.group(1))), html)


def relocate_corpus_locales(site: Path) -> None:
    try:
        from locale_strings import STRINGS
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from locale_strings import STRINGS
    import shutil
    moved = 0
    slugs = sorted(d.name for d in site.iterdir()
                   if d.is_dir() and d.name.startswith("corpus-") and (d / "index.html").exists())
    for slug in slugs:
        page = site / slug / "index.html"
        html = page.read_text(encoding="utf-8")
        if "x-default" not in html:
            html = html.replace("</head>", corpus_hreflang_cluster(slug, "en") + "</head>", 1)
        html = retarget_lang_menu_corpus(html, slug)
        page.write_text(html, encoding="utf-8")
        for loc in CORPUS_LOCALES:
            src = site / f"{loc}-{slug}"
            if not (src / "index.html").exists():
                continue
            dest = site / loc / slug
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(src), str(dest))
            html = (dest / "index.html").read_text(encoding="utf-8")
            code = LOCALES[loc]
            html = html.replace("/%s-%s/" % (loc, slug), "/%s/%s/" % (loc, slug))
            html = html.replace("</head>", corpus_hreflang_cluster(slug, code) + "</head>", 1)
            td = load_try_i18n(loc)
            if td:
                html = apply_chrome_extra(html, td)
            html = translate_chrome(html, STRINGS[loc])
            html = iso_english_dates(html)
            html = retarget_lang_menu_corpus(html, slug)
            html = retarget_journey_nav(html, loc)
            html = html.replace('href="/try/">', 'href="/%s/try/">' % loc)
            html = mark_english_submenu(html)
            html = lang_badge(html, loc)
            html = retag_body_lang(html, code)
            (dest / "index.html").write_text(html, encoding="utf-8")
            moved += 1
    # ssg derives every URL from the post's file name, so the tag pages,
    # feeds and search index still cite /<loc>-corpus-<id>/; rewrite them.
    stale = re.compile(r"/(%s)-corpus-" % "|".join(CORPUS_LOCALES))
    rewritten = 0
    for path in site.rglob("*"):
        if path.suffix not in (".html", ".xml", ".json", ".txt") or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        fixed = stale.sub(r"/\1/corpus-", text)
        if fixed != text:
            path.write_text(fixed, encoding="utf-8")
            rewritten += 1
    print(f"[postbuild] {len(slugs)} corpus page(s) clustered; {moved} locale variant(s) moved under "
          f"/<locale>/; stale paths rewritten in {rewritten} file(s)")


def inject_dataset_ld(site: Path) -> None:
    """Add schema.org Dataset markup to the corpus scenario pages.

    The generator records one JSON-LD object per page slug in
    scripts/corpus_pages.json; the block is a data script (not executed,
    so the CSP does not apply) placed before </head>.
    """
    table = Path(__file__).resolve().parent / "corpus_pages.json"
    if not table.exists():
        return
    import json as _json
    pages = _json.loads(table.read_text(encoding="utf-8"))
    for slug, ld in pages.items():
        page = site / slug / "index.html"
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        if '"@type": "Dataset"' in html:
            continue
        block = '<script type="application/ld+json">' + _json.dumps(ld, ensure_ascii=False) + "</script>\n"
        page.write_text(html.replace("</head>", block + "</head>", 1), encoding="utf-8")


def write_llms(site: Path) -> None:
    """Write llms.txt and llms-full.txt for agents that read the site.

    Both point at things an agent can fetch and use in one step: the
    corpus index, the per-edition JSON Schemas, the scenario pages, the
    MCP and LSP setup blocks, and the reference pages. The full file adds
    one line per scenario.
    """
    import json as _json
    root = Path(__file__).resolve().parent.parent
    index_path = root / "static" / "corpus" / "index.json"
    index = _json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else {"scenarios": []}
    version = index.get("pain001", "")
    head = [
        "# Pain001",
        "",
        "> Open-source ISO 20022 payment initiation suite: a Python library and CLI that turn CSV, Excel, "
        "SQLite, JSON, Parquet or SWIFT MT101 into schema-validated pain.001 (and pain.008) XML, a REST API, "
        "an MCP server for agents, an LSP server for editors, and a validated example corpus with provenance. "
        f"Suite version {version}. Dual-licensed Apache-2.0 OR MIT.",
        "",
        "## Install",
        "",
        "- `pip install pain001` (library and CLI); `pip install pain001-mcp` (MCP server, 21 tools); "
        + "`pip install pain001-lsp` (language server)",
        "- MCP, Claude Code: `claude mcp add pain001 -- pain001-mcp`; other clients: command `pain001-mcp` over stdio "
        + "(configuration blocks at https://pain001.com/pain001-mcp/)",
        "",
        "## Machine-readable data",
        "",
        "- Corpus index (every scenario, absolute URLs for XML, JSON twin, provenance, schema, demo): "
        + "https://pain001.com/corpus/index.json",
        "- JSON Schema 2020-12 per pain.001 edition, for the ISO 20022 JSON twin convention: "
        + "https://pain001.com/corpus/schemas/pain.001.001.09.schema.json (and .03 to .13)",
        "- Input column vocabulary (the flat rows the library reads): https://pain001.com/documentation/",
        "",
        "## Pages",
        "",
        "- Example corpus, downloads and method: https://pain001.com/example-corpus/",
        "- Schema coverage files per edition: https://pain001.com/example-corpus-coverage/",
        "- Browser demo running the library itself: https://pain001.com/try/",
        "- Technical reference (CLI, Python API, REST): https://pain001.com/documentation/",
        "- Message element references: https://pain001.com/message-specs/",
        "- MCP server: https://pain001.com/pain001-mcp/ ; LSP server: https://pain001.com/pain001-lsp/",
        "- MCP registry entry: io.github.sebastienrousseau/pain001-mcp ; Glama listing: https://glama.ai/mcp/servers/sebastienrousseau/pain001-mcp ; image: ghcr.io/sebastienrousseau/pain001-mcp",
        "- MT101 to pain.001 migration path: https://pain001.com/mt101-migration/ ; Excel workbooks as input: https://pain001.com/excel-to-pain001/",
        "- Trust centre, privacy, governance: https://pain001.com/trust/ https://pain001.com/privacy/ https://pain001.com/governance/",
        "- Supported channel, private profile derivation, integration help (the software stays free): https://pain001.com/enterprise/",
        "",
        "## Rules of use",
        "",
        "- Files are synthetic and built from public scheme rulebooks; no bank usage guideline is represented. "
        + "Apply your bank's own guideline privately with the library's overlay tooling.",
        "",
    ]
    lines = [f"- {s['id']} ({(s.get('country') or '').upper()}, {s.get('family')}): {s.get('description')} "
             f"{s['page']}" for s in index.get("scenarios", [])]
    (site / "llms.txt").write_text("\n".join(head + ["## Scenarios", "", f"{len(lines)} validated payment scenarios; "
                                                          "one line each in https://pain001.com/llms-full.txt", ""]),
                                   encoding="utf-8")
    (site / "llms-full.txt").write_text("\n".join(head + ["## Scenarios", ""] + lines + [""]), encoding="utf-8")


def stamp_suite_version(site: Path) -> int:
    """Say in every footer which suite version the site was generated against.

    The version comes from the corpus index the generator wrote, so the
    footer can never claim a version the corpus pages do not carry. Keep the
    stamp inside PRISM's ``footer-bottom`` container so it shares the footer's
    width, spacing, and responsive alignment on every generated page.
    """
    import json as _json
    index = Path(__file__).resolve().parent.parent / "static" / "corpus" / "index.json"
    if not index.exists():
        return 0
    version = _json.loads(index.read_text(encoding="utf-8")).get("pain001", "")
    if not version:
        return 0
    stamp = f'<p class="suite-version">Generated against pain001 {version}</p>'
    credit_re = re.compile(
        r'(<p class="footer-credit">.*?</p>)', re.DOTALL)
    existing_re = re.compile(
        r'<p class="suite-version">.*?</p>', re.DOTALL)
    count = 0
    for page in site.rglob("index.html"):
        html = page.read_text(encoding="utf-8")
        start = html.find("<footer")
        close = html.find("</footer>", start) if start >= 0 else -1
        if close < 0:
            continue
        footer = html[start:close]
        if 'class="suite-version"' in footer:
            fixed_footer = existing_re.sub(stamp, footer, count=1)
        else:
            fixed_footer, replacements = credit_re.subn(
                rf'\1\n      {stamp}', footer, count=1)
            if replacements == 0:
                continue
        page.write_text(
            html[:start] + fixed_footer + html[close:], encoding="utf-8")
        count += 1
    return count


_HTML_LANG_RE = re.compile(r'<html\b[^>]*\blang="([^"]+)"([^>]*)>')
_TAXO_LINK_RE = re.compile(r'<a href="(/[^"#?]*)">')


def taxonomy_language_and_index(site: Path) -> None:
    """Two gaps on the generated taxonomy pages.

    1. A tag page lists every page by its own title, so one English page
       carries titles in Arabic, Hindi, Hausa, Italian and 30 other
       languages with no ``lang`` on them: WCAG 3.1.2 (Language of Parts)
       fails and a screen reader reads Arabic with English phonetics.
       Each link takes the ``lang`` (and ``dir``) its target page declares.
    2. /tags/ said "pick a topic" and listed none. The list is built here
       from the generated tag pages, so it cannot drift from them.
    """
    langs: dict[str, tuple[str, str]] = {}

    def target_lang(href: str) -> tuple[str, str] | None:
        if href not in langs:
            page = site / href.strip("/") / "index.html"
            found = ("", "")
            if page.is_file():
                m = _HTML_LANG_RE.search(page.read_text(encoding="utf-8", errors="ignore")[:600])
                if m:
                    d = re.search(r'\bdir="(rtl|ltr)"', m.group(2))
                    found = (m.group(1), d.group(1) if d else "")
            langs[href] = found
        return langs[href] if langs[href][0] else None

    tagged = 0
    topics = []
    for page in sorted(site.glob("tags/*/index.html")):
        html = page.read_text(encoding="utf-8")
        own = _HTML_LANG_RE.search(html)
        own_lang = own.group(1).lower() if own else "en"
        start = html.find('class="taxonomy-page-list"')
        end = html.find("</ul>", start)
        if start == -1 or end == -1:
            continue

        def mark(m: re.Match) -> str:
            nonlocal tagged
            t = target_lang(m.group(1))
            if not t or t[0].lower().split("-")[0] == own_lang.split("-")[0]:
                return m.group(0)
            tagged += 1
            attrs = f' lang="{t[0]}"' + (f' dir="{t[1]}"' if t[1] == "rtl" else "")
            return f'<a href="{m.group(1)}"{attrs}>'

        body = _TAXO_LINK_RE.sub(mark, html[start:end])
        html = html[:start] + body + html[end:]
        page.write_text(html, encoding="utf-8")
        name = re.search(r'<span class="tag-name">([^<]+)</span>', html)
        count = re.search(r'class="taxonomy-meta">(\d+)', html)
        if name:
            topics.append((name.group(1), page.parent.name, count.group(1) if count else ""))

    index = site / "tags" / "index.html"
    if topics and index.is_file():
        html = index.read_text(encoding="utf-8")
        if 'class="topic-list"' not in html:
            items = "".join(
                f'<li><a href="/tags/{slug}/"><span>{label}</span>'
                f'<span class="topic-count">{n} pages</span></a></li>'
                for label, slug, n in topics)
            block = f'<ul class="topic-list" aria-label="Topics">{items}</ul>'
            html = html.replace("</article>", block + "</article>", 1)
            index.write_text(html, encoding="utf-8")
    print(f"[postbuild] taxonomy: lang on {tagged} link(s), {len(topics)} topic(s) indexed")


_SSG_TABLE_REGION = 'aria-label="Table, scrollable horizontally"'
_HEADING_TEXT_RE = re.compile(r"<h([2-4])\b[^>]*>(.*?)</h\1>", re.DOTALL)


def name_table_regions(site: Path) -> None:
    """ssg wraps some tables in a focusable `role="region"`, every one with
    the same English label. Several on one page break axe's
    landmark-unique rule, and on a translated page the label is in the
    wrong language. Each region is named after the heading above it (in
    the page's own language), numbered only when two would collide."""
    pages = 0
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        if _SSG_TABLE_REGION not in html:
            continue
        out, pos, used = [], 0, {}
        for m in re.finditer(re.escape(_SSG_TABLE_REGION), html):
            heads = list(_HEADING_TEXT_RE.finditer(html, 0, m.start()))
            label = _html.unescape(re.sub(r"<[^>]+>", "", heads[-1].group(2))).strip() if heads else ""
            label = re.sub(r"\s*#\s*$", "", label) or "Table"
            # The heading usually also names the section around the table,
            # so the table's first column header (in the page's language)
            # is added to keep the two landmarks distinct.
            th = re.search(r"<th\b[^>]*>(.*?)</th>", html[m.end():m.end() + 4000], re.DOTALL)
            if th:
                col = _html.unescape(re.sub(r"<[^>]+>", "", th.group(1))).strip()
                if col:
                    label = f"{label}: {col}"
            used[label] = used.get(label, 0) + 1
            if used[label] > 1:
                label = f"{label} ({used[label]})"
            out.append(html[pos:m.start()])
            out.append('aria-label="%s"' % _html.escape(label, quote=True))
            pos = m.end()
        out.append(html[pos:])
        page.write_text("".join(out), encoding="utf-8")
        pages += 1
    print(f"[postbuild] named table regions on {pages} page(s)")


_BOLD_PARA_RE = re.compile(r"<p>\s*<(strong|b)>([^<]{1,200})</\1>\s*</p>")
_ANY_HEADING_RE = re.compile(r"<h([1-6])\b")


def promote_bold_questions(site: Path) -> None:
    """A paragraph that is nothing but bold text is a heading written as
    formatting ("**What does Pain001 cost?**" in FAQ-style sections, and
    its translations). Screen-reader users cannot jump to it, and WAVE
    reports each one as a possible heading. It becomes a real heading one
    level below the nearest authored heading above it, so levels never
    skip, and consecutive questions stay siblings."""
    promoted = 0
    for page in site.rglob("index.html"):
        html = page.read_text(encoding="utf-8")
        start, end = html.find("<main"), html.find("</main>")
        if start == -1 or end == -1 or "<strong>" not in html[start:end]:
            continue
        body = html[start:end]
        out, pos, n = [], 0, 0
        for m in _BOLD_PARA_RE.finditer(body):
            text = m.group(2).strip()
            if not text or text.endswith((".", ",", ";")) and len(text) >= 50:
                continue
            authored = [int(h.group(1)) for h in _ANY_HEADING_RE.finditer(body, 0, m.start())]
            # Skip the headings this pass created (marked with the class).
            prior = [l for l, h in zip(authored, _ANY_HEADING_RE.finditer(body, 0, m.start()))
                     if 'class="promoted"' not in body[h.start():h.start() + 40]]
            level = min((prior[-1] if prior else 1) + 1, 6)
            out.append(body[pos:m.start()])
            # The <strong> stays inside the heading: translation keys for
            # these questions are written with it, and matching them is how
            # every locale gets its translation.
            out.append(f'<h{level} class="promoted"><{m.group(1)}>{text}</{m.group(1)}></h{level}>')
            pos = m.end()
            n += 1
        if n:
            out.append(body[pos:])
            html = html[:start] + "".join(out) + html[end:]
            page.write_text(html, encoding="utf-8")
            promoted += n
    print(f"[postbuild] promoted {promoted} bold paragraph(s) to headings")


_MILESTONE_RE = re.compile(r'<li class="milestone[^"]*">(.*?)</li>', re.DOTALL)


def mark_dated_content(site: Path) -> None:
    """Build-time state for dated content, so the output is deterministic
    for its build date: a `[data-expires]` element past its date is
    removed, and each timeline item is marked past or next. The page
    script re-checks against the visitor's clock for stale builds."""
    today = date.today().isoformat()
    for page in site.rglob("index.html"):
        html = page.read_text(encoding="utf-8")
        if "data-timeline" not in html and "data-expires" not in html:
            continue
        html = re.sub(r'<div class="ribbon" data-expires="(\d{4}-\d{2}-\d{2})">.*?</div>',
                      lambda m: "" if m.group(1) < today else m.group(0), html, flags=re.DOTALL)
        found = False

        def mark(m: re.Match) -> str:
            nonlocal found
            inner = m.group(1)
            t = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', inner)
            past = bool(t) and t.group(1) < today
            nxt = not past and not found
            found = found or nxt
            cls = "milestone" + (" is-past" if past else "") + (" is-next" if nxt else "")
            inner = re.sub(r'<span class="milestone-flag"( hidden)?>',
                           '<span class="milestone-flag">' if nxt else '<span class="milestone-flag" hidden>', inner)
            return f'<li class="{cls}">{inner}</li>'

        html = _MILESTONE_RE.sub(mark, html)
        page.write_text(html, encoding="utf-8")
    print(f"[postbuild] dated content marked for {today}")


# One photograph per page, never repeated: scripts/page_photos.json maps each
# English page path to a stock photo; translations use their English page's.
PAGE_PHOTO_MAP = Path(__file__).resolve().parent / "page_photos.json"
_PAGE_HERO_OPEN = '<section class="page-hero">'


def page_key(rel: str) -> str:
    parts = [p for p in rel.split("/") if p and p != "index.html"]
    if parts and parts[0] in LOCALES:
        parts = parts[1:]
    return "/".join(parts)


def add_page_photos(site: Path) -> None:
    """A photograph band at the top of every page hero, chosen by page
    family, as institutional sites carry one on every page. Decorative
    (alt=""), size-reserved, and fetched eagerly because it is the first
    thing painted. Text is never set on it."""
    photos = json.loads(PAGE_PHOTO_MAP.read_text(encoding="utf-8"))["pages"]
    n, unmapped = 0, set()
    for page in site.rglob("index.html"):
        html = page.read_text(encoding="utf-8")
        if 'class="page-photo"' in html:
            continue
        # Taxonomy pages have no page hero; the band opens their article.
        anchor = _PAGE_HERO_OPEN if _PAGE_HERO_OPEN in html else (
            '<article class="taxonomy-page' if '<article class="taxonomy-page' in html else None)
        if anchor is None:
            continue
        key = page_key(page.relative_to(site).as_posix())
        if key not in photos:
            unmapped.add(key)
            continue
        base = band_path(photos[key])
        sizes = "(min-width: 78rem) 76rem, calc(100vw - 2rem)"
        widths = (640, 768, 960, 1280, 1600)
        srcset = lambda ext: ", ".join(f"{base}-{w}.{ext} {w}w" for w in widths)
        img = (f'<picture class="page-photo-frame">'
               f'<source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}" />'
               f'<img class="page-photo" src="{base}-960.webp" srcset="{srcset("webp")}" '
               f'sizes="{sizes}" width="1600" height="800" '
               f'alt="" fetchpriority="high" /></picture>')
        html = html.replace(anchor, img + anchor, 1)
        page.write_text(html, encoding="utf-8")
        n += 1
    print(f"[postbuild] page photo on {n} page(s)")
    if unmapped:
        # A new page ships without a band rather than borrowing another
        # page's photo; add it to page_photos.json and re-run the importer.
        print(f"[postbuild] WARNING no photo mapped for: {sorted(unmapped)}")


# ssg's taxonomy template titles a tag page "Tag: X — <site title>". The
# site's copy carries no em dashes in any language, so the title is
# rewritten here, in the pages and in the search index built from them.
_TAG_TITLE = re.compile(r"Tag: ([^<\"]+?) \u2014 Pain001: ISO 20022 Payment Initiation Suite")


def retitle_tag_pages(site: Path) -> None:
    n = 0
    for page in [*(site / "tags").rglob("index.html"), site / "search-index.json"]:
        if not page.exists():
            continue
        text = page.read_text(encoding="utf-8")
        new = _TAG_TITLE.sub(r"Pages tagged \1 on Pain001", text)
        if new != text:
            page.write_text(new, encoding="utf-8")
            n += 1
    print(f"[postbuild] tag titles rewritten in {n} file(s)")


# ssg moves its search widget's inline script to /_csp/<hash>.js and loads
# it synchronously at the end of <body>. It only wires up the search
# overlay, whose elements precede it, so `defer` is equivalent and takes
# it off the first-paint path (Lighthouse counted it as render-blocking).
_CSP_SCRIPT = re.compile(r'<script src="(/_csp/[0-9a-f]+\.js)"(?![^>]*\bdefer\b)')


def defer_ssg_search(site: Path) -> None:
    n = 0
    for page in site.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        new = _CSP_SCRIPT.sub(r'<script defer src="\1"', text)
        if new != text:
            page.write_text(new, encoding="utf-8")
            n += 1
    print(f"[postbuild] search script deferred on {n} page(s)")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    site = Path(args[0] if args else "Pain001")
    # build.sh rsyncs static/ (sw.js, js/, pyodide/) into the output
    # AFTER this script's main pass, so the cache-version stamp has to
    # run in a second invocation once those files are actually there.
    # Called during the main pass it found no sw.js and silently did
    # nothing, which is the failure mode it exists to prevent.
    if "--stamp-sw" in sys.argv:
        stamp_redirect_map(site)
        stamp_sw_cache_version(site)
        return
    if "--optimise-assets" in sys.argv:
        bundle_stylesheets(site)
        # Our hand-written scripts ship without their block comments: the
        # translated /try/ pages sit close to ssg's 50 KB script budget.
        for name in ("prism.js", "pain001-prism.js", "home.js", "prism-theme-init.js"):
            js = site / "js" / name
            if js.is_file():
                js.write_text(strip_js_comments(js.read_text(encoding="utf-8")), encoding="utf-8")
        return
    repaired = 0
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        # Flatten the highlighter's invalid nested <pre> before protecting
        # inline code.  Doing this in the opposite order makes the protector
        # stop at the inner </pre>, after which the outer <code> delimiter is
        # escaped and the browser treats the remainder of the article as one
        # enormous code block.
        fixed = relocate_body_stylesheets(
            strip_align_attrs(
                stamp_table_labels(
                    wrap_tables(
                        add_article_furniture(
                            escape_inline_code(
                                restore_encoded_code(
                                    fix_code_blocks(
                                        fix_body(dedupe_head_metas(fix_head(html)))
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        if fixed != html:
            page.write_text(fixed, encoding="utf-8")
            repaired += 1
    print(f"[postbuild] unescaped head/body markup on {repaired} page(s)")
    add_version_requirements(site)  # before the locale generators copy pages
    fix_tag_pages(site)
    fix_social_descriptions(site)
    fix_double_encoded_meta(site)
    fix_manifest(site)
    fix_try_strip(site)
    localise_pages(site)
    gen_try_locales(site)
    gen_journey_locales(site)
    relocate_corpus_locales(site)  # before the Dataset markup, which is keyed by final path
    inject_dataset_ld(site)
    write_llms(site)
    stamp_suite_version(site)
    regen_sitemap(site)
    gen_legacy_redirects(site)  # after sitemap so stubs stay unindexed
    normalise_site_shell(site)  # includes taxonomy and redirect pages
    taxonomy_language_and_index(site)
    name_table_regions(site)
    promote_bold_questions(site)
    mark_dated_content(site)
    add_page_photos(site)
    retitle_tag_pages(site)
    defer_ssg_search(site)
    ensure_social_metadata(site)


LEGACY_REDIRECTS = {
    "executive-brief-fr": "/fr/executive-brief/",
    "executive-brief-de": "/de/executive-brief/",
    "executive-brief-es": "/es/executive-brief/",
}


def stamp_redirect_map(site: Path) -> None:
    """Write LEGACY_REDIRECTS into the shipped /js/redirect.js. The script
    looks its destination up by path in this map rather than reading it
    from the page, so it can only redirect to these same-origin paths
    (CodeQL js/xss-through-dom flagged the attribute read). Runs in the
    --stamp-sw pass, after static/ is copied and before the service
    worker's cache version is derived from the bytes."""
    js = site / "js" / "redirect.js"
    if not js.is_file():
        return
    table = {"/%s/" % old.strip("/"): new for old, new in LEGACY_REDIRECTS.items()}
    text = js.read_text(encoding="utf-8")
    stamped = text.replace("var REDIRECTS = {};",
                           "var REDIRECTS = %s;" % json.dumps(table, sort_keys=True), 1)
    if stamped == text:
        raise SystemExit("[postbuild] redirect.js has no REDIRECTS placeholder to stamp")
    js.write_text(stamped, encoding="utf-8")
    print(f"[postbuild] redirect map stamped: {len(table)} path(s)")


def gen_legacy_redirects(site: Path) -> None:
    """Redirect stubs for retired URLs (GitHub Pages has no server
    redirects). noindex + canonical point crawlers at the new location.

    Not a meta refresh: WAVE reports every `<meta http-equiv="refresh">`
    as an error (WCAG 2.2.1 / 3.2.5), whatever its delay. A same-origin
    script redirects at once, and the visible link is the fallback when
    scripting is off."""
    stub = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '<meta charset="utf-8" />\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1" />\n'
            '<meta name="robots" content="noindex" />\n'
            "%(csp)s\n"
            '<script src="/js/redirect.js"></script>\n'
            '<meta name="description" content="This page has moved to %(base)s%(new)s." />\n'
            '<meta property="og:title" content="Page moved: Pain001" />\n'
            '<meta property="og:type" content="website" />\n'
            '<meta property="og:url" content="%(base)s%(new)s" />\n'
            '<meta property="og:image" content="%(base)s/og/pain001-card.jpg" />\n'
            '<meta name="twitter:card" content="summary" />\n'
            '<link rel="canonical" href="%(base)s%(new)s" />\n'
            "<title>Page moved: Pain001</title>\n</head>\n<body>\n"
            '<main id="main-content">\n'
            "<h1>This page has moved</h1>\n"
            '<p>Continue to <a href="%(new)s">%(base)s%(new)s</a>.</p>\n'
            "</main>\n</body>\n</html>\n")
    for old, new in LEGACY_REDIRECTS.items():
        dest = site / old
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.html").write_text(
            stub % {"new": new, "base": BASE_URL, "csp": CSP_META},
            encoding="utf-8")
    print(f"[postbuild] {len(LEGACY_REDIRECTS)} legacy redirect stub(s)")


_CSP_TAG_RE = re.compile(
    r'<meta\b[^>]*Content-Security-Policy[^>]*>', re.IGNORECASE | re.DOTALL)
_PRISM_LINKS = (
    '<link rel="stylesheet" href="/css/prism.css" />'
    '<link rel="stylesheet" href="/css/pain001-prism.css" />'
    # Same preload base.html gives every other page, so the text face is
    # not discovered only after the stylesheet has been parsed.
    '<link rel="preload" href="/fonts/inter-var-latin.woff2" as="font" type="font/woff2" crossorigin />'
)
_FOOTER_CREDIT = (
    '<p class="footer-credit">Made in London. Built with '
    '<a href="https://static-site-generator.com/">SSG</a>.</p>'
)


def normalise_site_shell(site: Path) -> None:
    """Give authored, taxonomy, and redirect pages one security policy and
    one footer contract. Taxonomy pages are emitted outside the layouts, so
    add the PRISM assets and exact three-state control here as well."""
    root_html = (site / "index.html").read_text(encoding="utf-8")
    header_match = re.search(
        r'<header class="site-header">.*?</header>', root_html, re.DOTALL)
    footer_match = re.search(
        r'<footer class="site-footer">.*?</footer>', root_html, re.DOTALL)
    shared_header = header_match.group(0) if header_match else ""
    shared_footer = footer_match.group(0) if footer_match else ""

    changed = 0
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        fixed, count = _CSP_TAG_RE.subn(CSP_META, html, count=1)
        if count == 0 and "</head>" in fixed:
            fixed = fixed.replace("</head>", CSP_META + "</head>", 1)

        is_taxonomy = "/tags/" in "/" + page.relative_to(site).as_posix()
        is_redirect = '<script src="/js/redirect.js"' in fixed
        if is_taxonomy or is_redirect:
            if "/css/prism.css" not in fixed:
                fixed = fixed.replace("</head>", _PRISM_LINKS + "</head>", 1)
            fixed = fixed.replace("<body>", '<body class="prism-theme">', 1)
            # Taxonomy pages arrive with their own bare `<header role=banner>`
            # (a single home link, no class), so they never matched the
            # `site-header` test and shipped without the site navigation.
            if shared_header and ("site-header" in fixed or is_taxonomy):
                fixed = re.sub(
                    r'<header\b[^>]*>.*?</header>', shared_header, fixed,
                    count=1, flags=re.DOTALL)
            elif shared_header and is_redirect:
                fixed = fixed.replace(
                    '<body class="prism-theme">',
                    '<body class="prism-theme">' + shared_header, 1)
            if shared_footer and re.search(r'<footer\b', fixed):
                fixed = re.sub(
                    r'<footer\b[^>]*>.*?</footer>', shared_footer, fixed,
                    count=1, flags=re.DOTALL)
            elif shared_footer and is_redirect:
                fixed = fixed.replace("</body>", shared_footer + "</body>", 1)
            # ssg's taxonomy template ships an inline <style> (skip link,
            # focus ring, list-link targets). The CSP blocks it, which logs
            # a console error on every tag page; prism.css and taxonomy.css
            # already style all three, so the block is dropped.
            if is_taxonomy:
                fixed = re.sub(r"<style>.*?</style>", "", fixed, count=1, flags=re.DOTALL)
            if is_taxonomy and "<html" in fixed and 'class="no-js"' not in fixed:
                fixed = re.sub(r"<html\b", '<html class="no-js"', fixed, count=1)
            if _THEME_INIT_LINK not in fixed and _THEME_INIT_TAG not in fixed:
                fixed = fixed.replace("</head>", _THEME_INIT_LINK + "</head>", 1)
            if 'src="/js/prism.js"' not in fixed:
                fixed = fixed.replace(
                    "</body>", '<script src="/js/prism.js" defer></script>'
                    '<script src="/js/pain001-prism.js" defer></script></body>', 1)
        fixed = fixed.replace(_THEME_INIT_LINK, _THEME_INIT_TAG, 1)

        if 'class="footer-credit"' not in fixed:
            if "</footer>" in fixed:
                fixed = fixed.replace("</footer>", _FOOTER_CREDIT + "</footer>", 1)
            elif "</body>" in fixed:
                fixed = fixed.replace(
                    "</body>", '<footer class="footer">' + _FOOTER_CREDIT + "</footer></body>", 1)

        if fixed != html:
            page.write_text(fixed, encoding="utf-8")
            changed += 1
    print(f"[postbuild] normalised PRISM shell and CSP on {changed} page(s)")


if __name__ == "__main__":
    main()
