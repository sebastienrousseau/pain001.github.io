# ADR 0002: Cloudflare Web Analytics and first-party events

- Status: accepted
- Date: 2026-11-10
- Supersedes: the September 2026 choice of a self-hosted Umami instance on `metrics.pain001.com`

## Context

The site needs to know whether the browser demo, the install command and the evidence pack are used,
without cookies, identifiers or a third-party script, and without collecting anything a visitor
types or loads. The September 2026 plan chose a self-hosted Umami instance; Cloudflare Web
Analytics has counted page views since then. Cloudflare Web Analytics records
page views only, not custom events.

## Decision

Decision D1 (10 November 2026), final:

- Cloudflare Web Analytics counts page views on every page.
- First-party, cookie-free events go to `/e` on this origin, where a Cloudflare Worker writes them to
  Workers Analytics Engine. Events are kept for 3 months, with no IP addresses and no payment data.
- The event names are fixed: `hero_cta_click`, `sandbox_start`, `sandbox_xsd_run`, `xml_copy`,
  `xml_download`, `install_copy`, `outbound_github`, `outbound_pypi`, `evidence_pack_download`,
  `profile_guide_view`, `discussion_click`, `adoption_form_submit`.
- Umami is superseded and will not be deployed.

## Consequences

- `static/js/pain001-events.js` sends only those names, with the page path and at most a short
  label. It sends nothing from localhost, under Do Not Track or Global Privacy Control, or without
  `sendBeacon`.
- The privacy page, the demo's "Verify it yourself" panel and `METRICS.md` describe both kinds of
  count. The demo previously said it ran no analytics script while the layout already loaded the
  page-view beacon there; the panel now names every request it makes.
- The Worker and its Analytics Engine dataset are deployed by the maintainer. Until then the event
  beacons reach GitHub Pages and are discarded.

## Amendments

- 2026-11-10: the events Worker and its Analytics Engine dataset are deployed at
  `pain001.com/e`, so event beacons are now counted rather than discarded.
- 2026-11-10: `discussion_click` was dropped when the repository turned GitHub Discussions off
  and pointed questions to issues (commit 11701d62). The Worker accepts the other eleven names.
