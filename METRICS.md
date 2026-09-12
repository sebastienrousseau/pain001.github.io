# Measurement: what is counted and how to switch it on

pain001.com counts one page view and five interactions, cookieless and without
identifiers, on the project's own host. Nothing is sent until the host exists
and the website id is set; until then the script is a no-op.

## What is counted

| Event | Fired by |
| :--- | :--- |
| page view | every page load |
| `try_run` | the demo's "Run" button (`data-track` on `#run-btn`) |
| `try_download_xml` | the demo's XML download button |
| `corpus_zip_download` | any link to `/corpus/*.zip` |
| `install_click` | any link to `https://pypi.org/project/pain001*` |
| `contact_submit` | the contact form's submit |

Do-Not-Track and Global Privacy Control switch everything off. The payload is
the page path, the referrer when it is another site, language, screen size and
title. Source: `static/js/metrics.js` and `static/js/metrics-core.js`; tests in
`tests/metrics.test.mjs`.

## Switching it on (one-time, maintainer)

1. **Host [Umami](https://umami.is/) (MIT).** Any small VM or container host
   with PostgreSQL works; the official image is `ghcr.io/umami-software/umami`.
   Set `DATABASE_URL`, `APP_SECRET`, and `DISABLE_TELEMETRY=1`. Keep it on a
   host in a jurisdiction you are comfortable naming on the privacy page.
2. **DNS.** `metrics.pain001.com` → the Umami host (CNAME or A record), with
   TLS. GitHub Pages cannot proxy, so the beacon goes to this subdomain
   directly; the site's Content-Security-Policy already allows it in
   `connect-src`.
3. **Website id.** In Umami, add the website `pain001.com` and copy its id.
   Replace the placeholder `00000000-0000-0000-0000-000000000000` in the
   `<script … data-website-id>` tag of the four layouts (`_layouts/*.html`).
4. **Rebuild and deploy.** `./build.sh`, commit `docs/`. Within a day the
   five events appear in Umami under Events; the governance page's traction
   table can then be extended from Umami's API.

Umami's own tracker script is not used: the site sends the same JSON body
Umami's `/api/send` accepts from a 40-line first-party script, so no
third-party code runs on the page.
