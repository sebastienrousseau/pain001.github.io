<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Cloudflare audit of pain001.com

Audited on 2026-11-11 against the workspace Cloudflare standard
(`~/Code/CLOUDFLARE-STANDARD.md`), read-only and from public checks only:
`curl` against the live site, `dig` against 1.1.1.1, a Python TLS
handshake per protocol version, and the standard's own verification
script (section 9). No dashboard or API access was used, and no setting
was changed. Anything the public cannot observe is listed as not
verifiable rather than assumed.

The maintainer approves Cloudflare changes separately. This file records
evidence; it does not change the zone.

## Approved deviations already in place

| Deviation | Evidence |
| :--- | :--- |
| WAF exemption for exactly `POST /e` (the events Worker in `workers/events`) | `POST /e` with `{}` returns 400 from the Worker; `PUT /e` and `POST /e/x` return 403; `POST /` returns 403 |
| 301 from `/enterprise` to `/for-banks/` | `curl -sI https://pain001.com/enterprise` returns `301`, `location: https://pain001.com/for-banks/` |

## Deviations found

| # | Standard section | Expected | Observed (public evidence) |
| :--- | :--- | :--- | :--- |
| 1 | 1, Email (Profile B: the zone receives mail through Cloudflare Email Routing) | One SPF record ending in hard fail `-all` | `dig TXT pain001.com` returns `"v=spf1 include:_spf.mx.cloudflare.net ~all"` (soft fail) |
| 2 | 1, DMARC management | `rua` limited to the zone's Cloudflare collector | `_dmarc` carries a second `rua`, `mailto:tech@pain001.com.whoisproxy.org`; the external-destination authorization record `pain001.com._report._dmarc.pain001.com.whoisproxy.org` does not resolve, so receivers that check it (RFC 7489 section 7.1) drop those reports |
| 3 | 1, Zero DNS UI warnings | Bing verification `CNAME b32854ae0fc5488b25cc5146f26bc639 -> verify.bing.com`, DNS only | The name resolves to Cloudflare anycast A records (`104.21.87.77`, `172.67.142.92`) and no CNAME is visible, which is what a proxied record returns. A random label under the zone does not resolve, so this is not a wildcard |
| 4 | 1 and 4, `doc` / `docs` hosts | `docs.` 301 to `doc.` | Reversed: `https://doc.pain001.com/` returns 301 to `https://docs.pain001.com/`, which serves the library documentation with 200. Likely intentional (the library's docs site is `docs.`); recorded so the standard and the zone can be reconciled |
| 5 | 8, `security.txt` un-obfuscated and current | `/.well-known/security.txt` is the repository's `static/security.txt` | The edge serves a different file at `/.well-known/security.txt`: `Contact: mailto:sebastian.rousseau@gmail.com`, `Expires: 2027-10-30T23:59:59Z`, `Policy: https://sebastienrousseau.com/about/#security`. `/security.txt`, built from the same source file, serves the repository version (`Contact: mailto:contact@pain001.com`, the GitHub advisory form, `Expires: 2027-09-01`). Something at the edge (consistent with Cloudflare's own security.txt feature) overrides the origin file on the RFC 9116 path, and its contact differs from `SECURITY.md` |
| 6 | 6, Static asset cache rule | Long TTLs for assets that exist | `/favicon.ico` is a 404 (the site declares `/img/pain001.svg` as its icon) and that 404 is served `cf-cache-status: HIT` with `cache-control: max-age=604800`. The cache rule applies its seven-day browser TTL to error responses too, so a missing asset that is later added stays missing in browsers for up to a week |

## Matches the standard

