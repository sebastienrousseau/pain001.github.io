<!-- SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->
<!-- markdownlint-disable MD033 MD041 -->

<p align="center">
  <img src="https://pain001.com/img/pain001.svg" alt="Pain001 logo" width="128" />
</p>

<h1 align="center">Pain001</h1>

<p align="center">
  The official website for the Pain001 open-source ISO 20022 payment initiation suite.
</p>

<p align="center">
  <a href="https://github.com/sebastienrousseau/pain001.github.io/actions/workflows/ci.yml"><img src="https://github.com/sebastienrousseau/pain001.github.io/actions/workflows/ci.yml/badge.svg" alt="Build" /></a>
  <a href="https://github.com/sebastienrousseau/pain001.github.io/releases"><img src="https://img.shields.io/github/v/release/sebastienrousseau/pain001.github.io" alt="Release" /></a>
  <a href="https://pain001.com/documentation/"><img src="https://img.shields.io/badge/API-reference-07172b" alt="Docs" /></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/sebastienrousseau/pain001.github.io"><img src="https://img.shields.io/ossf-scorecard/github.com/sebastienrousseau/pain001.github.io?label=OpenSSF%20Scorecard&logo=openssf" alt="OpenSSF Scorecard" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-blue.svg" alt="License: Apache-2.0 OR MIT" /></a>
  <a href="https://static-site-generator.com/"><img src="https://img.shields.io/badge/SSG-0.0.63-8f341f" alt="Minimum toolchain: SSG 0.0.63" /></a>
</p>

<!-- markdownlint-enable MD033 MD041 -->

---

