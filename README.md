<!-- markdownlint-disable MD033 MD041 -->

<img
  align="right"
  alt="Logo of Pain001"
  height="261"
  src="https://kura.pro/pain001/images/logos/pain001.webp"
  width="261"
  />

<!-- markdownlint-enable MD033 MD041 -->

# pain001.com — Official Website 🌏

The website for the [Pain001](https://github.com/sebastienrousseau/pain001)
open-source ISO 20022 payment initiation suite: core library, MCP server for
AI agents, LSP server, and the MT101 / Excel loaders. Its job is to convert a
treasury engineer, an integrator or an AI agent into an installed user, and
to hand a regulated buyer the evidence they need.

Built with the [Shokunin Static Site Generator (ssg)][00] **0.0.47 exactly**
and published to GitHub Pages from `docs/` on the default branch. Cloudflare
fronts the domain.

## Repository layout

| Path | Purpose |
| :--- | :--- |
| `_posts/` | Page content (Markdown + front matter), the source of truth. Corpus scenario pages (`corpus-*.md`, `<locale>-corpus-*.md`) and message-spec pages are **generated**; edit the generator, not the page |
| `_layouts/` | HTML templates: `index`, `page`, `contact`, `try` (the demo). The CSP meta and the measurement beacon live here |
| `static/` | Copied verbatim into the output: the demo's ES modules (`js/`), the vendored Pyodide runtime and wheels (`pyodide/`), corpus files, schemas and samples (`corpus/`), the service worker, the vendored analytics beacon |
| `scripts/` | Generators, post-build repairs, translation tables and the validators CI runs (see below) |
| `tests/` | Node tests: demo input handling and the browser engine integration run against the vendored runtime |
| `docs/` | The built site. Committed, served by GitHub Pages, **never edited by hand** |
| `.github/workflows/` | `ci.yml` (build and every gate on push and PR) and `regenerate.yml` (release-triggered regeneration, opens a PR) |

## Build

Prerequisites: Rust toolchain with `cargo install ssg --locked --version 0.0.47`
(newer ssg parses the posts' front matter differently and fails), Node 20+,
Python 3.10+ with the `pain001` library installed for the generators and the
snippet gate, and Chrome for the browser gates.

```shell
./build.sh          # build, post-build repairs, publish to docs/
./build.sh --audit  # same, then ssg's audit gates at warn severity
```

`build.sh` runs, in order: `scripts/traction.py` (PyPI and GitHub figures into
the governance page), `ssg build`, `scripts/postbuild_fix.py` (head and body
repairs, tag pages, the 34-locale variants of the core pages, the six-locale
corpus variants, Dataset JSON-LD, `llms.txt`, footer version stamp, sitemap),
the `static/` copy, sample CSV generation, and the service-worker cache stamp.

## Regenerating from a library release

Everything derived from the library is regenerated from the installed version:

```shell
python3 scripts/generate_try_samples.py                 # demo corpus samples
python3 scripts/generate_corpus_page.py <path-to-pain001-checkout>
python3 scripts/stamp_version.py <version>              # version literals on pages
./build.sh
```

`regenerate.yml` does exactly this when the library's publish job sends a
`repository_dispatch` (`suite-release`), or on `workflow_dispatch` with a
version, and opens a `release/pain001-<version>` pull request. A human merges.
The library needs the `SITE_DISPATCH_TOKEN` secret for the dispatch.

## Gates

CI fails on any of these; run them locally before opening a PR.

| Gate | Command |
| :--- | :--- |
| ssg audit, warnings fail | `ssg audit -f ssg.toml -o docs --severity warn --fail-on warn` |
| Unit tests | `node --test tests/*.test.mjs` |
| Browser engine runs the library | `npm i --no-save pyodide@0.27.2 && node tests/engine.integration.mjs` |
| Translation table integrity | `scripts/validate_try_i18n.py`, `scripts/validate_pages_i18n.py pages_i18n`, `… docs_i18n` |
| Translation keys still match the built pages | `scripts/validate_i18n_keys_live.py` |
| Content integrity (no eaten markup, no double encoding) | `scripts/validate_content_integrity.py` |
| Link integrity | `scripts/validate_links.py docs` |
| Suite version currency | `scripts/validate_versions.py` |
| Documentation snippets reference the real API | `scripts/validate_snippets.py` (with `pain001` installed) |
| Layout and print integrity, real Chrome | `node scripts/layout_audit.cjs`, `node scripts/print_audit.cjs` (needs `.a11y-tools/` with `puppeteer-core`, see the script headers) |
| Performance budgets, Lighthouse mobile | `node scripts/perf_budget.mjs http://127.0.0.1:8899` |
| Accessibility, WCAG 2 AAA | `npx -y pa11y-ci@4.1.1` against the `.pa11yci` list, or `node scripts/a11y_local.mjs` |

The layout, performance and accessibility gates need `docs/` served locally:
`(cd docs && python3 -m http.server 8899)`.

## Editing content

Edit the Markdown in `_posts/`; keep `title`, `description` and `keywords`
unique per page; run the build and the gates; commit the source **and** the
regenerated `docs/`. Because `docs/` is committed, a branch that is behind
`main` conflicts there on every merge: resolve by taking either side and
rebuilding, never by hand-merging built HTML.

Translated pages are produced at post-build from tables keyed by exact
fragments of the built English HTML (`scripts/pages_i18n`, `docs_i18n`,
`try_i18n`, `runtime_i18n`, `locale_strings.py`, `corpus_l10n.py`). A change
to an English sentence on a localised page needs the key re-extracted and the
34 tables migrated, or the live-key gate fails.

## Measurement and privacy

Page views are counted by Cloudflare Web Analytics from a beacon served from
this origin; the demo page carries none. What is counted, where the tag lives
and how to switch it off is in [`METRICS.md`](METRICS.md). The privacy and
trust pages state the same facts publicly.

## Licence

Dual-licensed under Apache-2.0 or MIT, at your option. See `LICENSE-APACHE`
and `LICENSE-MIT`.

[00]: https://shokunin.one "Shokunin Static Site Generator (SSG)"
