# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/css_minify.py.

Pins the minifier's documented examples (run as doctests) and its
handling of escaped quotes and unterminated comments, in both the CSS
minifier and the JavaScript comment stripper.
"""

from __future__ import annotations

import doctest

import css_minify


def test_documented_examples_hold():
    result = doctest.testmod(css_minify)
    assert result.attempted >= 9
    assert result.failed == 0


def test_css_strings_with_escaped_quotes_are_copied_whole():
    assert css_minify.minify_css('a { content: "x\\" ; y" ; }') == 'a{content: "x\\" ; y"}'


def test_css_unterminated_comment_runs_to_the_end():
    assert css_minify.minify_css("a { b: c }  /* never closed { d: e }") == "a{b: c}"


def test_js_escaped_quote_and_unterminated_comment():
    assert css_minify.strip_js_comments("s = 'it\\'s /* x */';\n\n\nf(); /* open") == "s = 'it\\'s /* x */';\nf(); "
