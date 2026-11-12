# Changelog

All notable changes to this website are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- The events Worker takes Content Security Policy violation reports at
  `pain001.com/e/csp` (`workers/events/src/csp.js`), so the policy can
  run as `Content-Security-Policy-Report-Only` for a week before it is
  enforced. Each report keeps only the directive, the page path, the
  blocked item's origin and the country; the privacy page and
  `docs/ARCHITECTURE.md` say so.

### Changed

- Suite Consistency no longer runs on another workflow's completion
  (`workflow_run`). It audits the family daily and on dispatch, as the
  core's does, since that trigger runs with the default branch's trust
  whatever started it. Regenerated from pain001's
  `scripts/render_ecosystem_workflows.py`.
- The site rebuilds and redeploys from main every Monday (CI `schedule`),
  so the traction figures on the governance page, fetched at build time,
  are never more than a week old; the page says so. IndexNow is not
  pinged for the weekly run. ADR 0002 gains an amendments note: the
  events Worker is deployed and `discussion_click` was dropped.

### Fixed

- Suite Consistency pins the core's ecosystem check at `febcd0a`, which
  accepts the five pain001 SDK repositories as known members not yet
  released. From the 0.0.86 release until this change every scheduled
  run failed on them as undeclared repositories.
- `docs/assurance-case.md` and `docs/ARCHITECTURE.md` described the site as having no server-side code, though the `pain001-events` Cloudflare Worker serves `pain001.com/e`. Both now describe what it receives, how it validates and caps input, what it stores in Workers Analytics Engine and for how long, and how it is tested and deployed. `docs/ARCHITECTURE.md` also no longer says Cloudflare measurement is excluded from the demo, and `METRICS.md` drops `discussion_click`, an event neither the site nor the Worker accepts, and the note that the Worker was not yet deployed.

## [0.0.86] - 2026-11-11

### Fixed

- `make deps` can now except an npm advisory that has no GHSA id. Exception ids were upper-cased and finding ids (`npm:<source>`) were not, so such an exception never matched and was reported as stale.
- A bold-only paragraph promoted to a heading now takes its level from the nearest authored heading. A short authored heading directly before an already promoted one was mistaken for a promoted heading, because the check read 40 characters past its start, and the new heading came out a level too high.
- Validate documentation snippets against the released core 0.0.85 instead of 0.0.70. The release version gate now rejects runtime or snippet input/lock pins that differ from `VERSION`.
- Record in the maintainer handover note that the Cloudflare 301 from `/enterprise/` to `/for-banks/` is live and how it was checked; `/thanks/` still has no rule.

### Changed

- Release 0.0.86 in lockstep with the pain001 suite. Pin the browser runtime and the documentation snippet environment to the published core 0.0.86 wheel, regenerate the corpus pages, versioned downloads, demo samples and translations from the `v0.0.86` tag, and pin the ecosystem check to the 0.0.86 release commit.
- Raise the coverage floors to 100%: lines, branches and functions of the shipped JavaScript (was 90% of lines and 80% of branches), and lines and branches of every Python script in `scripts/` (was unmeasured, at 31%). `make test` and CI enforce both; `.coveragerc` holds the Python floor.
- Remove three branches no input can reach: the empty-phase return in the demo's layer summary, an always-empty `missing` list in `extract_try_i18n.py`, and an always-true duplicate check in `generate_corpus_page.py`. Output is unchanged.
- Hold every Python function in `scripts/` and `tests/python/` to the workspace complexity ceilings with `scripts/check_complexity.py` (radon and complexipy, hash-pinned in `requirements/test.txt`), run by `make check` and CI. The 44 functions and 3 files already over a ceiling are recorded in `complexity-baseline.json`, which may only shrink. `promote_bold_questions` is split into two helpers and is no longer an offender.
- Add `make check` as the workspace name for the full local gate; the dev container now installs the Node toolchain and the linters and boots to a working `make check`. `DEVELOPMENT.md` documents the test layout, every CI gate's local command and the release model.
- Bring `README.md` closer to the workspace template: badge style, the screenshot in the demo position, section separators, the ecosystem, capability and benchmark tables in the template's columns, and the Development and Security closings.

