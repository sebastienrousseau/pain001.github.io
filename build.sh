#!/usr/bin/env bash
set -euo pipefail

# Build pain001.com with the Static Site Generator (ssg), then publish the result to site/
# (GitHub Pages deploys this directory as the checked workflow artefact).
#
#   1. `ssg build -f ssg.toml` compiles _posts/ + _layouts/ into ./Pain001
#      (ssg names the final directory after site_name, which also feeds the
#      JSON-LD publisher and llms.txt title — hence "Pain001", not "site").
#   2. The CNAME ssg emits is a DNS zone record; GitHub Pages requires the
#      bare domain, so it is rewritten.
#   3. ./Pain001 is synced into ./site and the staging dirs are removed.
#
# Usage: ./build.sh          (build + publish to site/)
#        ./build.sh --audit  (build, publish, then run the ssg audit gates)

cd "$(git rev-parse --show-toplevel)"

AUDIT=0
[[ "${1:-}" == "--audit" ]] && AUDIT=1

# One build at a time. ssg deletes Pain001/ and renames output/ onto it,
# and nothing inside it writes after it exits (its threads are joined), so
# the only way `rm -rf` here or ssg's own remove can fail with "Directory
# not empty" is a second writer in the same tree: a build started twice,
# or Finder and Spotlight dropping .DS_Store into a directory being
# removed. The lock stops the first; the retry below absorbs the second.
LOCK=.build.lock
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "build.sh: another build holds $LOCK (remove it if no build is running)" >&2
  exit 1
fi
trap 'rmdir "$LOCK" 2>/dev/null || true' EXIT

clean_staging() {
  rm -rf output Pain001 2>/dev/null || { sleep 1; rm -rf output Pain001; }
}

clean_staging

# The demo's WebAssembly runtime and wheels are not committed: fetch them
# from their upstream URLs and refuse any byte that does not match the
# SHA-256 pinned in static/pyodide/pain001-runtime.json (see the script).
python3 scripts/fetch_runtime.py

python3 scripts/traction.py
ssg build -f ssg.toml

# GitHub Pages custom-domain file must contain exactly the apex domain.
printf 'pain001.com\n' > Pain001/CNAME

# GitHub Pages runs Jekyll by default, and Jekyll drops underscore-prefixed
# paths — which 404s every fingerprinted /_csp/* asset. Opt out entirely.
touch Pain001/.nojekyll

# ssg's CycloneDX SBOM has no serialNumber, and GitHub's attestation action
# refuses to recognise the format without one, which is what stopped v0.0.4
# publishing. Derived, not random, so rebuilds stay byte-identical.
python3 scripts/sbom_serial.py Pain001

# Repair the ssg output: unescape entity-escaped head metas and content
# bodies, patch CSP/og:image into the generated tag pages, and regenerate
# the sitemap. See scripts/postbuild_fix.py for the why of each pass.
python3 scripts/postbuild_fix.py Pain001

# Static assets that mirror the site root: the self-hosted WASM engine
# for /try/ (Pyodide + xmlschema + official XSD, same-origin so the CSP
# needs no third-party carve-outs), the demo's ES module (/js/), and the
# demo-scoped service worker (/sw.js) that makes /try/ work offline.
rsync -a static/ Pain001/

# RFC 9116 location. static/security.txt replaces the generator's empty
# file in the rsync above, so the .well-known copy is made here, after it;
# made any earlier, it copied the empty file.
mkdir -p Pain001/.well-known
cp Pain001/security.txt Pain001/.well-known/security.txt

# Preserve the authored PRISM/adapter separation in source, but publish a
# single SRI-protected stylesheet per layout to eliminate render-blocking
# request chains on mobile.
python3 scripts/postbuild_fix.py Pain001 --optimise-assets

# Downloadable sample CSVs, generated from the demo module's SAMPLES so
# the files users download are byte-identical to what "Load a sample"
# loads — one source of truth, no drift.
node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON scripts/gen_samples.mjs Pain001/samples

# Derive the service worker's cache name from the bytes it caches,
# so a change to /try/ can never be invisible to a returning visitor.
# Runs here because everything the worker caches — sw.js and /js/ and
# /pyodide/ from the rsync, /samples/ from the line above — only
# exists in the output by this point. The main postbuild pass is too
# early: it would find no sw.js and silently stamp nothing.
python3 scripts/postbuild_fix.py Pain001 --stamp-sw

# Carry the previous deploy's fingerprinted assets forward. Browsers and
# CDN edges cache HTML for up to ~10 minutes; if a rebuild deleted the old
# /_csp/<hash> files, every cached page 404'd its CSS/JS during that
# window on each deploy. Old hashes are tiny; keep them alongside the new.
if [ -d site/_csp ]; then
  rsync -a --ignore-existing site/_csp/ Pain001/_csp/
fi
# site/ is no longer committed: in CI there is no previous build to copy
# from, so the assets the live pages reference are fetched instead.
python3 scripts/carry_forward_assets.py Pain001

# Publish: replace site/ content with the fresh build (keep the dir itself).
# site/ is untracked; CI uploads it as the Pages artifact.
mkdir -p site
rsync -a --delete --exclude '.ssg-cache' Pain001/ site/

clean_staging

if [[ "$AUDIT" == "1" ]]; then
  ssg audit -f ssg.toml -o site --severity warn
fi

echo "Build published to site/."
