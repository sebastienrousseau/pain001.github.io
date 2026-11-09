# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The homepage suite heading counts the package tiles.

The heading said "Five focused packages" by hand above six tiles, and an
audit read it as a miscount: the sixth tile is the example corpus, which
is not a package. postbuild_fix.stamp_package_count now derives the
number from the tiles marked data-package.
"""

from pathlib import Path

import pytest

import postbuild_fix as pb

ROOT = Path(__file__).resolve().parents[2]


def _home(tiles):
    return (
        '<h2 id="suite-title"><span data-package-count>Five</span> focused packages.</h2>'
        + "".join(f'<article class="tile" data-package="{t}"></article>' for t in tiles)
        + '<article class="tile"><h3>Example corpus</h3></article>'
    )


def test_the_heading_counts_package_tiles_only():
    html = pb.stamp_package_count(_home(["a", "b", "c", "d", "e", "f"]))
    assert "<span data-package-count>Six</span>" in html


def test_a_page_without_the_heading_is_untouched():
    assert pb.stamp_package_count("<p>no heading</p>") == "<p>no heading</p>"


def test_no_package_tiles_is_an_error():
    with pytest.raises(ValueError):
        pb.stamp_package_count(_home([]))


def test_the_layout_marks_exactly_the_published_packages():
    layout = (ROOT / "_layouts" / "index.html").read_text(encoding="utf-8")
    assert sorted(pb._PACKAGE_TILE_RE.findall(layout)) == [
        "pain001",
        "pain001-loader-mt101",
        "pain001-loader-xlsx",
        "pain001-lsp",
        "pain001-mcp",
    ]
    assert "data-package-count" in layout