### Documentation

- Add `docs/cloudflare-audit.md`, a read-only audit of the pain001.com zone against the workspace Cloudflare standard from public checks, with six deviations and their evidence. No Cloudflare setting was changed.
- Correct the README's Security section: no response carries a `Content-Security-Policy` header and HTML is not cached at the edge, contrary to what it said.

## [0.0.85] - 2026-11-10

### Fixed

- Preload each responsive hero image from the photo map, and encode the oversized tablet demo hero within its existing byte budget.
- Retry transient PyPI connection resets twice with bounded delays; permanent errors and exhausted retries still fail the version-currency gate.
- Stop tracking a `node_modules` symlink that the 0.0.85 regeneration committed by mistake; it made the REUSE check fail. `.gitignore` now ignores `node_modules` as a link too, and a test rejects any tracked symlink.

### Changed

- Release the website with pain001 0.0.85. Pin the browser runtime to the published core wheel, regenerate the corpus pages, versioned downloads, demo samples and translations from the `v0.0.85` tag, and pin the ecosystem check to the 0.0.85 release commit.
- Replace the enterprise page with `/for-banks/`, a self-service evidence page for bank reviewers: the evidence pack, the published maintenance policy, a guide to building a bank profile in-house, open integration recipes, and the three questions a review asks. There is no paid tier, no briefing and no enquiry form; `/enterprise/` and `/thanks/` become redirect stubs (decision D2).
- Navigation is Try it, Developers, Docs, For banks and Insights, with a "Try it free" button; the footer states that Pain001 is an independent project maintained in a personal capacity and links the governance page (decisions D0 and D3).
- The homepage leads bank reviewers to the evidence pack, adds the two paths (building an integration, evaluating for an organisation), and points the bank-profile layer at the new guide (decision D3).
- The privacy page, `METRICS.md` and the demo's "Verify it yourself" panel (in all 34 locales) describe the page-view and event counts. The demo said it ran no analytics script while the layout already loaded the page-view beacon there; it now names every request it makes.
- The demo and event scripts lose their block comments at build, keeping the translated `/try/` pages inside the 50 KB script budget.
- Questions and the maintainer route point to GitHub issues instead of GitHub Discussions, which are not enabled, and `/for-banks/` states that there is no long-term-support line at present (fixes ship in the next release).
- Remove every remaining paid offer from the why, executive-brief, Excel, MT101, governance and comparison pages (and the why and executive-brief translations in all 34 locales), from llms.txt, and an employer's name from a stylesheet comment (decision D0).

### Added

- The governance page states how decisions are made (pull requests, ADRs, DCO), the release process, how to become a maintainer, and a bus-factor plan that marks the key, domain and ownership items as not yet arranged (decision D6).
- `/developers/`, `/developers/ci/` (the GitHub Action) and `/docs/bank-profiles/`; nested routes are moved into place after the ssg build.
- First-party, cookie-free event counts (`static/js/pain001-events.js`) for the eleven events of decision D1 (a Discussions click is not counted, since Discussions are off), sent to `/e` on this origin with the event name, page path and at most a short label; nothing is sent locally or under Do Not Track or Global Privacy Control. ADR 0002 records that Cloudflare Web Analytics plus Workers Analytics Engine supersede Umami.
- A claims register, `data/claims.yml` (decision D5): each figure the homepage shows has its evidence URL and the release it was verified for. `scripts/claims.py` refreshes the live figures before the build, postbuild writes them into the page, and `scripts/validate_claims.py` fails the build when a shown figure differs from the register or an entry was not verified for the current release. The homepage gains a proof strip (GitHub stars, PyPI downloads a month, OpenSSF Scorecard, releases since 2023, branch coverage, signed releases with provenance) and a "Tell us how you use it" link to the core's adoption issue form; the "34 languages" figure becomes PyPI downloads a month. No testimonial or name is shown.
- Twenty-six indexed languages (decision D4): English (also x-default), French, German, Dutch, Spanish and Italian, plus the twenty locales with at least 100 Search Console impressions in the last 3 months on 10 November 2026 (Polish, Swedish, Japanese, Russian, Korean, Traditional and Simplified Chinese, Yoruba, Malay, Czech, Turkish, Brazilian Portuguese, Persian, Arabic, Thai, Hungarian, Vietnamese, Indonesian, Hebrew and Greek). The other 9 locales (Ukrainian, Bengali, Hindi, Romanian, Hausa, Tamil, Telugu, Marathi, and Filipino with none) stay live but are noindex, follow, with no hreflang or canonical link, out of the sitemap and off the tag pages; the language menu lists the first six and "More languages". `INDEXED_LOCALES` in `scripts/postbuild_fix.py` is the one list to extend. `scripts/validate_locale_index.py` fails the build when an indexed page links to, or lists as an alternate, an unindexed locale (except `/languages/`). `/ar/` is indexed, so the Lighthouse SEO budget no longer skips its is-crawlable audit.
- `scripts/validate_no_commercial.py`, run in `make test` and CI: the build fails on a retired paid phrase, a funding-platform link, a link to `/enterprise/` or `/thanks/`, or an employer's name.

