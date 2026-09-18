# Measurement: what is counted and how

pain001.com counts page views through [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/):
cookieless, no IP address stored, no fingerprint, no identifier. Cloudflare already fronts the domain,
so measurement adds no new processor.

## What is counted

Page views, paths, referrers, country, browser family and Core Web Vitals, on every page **except
`/try/`**. The browser demo carries no beacon: its "Verify it yourself" panel tells visitors there is no
analytics script and invites them to confirm it with DevTools open, and that claim stays true.

Custom events are not available in Cloudflare Web Analytics, so demo runs, downloads and PyPI clicks
are not counted. PyPI download figures come from PyPI itself (`scripts/traction.py`).

## Where it lives

- The beacon is **vendored** at `static/js/cf-beacon.min.js` (Cloudflare's `beacon.min.js`, version
  2026.9.1, sha256 `08c4fd72f9d96a7aa554510dff2c293973b1b092dff1b9b282bce9111b50ef41`) and served from
  this origin. Cloudflare publishes no SRI hash and replaces the file without notice, so loading it
  from their CDN would either fail the audit's SRI gate or silently stop measuring on their next
  release. Refresh it with `scripts/refresh_beacon.sh` and commit the new bytes.
- The tag sits at the end of `_layouts/index.html`, `_layouts/page.html` and `_layouts/contact.html`
  (not `_layouts/try.html`); `postbuild_fix.fix_tag_pages` adds the same tag to the taxonomy pages ssg
  emits outside the layouts. The token is public by design; it identifies the site, not a visitor.
- One Content-Security-Policy applies to every page: `script-src 'self'`, and `connect-src 'self'
  https://cloudflareinsights.com` for the beacon's one POST to `/cdn-cgi/rum`. The demo page has the
  same policy but no beacon, so it makes no such request.
- The dashboard: Cloudflare, Team Rousseau account, Analytics & Logs, Web Analytics, site `pain001.com`,
  set to "Enable with JS Snippet installation" so Cloudflare does not inject the beacon into every
  response (which would put it on the demo page).

## Switching it off

Remove the three layout tags, the `fix_tag_pages` injection and the vendored file, and drop
`https://cloudflareinsights.com` from `connect-src`; nothing else depends on it.
