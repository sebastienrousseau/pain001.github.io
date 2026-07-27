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
    "style-src 'self'  'unsafe-hashes' 'sha256-+naa4DVyLB6dFJG6pe9ePhWQvc+IemcuXsxc1C9yQdg='; "
    "script-src 'self'  'wasm-unsafe-eval'; "
    "connect-src 'self'; font-src 'self'; "
    "form-action 'self' https://formspree.io\" "
    "http-equiv=Content-Security-Policy>"
)
OG_IMAGE_META = (
    '<meta property="og:image" '
    'content="https://pain001.com/og/pain001-card.jpg" />'
    '<meta property="og:image:alt" content="Pain001 — payment files your bank will not reject" />'
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
    import json

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

# Submenu targets that exist only in English get a visible cue on
# localized pages, so the language jump is expected instead of surprising.
EN_ONLY_SUB = (
    "/competitors-comparison/", "/installation/", "/glossary/", "/faqs/",
    "/pain002-reason-codes/", "/pain001-mcp/", "/pain001-lsp/",
    "/pain001-loader-mt101/", "/pain001-loader-xlsx/",
    "/architecture-and-patents/", "/2026-iso20022-migration-trends/",
    "/iso20022-roadmap/",
    "/iso-20022-payment-initiation-for-cross-border-payments/", "/languages/",
)


def retarget_journey_nav(html: str, slug: str) -> str:
    """Nav/footer/body links to localized journey pages stay in-locale."""
    for p in JOURNEY_PAGES:
        html = html.replace('href="/%s/"' % p, 'href="/%s/%s/"' % (slug, p))
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
        dir_attr = ' dir="rtl"' if slug in RTL_LANGS else ""
        html = html.replace('<html lang="en-GB">',
                            '<html lang="%s"%s>' % (code, dir_attr), 1)
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
            if ">%s<" % k in html:
                html = html.replace(">%s<" % k, ">%s<" % v)
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
        dest = site / slug / "try"
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.html").write_text(html, encoding="utf-8")
        n += 1
    print(f"[postbuild] generated {n} locale /try/ page(s)")


def gen_journey_locales(site: Path) -> None:
    """Generate /<slug>/{why,solutions,executive-brief}/ for every locale
    with a pages_i18n table — same mechanics as the /try/ variants."""
    try:
        from locale_strings import STRINGS
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from locale_strings import STRINGS
    en_all = load_pages_i18n("en") or {}
    for page_name in JOURNEY_PAGES:
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
            d = load_pages_i18n(slug)
            if not d or page_name not in d or slug not in STRINGS:
                continue
            pd = d[page_name]
            html = base
            dir_attr = ' dir="rtl"' if slug in RTL_LANGS else ""
            html = html.replace('<html lang="en-GB">',
                                '<html lang="%s"%s>' % (code, dir_attr), 1)
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
                if ">%s<" % k in html:
                    html = html.replace(">%s<" % k, ">%s<" % v)
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
    fix_try_strip(site)
    localise_pages(site)
    gen_try_locales(site)
    gen_journey_locales(site)
    regen_sitemap(site)


if __name__ == "__main__":
    main()