## [0.0.84] - 2026-11-09

### Added

- Audit all nine pain001 repositories and their publication channels daily, after release workflows and after the main deployment completes. Use the shared read-only checker pinned to a core commit and retain its JSON evidence.

### Fixed

- Export regenerated website sources as a checksummed review patch. Keep repository permissions read-only and apply updates through the approved suite iteration instead of creating and force-pushing a separate bot branch.
- A manual run of CI on `main` now deploys to GitHub Pages, as a push
  does. On 2026-11-09 GitHub's Actions outage dropped the deploy job
  from the 0.0.83 merge run, which then could not be retried.
- The homepage's "Five focused packages" heading is counted from the
  package tiles at build time, so it cannot drift from them. Five is
  right: the sixth tile is the example corpus, not a package.
- The homepage and the 34 locale homepages declare `og:type` `website`;
  ssg wrote `article` on every page whatever the front matter said.
- The homepage's structured data names Pain001 as free software
  (`SoftwareApplication`, version from the release the site is built
  from, price 0) published by an `Organization` founded by the
  maintainer's Person entity on sebastienrousseau.com.
  `scripts/validate_jsonld.py` checks every JSON-LD block on the site
  parses and that the homepage graph stays current.
- `robots.txt` allows every public page and names the AI crawlers
  (GPTBot, ClaudeBot, PerplexityBot, Google-Extended and others)
  explicitly, with the sitemap link kept.
- Each sitemap URL's `lastmod` is the last commit to the page's
  sources (its post, layout and locale table) instead of the build
  date stamped on all 493 URLs at every deploy. CI's build job now
  checks out full history for it.
- The sitemap lists the homepage. It never had: the filter that skips
  dot-directories also matched the homepage's own path, `.`.
- `llms.txt` no longer says the MCP server has 21 tools (0.0.83 ships
  30); it links the MCP page instead of a hand-typed count.
- `/try/#sample=sepa-sct` (and any built-in sample key) opens that
  sample and validates it; only corpus scenarios could be linked before.
