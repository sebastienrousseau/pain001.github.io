#!/usr/bin/env bash
set -euo pipefail

# Build pain001.com with Shokunin SSG, then publish the result to docs/
# (GitHub Pages serves from docs/ on the default branch).
#
#   1. `ssg build -f ssg.toml` compiles _posts/ + _layouts/ into ./Pain001
#      (ssg names the final directory after site_name, which also feeds the
#      JSON-LD publisher and llms.txt title — hence "Pain001", not "docs").
#   2. The CNAME ssg emits is a DNS zone record; GitHub Pages requires the
#      bare domain, so it is rewritten.
#   3. ./Pain001 is synced into ./docs and the staging dirs are removed.
#
# Usage: ./build.sh          (build + publish to docs/)
#        ./build.sh --audit  (build, publish, then run the ssg audit gates)

cd "$(git rev-parse --show-toplevel)"

AUDIT=0
[[ "${1:-}" == "--audit" ]] && AUDIT=1

rm -rf output Pain001

ssg build -f ssg.toml

# GitHub Pages custom-domain file must contain exactly the apex domain.
printf 'pain001.com\n' > Pain001/CNAME

# GitHub Pages runs Jekyll by default, and Jekyll drops underscore-prefixed
# paths — which 404s every fingerprinted /_csp/* asset. Opt out entirely.
touch Pain001/.nojekyll

# Repair the ssg output: unescape entity-escaped head metas and content
# bodies, patch CSP/og:image into the generated tag pages, and regenerate
# the sitemap. See scripts/postbuild_fix.py for the why of each pass.
python3 scripts/postbuild_fix.py Pain001

# Self-hosted WASM engine for /try/ (Pyodide + xmlschema + official XSD).
# Served same-origin so the strict CSP needs no third-party carve-outs;
# downloaded by the browser only when the visitor asks for the XSD gate.
rsync -a static/pyodide/ Pain001/pyodide/

# Publish: replace docs/ content with the fresh build (keep the dir itself).
rsync -a --delete --exclude '.ssg-cache' Pain001/ docs/

rm -rf output Pain001

if [[ "$AUDIT" == "1" ]]; then
  ssg audit -f ssg.toml -o docs --severity warn
fi

echo "Build published to docs/."
