<!-- SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# pain001.com redirects (Cloudflare)

GitHub Pages cannot answer with a `301`, so permanent redirects for
pain001.com are Cloudflare Redirect Rules on the zone, which sits in
front of Pages. They are applied by hand; nothing here is automated.

## /enterprise/ to /for-banks/ (decision D2)

`/enterprise/` becomes `/for-banks/`. Every request under
`/enterprise/` answers `301` to the same place under `/for-banks/`,
keeping the query string. A fragment such as `#ask` never reaches the
server; the browser keeps it across the redirect, and `/for-banks/` has
no `ask` anchor, so the page opens at the top.

### Dashboard

1. pain001.com zone, Rules, Redirect Rules, Create rule.
2. Name: `enterprise to for-banks (D2)`.
3. When incoming requests match: Custom filter expression:

   ```text
   (http.host eq "pain001.com" and starts_with(http.request.uri.path, "/enterprise"))
   ```

4. Then: Dynamic redirect, status code `301`, preserve query string on,
   expression:

   ```text
   regex_replace(http.request.uri.path, "^/enterprise", "/for-banks")
   ```

5. Deploy, then check:

   ```sh
   curl -sI https://pain001.com/enterprise/ | grep -i -E '^(HTTP|location)'
   # HTTP/2 301
   # location: https://pain001.com/for-banks/
   ```

`regex_replace` in a redirect target needs a plan that offers it; if the
dashboard refuses it, use a static target instead
(`https://pain001.com/for-banks/`, `301`, preserve query string on),
which covers the only page that existed under `/enterprise/`.

### The same rule through the API

Rulesets API, phase `http_request_dynamic_redirect` on the zone (read
the existing ruleset first and add the rule to it, so other rules are
kept):

```json
{
  "description": "enterprise to for-banks (D2)",
  "expression": "(http.host eq \"pain001.com\" and starts_with(http.request.uri.path, \"/enterprise\"))",
  "action": "redirect",
  "action_parameters": {
    "from_value": {
      "status_code": 301,
      "target_url": {
        "expression": "concat(\"https://pain001.com\", regex_replace(http.request.uri.path, \"^/enterprise\", \"/for-banks\"))"
      },
      "preserve_query_string": true
    }
  },
  "enabled": true
}
```

```sh
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rulesets/phases/http_request_dynamic_redirect/entrypoint" \
  --header "Authorization: Bearer $API_TOKEN"     # read, then add the rule
```

Keep the site's own `/enterprise/` page as a plain link to
`/for-banks/` until the rule is live, so nobody lands on a 404 in
between.