- The homepage hero leads with the sandbox: "Catch pain.001 errors
  before your bank does", a "Validate a sample file for free" button
  that opens the SEPA sample already validated, "No sign-up · runs in
  your browser · nothing is uploaded", a copyable `pip install
  pain001`, and "Evaluating for a bank? Book a briefing" as a text
  link. The documentation link leaves the hero (it stays in the
  navigation), and the demo section's link reads "Try it with your own
  CSV".

### Changed

- Release the website with pain001 0.0.84. Pin the browser runtime to the published core wheel and regenerate the corpus pages, versioned downloads, demo samples and translations from the merged core release.

## [0.0.83] - 2026-11-09

### Changed

- Regenerate corpus pages, versioned downloads, demo samples and the pinned
  browser wheel from the published pain001 0.0.83 release. The generated
  files are the same as for 0.0.82 apart from the version they name.
- Document the core's 0.0.83 signing work on the reference, installation
  and compatibility pages: `pain001 verify-signature` against the signer's
  certificate, `verify_signature` and its `SignatureReport`,
  `--xml-sign-alg` with RSA-PSS and ECDSA on P-256 and P-384, the `sign`
  extra (`cryptography` and `lxml`), and the deprecation of
  `verify_xml_signature` without a key, which pain001 0.0.84 refuses.

### Fixed

- The reference's subcommand table now lists `pain001 check`, which the
  core has shipped since 0.0.82.
- The CHANGELOG's 0.0.82 link compared v0.0.14 with v0.0.15; it now
  compares v0.0.14 with v0.0.82.

## [0.0.82] - 2026-11-09

### Changed

- Join the pain001 suite at 0.0.82 by explicit maintainer decision, replacing
  the website's independent 0.0.14 release line. Existing tags remain intact;
  subsequent website releases advance with the suite one step at a time.
- Regenerate corpus pages, versioned downloads, demo samples and the pinned
  browser wheel from the published pain001 0.0.82 release.
- Integrate the pending CodeQL action updates on the suite release branch.
- Pin markdownlint-cli2 in the npm lockfile so local `make verify` and CI
  use the same installed linter.

- Built with ssg 0.0.75, the latest release, up from 0.0.74. Every
  workflow's `SSG_VERSION`, the devcontainer and the setup docs name
  0.0.75, and the pages' `generator` metadata, which still named
  0.0.72, now names 0.0.75. `AGENTS.md` points at the `SSG_VERSION`
  pin instead of repeating the number.

### Added

- Message specifications for `pain.008.001.08`, which pain001 has
  generated since 0.0.67: the element reference, its type pages, its
  code lists and the `pain.008.001.02` to `.08` changes, produced by
  `scripts/extract_message_specs.py` and
  `scripts/generate_message_specs.py` from the XSD the library ships.
  The home page's message-edition figure moves from 12 to 13 with it.

### Fixed

- Library facts checked against pain001 0.0.78 and its siblings and
  corrected across the site:
  - Python 3.11 or later (CI tests 3.11 to 3.14), not 3.10 to 3.12.
  - Thirteen message types, including `pain.008.001.08`.
  - `pain001-mcp` has 28 tools, not 17 or 22. It also serves HTTP on
    request, and `commit_payment_batch` writes the XML to the path the
    caller gives, so "all read-only" and "never writes" are gone.
  - The scheme rulebooks go well beyond the five SEPA and
    cross-border ones.
  - lxml is the optional `fast` extra, not absent.
  - `pain001 upload` delivers to SFTP, so "stops at the file" is
    narrowed.
  - The companions are lockstep and dual-licensed.
  - The BAH and XML-DSig flags shipped in 0.0.72, not "the next
    release".
  - CSV formula cells are kept as supplied by default.
  - `process_files` takes `output_path`, not `output_dir`.
  - `xborder-ct` checks no charge bearer.
- The technical reference documents `pain001 face`, `pain001 upload`,
  the faces REST endpoints, `PAIN001_API_KEY`, and every `generate`
  flag the CLI has.
- The "first file in three commands" recipe works: `init -o` takes a
  file, so it writes `payments.csv`, which the next command reads.
  The version pages' snippets match.
- `pain001-fast` is marked as experimental and links its 0.0.82 GitHub
  release. Automatic core activation and cryptographic-parity claims are
  removed. The
  `pip install pain001-fast` line and the PyPI download link are
  removed; neither resolves.
- The compliance toolkit no longer links GitHub Discussions, which the
  repository does not have.
- 20 changed English fragments, and the installation page's
  description and subtitle, are migrated in all 34 locale tables under
  `scripts/docs_i18n/` and `scripts/pages_i18n/`, with their
  translations updated.
- Code blocks keep a readable text colour with the light theme chosen on
  a dark system. ssg's highlighter stylesheet sets the block's text to
  `#e6edf3` under `prefers-color-scheme: dark`, which the theme toggle
  cannot override, so the `/try/` command block read at 1.07:1 on the
  light code ground. The block now takes the theme's `--code-plain`.
