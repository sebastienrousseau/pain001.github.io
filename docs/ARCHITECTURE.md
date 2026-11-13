# Architecture

## System context

Pain001.com is a static documentation and browser-tool site. Authors edit
Markdown, HTML templates, CSS, and dependency-free JavaScript. The Static
Site Generator (ssg) 0.0.75 produces HTML; deterministic post-build passes add locale variants,
search metadata, accessibility affordances, and downloadable artefacts.
GitHub Actions runs all gates and deploys the exact checked Pages artefact.
The site is static apart from one Cloudflare Worker, `pain001-events`,
which receives first-party event counts at `pain001.com/e` (see
[Events Worker](#events-worker)).

## Build flow

```text
_posts + _layouts + ssg.toml
              |
              v
         ssg 0.0.75
              |
              v
     Pain001/ generated tree
              |
       post-build validators
              |
              v
        docs/ Pages artefact
              |
     CI accessibility/security/performance gates
              |
              v
        GitHub Pages deployment
```

The `/try/` tool loads only same-origin Pyodide, schema, and wheel assets,
fetched at build time and verified against the SHA-256 pins in
`static/pyodide/pain001-runtime.json`. Payment data stays in the browser.
Every page, `/try/` included, loads the Cloudflare Web Analytics page-view
beacon and `static/js/pain001-events.js`; neither sends anything typed or
loaded into the demo. The content security policy blocks arbitrary
third-party code.

## Events Worker

`workers/events/src/index.js` is the only server-side code. It is a
Cloudflare Worker with no runtime dependencies, routed at `pain001.com/e`
by `workers/events/wrangler.jsonc`, with `workers.dev` and preview URLs
off. `static/js/pain001-events.js` posts to it with
`navigator.sendBeacon`, except from a local preview, under Do Not Track
or Global Privacy Control, or when `sendBeacon` is missing.

- **Receives:** `POST /e` with a JSON body of at most 1,024 bytes,
  holding `event`, `page` and an optional `label`. Any other path gets
  `404`, any other method `405`; no CORS headers are sent.
- **Validates:** `event` is one of eleven allow-listed names; `page`
  loses its query string and fragment and must be a same-site path of at
  most 200 characters; `label` is 1 to 64 letters, digits, spaces or
  `._:-`; no other key is accepted. An oversized body is refused before
  it is parsed. A failure gets `400` with no detail.
- **Drops:** posts with `DNT: 1` or `Sec-GPC: 1`, or whose `Origin` or
  `Sec-Fetch-Site` is not this site, get `204` and are not written.
- **Stores:** one Workers Analytics Engine data point per accepted event
  in the `pain001_events` dataset: event name, cleaned path, label and
  the two-letter country Cloudflare reports. No IP address, user agent,
  referrer, cookie or identifier is stored, and nothing is forwarded
  elsewhere. Analytics Engine keeps data points for three months.
- **Logs:** invocation logs and traces are off; a failed write logs one
  error line without request data, and the visitor still gets `204`.
- **CSP reports:** `POST /e/csp` (a second route) takes Content
  Security Policy violation reports, which the browser sends itself, so
  no `Origin` check applies. The body may be 4,096 bytes, in the
  `report-uri` form or as a Reporting API list (first ten entries). A
  report is kept only when its document is a page on `pain001.com`, as
  one data point: `csp_violation`, the cleaned path, the effective
  directive, the country and the blocked item reduced to a keyword, a
  scheme or an origin. `DNT` and `Sec-GPC` reports are dropped; a
  malformed body gets `400`, every other outcome `204`. Source:
  `workers/events/src/csp.js`.

Its tests (`workers/events/test/index.test.mjs`, on `node:test` with a fake
Analytics Engine binding) run in CI with a 100% line, branch and function
coverage floor. The maintainer deploys it by hand with `wrangler`, never
from CI; [`workers/events/README.md`](../workers/events/README.md) has the
steps.

## Theme

PRISM supplies the visual language and interaction contract. Skeletonic CSS
v3.0.0 supplies the CSS foundation. Upstream files are vendored unmodified;
`static/css/pain001-prism.css` adapts the established Pain001 semantic markup.
This separation makes future upstream comparison auditable.

## Deployment and rollback

Only a green `main` workflow may deploy. Releases use signed, immutable tags.
Rollback means redeploying a previously verified tag through the same workflow,
not hand-editing the Pages output.
