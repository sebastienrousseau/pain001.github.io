#!/usr/bin/env bash
set -euo pipefail
# Refresh the vendored Cloudflare Web Analytics beacon (see METRICS.md).
# Served from this origin so the CSP keeps script-src 'self' and the audit's
# SRI gate holds; Cloudflare publishes no SRI hash and replaces the file
# without notice, so a pinned hash would silently stop measurement.
cd "$(git rev-parse --show-toplevel)"
curl -fsSL https://static.cloudflareinsights.com/beacon.min.js -o static/js/cf-beacon.min.js
printf 'version %s  sha256 %s\n' "$(grep -o '"20[0-9][0-9]\.[0-9]*\.[0-9]*"' static/js/cf-beacon.min.js | head -1)" \
  "$(shasum -a 256 static/js/cf-beacon.min.js | cut -d' ' -f1)"
