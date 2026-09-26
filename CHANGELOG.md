# Changelog

All notable changes to this website are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Property-based fuzzing of the demo's input handling: eight fast-check
  properties run with the unit tests on every push, covering the CSV
  splitter and parser, the delimiter sniffer, the error-report writer,
  byte decoding and message templates.
- A release backfill workflow. It gives an existing signed tag the
  archive, SBOM, checksums and attestations a release carries, keeps the
  assets a release already has, and never touches the tag.
- `scripts/release_notes.py` composes every release page in one format:
  title `pain001.com X.Y.Z`, hand-written Highlights from
  `docs/releases/`, GitHub's generated What's Changed and New
  Contributors, the checksums and the Full Changelog link. CI and
  `make lint` check the Highlights files.

### Changed

- The site is regenerated for pain001 0.0.71, and the browser demo runs
  the 0.0.71 wheel.
- The demo's WebAssembly runtime is no longer committed. `build.sh`
  downloads each of its 18 binaries from the Pyodide CDN or PyPI and
  refuses any file whose SHA-256 differs from
  `static/pyodide/pain001-runtime.json`.
- Every dependency the workflows install is pinned: Python tools by hash
  from `requirements/`, the browser-audit tools from a committed
  lockfile, and a new library release by the digest PyPI publishes for
  it. The audit tools move to puppeteer-core 25.12.0 and axe-core 4.13.0.
- Release notes in `docs/releases/` hold the Highlights only.
- Roadmap: Phase C, the declarative rule engine, is deferred. The library
  already has 23 of its 29 profiles as data and a shipped declarative
  overlay grammar, and issue #184 proposes a CEL policy language, so
  building Phase C as planned would add a fourth rule format. Its first
  step is now an ADR in the library choosing one format; it reopens once
  the library's v0.0.71 release has landed and profile maintenance can
  be staffed beyond one person.

### Fixed

- Scorecard's Fuzzing check still scored 0 after the property tests
  landed: it looks for fast-check only in `*.js` and `*.ts` files, and
  the tests were `.mjs`. They are now a CommonJS `.js` file, and
  `npm test` runs both kinds.
- The regenerate workflow reads PyPI's wheel digest in Python instead
  of piping `curl` into `python`, which Scorecard reported as an
  unpinned download-then-run.
- The version stamper now updates the translation tables too. The
  documentation page's English key quotes the library version, so the
  0.0.71 regeneration failed its live-key gate, and 35 locales still
  described pain001 v0.0.56 in that page's metadata.

## [0.0.8] - 2026-09-25

### Added

- The demo's downloadable error report carries the same layers as the
  on-screen summary. It opens with one row per layer (ISO 20022 schema,
  data quality, scheme rulebook, your bank's profile, channel and
  eligibility) stating what that layer concluded, in the visitor's own
  language, including the two layers Pain001 never evaluates; every
  finding then names its layer. Before, the report was a flat list with
  no layer and no record of what was not checked.

### Fixed

- The explainer under the demo said the scheme rulebooks were CLI-only
  and that the demo implemented only the "fail-fast" layer. The demo runs
  the pain001 library itself, including the scheme rulebook you choose and
  the XSD gate; the text now says so, lists what the CLI adds (any file
  size, Excel, SQLite, JSON, Parquet and MT101 input, all 29 scheme
  profiles where the demo offers 16, `--explain`, every edition), and is
  retranslated in all 34 languages.