| Standard section | Check | Evidence |
| :--- | :--- | :--- |
| 1 | DNSSEC | `DS 2371 13 2 ...` published at the parent; `DNSKEY` present |
| 1 | DMARC policy | `v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s; pct=100`, with the Cloudflare `rua` collector |
| 1 | `*._domainkey` | `"v=DKIM1; p="` |
| 1 | GitHub Pages challenge and Google verification | `_github-pages-challenge-sebastienrousseau` TXT present; the standard's `google-site-verification=fEL-...` TXT present (a second Google token and an Ahrefs token are also present) |
| 1 | CAA | Records name `comodoca.com`, `digicert.com`, `letsencrypt.org`, `pki.goog` and `ssl.com`, the set Cloudflare manages for Universal SSL. Whether any were added by hand cannot be seen publicly |
| 2 | Always Use HTTPS | `http://pain001.com/` returns 301 to `https://pain001.com/` |
| 2 | HSTS | `max-age=31536000; includeSubDomains; preload` on every response; hstspreload.org reports `pending` |
| 2 | Minimum TLS 1.2 | A TLS 1.0/1.1 handshake is refused (`protocol version` alert); TLS 1.2 and 1.3 succeed |
| 2 | ECH | The `HTTPS` DNS record carries an ECH configuration (`cloudflare-ech.com`) and `alpn` h3, h2 |
| 3 | Six security headers | `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`, `X-Permitted-Cross-Domain-Policies` on the homepage, redirects and 403s, with the standard's values |
| 3 | Remove `X-Powered-By` | Absent |
| 4 | `www` to apex | `http://www.` goes to `https://www.` first (Always Use HTTPS), then 301 to `https://pain001.com/`: the `ssl` gate holds |
| 5 | WAF block rule | `/.env`, `/.git/config`, `/wp-login.php`, `/x.aspx` and `POST /` return 403; `OPTIONS /` is let through (405 from the origin) |
| 6 | Static asset cache rule | `/img/pain001.svg`: `cache-control: max-age=604800`, `cf-cache-status: HIT` |
| 6 | HTML respects origin headers | Pages return `cf-cache-status: DYNAMIC` with the origin's `max-age=600`, so no Cache Everything rule is in effect on HTML |
| 7 | Compression | `content-encoding: zstd` when offered, `br` when only Brotli is offered |
| 7 | Speed Brain | `speculation-rules: "/cdn-cgi/speculation"`; the endpoint returns the conservative same-origin prefetch rule |
| 7 | HTTP/3 | `alt-svc: h3=":443"` |
| 7 | Rocket Loader off | No `rocket-loader` or `data-cfasync` markers in the homepage HTML |
| 8 | Email obfuscation off | No `email-decode` script or `__cf_email__` markup in the homepage; `security.txt` contacts are not mangled |

## Not verifiable from public checks

Rate limiting (testing it means flooding the zone), URL normalization,
Security Level, Browser Integrity Check, Bot Fight Mode and AI Labyrinth,
the Cloudflare Managed Ruleset, Crawler Hints, Always Online, Tiered
Cache, Early Hints (no `103` was observed, but the origin sends no `Link`
headers for it to hint), Enhanced HTTP/2 prioritization, 0-RTT, Onion
Routing, post-quantum key exchange, the SSL mode (Full or Full strict),
registrar lock and auto-renew, whether legacy Page Rules exist, and
whether the CAA rows were added by hand. Each needs the dashboard or the
API.

## Repository text corrected by this audit

`README.md` said the edge adds `Content-Security-Policy: frame-ancestors
'none'` to every response and that a page rule caches everything with a
two-minute browser TTL. Neither is visible on 2026-11-11: no response
carries a `Content-Security-Policy` header, and HTML is served `DYNAMIC`
with the origin's `max-age=600`. The README now states what the live
headers show and points here.

## How to repeat it

Run section 9 of the standard with `DOMAIN="pain001.com"`, then:

```shell
curl -sI https://pain001.com/enterprise
curl -s -o /dev/null -w '%{http_code}\n' -X POST -H 'content-type: application/json' --data '{}' https://pain001.com/e
curl -s https://pain001.com/.well-known/security.txt
curl -s https://pain001.com/security.txt
dig +short A b32854ae0fc5488b25cc5146f26bc639.pain001.com @1.1.1.1
dig +short TYPE65 pain001.com @1.1.1.1
dig +short TXT pain001.com._report._dmarc.pain001.com.whoisproxy.org @1.1.1.1
```
