# Measurement: what is counted and how

pain001.com counts page views through [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/):
cookieless, no IP address stored, no fingerprint, no identifier. Cloudflare already fronts the domain,
so measurement adds no new processor.

## What is counted

Two things, both without identifying anyone (decision D1, 10 November 2026; see
[ADR 0002](docs/adr/0002-cloudflare-analytics-and-events.md)):

- **Page views**, on every page including `/try/`: paths, referrers, country, browser family and
  Core Web Vitals, through Cloudflare Web Analytics.
- **Events**, first-party and cookie-free, through `static/js/pain001-events.js`: `hero_cta_click`,
  `sandbox_start`, `sandbox_xsd_run`, `xml_copy`, `xml_download`, `install_copy`, `outbound_github`,
  `outbound_pypi`, `evidence_pack_download`, `profile_guide_view` and
  `adoption_form_submit`. Each is one `navigator.sendBeacon` to `/e` on this origin carrying the event
  name, the page path and at most a 64-character label: no cookie, no identifier, nothing typed or
  loaded into the demo. A Cloudflare Worker routed at `pain001.com/e` writes it to Workers Analytics
  Engine, which keeps it for 3 months and stores no IP address. No payment data is ever involved.
  Nothing is sent from localhost, when the browser sends Do Not Track or Global Privacy Control, or
  when `sendBeacon` is unavailable; a failed send is ignored. The Worker's source and tests are in
  `workers/events/`.

The demo's "Verify it yourself" panel names both requests. PyPI download figures come from PyPI itself
(`scripts/traction.py`).

## Where it lives

- The beacon is **vendored** at `static/js/cf-beacon.min.js` (Cloudflare's `beacon.min.js`, version
  2026.9.1, sha256 `08c4fd72f9d96a7aa554510dff2c293973b1b092dff1b9b282bce9111b50ef41`) and served from
  this origin. Cloudflare publishes no SRI hash and replaces the file without notice, so loading it
  from their CDN would either fail the audit's SRI gate or silently stop measuring on their next
  release. Refresh it with `scripts/refresh_beacon.sh` and commit the new bytes.
- The loader tag sits in `_layouts/base.html`, so every page built from the layouts carries it,
  including `/try/`; `postbuild_fix.fix_tag_pages` adds the same tag to the taxonomy pages ssg emits
  outside the layouts. `static/js/pain001-analytics.js` skips the beacon on localhost so CI and local
  audits do not attempt an external RUM POST; deployed hosts load the vendored beacon. The token is
  public by design; it identifies the site, not a visitor. `static/js/pain001-events.js` is loaded
  next to it.
- One Content-Security-Policy applies to every page: `script-src 'self'`, and `connect-src 'self'
  https://cloudflareinsights.com` for the beacon's one POST to `/cdn-cgi/rum`. The event beacons go
  to `'self'`.
- The dashboard: Cloudflare, Team Rousseau account, Analytics & Logs, Web Analytics, site `pain001.com`,
  set to "Enable with JS Snippet installation" so Cloudflare does not inject the beacon into every
  response (which would put it on the demo page).

## Switching it off

Remove the three layout tags, the `fix_tag_pages` injection and the vendored file, and drop
`https://cloudflareinsights.com` from `connect-src`; nothing else depends on it.
