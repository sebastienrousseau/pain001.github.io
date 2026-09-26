# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests for earlier site fixes.

- 05c6ba84 "derive the demo cache version from what it caches": the
  service worker's cache name was bumped by hand and forgotten three
  times, so returning visitors kept stale demo pages.
- 27fe136a "full head metadata on legacy redirect stubs" and 40491e67
  "stubs for retired URLs": each retired URL needs a noindex stub with a
  canonical link, social metadata and a visible link, and no meta
  refresh (WAVE flags every one).
- 34e786fa "replace inline style attributes with classes": the strict
  CSP blocks inline style attributes, so layouts must not use them.
- 0e1ff294 "restore LICENSE as a pointer to the dual grant".
"""

import re
from pathlib import Path

import postbuild_fix as pb

ROOT = Path(__file__).resolve().parents[2]
SW = 'const CACHE = "pain001-try-000000000000";\nself.addEventListener("fetch", () => {});\n'


def _site(tmp_path):
    site = tmp_path / "site"
    for rel, data in {
        "sw.js": SW,
        "try/index.html": "<h1>demo</h1>",
        "fr/try/index.html": "<h1>démo</h1>",
        "js/try-demo.js": "export const x = 1;",
        "samples/sepa.csv": "id,date\n1,2026-01-01\n",
        "pyodide/pyodide.asm.wasm": "wasm",
    }.items():
        path = site / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")
    return site


def _cache_name(site):
    return re.search(r'"pain001-try-([0-9a-f]+)"', (site / "sw.js").read_text(encoding="utf-8")).group(1)


def test_sw_cache_version_follows_the_cached_content(tmp_path):
    site = _site(tmp_path)
    first = pb.stamp_sw_cache_version(site)
    assert first == _cache_name(site) and first != "000000000000"

    assert pb.stamp_sw_cache_version(site) == first  # a no-op rebuild keeps it

    (site / "fr" / "try" / "index.html").write_text("<h1>démo traduite</h1>", encoding="utf-8")
    second = pb.stamp_sw_cache_version(site)
    assert second != first and _cache_name(site) == second


def test_sw_cache_version_changes_with_a_new_runtime_file(tmp_path):
    site = _site(tmp_path)
    first = pb.stamp_sw_cache_version(site)
    (site / "pyodide" / "pain001-0.0.72-py3-none-any.whl").write_text("wheel", encoding="utf-8")
    assert pb.stamp_sw_cache_version(site) != first


def test_legacy_redirect_stubs_are_complete_and_have_no_meta_refresh(tmp_path):
    site = tmp_path / "site"
    site.mkdir()
    pb.gen_legacy_redirects(site)

    assert pb.LEGACY_REDIRECTS
    for old, new in pb.LEGACY_REDIRECTS.items():
        html = (site / old / "index.html").read_text(encoding="utf-8")
        target = pb.BASE_URL + new
        assert '<meta name="robots" content="noindex" />' in html
        assert f'<link rel="canonical" href="{target}" />' in html
        assert f'<meta property="og:url" content="{target}" />' in html
        assert '<meta name="description"' in html and "<title>" in html
        assert f'<a href="{new}">' in html
        assert "http-equiv=\"refresh\"" not in html.lower()
        assert "Content-Security-Policy" in html


def test_layouts_use_no_inline_style_attributes():
    offenders = [
        f"{path.relative_to(ROOT)}:{n}"
        for path in sorted((ROOT / "_layouts").glob("*.html"))
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if re.search(r"\sstyle=\"", line)
    ]
    assert offenders == []


def test_license_points_to_the_dual_grant():
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "LICENSE-APACHE" in text and "LICENSE-MIT" in text
    assert "SPDX-License-Identifier: Apache-2.0 OR MIT" in text
    assert (ROOT / "LICENSE-APACHE").is_file() and (ROOT / "LICENSE-MIT").is_file()