- Release pages list their checksums in the portfolio's shape: the
  `SHA-256 of every asset attached to this release:` lead-in, a `text`
  fence, asset names without the `./` that `SHA256SUMS` carries, and
  the digest of `SHA256SUMS` itself, which is an asset too. v0.0.13
  and v0.0.14 shipped without them and were corrected by hand.

## [0.0.14] - 2026-11-07

### Changed

- Regenerated for pain001 0.0.78, up from 0.0.75 (0.0.76 and 0.0.77
  were never deployed): corpus pages, scenario pages, demo samples,
  localized corpus strings, version stamps, the corpus archives and the
  demo's pinned pain001 wheel, from the regenerate workflow's run for
  0.0.78.
- Built with ssg 0.0.74, the latest release, up from 0.0.72. Every
  workflow's `SSG_VERSION`, the devcontainer and the setup docs name
  0.0.74. ssg 0.0.73 gave the generated `highlight.css` token colours
  that switch on `prefers-color-scheme` only, so with the dark theme
  chosen on a light system the code tokens on `/try/` failed AAA
  contrast; the adapter makes every token take its block's colour,
  which follows the theme toggle, as the code blocks did before.
- PRISM is current with the theme suite: the footer's ssg credit link
  carries the `made-with-ssg` class that ssg's quality gate looks for
  (ssg-themes `ceaf3cb`, the one theme change since this site adopted
  PRISM).

### Fixed

- The weekly Dated claims check failed on 26 October and 2 November while
  every claim held: the Internet Archive refused the runner's connections
  for longer than the retries waited, and answered `503` or `429` when it
  was throttling, which the check treated as final. Throttling answers
  (`429`, `502`, `503`, `504`) are now retried like a refused connection,
  honouring `Retry-After` up to 120 s; the check makes four attempts per
  source with a 30 s backoff, and the job's timeout moves to 50 minutes to
  fit. A source that stays unreadable, or any other HTTP error, still
  fails the check.

## [0.0.13] - 2026-11-01

### Changed

- Built with ssg 0.0.72, the latest release, up from 0.0.63. Every
  workflow that installs ssg (`ci.yml`, `release.yml`,
  `release-backfill.yml`, `regenerate.yml`) reads one `SSG_VERSION`
  for its cache key and install step; `regenerate.yml` no longer
  hard-codes the version twice. The pages' `generator` metadata, the
  devcontainer and the setup docs name 0.0.72. ssg 0.0.72 no longer
  emits the entity-escaped metas, bodies and code delimiters or the
  stale `/highlight.css` link that `scripts/postbuild_fix.py` repairs;
  those passes stay as no-op guards.
- ssg 0.0.72 no longer wraps each page body in `<div lang>`, so on
  pages with the contents rail every `<hr>` became a grid item and
  collapsed to a centred zero-width rule (138 layout-audit strays).
  The rail layout now gives a direct-child rule zero inline margins,
  and the dead `div[lang]` selectors are gone.
