# Measurement: what is counted and how to switch it on

pain001.com counts one page view and five interactions, cookieless and without
identifiers, through GoatCounter at the project's own host. Nothing is sent
until the layout enables it; until then the script is a no-op.

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

1. **Create a [GoatCounter](https://www.goatcounter.com/) site** (open source,
   cookieless, no personal data; free for non-commercial use, paid plans for
   commercial use). Choose the code `pain001`, so the site lives at
   `pain001.goatcounter.com`.
2. **Custom domain.** In GoatCounter's settings set the custom domain to
   `metrics.pain001.com`, and add a DNS CNAME `metrics.pain001.com` →
   `pain001.goatcounter.com`. GitHub Pages cannot proxy, so the beacon goes to
   this subdomain directly; the site's Content-Security-Policy already allows
   it in `connect-src`. (Without a custom domain, set `data-host-url` to
   `https://pain001.goatcounter.com` and add that host to `connect-src` in
   the four layouts and `scripts/postbuild_fix.py`.)
3. **Enable.** In the four layouts (`_layouts/*.html`) change the metrics
   script tag's `data-enabled="false"` to `"true"`.
4. **Rebuild and deploy.** `./build.sh`, commit `docs/`. Page views appear in
   GoatCounter immediately; the five events appear under Events, named
   `try_run`, `try_download_xml`, `corpus_zip_download:<file>`,
   `install_click:<package>` and `contact_submit:<form>`.

GoatCounter's own `count.js` is not used: the site sends the same `/count`
request from a first-party script, so no third-party code runs on the page.
GoatCounter also honours Do-Not-Track on its side; the script never sends
under Do-Not-Track or Global Privacy Control.