- Seven demo status strings had never been translated in any of the 34
  languages, including the scheme verdicts ("Passed {scheme}", "{n}
  violation(s) against {scheme}") that the layer summary and the report
  show; a French visitor saw them in English. All seven are translated.
  Finding messages remain in English: the pain001 library emits them.
- Every page's footer credit reads "Built with the Static Site Generator
  (ssg)" and links its documentation, in place of "Built with SSG" and
  static-site-generator.com.
- The local audit server (`scripts/serve_audit.mjs`) served `.wasm` as
  `application/octet-stream`, so the demo's Python runtime never compiled
  under it and every browser audit of `/try/` saw only the page before
  validation. It now sends the content types GitHub Pages sends.

## [0.0.7] - 2026-09-25

### Fixed

- The README, architecture and packaging docs, pull-request template and
  build comments name the generator as the Static Site Generator (ssg) and
  link its documentation at <https://docs.static-site-generator.com/ssg/>.
- The build-toolchain page moves from `/made-with-shokunin/` to
  `/made-with-ssg/` and names the Static Site Generator (ssg); the old URL
  redirects. Its text also said the only client-side script was theme
  and navigation; it now lists search, the page-view beacon and the
  WebAssembly demo as well.
- README: the logo pointed at an external host that now returns 404; it
  uses the site's own logo. The screenshot showed the pre-redesign theme;
  it is now a light and dark pair captured from the live homepage and
  published with the site (`static/img/readme/`), and the old image is
  removed. Every README image is an absolute pain001.com URL, so it also
  renders where the README is shown outside GitHub. Claims
  corrected against the repository: the Lighthouse gate (13 routes, five
  profiles, timing metrics gated through the performance score, not
  five routes with timing ungated), the JSON-LD types actually emitted,
  agent files (`agents.txt` and an MCP descriptor were listed and do not
  exist), the Python floor CI runs (3.12, not 3.10), the seven workflows,
  the full build order and post-build passes, one local serving command,
  and framing, which Cloudflare already restricts at the edge.

### Removed

- pa11y-ci, and with it the only open Dependabot alerts: two high
  advisories in `extract-zip`, reached through pa11y-ci's bundled
  puppeteer, with no patched release. pa11y scanned 19 sampled pages; the
  site-wide scan (WAVE's rules plus axe AAA on every page, light and dark)
  already covered all of them, and the audit-exception list is now empty.
  The accessibility statement, trust page, audit brief and outreach text
  now name the scan that runs; the statement had also still said twelve
  pages where the list held nineteen.

## [0.0.6] - 2026-09-24

### Changed

- PRISM redesigned for institutional buyers. One typeface (Inter, self-hosted,
  OFL-1.1) replaces the serif display face and the system UI stack; a
  cobalt-on-warm-grey palette of its own (cobalt #1f3db0 links and
  actions, periwinkle #a8b8ff in dark mode, energy orange kept for dated
  signals; no teal or mint, so nothing reads as another network's brand),
  every text pair at 7:1 in both themes and in Display P3; distinct light and dark themes (the header, hero and developer band
  were navy in both); hairline cells, figures and columns in place of
  tinted cards and gradient icon tiles.
- Homepage: positioning around deterministic, air-gapped, auditable
  validation; primary action "Book an architecture briefing"; the hero shows
  three recorded CLI runs (clean, SEPA IBAN error, CBPR+ address and UETR
  findings), captured with all network access denied, behind accessible
  tabs; a proof band of figures counted from the corpus and specifications.
- Header reduced to four sections, a ⌘K search field and one action;
  language and theme controls moved to the footer. "Ecosystem" is now
  "Products" and "Research" is "Insights".
- Enterprise hero carries the reviewer's own verification: release download,
  SHA256SUMS check and `gh attestation verify`, each run against the
  published release.
- Skeletonic CSS retired. It sat under PRISM with a second container width,
  element margins and a 700 bold that the theme no longer ships.
- Regulatory timeline (DORA 17 Jan 2025, MT–MX end 22 Nov 2025, CBPR+
  structured addresses 14 Nov 2026, the roadmap to 2028) with what Pain001
  does about each date, and an executive-briefing card, in place of the
  closing prose. Enterprise gains a risk-review table whose answers are
  limited to how the software works and what the page offers.
- Material depth: an 8% hairline and a two-layer shadow on the lifted
  panels, a soft light behind the hero panel, and a light code window in
  the light theme.
- The comparison page is a vendor evaluation: a category matrix with
  Pain001 in a highlighted column, project and platform cards, both sides
  of the ledger, four decision paths, an FAQ accordion and a sticky
  in-page navigation that marks the current section.
- Article tables use the full content width and hairline rows.
- Homepage rebuilt in the product-page pattern: centred heads at a larger
  type scale, a dated ribbon, a segmented
  scenario switch, a figures band with a footnote, review tiles, the four
  validation layers in a dark band, a pipeline
  gallery, a packages bento with a real Python example and its real
  output, copyable install commands, a specs strip and a dated timeline.
- Articles get a sticky contents rail from 72rem that marks the current
  section, and a quieter save control; `/try/` uses the shared page hero.
- The homepage opens on a full-width photograph of the City of London with
  the headline on a solid card over its lower edge; every other page,
  including tag pages, opens on a photo band of its own: 149 pages and six
  homepage sections, no photograph used twice, chosen for the page (the
  country of each corpus scenario, London landmarks for the message
  versions). `scripts/page_photos.json` is the single map; translations
  share their English page's photo. Bands keep one 2:1 shape inside the
  content column at every screen size (the homepage banner 21:9 in a
  wider column), so a phone and an 8K screen see the same framing; only
  landscape photos are used, cropped where the detail is, at
  640/768/960/1280/1600px, AVIF first with WebP as the fallback. A band is
  its page's largest paint, so each AVIF is held to a byte budget per
  width (the importer steps quality down until it fits). Text never sits
  on a photograph.
- ssg's search script is deferred instead of blocking first paint, and
  the /try/ upload area takes its accessible name from its visible text
  (it previously announced different wording, WCAG 2.5.3).
- Copy in every language drops the em dash: each sentence was rewritten
  with the punctuation a native editor would use (commas, colons, full
  stops, parentheses; full-width marks in Chinese and Japanese, the
  Arabic comma in Arabic and Persian). Generated pages were fixed in
  their generators (message specifications, corpus scenarios) and
  regenerated; translation tables were re-keyed to the new English.
- Photography on the homepage review tiles, the regulated-teams section,
  the executive briefing and the enterprise page: Unsplash and Pexels
  photographs, each under its own licence file and REUSE annotation,
  copied into the site (never hotlinked, so the same-origin CSP holds),
  cropped and re-encoded by `scripts/import_photos.py` at 480/800/1200px
  (the homepage banner also at 1600/2400px), decorative and size-reserved;
  banners load eagerly, everything below the fold lazily. Credits in
  THIRD_PARTY_NOTICES.md.
- Homepage-only behaviour moved to `/js/home.js`; the site scripts ship
  without block comments, keeping the translated /try/ pages under ssg's
  50 KB script budget.
- A footer "Reduce motion" control (WCAG 2.3.3), stored on the device;
  motion is transform-only so no text is ever sampled mid-fade.
- Tag pages carry the site header, fonts and palette; `/tags/` lists the
  topics; tag-list links declare the language of the page they name.
- The published stylesheet bundle is minified (`scripts/css_minify.py`,
  comments and whitespace only, doctested): 111 KiB to 81 KiB on the
  homepage.

### Fixed

- The first deploy of this release was invisible: a Cloudflare page rule
  cached every page at the edge for seven days, so the live site kept
  serving a four-day-old copy after a successful deploy. The edge TTL
  override is removed (the edge now follows the origin's ten-minute
  `max-age`) and the cache was purged; the README records the rule.
- The element and type reference pages (up to 1,600 elements, five wide
  tables) lost the last Lighthouse point on a busy runner to layout work
  that landed after first paint. The gate now measures a performance-only
  99 a second time, as Lighthouse recommends, so runner load cannot block
  a deploy while a real regression still fails twice. (Skipping layout of
  off-screen tables was tried and reverted: links inside them then have no
  size and fail the touch-target audit.)
- The tag pages laid out their 386 entries with CSS columns; balancing
  them was a 270ms layout task on a tablet, and on a loaded CI runner
  enough of it landed after first paint to score 99 and block the first
  deploy of this release. The list is a grid now, and entries below the
  fold are not laid out until scrolled to.
- Deadline content corrected site-wide, in all 35 languages: on 27 August
  2026 Swift deferred every payments change in Standards Release 2026,
  including the 14 November 2026 rule against unstructured postal
  addresses and the interbank MT101 move to pain.001, with new timing due
  by December 2026. The ribbon, homepage timeline, business pages, FAQs,
  glossary, roadmap and the 2026 briefing now say so, cite Swift and the
  Federal Reserve (Fedwire's November 2026 release moved to November
  2027), and keep the dates that stand (12 June 2027, November 2027,
  November 2028). The 2026 briefing was re-checked against primary
  sources on 23 September 2026, correcting the ISO 20022 share (more
  than 98%), MT category 9 (statements run to 2028), BOJ-NET, FedNow and
  Aani figures, the TIPS date, the ACI forecast, and an unsupported claim
  about MCP servers.
- `/security.txt` was published empty and `/.well-known/security.txt`
  returned 404: the generator wrote an empty file, the `.well-known` copy was
  made before the real file arrived, and the Pages upload excluded
  dot-directories. A real RFC 9116 file now ships at both paths.
- The homepage terminal showed `pain001 validate payments.csv` and
  `generate --type … --output …`, which pain001 0.0.70 rejects; the commands
  now use `-d`, `-t` and `-o`.
- Wide-gamut (Display P3) screens were repainted in the retired accent
  colour by a stale P3 block.
- Header and footer navigation, panel descriptions and footer lines were in
  English on all 34 locale pages; they are now translated.
- The fonts' REUSE annotation named files that did not exist.
- "2 min read·Last reviewed" lost its space to a CSS escape terminator.
- The article contents box set its label at full H2 size.
- The article contents rail overlapped wide tables; rail pages now use a
  two-column grid, and the site audit fails any overlap with the rail.
- The hero's decorative glow widened the homepage past the viewport, and
  long type names widened the tag pages at 320px.
- The header's Products link pointed to a homepage anchor that no longer
  existed, on every page.
- Tables squeezed columns to one or two characters ("Proje / ct"):
  `overflow-wrap: anywhere` on cells lowered their minimum width, and the
  wrapper meant to let wide tables leave the reading measure had no CSS.
- Stale capability counts: the comparison said ten `pain.001` versions
  (.03–.12) and the reference said `versions` lists 11 definitions;
  pain001 0.0.70 supports eleven `pain.001` versions and two `pain.008`.
- `--type-body` pointed at a `--font-body` token that never existed, so
  tag pages and parts of the demo rendered in the browser's serif.
- On translated docs pages the language menu's "English" entry pointed
  back to the translated page.
- Legacy redirect stubs used a meta refresh (a WAVE error); they now
  redirect with a same-origin script and keep the visible link. The
  script carries the retired-path map itself (stamped at build time)
  rather than reading a destination from the page, so it can only
  ever send a visitor to one of those paths.
- The theme script (stored theme and motion choice, applied before
  first paint) was a render-blocking request on every page; it is now
  inlined in the head under a CSP hash. Lighthouse had put a third of
  the mobile first paint on that request and scored 99 on the tablet
  and locale home pages.
- Search Console coverage: `/404/` was served with a 200 and indexable (a
  soft 404) and GitHub Pages never showed it for a missing URL; it is now
  published as `/404.html` and, with the offline fallback and the form
  confirmation page, carries robots noindex and stays out of the sitemap.
  A Cloudflare redirect rule (set on 23 September 2026, documented in the
  README) sends any `/index.html` URL to its directory URL with a 301.
- The 252 "Open this scenario in the demo" links used `/try/?sample=…`,
  which made every scenario a separate URL to a crawler: Search Console
  listed 41 of them as alternates of `/try/`. They now use a fragment,
  `/try/#sample=…`, which the demo reads first (the query form still
  works), and the link validator knows the fragment is a parameter.
- Reference pages read as a squashed left column: the contents rail was
  only built from four sections, so a three-section page had a 68ch column
  and nothing beside it, and titles at the display step wrapped three to
  six lines. The rail now starts at two sections and is 18rem wide, article
  titles are one step smaller and span the container, and table columns
  have a 9rem floor so a wide table scrolls instead of crushing a column
  beside an unbreakable file name.
- The 34 type-reference pages carried the span of type names in their
  title (up to 120 characters, three lines on a laptop); the span stays in
  the subtitle and description, and the headline ratchet drops from 292 to
  258 over-long H1s.
- ssg's search widget (button, dialog, placeholder and the Esc, arrow and
  Enter hints) read "Search" in English on every translated page; it now
  follows the locale string table.
- Two enterprise sentences on the Why and Executive brief pages were English
  in all 34 translations; the executive-brief eyebrow and title in six
  languages, and a handful of table headers and labels, were untranslated.
- `build.sh` takes a lock so two builds cannot run in the same tree, and
  retries the staging clean-up once. ssg itself joins every thread before it
  exits, so the transient "Directory not empty" seen once could only have
  been a second writer in the tree.
- The photo band at the top of a page is capped at 24rem tall from 64rem,
  so on a laptop the headline no longer starts below the fold.
- French pages fetched 36 KB of the latin-ext Inter subset for the
  single "œ" in "cœur": both subsets declared U+0153 and the later
  declaration wins. The ext faces are now declared first, so the
  glyph comes from the preloaded latin subset.
- 653 bold-only paragraphs (FAQ questions) are now real headings.
- Identical "Table, scrollable horizontally" regions on translated docs
  pages are named after their section, so landmarks are unique.
- The demo's XML panel read an undefined `--code-text` and inherited the
  page ink instead of the code-window colour.

### Added

- `scripts/check_dated_claims.py` and `dated-claims.yml`: the dated regulatory
  claims the pitch depends on (Swift's Standards Release 2026 deferral and its
  promised December update, the Fedwire release moved to November 2027, the
  CHAPS purpose-code mandate) are listed in `scripts/dated_claims.json` with
  the sentence each source must still contain and a review date. A weekly run
  fails the moment a source changes or a review date passes. swift.com refuses
  non-browser clients, so it is read through the Internet Archive after asking
  it for a fresh capture.
- `scripts/measure_audit.cjs`: every page at phone, tablet, laptop and desktop
  widths in real Chrome, failing on a reading column under 55% of its
  container, a title over three lines, a paragraph narrower than a phone, or
  a page that scrolls sideways. The layout audit caught cropping; nothing
  caught the opposite, and the reference pages shipped with the body on 60%
  of the container and titles on three to six lines.
- `scripts/validate_contrast.py`: every token pair, both schemes and both
  gamuts, at 7:1 for text and 3:1 for borders and focus; the two dark blocks
  must agree.
- `scripts/validate_proof.py`: each homepage figure must equal its source.
- `scripts/validate_security_txt.py`: both copies present, identical, with
  Contact, a single Expires within a year, and Canonical.
- `scripts/validate_headings.py` now decodes entities before counting.
- `scripts/audit_site.mjs`: every built page, WAVE's documented error and
  alert rules plus the full axe rule set, light and dark; in CI.
- The Lighthouse gate covers 13 routes (every layout, both text
  directions) on mobile, tablet, desktop, 4K and 8K; the layout audit
  adds 4K and 8K viewports.

## [0.0.5] - 2026-09-22

### Fixed

- Release publishing, second cause. With the SBOM path fixed in 0.0.4, the
  attestation then failed with "Unsupported SBOM format". GitHub's
  attestation action recognises CycloneDX by `bomFormat && serialNumber &&
  specVersion`, and ssg's SBOM omits the optional `serialNumber`, so the
  release still did not publish. `scripts/sbom_serial.py` now adds a derived
  UUIDv5 serial during the build, stable across rebuilds of a version so it
  adds no nondeterminism of its own. The generator should emit the field
  itself; this keeps releases publishable until that lands.

## [0.0.4] - 2026-09-22

### Fixed

- Release publishing. The v0.0.3 release workflow failed at the SBOM
  attestation with "SBOM file not found" and skipped publishing, because
  `actions/attest-sbom` expands globs in `subject-path` but not in
  `sbom-path`. Both paths are now spelled out from an exported
  `RELEASE_VERSION`, so the archive, checksums, SBOM and attestations reach
  the release.

## [0.0.3] - 2026-09-21

### Added

- PRISM visual system with Skeletonic CSS v3.0.0, an AAA-gated three-state
  system/light/dark control, proportional heading rhythm, and a consistent
  linked footer credit on every generated page.
- Local page bookmarks, compliance and implementation toolkit, current
  standards-source map, implementation checklist, audit-evidence template,
  migration and community routes addressing issue #1.
- Repository governance, development, architecture, ADR, migration, release,
  support, security, citation, signing-key, REUSE, editor, pre-commit,
  devcontainer, issue-template, and pull-request-template documentation.
- Tag-triggered release pipeline with site archive, checksums, CycloneDX SBOM,
  build provenance and SBOM attestations; 100% line, branch, and function
  coverage enforced for browser input handling.

### Changed

- Shokunin SSG upgraded from 0.0.47 to 0.0.63 in local instructions and every
  workflow; strict YAML front matter is now accepted by the current compiler.
- GitHub Actions dependencies updated to their current pinned releases.

### Fixed

- All social-handle front-matter values are explicitly quoted for strict YAML
  parsing. Contact pages now have the same footer contract as every other
  page.

### Changed

- The built site is no longer committed: `ci.yml` deploys `docs/` to GitHub
  Pages from the run that passed every gate, the previous deploy's
  fingerprinted assets are fetched from the live site instead of copied
  from the tree, and the `docs/` merge conflicts are gone. CodeQL over the
  first-party JavaScript and the Python scripts.
- Site hygiene: icon links on the taxonomy pages, which had answered every
  visit with a 404 for `/favicon.ico`; lower layout cost on the corpus index;
  this README rewritten around the pipeline and the gates; this changelog.
- MT101 migration page (`/mt101-migration/`) and Excel on-ramp page
  (`/excel-to-pain001/`); the MT101 reference page's stale version and date
  wording fixed; the version gate now matches one-digit patch numbers (#20).
- Every GitHub Action pinned by commit SHA, Dependabot keeps the pins (#19).
- Measurement moved to Cloudflare Web Analytics with the beacon vendored and
  served from this origin; not on the demo page; first-party GoatCounter code
  removed; privacy and trust pages restated (#18).
- Single `SSG_VERSION` pin in CI and a relative library path for the
  message-spec extractor (#7).

### Added

- W7: the 42 corpus scenario pages in de, fr, es, it and nl with a six-way
  hreflang cluster (#17).
- W6 and W8: Lighthouse budgets in CI, release-triggered regeneration
  workflow, footer suite-version stamp (#16).
- W5: enterprise page, trust-centre artefacts, three copy changes on the
  governance, why and executive-brief pages (#15).
- W4: corpus index JSON, twin JSON Schemas, `llms.txt` for agents, paste-ready
  MCP configuration blocks (#14).
- W3: one page per corpus scenario with Dataset JSON-LD (#13).
- W2: the browser demo runs the pain001 library itself in Pyodide, with a
  corpus selector and the JSON twin tab (#12).
- W1: first-party, cookieless measurement of five interactions (#11);
  superseded on 2026-09-18.
- W0: current suite versions everywhere, the Swift Standards Release 2026
  wording with its source, logo alt text, the version gate (#9).
- Example-corpus page with downloadable pain.001 and pain.008 files (#8).

### Fixed

- Licence: ship Apache-2.0 OR MIT and restore `LICENSE` as the pointer to the
  dual grant (#5, #6).

## [0.0.2] - 2026-07-26

### Added

- Editorial redesign, research-backed content, and repaired
  build pipeline (#2); copyright byline linked, layout and print regressions
  gated in CI (#3); roadmap re-ordered by what unblocks the most (#4).

## [0.0.1] - 2023-06-16

### Added

- Initial public Pain001 documentation website, generated by SSG and deployed
  through GitHub Pages.

[Unreleased]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.8...HEAD
[0.0.8]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/sebastienrousseau/pain001.github.io/releases/tag/v0.0.1