- CI adds a gate job after each versioned test matrix (for example
  `Unit tests (all)`), so branch protection can require one check name
  that survives Python, Node and Rust version bumps (#85).

### Fixed

- Pages that are noindex no longer name themselves canonical. Search
  Console listed the translated corpus scenario pages (for example
  `/es/corpus-cz-sepa-sct/`) as excluded by noindex while each one's
  canonical pointed at itself; `/offline/` and `/thanks/` did the same.
  The noindex stays (the translations are deliberately kept out of the
  index, sitemap and hreflang clusters); the canonical link goes.
  `scripts/validate_sitemap.py` now checks every build: each sitemap URL
  is a built, indexable, self-canonical page.

### Security

- `package.json` overrides minimatch to `^11.0.1`
  (GHSA-g3hv-75wg-m249), which eslint still pulls in at `^10`.
- `requirements/seo.in` floors pyasn1 at 0.6.5, and the hashed
  `requirements/seo.txt` moves 0.6.4 to 0.6.5 (GHSA-2qm8-x737-gmw5,
  GHSA-mm57-4v3p-rchx, GHSA-9m75-vc3g-4x39, GHSA-fm9c-5rcf-2q5p).

## [0.0.12] - 2026-10-29

### Changed

- Regenerated for pain001 0.0.75 (#79): the corpus and scenario pages,
  demo samples, twin schemas, version stamps, the coverage and example
  corpus downloads, and the in-browser demo's pinned pain001 wheel now
  come from the 0.0.75 release. The compatibility page states the
  0.0.75 baseline.

## [0.0.11] - 2026-10-27

### Added

- Documentation article for `pain001-fast`, the high-throughput PyO3 native
  extension engine for ISO 20022 payments: architecture, sub-25ns
  zero-allocation validators, multi-core Rayon batch processing exceeding
  50,000 tx/s, and seamless pure Python fallbacks.
- Updated governance telemetry counts.

### Changed

- `KEYS.asc` and `.github/allowed_signers` trust a second maintainer signing
  key, `SHA256:kIOPAavp1TCEauTr1tTIN3cv+tSs6F9m/4lZjuM9tqk` (rousseau-mbp-m1),
  so release tags can be signed on either maintainer machine.

### Fixed

- `KEYS.asc` is now in OpenSSH allowed-signers format, so
  `git -c gpg.ssh.allowedSignersFile=KEYS.asc tag -v <tag>` verifies release
  tags. It previously held a bare public-key line that Git rejected as
  "invalid key". `KEYS.md` documents the command and lists each key's
  fingerprint.
- The weekly dated-claims check retries a refused or timed-out connection
  (three attempts, with backoff) before it reports a source as unreadable.
  It failed three of its last five runs on the Internet Archive refusing
  or timing out the runner, while every claim held when read again. An
  HTTP error answer is not retried, and a source that stays unreadable
  still fails the check. The job's limit rises from 15 to 30 minutes to
  leave room for the retries.

### Security

- The Search Console scoreboard authenticates without a stored key.
  Workload Identity Federation exchanges the job's GitHub OIDC token for
  a one-hour Google token, and the provider accepts only this repository
  and only `seo-scoreboard.yml`. The service-account key and the
  `GSC_SERVICE_ACCOUNT_JSON` secret are deleted, so the site again keeps
  no long-lived credentials.

## [0.0.10] - 2026-09-27

### Added

- `docs/seo/`: an outreach pack (curated-list entries, Stack Overflow
  drafts with disclosure, Bing Webmaster Tools steps) and a case-study
  template with a permission request, for the maintainer to send.
- A weekly Search Console scoreboard (`scripts/seo_scoreboard.py`,
  `.github/workflows/seo-scoreboard.yml`): the last 28 days against the
  previous 28 for the site, the queries its content targets, and the top
  pages and countries. It needs a read-only service account; until one is
  set up it reports "not configured" (see `DEVELOPMENT.md`).
- IndexNow: after each deploy of `main`, CI submits every sitemap URL so
  Bing, Yandex, Seznam, Naver and the other participating engines recrawl
  within hours. Ownership is proven by a key file at the site root; no
  account or secret is involved, and a failed submission never fails CI.
- A "What is pain.001?" reference page at `/pain-001/`, in all 35
  languages: what the message is, its structure, a complete example
  that validates against the official XSD, every version from .03 to
  .13, how it compares with pain.002, pain.008, pacs.008 and MT101, and
  how to create one. It carries TechArticle structured data in each
  language.
- `CONTRIBUTING.md` sets out the code-review standard every pull request
  is checked against, and the pull request template links it. It also
  points newcomers to the good-first-issue tasks.
- Tests for the demo's service worker, `static/sw.js`: which requests it
  caches, cache-first serving, storing a clone of a good response and
  never a failed one, and activation deleting stale caches before claiming
  clients. The coverage gate now includes `sw.js`, at 100% of lines and
  branches (#52).
- Tests for the legacy-URL redirect as the build stamps it: a retired
  path is sent to its new page, other paths stay put, and names such as
  `toString` or `constructor` never redirect. `redirect.js` now has 100%
  branch coverage, up from 50% (#53).
- Tests for the SPDX header gate (`scripts/validate_spdx_headers.py`):
  what it accepts, what it reports, which paths it exempts, and that it
  reads only the first ten lines of a file (#51).
- The README links the OpenSSF Best Practices passing badge the
  project earned on 26 September 2026.
- Tests for every script the site ships, run in a jsdom page with fake
  runtimes: the theme and motion boot script, the analytics loader, the
  legacy redirect, the navigation and theme control, the Pain001 chrome
  layer, the homepage, and the demo's engine and page wiring. A coverage
  gate, `npm run coverage`, holds `static/js/` (less the vendored
  Cloudflare beacon) at 90% of lines and 80% of branches in CI and in
  the release workflow; it measures 99.76% of lines, 96.63% of branches
  and 99.39% of functions. A guard test fails if a new script in
  `static/js/` has no test, since the report only lists files a test
  loads.
- A pytest suite under `tests/python/` of regression tests for the
  build and release scripts: the version stamper, the corpus zips, the
  release-notes composer, the library-release trigger, the runtime
  fetcher, release packaging and the SBOM serial, plus earlier site
  fixes (the service-worker cache version, legacy redirect stubs,
  inline styles under the CSP, the LICENSE pointer). Each test was seen
  to fail without the fix it guards. `make test` and CI run it, from the
  hash-pinned `requirements/test.txt`.
- `docs/assurance-case.md`: the site's security requirements, trust
  boundaries, design principles and the weaknesses it counters.
- `docs/security-review-2026-09.md`: a review against that case with
  seven findings and their status. It is not independent: the
  maintainer did it with an AI assistant.
- Coding standards, named in `DEVELOPMENT.md` and enforced in CI: ruff
  for Python (`ruff.toml`) and ESLint for JavaScript
  (`eslint.config.mjs`). `make lint` runs every linter.
- Every source file carries its own SPDX copyright and licence header,
  checked by `scripts/validate_spdx_headers.py` in CI.

### Changed

- The eleven pain.001 version pages lead with what searchers look for:
  each title names the XSD, an example and the format (and, for
  `.09`, the in-browser validator), and a new section links the
  official ISO schema, the element reference generated from it, and
  XSD-valid example files for that version. The `.12` page no longer
  calls itself the newest supported version.
- The pain.002 page is titled for the status report as well as its
  reason codes, and the message-specification hub for the XSD element
  reference it is.
- The translated corpus scenario pages (`/<locale>/corpus-*/`, 210 in
  five languages) carry `noindex, follow` and leave the sitemap and every
  hreflang cluster. Search Console listed them as discovered or crawled
  but not indexed; they stay published for visitors, and the English
  scenario pages stay indexable.
- Search titles and descriptions for every language's homepage and
  for the browser demo match how people search: each homepage title
  now names pain.001 (and SEPA-XML where that market searches for it),
  the demo is titled as a pain.001 generator and validator, and every
  description stays within 155 characters.
- The new page is linked from the Developers menu and the footer on
  every page, from each language's homepage, and from every version
  page. The English homepage title now names pain.001.
- Build provenance is attested with `actions/attest` v4.2.2, the action
  `actions/attest-build-provenance` v4 wraps; this supersedes Dependabot's
  bump in #50.
- Release archives are reproducible. The release workflow pins every
  timestamp to the tagged commit (`SOURCE_DATE_EPOCH`), packages the
  site deterministically, builds it again from a clean tree and refuses
  to release unless the release files are byte-identical.
- `SECURITY.md` sets out how a report is handled, from acknowledgement
  to advisory, and credits reporters unless they ask not to be.

- `CONTRIBUTING.md` states the test policy the project already follows:
  new or changed behaviour comes with tests, and a fix with a test that
  fails without it.

### Fixed

- The technical reference and the MCP page describe what is released:
  pain001 0.0.71 and pain001-mcp 0.0.71, with 22 MCP tools (the pages
  had said 17, 21, 23 and 26 in different places). The Business
  Application Header, XML-DSig and formula-injection options and the
  four dual-control MCP tools, which are not in any release yet, are
  documented in "In the next release" sections instead.
- The site no longer publishes 1,931 stray per-page files that ssg wrote
  beside every page (empty sitemaps, robots.txt files pointing at them,
  RSS and manifest copies, timestamped news sitemaps), nor the `/404/`
  copy Search Console reported as a soft 404. Tag archives no longer
  list the not-found, offline and thanks pages.
- A deploy no longer risks publishing a CDN challenge or error page as a
  stylesheet or script. `scripts/carry_forward_assets.py` keeps a file it
  downloads from the live site only when it is served as CSS or
  JavaScript to match its name and is not an HTML page, and logs what it
  skipped (security review finding SR-3, #54).
- The build no longer publishes 385 invalid per-page
  `news-sitemap.xml` files that ssg wrote beside every page, each with
  an empty `<loc>` and the build time. The root news sitemap is kept.
- CodeQL flagged an empty `except` in the corpus-zip check added in
  0.0.9 (`py/empty-except`). The check is now a function that returns
  whether an existing zip already holds the entries, and a damaged zip
  answers no, so it is replaced.

## [0.0.9] - 2026-09-26

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
- The MCP page and installation guide describe 23 tools in pain001-mcp,
  including `suggest_record_fix` and `simulate_payment_batch`, and the
  page's subtitle no longer says seventeen.
- The SBOM attestation in both release workflows uses `actions/attest`,
  which replaces the deprecated `actions/attest-sbom` with the same inputs.
- Every workflow job runs on `ubuntu-24.04` instead of `ubuntu-latest`,
  which moves to Ubuntu 26 on 19 October 2026; the image is now changed
  deliberately, after the builds are tested on it.
- The README lists the release backfill workflow, describes how
  regeneration is triggered now, and says the demo's input handling is
  fuzzed here.
- The roadmap records that Phase C's first reopening condition, the
  library's v0.0.71 release, is met, and no longer calls 14 November
  2026 a live deadline.
- Roadmap: Phase C, the declarative rule engine, is deferred. The library
  already has 23 of its 29 profiles as data and a shipped declarative
  overlay grammar, and issue #184 proposes a CEL policy language, so
  building Phase C as planned would add a fourth rule format. Its first
  step is now an ADR in the library choosing one format; it reopens once
  the library's v0.0.71 release has landed and profile maintenance can
  be staffed beyond one person.

### Fixed

- A regeneration that changes nothing no longer rewrites corpus zips.
  DEFLATE output differs between zlib builds, so the Linux runner
  re-compressed five zips the macOS build had produced. An existing zip
  whose members, metadata and bytes all match is now kept.
- The tests no longer print Node's module-type warning for the demo's
  ES module, which `package.json` deliberately leaves untyped.
- The site regenerates for every pain001 release again. The library's
  notification needed a `SITE_DISPATCH_TOKEN` secret that was never
  created, so no release since the workflow was added regenerated the
  site. The regenerate workflow now also checks PyPI every six hours and
  runs when a newer release appears, with no token. It pins the demo's
  pain001 wheel itself, and starts CI on the pull request it opens.
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

[Unreleased]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.86...HEAD
[0.0.86]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.85...v0.0.86
[0.0.85]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.84...v0.0.85
[0.0.84]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.83...v0.0.84
[0.0.83]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.82...v0.0.83
[0.0.82]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.14...v0.0.82
[0.0.14]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.13...v0.0.14
[0.0.13]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.12...v0.0.13
[0.0.12]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.11...v0.0.12
[0.0.11]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.9...v0.0.10
[0.0.9]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/sebastienrousseau/pain001.github.io/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/sebastienrousseau/pain001.github.io/releases/tag/v0.0.1
