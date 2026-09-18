# Changelog

The site has no version of its own; entries are dated and name the pull
request. Pages regenerated from a library release are listed under the
release that produced them.

## 2026-09-18

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

## 2026-09-12 and 2026-09-13

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

## 2026-08-23

- Licence: ship Apache-2.0 OR MIT and restore `LICENSE` as the pointer to the
  dual grant (#5, #6).

## 2026-07-26 to 2026-07-30

- v0.0.2 of the site: editorial redesign, research-backed content, repaired
  build pipeline (#2); copyright byline linked, layout and print regressions
  gated in CI (#3); roadmap re-ordered by what unblocks the most (#4).
