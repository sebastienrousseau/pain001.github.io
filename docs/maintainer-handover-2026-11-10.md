<!-- SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Maintainer handover: decisions of 10 November 2026

The site changes for decisions D0 to D6 are on `feat/v0.0.85`. These items
need the maintainer: an account, a number, or a fact only the maintainer
holds. Nothing here is done by the build.

## Cloudflare: a real 301 for `/enterprise/`

GitHub Pages cannot send a redirect status, so `/enterprise/` and `/thanks/`
are noindex stubs that redirect with a same-origin script and name the new
page as canonical. For a server-side 301, add a Single Redirect rule in the
Cloudflare dashboard (pain001.com, Rules, Redirect Rules):

- When incoming requests match: custom filter expression
  `(http.request.uri.path eq "/enterprise" or starts_with(http.request.uri.path, "/enterprise/"))`
- Then: static URL redirect to `https://pain001.com/for-banks/`, status code
  `301`, query string not preserved.

A fragment such as `#ask` never reaches the server, so the rule covers
`/enterprise/#ask` too. `/thanks/` can get the same rule pointing at
`https://pain001.com/contact/`.

## Cloudflare: the events Worker

`static/js/pain001-events.js` sends events to `/e` on this origin. The Worker
that receives them (route `pain001.com/e`, writing to a Workers Analytics
Engine dataset kept 3 months, storing no IP address) is deployed by the
maintainer. Until then the beacons reach GitHub Pages and are discarded.

## GitHub Discussions on the core repository

`/for-banks/`, `/docs/bank-profiles/`, `/developers/` and the homepage send
questions and "Tell us how you use it" to
<https://github.com/sebastienrousseau/pain001/discussions>. Discussions are
switched off on that repository today, so those links fail until they are
switched on. The D5 discussion "How are you using pain001?" also needs
opening there.

## Search Console: locales beyond the six

D4 indexes English, French, German, Dutch, Spanish and Italian, plus any
locale with at least 100 Search Console impressions in the last 90 days.
Those numbers have not been pulled. To add a locale, add it to
`INDEXED_LOCALES` in `scripts/postbuild_fix.py`; the build and
`scripts/validate_locale_index.py` follow. Review in February 2027.

The indexed locales also need a person to review the translated hero and
FAQ, as D4 asks.

## Governance: the bus-factor plan

The governance page marks three items `TODO (maintainer)`: custody and
hand-over of the release keys, the domain registration and DNS, and the PyPI
and GitHub ownership transfer.
