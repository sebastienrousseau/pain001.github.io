# Assurance case: pain001.com

This document argues why pain001.com meets its security requirements. It
states what the site must guarantee, where the trust boundaries lie, which
design principles it follows, and how it counters the common weaknesses of
a static website that runs code in the visitor's browser. The latest
review against this case is
[security-review-2026-09.md](security-review-2026-09.md).

## 1. What the site is

pain001.com is a static website built from this repository with the Static
Site Generator (ssg) and served by GitHub Pages behind Cloudflare. It has
no user accounts and no database. Its one piece of server-side code is a
Cloudflare Worker, `pain001-events` (source in `workers/events/`), routed
at `pain001.com/e`: it receives first-party, cookie-free event counts
from the site's pages and writes them to Workers Analytics Engine
(section 4). One page, `/try/`, runs the pain001 library in the
visitor's browser (Pyodide, WebAssembly) to validate payment data the
visitor pastes or uploads.

## 2. Security requirements

| # | Requirement |
| --- | --- |
| R1 | Payment data a visitor gives the demo never leaves the visitor's browser. |
| R2 | A visitor receives exactly the pages, scripts and runtime this repository defines; nothing can be injected into them. |
| R3 | The site cannot be framed or used to run a third party's script. |
| R4 | A release archive is the site as built from its tagged commit, and anyone can verify that. |
| R5 | Only the maintainer can change what is deployed, and CI cannot be used to escalate privileges. |

The site makes no promise about the correctness of a payment file for a
particular bank; the demo's own page states its layers and limits.

## 3. Trust boundaries

```text
Visitor's browser ── HTTPS ──> Cloudflare ──> GitHub Pages (static files)
   │  demo: CSV/XML stays in the tab; Pyodide runs locally
   ├── RUM beacon ──> cloudflareinsights.com (page views, no content)
   ├── event beacon ──> pain001.com/e (Worker) ──> Workers Analytics Engine
   └── enterprise form ──> formspree.io (only what the visitor submits)

Maintainer ── signed commits / PRs ──> GitHub ──> Actions ──> Pages deploy
                                                   ├──> signed release + attestations
                                                   └──> Search Console API, read-only
                                                        (OIDC -> one-hour token, no key)
Build inputs: this repository, ssg (pinned), PyPI and npm (hash/lockfile),
the Pyodide CDN (SHA-256 per file)
```

Everything left of the arrows in the first block is the visitor's; the
site's code runs there but sends nothing back except the page-view beacon
and the event beacons, which carry an event name, a page path and an
optional short label.
The enterprise contact form is the one place data leaves by design, and
only when the visitor submits it.

## 4. Secure design principles applied

- **Economy of mechanism:** a static site plus one small Worker. The
  attack surface is the files served, the build that produces them, and
  the Worker's single endpoint, `POST /e`
  (`workers/events/src/index.js`, with no runtime dependencies). The
  Worker answers `404` to any other path and `405` to any other method,
  and sends no CORS headers.
- **Input validation at `/e`:** a body over 1,024 bytes is refused with
  `400`, by declared `Content-Length` or while it streams, before it is
  parsed. The JSON must be an object with only the keys `event`, `page`
  and an optional `label`. `event` must be one of eleven allow-listed
  names; `page` loses its query string and fragment and must then be a
  same-site path of at most 200 characters; `label` must be 1 to 64
  letters, digits, spaces or `._:-`. Anything else gets `400` with no
  detail and nothing is written. Posts carrying Do Not Track or Global
  Privacy Control, or whose `Origin` or `Sec-Fetch-Site` is not this
  site, get `204` and are dropped.
- **Data minimisation at `/e`:** each accepted event is one Workers
  Analytics Engine data point holding the event name, the cleaned path,
  the label and the two-letter country Cloudflare reports. The Worker
  stores no IP address, user agent, referrer, cookie or identifier, and
  forwards nothing elsewhere. Analytics Engine keeps data points for
  three months. Invocation logs and traces are off; a failed write logs
  one error line with no request data.
- **Fail-safe defaults:** a restrictive Content-Security-Policy on every
  page: `default-src 'self'`, no inline script except by hash,
  `object-src 'none'`, `base-uri 'self'`, connections only to the site and
  the Cloudflare beacon. Framing is refused by header (`X-Frame-Options:
  DENY`, `frame-ancestors 'none'`).
