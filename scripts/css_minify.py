#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""A deliberately small CSS minifier for the published stylesheet bundle.

Lighthouse reported ~10 KB of avoidable bytes in the render-blocking
bundle, enough to move mobile First Contentful Paint. This removes
comments and collapses whitespace, and nothing else: no property
rewriting, no shorthand merging, nothing that needs a CSS parser to be
safe. Quoted strings are copied through untouched, and whitespace is
never removed around ``:`` (``a :hover`` and ``a:hover`` differ).

>>> minify_css("a  {\\n  color : red;\\n}\\n/* note */ b , i { x: y }")
'a{color : red}b,i{x: y}'
>>> minify_css('p::after { content: "  /* kept */  "; }')
'p::after{content: "  /* kept */  "}'
>>> minify_css("a :hover { top: 0 }")
'a :hover{top: 0}'
>>> minify_css("@media (min-width: 40rem) {\\n  .x { gap: 1px }\\n}")
'@media (min-width: 40rem){.x{gap: 1px}}'
>>> minify_css(".a { b: calc(1px + 2px); }")
'.a{b: calc(1px + 2px)}'
>>> minify_css('q::before { content: ";}"; }')
'q::before{content: ";}"}'
"""

from __future__ import annotations

import re

_WS = re.compile(r"\s+")
_AROUND = re.compile(r"\s*([{};,>])\s*")


def _squeeze(chunk: str) -> str:
    chunk = _WS.sub(" ", chunk)
    # A declaration block's last semicolon is optional. Applied here, to
    # text outside strings only.
    return _AROUND.sub(r"\1", chunk).replace(";}", "}")


def minify_css(css: str) -> str:
    out: list[str] = []
    buf: list[str] = []
    i, n = 0, len(css)
    while i < n:
        c = css[i]
        if c in "\"'":
            out.append(_squeeze("".join(buf)))
            buf = []
            j = i + 1
            while j < n and css[j] != c:
                j += 2 if css[j] == "\\" else 1
            out.append(css[i : j + 1])
            i = j + 1
        elif css.startswith("/*", i):
            end = css.find("*/", i + 2)
            i = n if end == -1 else end + 2
            buf.append(" ")
        else:
            buf.append(c)
            i += 1
    out.append(_squeeze("".join(buf)))
    return "".join(out).strip()


def strip_js_comments(js: str) -> str:
    r"""Remove /* block */ comments (keeping /*! licence notices) and blank
    lines from our own hand-written scripts. Quoted strings and template
    literals are copied through. Line comments and regex literals are left
    alone: this is a byte trim for the /try/ page's 50 KB script budget,
    not a minifier.

    >>> strip_js_comments('a = 1; /* note */\n\n\nb = "/* kept */";')
    'a = 1; \nb = "/* kept */";'
    >>> strip_js_comments('/*! Licence */\nx();')
    '/*! Licence */\nx();'
    >>> strip_js_comments("s = '/*'; /* gone */ t = `*/`;")
    "s = '/*';  t = `*/`;"
    """
    out: list[str] = []
    i, n = 0, len(js)
    while i < n:
        c = js[i]
        if c in "\"'`":
            j = i + 1
            while j < n and js[j] != c:
                j += 2 if js[j] == "\\" else 1
            out.append(js[i : j + 1])
            i = j + 1
        elif js.startswith("/*", i) and not js.startswith("/*!", i):
            end = js.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(c)
            i += 1
    return re.sub(r"\n[ \t]*\n+", "\n", "".join(out))


if __name__ == "__main__":
    import doctest

    raise SystemExit(doctest.testmod().failed)
