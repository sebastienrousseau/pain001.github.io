# Security review, September 2026

| | |
| --- | --- |
| Date | 26 September 2026 |
| Scope | pain001.com as built from `main` at v0.0.9, its build and release pipeline, and its GitHub configuration |
| Measured against | the security requirements and trust boundaries in [assurance-case.md](assurance-case.md) |
| Reviewer | The maintainer, assisted by an AI coding assistant (Claude). **This is not an independent review**: the reviewer also works on the code under review. An independent review is planned in `ROADMAP.md`, Phase G. |

## Method

1. Read every script the site ships (`static/js/`, `static/sw.js`) for
   DOM injection sinks, redirect targets, network calls and storage use.
2. Read the Content-Security-Policy and the HTTP response headers the
   live site sends.
3. Read every workflow for token permissions, untrusted triggers and
   untrusted input reaching a shell.
4. Traced every build input to its integrity check.
5. Built the same commit twice and compared every output file.
6. Checked the repository's GitHub security settings.

## Findings

| ID | Severity | Finding | Status |
| --- | --- | --- | --- |
| SR-1 | Medium | Private vulnerability reporting is disabled on the repository, while `SECURITY.md` directs reporters to it. Reporters fall back to e-mail, which works but is not what the policy promises. | Open: the owner enables it in the repository settings. |
| SR-2 | Low | Secret scanning and push protection are disabled. A scan of all 128 commits for common credential patterns found nothing, and the site stores no long-lived secrets. | Open: the owner enables both in the repository settings. |
| SR-3 | Low | `scripts/carry_forward_assets.py` republishes the previous deploy's assets downloaded from the live site without an integrity check; their fingerprints are not content hashes. The source is the site's own origin over HTTPS, and the files are reached only by HTML cached for about ten minutes. | Accepted for deploys. Release builds (`SOURCE_DATE_EPOCH` set) no longer fetch anything. |
| SR-4 | Low | ssg writes an invalid `news-sitemap.xml` into every page directory, 385 files publicly served with an empty `<loc>` and the build time, which also made builds non-reproducible. | Fixed: the post-build pass removes them; the root news sitemap is kept. |
| SR-5 | Low | The SBOM's `metadata.timestamp` was the build time, so the SBOM differed between two builds of one commit. | Fixed: it is set to `SOURCE_DATE_EPOCH` or the commit time. |
| SR-6 | Info | `static/sw.js` still told contributors to bump the cache name by hand, although the build has derived it from a content hash since the fix for this. | Fixed: the comment describes the build step. |
| SR-7 | Info | Python and JavaScript sources were not linted in CI. | Fixed in v0.0.10: ruff and ESLint run in CI. |

## What was checked and found sound

- **Injection.** The shipped scripts write visitor data only with
  `textContent`; `innerHTML` is used only to clear elements. No `eval`,
  `new Function`, `document.write` or string timers.
- **Redirects.** `redirect.js` can only send a visitor to a same-origin
  path from a build-time map.
- **CSP.** `default-src 'self'`, no inline script except one by hash,
  `object-src 'none'`, `base-uri 'self'`, `connect-src` limited to the site
  and `cloudflareinsights.com`, and `form-action` limited to the site and
  `formspree.io`. `wasm-unsafe-eval` is required by Pyodide.
- **Headers.** HSTS, `X-Frame-Options: DENY`, `frame-ancestors 'none'` and
  `X-Content-Type-Options: nosniff`.
- **Service worker.** Caches only same-origin demo assets; every other
  request passes to the network untouched.
- **Workflows.** Read-only by default with per-job write scopes; no
  `pull_request_target`; dispatch input reaches scripts through
  environment variables and is validated before use.
- **Dependencies.** Hash-pinned pip installs, an npm lockfile with no
  audit findings, SHA-pinned actions, and a SHA-256 check on every demo
  runtime file.
- **Releases.** Signed tags verified in CI, Sigstore-signed provenance and
  SBOM attestations, and a reproducibility check on each release archive.

## Next review

After any change to the trust boundaries in the assurance case, and in
any case within twelve months. The independent review in Phase G replaces
this one when it happens.