- **Least privilege:** every workflow token is read-only by default; write
  scopes (`contents`, `pages`, `id-token`, `attestations`) are granted per
  job and only where needed. The one Google Cloud identity, a read-only
  Search Console service account, has no keys: only this repository's
  `seo-scoreboard.yml` can obtain its one-hour tokens, through Workload
  Identity Federation. No workflow runs untrusted pull-request code
  with secrets (`pull_request_target` is not used).
- **Complete mediation of dependencies:** Python packages install with
  `--require-hashes`, Node packages from a committed lockfile, every
  GitHub Action is pinned by commit SHA, and each of the demo's 18
  runtime files is refused unless its SHA-256 matches the manifest.
- **Separation of privilege:** deploys and releases run only from `main`
  and signed tags; the release workflow verifies the tag's SSH signature
  against `.github/allowed_signers` before building.
- **Open design:** the demo's input handling (`static/js/try-demo.js`) is
  small, dependency-free and written to be read in one sitting.

## 5. Common weaknesses and how they are countered

| Weakness | Where it could arise | Counter |
| --- | --- | --- |
| CWE-79 cross-site scripting | The demo renders visitor data | Values are written with `textContent`; the only `innerHTML` writes clear elements. CSP forbids inline and third-party script. CodeQL runs on every change. |
| CWE-601 open redirect | Legacy-URL redirect script | Destinations come from a build-time map of same-origin paths, never from the page or URL. |
| CWE-1021 clickjacking | Any page | `X-Frame-Options: DENY` and `frame-ancestors 'none'` headers. |
| CWE-494 download without integrity check | Demo runtime, dependencies | SHA-256 per runtime file, hash-pinned pip installs, npm lockfile, SHA-pinned actions. |
| CWE-829 untrusted functionality | Third-party scripts | Only the vendored Cloudflare beacon, loaded from this origin and only on the deployed host. |
| CWE-400 resource exhaustion | Demo input | Input files over 2 MB are refused before parsing. |
| CWE-400 resource exhaustion | Event endpoint `/e` | Bodies over 1,024 bytes are refused before parsing; the stream is abandoned at the cap rather than buffered. |
| CWE-20 improper input validation | Event endpoint `/e` | Allow-listed event names and keys, character-class and length checks on path and label; anything else is refused with `400` and not written. |
| CWE-359 exposure of private information | Event endpoint `/e` | Only the event name, cleaned path, label and country are stored; no IP address, user agent, referrer, cookie or identifier. |
| CWE-200 information exposure | Payment data in the demo | Processed in the browser only; the demo makes no request carrying it. |
| CWE-522 credential exposure | Repository and CI | No long-lived secrets are stored for the site; workflows use the short-lived `GITHUB_TOKEN`, and the Search Console scoreboard exchanges GitHub's OIDC token for a one-hour Google token instead of holding a key. |

## 6. Evidence

- CI (`.github/workflows/ci.yml`) builds the site and runs every gate on
  each push and pull request, including axe and WAVE accessibility scans
  and Lighthouse in real Chrome.
- CodeQL (`codeql.yml`) and OpenSSF Scorecard (`scorecard.yml`) run on
  every push to `main`.
- The demo's input handling is covered by unit and property-based (fuzz)
  tests.
- The events Worker's tests (`workers/events/test/index.test.mjs`, on
  `node:test` with a fake Analytics Engine binding) run in CI with a
  100% line, branch and function coverage floor.
- Each release carries Sigstore-signed build provenance, an SBOM
  attestation and SHA256SUMS, and its archive is rebuilt from a clean
  tree during the release to prove it is reproducible.

## 7. Residual risks

- **One maintainer.** A compromised maintainer account could deploy
  arbitrary content. Signed commits and tags limit, but do not remove,
  this risk; see `GOVERNANCE.md`.
- **Hosting and CDN.** GitHub Pages and Cloudflare are trusted to serve the
  built files unmodified.
- **Third parties.** Cloudflare Web Analytics receives page-view metadata;
  Formspree receives what a visitor submits through the enterprise form.
- **Worker deployment.** The events Worker is deployed by the maintainer
  with `wrangler`, never from CI, so the running copy is the maintainer's
  deploy rather than a CI artefact. The maintainer handover note records
  the deploy and its settings.
- **The library.** The demo's verdicts are the pain001 library's; its own
  assurance case covers them.