This repository builds <https://pain001.com>, the website for the
[Pain001](https://github.com/sebastienrousseau/pain001) open-source ISO 20022
payment initiation suite: core library, MCP server for AI agents, LSP server,
and the MT101 / Excel loaders. Its job is to convert a treasury engineer, an
integrator or an AI agent into an installed user, and to hand a regulated
buyer the evidence they need.

Built with the [Shokunin Static Site Generator (ssg)][00] **0.0.63 exactly**
and deployed to GitHub Pages by `ci.yml` from the same run that passed every
gate; the built tree is never committed. Cloudflare fronts the domain.

<!-- markdownlint-disable MD033 -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://pain001.com/img/readme/pain001-home-dark.webp" />
  <img src="https://pain001.com/img/readme/pain001-home-light.webp" alt="The pain001.com homepage: the deferred-deadline ribbon, a photograph of the City of London, and the headline 'Deterministic ISO 20022 validation. Inside your perimeter.'" />
</picture>
<!-- markdownlint-enable MD033 -->

---

## Contents

<!-- The workspace README template groups these links under bold labels rather
     than headings, so that only the real sections appear in the table of
     contents. MD036 is suppressed for that block alone. -->
<!-- markdownlint-disable MD036 -->

**Getting started**

- [Install](#install) — clone and pin the generator; there is no installable artifact
- [Requirements](#requirements) — toolchain floor, platforms
- [Quick Start](#quick-start) — build the site and serve it locally

**The Pain001 ecosystem**

- [The Pain001 ecosystem](#the-pain001-ecosystem) — the five packages this site documents

**Reference**

- [Capabilities at a glance](#capabilities-at-a-glance) — what the built site contains
- [Ecosystem comparison](#ecosystem-comparison) — why the comparison lives in the library
- [Benchmarks](#benchmarks) — the performance budgets CI enforces
- [Features](#features) — repository layout and what each directory owns
- [Configuration](#configuration) — `ssg.toml`, the generator pin, the compliance declaration
- [Examples](#examples) — regenerating the site from a library release

**Operational**

- [When not to use Pain001](#when-not-to-use-pain001) — limitations
- [Development](#development) — build, post-build passes, gates, content editing
- [Security](#security) — reporting, hardening, supply chain
- [Documentation](#documentation) — all reference docs
- [Stability guarantees](#stability-guarantees) — SemVer axis, URL durability, toolchain discipline
- [License](#license)

<!-- markdownlint-enable MD036 -->

---

## Install

This repository produces a website, not an installable binary or library.
There is intentionally no system-wide `make install` for a Pages site.

```shell
git clone https://github.com/sebastienrousseau/pain001.github.io.git
cd pain001.github.io
cargo install ssg --locked --version 0.0.63
npm ci
```

Release archives of the built site are available from
[GitHub Releases](https://github.com/sebastienrousseau/pain001.github.io/releases)
for review or static hosting.

## Requirements

| Component | Floor | Enforced by |
| :--- | :--- | :--- |
| Shokunin SSG | 0.0.63 exactly | `SSG_VERSION` in `ci.yml`; the pin is the cache key |
| Node.js | 22 (24 also tested) | `engines` in `package.json`; the `node-matrix` job runs the unit tests on both |
| Python | 3.12 | `python-version` in `ci.yml`; generators, post-build passes and validators |
| Chrome or Chromium | any current | layout, print, accessibility and Lighthouse gates |

The minimum may rise only in a patch release when a security fix, a parser
correctness fix, or a required generator feature demands it; the reason must
appear in `CHANGELOG.md` and a migration guide. No distro LTS compatibility is
claimed beyond those explicit floors.

## Quick Start

```shell
make build     # build, post-build repairs, publish to site/
make serve     # serve site/ on http://127.0.0.1:8099/
make verify    # reproduce the non-network CI gates
make deps      # audit npm advisories against the documented exceptions
```

## The Pain001 ecosystem

This site documents five packages, each with its own repository and release
cadence. The full map is in [`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md).

| Package | Role |
| :--- | :--- |
| `pain001` | Core library, CLI and REST API; the validation pipeline everything else calls |
| `pain001-mcp` | MCP server exposing the pipeline as tools for AI agents |
| `pain001-lsp` | Language server: diagnostics on payment files as you type |
| `pain001-loader-mt101` | SWIFT MT101 bridge onto the ISO 20022 pipeline |
| `pain001-loader-xlsx` | Excel on-ramp with the spreadsheet hazards handled |

## Capabilities at a glance

Measured on the current build.

| Surface | Detail |
| :--- | :--- |
| Pages | 668 built pages; 661 URLs in the sitemap (utility pages such as the 404, offline and form-confirmation pages are noindexed and left out) |
| Locales | 34, with an hreflang cluster per localised page and RTL handling for 3 |
| Browser demo | `/try/` runs the `pain001` library itself in WebAssembly, same-origin, offline-capable; payment data never leaves the browser |
| Example corpus | 42 scenarios, each on an English page and five translated pages (252 in all), with schema.org `Dataset` markup, downloadable inputs and expected output |
| Agent discovery | `llms.txt`, `llms-full.txt` and a JSON search index |
| Structured data | JSON-LD on every page: `WebSite` and `WebPage`; the corpus scenario pages add `Dataset`, `DataCatalog`, `DataDownload` and `Organization` |

## Ecosystem comparison

Not applicable to this repository. A comparison against other ISO 20022
tooling is a claim about the library, not about its website, so it is
maintained with the library and published at
<https://pain001.com/competitors-comparison/>. Reproducing it here would
create a second copy to drift.

## Benchmarks

`scripts/perf_budget.mjs` gates every push. Thirteen routes, one per layout
and generator, are measured under five Lighthouse profiles (mobile, tablet,
desktop, 4K and 8K), and **all four categories must score exactly 100**:
performance, accessibility, best practices and SEO. The performance score is
computed from the timing metrics (LCP, FCP, total blocking time, CLS, speed
index), so they are gated through it. A performance-only 99 is measured once
more and the second sample counts, because a shared CI runner makes single
samples noisy; a real regression fails both.

| Routes | Byte budget |
| :--- | ---: |
| `/`, `/documentation/`, `/compliance-toolkit/`, `/example-corpus/`, `/why/`, `/enterprise/`, `/competitors-comparison/`, `/corpus-gb-fps-single/`, `/tags/iso-20022/`, `/fr/`, `/ar/` | 300 KiB |
| `/try/` (before the WebAssembly runtime, which loads on intent), `/message-spec-pain.001.001.09/` | 400 KiB |

## Features

| Path | Purpose |
| :--- | :--- |
| `_posts/` | Page content (Markdown + front matter), the source of truth. Corpus scenario pages (`corpus-*.md`, `<locale>-corpus-*.md`) and message-spec pages are **generated**; edit the generator, not the page |
| `_layouts/` | HTML templates. `base` holds the head: the CSP meta, the security metas and the JSON-LD graph are declared once there and inherited by `index`, `page`, `contact` and `try` |
| `static/` | Copied verbatim into the output: the demo's ES modules (`js/`), the vendored Pyodide runtime and wheels (`pyodide/`), corpus files, schemas and samples (`corpus/`), the service worker, the vendored analytics beacon |
| `scripts/` | Generators, the post-build passes, translation tables and the validators CI runs |
| `tests/` | Node tests: demo input handling and the browser engine integration run against the vendored runtime |
| `site/` | The built site, produced by `build.sh`; ignored by git and uploaded by CI as the Pages artifact |
| `.github/workflows/` | `ci.yml` (build, every gate, and on `main` the Pages deploy), `release.yml` (signed-tag release: archive, SBOM, attestations), `regenerate.yml` (library-release regeneration, opens a PR), `dated-claims.yml` (weekly check of dated regulatory claims), `codeql.yml`, `scorecard.yml`, `dco.yml` |

## Configuration

| File | What it controls |
| :--- | :--- |
| `ssg.toml` | Site name, description, language, base URL, and the content, template and output directories |
| `SSG_VERSION` in `.github/workflows/ci.yml` | The generator pin, single-sourced: it is both the install version and the binary cache key |
| `.compliance.yml` | Declared compliance tier, criticality and owner, per the workspace standard |
| `scripts/perf_budget.mjs` | Routes, Lighthouse profiles and byte budgets |

## Examples

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

## When not to use Pain001

Do not use this website as a bank connectivity service, legal or regulatory
advice, a substitute for your bank's implementation guide, or proof that a
file is eligible for a particular account and channel. The browser demo is a
local validation aid and never submits payments. Use the separate Pain001
library for production automation, and complete bank certification before
going live.

## Development

### Build

Prerequisites: the Rust toolchain with `cargo install ssg --locked --version 0.0.63`,
Node 22+, Python 3.12 with the `pain001` library installed for the generators
and the snippet gate, and Chrome for the browser gates.

```shell
./build.sh          # build, post-build repairs, publish to site/
./build.sh --audit  # same, then ssg's audit gates at warn severity
```

`build.sh` takes a lock, then runs, in order: `scripts/traction.py` (PyPI and
GitHub figures into the governance page), `ssg build`, `scripts/sbom_serial.py`
(a deterministic `serialNumber` for the SBOM), `scripts/postbuild_fix.py` (the
passes below), the `static/` copy, `postbuild_fix.py --optimise-assets` (one
SRI-protected stylesheet bundle per layout, comments stripped from the site's
own scripts), sample CSV generation, `postbuild_fix.py --stamp-sw`, and
`scripts/carry_forward_assets.py`, then publishes the result to `site/`.

### The post-build passes

`scripts/postbuild_fix.py` runs once over the ssg output before the
`static/` copy, then with `--optimise-assets` and `--stamp-sw` after it. Each pass
exists because a specific defect shipped without it; the script's
docstrings say which.

| Pass | What it does |
| :--- | :--- |
| Per-page repairs | Unescape the head metas and body markup ssg entity-escaped; drop duplicate `description` and `viewport` metas; re-escape inline `<code>` so element names read as text; add heading ids, anchors, a Contents block and a reading time; wrap tables for horizontal scroll and stamp their column labels; flatten nested `<pre>`; strip `align` attributes; move body stylesheets to the head |
| `add_version_requirements` | Version literals on the package pages, before the locale copies are made |
| `fix_tag_pages` | The taxonomy pages ssg emits outside the layouts: CSP, og:image, stylesheet, viewport, icon links and the measurement beacon |
| `fix_social_descriptions`, `fix_double_encoded_meta`, `fix_manifest` | Share-card descriptions aligned with the page, doubled entities undone, the web-app manifest colour |
| `fix_try_strip` | The status strip mirrored onto the demo page |
| `localise_pages`, `gen_try_locales`, `gen_journey_locales` | The 34 locale variants of the home page, the demo and the journey and docs pages, from the translation tables in `scripts/*_i18n/` |
| `relocate_corpus_locales` | The five-locale corpus scenario pages moved under `/<locale>/`, their six-way hreflang cluster, and the paths ssg derived from file names rewritten in feeds, tag pages and the search index |
| `inject_dataset_ld`, `write_llms` | schema.org Dataset markup per scenario page from `scripts/corpus_pages.json`; `llms.txt` and `llms-full.txt` for agents |
| `stamp_suite_version` | "Generated against pain001 X" inside every footer |
| `add_page_photos` | The photo band at the top of every page hero and tag page, AVIF first with WebP as the fallback, from `scripts/page_photos.json` |
| `mark_dated_content`, `retitle_tag_pages`, `defer_ssg_search`, `ensure_social_metadata` | Expired ribbons removed and timeline milestones marked by build date; ssg's tag-page titles rewritten; ssg's search script deferred off the first-paint path; share-card metadata on any page missing it |
| `mark_noindex_pages`, `regen_sitemap`, `gen_legacy_redirects` | The 404 page published at `/404.html` and noindexed with the offline and form-confirmation pages; the sitemap from what was built, without them; redirect stubs for the old localised-brief URLs |
| `taxonomy_language_and_index`, `name_table_regions`, `promote_bold_questions` | Language attributes and an index on the tag pages; an accessible name for each scrollable table region; bold-only question paragraphs promoted to headings |
| `normalise_site_shell` | One CSP on every page, carrying the hash of the theme script it inlines into the head (stored theme and motion choice applied before first paint, with no render-blocking request); taxonomy and redirect pages given the site header, footer and stylesheet |
| `--optimise-assets` | Each layout's stylesheets merged into one SRI-protected bundle, and block comments stripped from the site's own scripts |
| `--stamp-sw` | The legacy redirect map written into `/js/redirect.js` (the script redirects only to those paths), then the service worker's cache name derived from the bytes it caches, run after `static/` and the samples exist |

`build.sh` also runs `scripts/carry_forward_assets.py`, which fetches the
fingerprinted `/_csp/` assets the live pages still reference into the new
build, so cached HTML keeps working through the CDN's ten-minute window. It
fetches only what the live pages reference, so the set stays bounded.

### Gates

CI fails on any of these; run them locally before opening a PR.

| Gate | Command |
| :--- | :--- |
| ssg audit, warnings fail | `ssg audit -f ssg.toml -o site --severity warn --fail-on warn` |
| Unit tests, Node 22 and 24 | `npm test` |
| Dependency advisories, documented exceptions only | `make deps` (`scripts/audit_deps.py`) |
| README conforms to the workspace template | `make lint` (`scripts/validate_readme.py`) |
| Browser engine runs the library | `node tests/engine.integration.mjs` |
| Translation table integrity | `scripts/validate_try_i18n.py`, `scripts/validate_pages_i18n.py pages_i18n`, `… docs_i18n` |
| Translation keys still match the built pages | `scripts/validate_i18n_keys_live.py` |
| Content integrity (no eaten markup, no double encoding) | `scripts/validate_content_integrity.py` |
| Link integrity | `scripts/validate_links.py site` |
| Suite version currency | `scripts/validate_versions.py` |
| Documentation snippets reference the real API | `scripts/validate_snippets.py` (with `pain001` installed) |
| Layout and print integrity, real Chrome | `node scripts/layout_audit.cjs`, `node scripts/print_audit.cjs` |
| Reading measure, real Chrome: no squashed column, title or paragraph, no sideways scroll, every page at four widths | `node scripts/measure_audit.cjs --all` |
| Dated regulatory claims still match their primary sources (weekly, `dated-claims.yml`) | `python3 scripts/check_dated_claims.py` (`scripts/dated_claims.json`) |
| Colour contrast 7:1 for text in both themes and Display P3 | `python3 scripts/validate_contrast.py` |
| Every page in both themes, WAVE-documented rules plus axe AAA | `CONCURRENCY=2 node scripts/audit_site.mjs` |
| Lighthouse 100 in all four categories: mobile, tablet, desktop, 4K and 8K (a performance-only 99 is measured once more; the second sample counts) | `node scripts/perf_budget.mjs http://127.0.0.1:8899` |
| Accessibility, WCAG 2.2 AAA, in system, light and dark modes on 13 key pages | `node scripts/a11y_modes.mjs` |

The browser gates need `site/` served the way CI serves it, with compression
and CDN-like caching: `node scripts/serve_audit.mjs site 8899`. They also need
`puppeteer-core@23` and `@axe-core/puppeteer` in `.a11y-tools/` (see the
Layout step in `ci.yml`).

### Editing content

Edit the Markdown in `_posts/`; keep `title`, `description` and `keywords`
unique per page; run the build and the gates; commit the source only. The
built `site/` is not tracked: CI rebuilds it on every push and deploys it
from `main`, so there is nothing to merge by hand.

Translated pages are produced at post-build from tables keyed by exact
fragments of the built English HTML (`scripts/pages_i18n`, `docs_i18n`,
`try_i18n`, `runtime_i18n`, `locale_strings.py`, `corpus_l10n.py`). A change
to an English sentence on a localised page needs the key re-extracted and the
34 tables migrated, or the live-key gate fails.

Photographs are assigned in `scripts/page_photos.json`: one per English
page and homepage section, never repeated, landscape only. Run
`uv run --with pillow python3 scripts/import_photos.py` after changing it;
it crops each photo, holds every band to a per-width byte budget, writes
AVIF and WebP, removes stale files and regenerates the credits in
`THIRD_PARTY_NOTICES.md`. Unsplash and Pexels photos live in separate
folders so REUSE annotates each under its own licence.

### Measurement and privacy

Page views are counted by Cloudflare Web Analytics from a beacon served from
this origin; the demo page carries none. What is counted, where the tag lives
and how to switch it off is in [`METRICS.md`](METRICS.md). The privacy and
trust pages state the same facts publicly.

## Security

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md),
not in a public issue.

The site uses a restrictive Content-Security-Policy, same-origin vendored
runtime assets, non-networked payment-data processing, CodeQL, dependency
review, Dependabot, OpenSSF Scorecard, signed tags, release attestations, and a
CycloneDX SBOM. Every GitHub Action is pinned by commit SHA, and workflow
tokens are read-only except on the job that needs write scope. Node
dependencies are installed from a committed lockfile and audited in CI.

Input parsing lives in the separately fuzzed and tested core library; this
repository replays browser integration and fixed regression cases on every
push. The browser demo refuses input files larger than 2 MB.

**Framing.** The policy is delivered as a `<meta http-equiv>` element, where
browsers ignore `frame-ancestors`, and GitHub Pages cannot set response
headers. Cloudflare adds them at the edge: every response carries
`Content-Security-Policy: frame-ancestors 'none'` and `X-Frame-Options: DENY`.
That rule lives in the Cloudflare dashboard, not in this repository, so the
headers are the thing to check after any change there. Three more settings
live there: Always Use
HTTPS (SSL/TLS, Edge Certificates); a redirect rule that sends any
`/index.html` URL to its directory URL with a 301, because GitHub Pages serves
both with a 200 and Search Console then lists one as an alternative of the
other; and a page rule on `pain001.com/*` that caches everything at the edge
with a two-minute browser TTL and no edge TTL override, so the edge follows
the origin's ten-minute `max-age`. Until 23 September 2026 that rule pinned
the edge TTL to seven days, which kept every deploy invisible for up to a
week; a deploy that does not appear within ten minutes means the rule has
regained an edge TTL. GitHub Pages itself redirects `www` to the apex and
slash-less paths to the trailing slash. The site holds no credentials, session
state or authenticated actions.

## Documentation

- [User manual and compliance hub](https://pain001.com/documentation/)
- [Library API reference](https://docs.pain001.com/)
- [Developer documentation](DEVELOPMENT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Pain001 ecosystem map](docs/ECOSYSTEM.md)
- [Release process](docs/RELEASES.md)
- [Architecture decision records](docs/adr/)
- [Migration guides](docs/migrations/)

## Stability guarantees

The website follows SemVer from v0.0.1. During the `0.x` series, a patch
release may change content, design, generated markup, browser storage, and
build tooling, but published URLs are preserved or redirected. A change to
the validator's interpreted input or generated output is treated as breaking
and belongs to the library's own version contract. Deprecated website URLs
remain redirected for at least two patch releases. Tags and release assets
are immutable.

## License

Project-authored work is dual-licensed under Apache-2.0 or MIT, at your option.
See `LICENSE-APACHE`, `LICENSE-MIT`, `REUSE.toml`, and
`THIRD_PARTY_NOTICES.md` for vendored components.

[00]: https://shokunin.one "Shokunin Static Site Generator (SSG)"
