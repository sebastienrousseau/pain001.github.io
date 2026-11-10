<!-- SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# pain001.com events Worker

First-party, cookie-free counts of what visitors do on pain001.com
(decision D1, 10 November 2026). Page views come from Cloudflare Web
Analytics; this Worker adds a small set of named events, written to
Workers Analytics Engine.

## What it collects

One data point per accepted event:

| Field | Value |
| --- | --- |
| `blob1`, `index1` | The event name, from the allow-list below |
| `blob2` | The page path, with any query string and fragment removed |
| `blob3` | An optional short label (letters, digits, space and `._:-`, at most 64 characters), such as a sample id |
| `blob4` | The visitor's country as a two-letter code from Cloudflare, or empty |
| `double1` | `1` |

Allowed events: `hero_cta_click`, `sandbox_start`, `sandbox_xsd_run`,
`xml_copy`, `xml_download`, `install_copy`, `outbound_github`,
`outbound_pypi`, `evidence_pack_download`, `profile_guide_view`,
`adoption_form_submit`. Any other event, field or
value is refused with `400` and nothing is written.

## What it does not collect

- No IP address, user agent, referrer, cookie, local storage or
  identifier of any kind; nothing that links two events to the same
  visitor.
- No query strings or fragments: a URL's search terms or tokens are
  dropped before the path is checked.
- No payment data. The demo runs in the browser and its files never
  reach this Worker; events carry only the fields above.
- No events from visitors who send `DNT: 1` or `Sec-GPC: 1` (Do Not
  Track, Global Privacy Control): those posts are answered `204` and
  dropped, so a page cannot tell whether it was counted.
- No events from other sites: a post whose `Origin` is not
  `https://pain001.com`, or whose `Sec-Fetch-Site` is not
  `same-origin`, is dropped the same way. The Worker sends no CORS
  headers.

## Retention

Workers Analytics Engine stores data points for three months
([Cloudflare limits](https://developers.cloudflare.com/analytics/analytics-engine/limits/)),
after which they are deleted by the platform. Nothing is kept anywhere
else. The Worker's logs hold only its own error line when a write
fails, with no request data; invocation logs and traces are off.

## Requests

`POST https://pain001.com/e` with a JSON body of at most 1 KB:

```json
{"event": "sandbox_start", "page": "/try/", "label": "sepa-sct"}
```

| Response | When |
| --- | --- |
| `204` | Written, or dropped (opted out, cross-site) |
| `400` | Malformed, oversized or not allowed; no detail |
| `405` | Any method other than `POST` |
| `404` | Any path other than `/e` |

From a page, `navigator.sendBeacon("/e", JSON.stringify({...}))` sends
it without blocking navigation; the site's CSP `connect-src 'self'`
already allows the same-origin request.

## Tests

```sh
cd workers/events
npm test            # node:test with a fake Analytics Engine binding
npm run coverage    # fails below 100% line, branch and function coverage
```

The Worker has no runtime or development dependencies. CI runs the
coverage command in the Node unit-test job.

## Deploy (maintainer)

These steps change the Cloudflare account, so they are run by hand and
never from CI.

1. Analytics Engine needs no setup beyond the binding: the
   `pain001_events` dataset is created on the first write.
2. From this directory, with a Cloudflare API token that can edit
   Workers and routes on the pain001.com zone:

   ```sh
   cd workers/events
   npx wrangler@latest deploy --dry-run   # check the bundle and bindings
   npx wrangler@latest deploy
   ```

   `wrangler.jsonc` binds `EVENTS` to the `pain001_events` dataset and
   routes `pain001.com/e` to the Worker, with `workers.dev` and preview
   URLs off.
3. In the dashboard (Workers & Pages, `pain001-events`, Settings), check
   that the route `pain001.com/e` and the `EVENTS` Analytics Engine
   binding are listed.
4. Check it from a terminal:

   ```sh
   curl -si -X POST https://pain001.com/e \
     -H 'Origin: https://pain001.com' -H 'Sec-Fetch-Site: same-origin' \
     --data '{"event":"install_copy","page":"/"}' | head -1   # 204
   curl -si -X POST https://pain001.com/e --data 'x' | head -1  # 400
   ```

## Query

With an API token that has Account Analytics Read:

```sh
curl "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/analytics_engine/sql" \
  --header "Authorization: Bearer $API_TOKEN" \
  --data "SELECT blob1 AS event, SUM(_sample_interval) AS count
          FROM pain001_events
          WHERE timestamp > NOW() - INTERVAL '7' DAY
          GROUP BY event ORDER BY count DESC"
```

`_sample_interval` accounts for Analytics Engine's sampling, so the sum
is the estimated number of events.

## Privacy page wording

The privacy page can state, word for word:

> Page views are counted by Cloudflare Web Analytics, which sets no
> cookies. A few actions (starting the demo, copying the install
> command, downloading the evidence pack, following a link to GitHub or
> PyPI) are also counted by our own service on pain001.com: it records
> the action, the page path without any query string, and the country
> Cloudflare reports, and nothing else. No IP address, cookie or
> identifier is kept, nothing links one action to another, and records
> are deleted after three months. If your browser sends Do Not Track or
> Global Privacy Control, nothing is counted. Files you open in the demo
> never leave your browser.
