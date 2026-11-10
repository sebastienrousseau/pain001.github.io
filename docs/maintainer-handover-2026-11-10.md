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

Deployed on 10 November 2026 from `workers/events/src/index.js` (byte
for byte) as `pain001-events` in the account that holds the pain001.com
zone: route `pain001.com/e`, Analytics Engine binding `EVENTS` to dataset
`pain001_events`, invocation logs off, workers.dev and preview URLs off.
The zone's custom rule "Block Exploit Scanners and Unsafe HTTP Methods"
blocked every POST, so it now exempts exactly `POST /e`; every other
non-GET request is still blocked. A later `npx wrangler deploy` from
`workers/events/` applies the same settings.

## Search Console: the indexed locales

D4 indexes English, French, German, Dutch, Spanish and Italian, plus any
locale with at least 100 Search Console impressions in the last 90 days.
On 10 November 2026 (last 3 months, web search, summed over each
locale's pages) twenty more qualified: pl 1541, sv 1068, ja 1005, ru 648,
ko 366, zh-hant 335, yo 322, ms 321, cs 298, tr 288, pt-br 251, fa 246,
zh-hans 238, ar 215, th 198, hu 195, vi 173, id 166, he 111, el 108.
Under 100: uk 69, bn 62, hi 55, ro 46, ha 31, ta 17, te 12, mr 9, fil 0.
They are in `INDEXED_LOCALES` in `scripts/postbuild_fix.py`. Review in
February 2027.

The indexed locales also need a person to review the translated hero and
FAQ, as D4 asks.

## Governance: the bus-factor plan

The governance page marks three items "Not yet arranged": custody and
hand-over of the release keys, the domain registration and DNS, and the PyPI
and GitHub ownership transfer. The maintainer decided on 10 November 2026 not
to arrange them yet, and that there is no long-term-support line at present.
