#!/usr/bin/env node
/*
 * Local structural accessibility pre-flight, driven by Lightpanda.
 *
 * WHAT THIS IS NOT
 * ----------------
 * This is not the accessibility gate. The gate is pa11y-ci under real
 * Chrome, in .github/workflows/ci.yml, and only that result counts.
 *
 * Lightpanda has no layout or cascade engine. getComputedStyle echoes
 * inline styles back and nothing else: a stylesheet rule never appears,
 * backgroundColor comes back transparent, fontSize comes back empty,
 * and getBoundingClientRect returns a stub 5x5 box. HTML_CodeSniffer's
 * contrast algorithm needs a real font-size and a resolved background,
 * so it SKIPS the element rather than failing. Measured: a page whose
 * only defect is 1.6:1 grey-on-white reports zero issues here.
 *
 * So a clean run means "no structural violations found". It does not
 * mean the page passes WCAG, and it never means the contrast is fine —
 * the failure mode this repo has actually shipped before (two sub-7:1
 * widget labels) is exactly the one this cannot see.
 *
 * WHAT IT IS FOR
 * --------------
 * Catching missing alt text, unlabelled inputs, empty links, bad
 * heading order, missing lang, and table-header problems in seconds,
 * on a machine where Chrome will not launch. Run it before pushing;
 * let CI have the final word.
 *
 * Usage:
 *   lightpanda serve --host 127.0.0.1 --port 9222 &
 *   (cd docs && python3 -m http.server 8899 &)
 *   node scripts/a11y_local.mjs            # the .pa11yci URL list
 *   node scripts/a11y_local.mjs /fr/try/   # one or more paths
 *
 * One-time setup (the repo intentionally has no package.json, so the
 * tools live in a gitignored corner rather than becoming a project
 * dependency CI would have to install):
 *
 *   mkdir -p .a11y-tools && cd .a11y-tools
 *   echo '{"name":"pain001-a11y-tools","private":true}' > package.json
 *   PUPPETEER_SKIP_DOWNLOAD=1 npm install pa11y@8 puppeteer-core@23
 *
 * PUPPETEER_SKIP_DOWNLOAD matters: pa11y depends on full puppeteer,
 * which otherwise downloads the Chromium this whole exercise avoids.
 */
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";

const toolsDir = process.env.A11Y_MODULES ?? new URL("../.a11y-tools/", import.meta.url).pathname;
let pa11y, puppeteer;
try {
  const req = createRequire(toolsDir + "resolve.cjs");
  pa11y = req("pa11y");
  puppeteer = req("puppeteer-core");
} catch {
  console.error(`pa11y/puppeteer-core not found under ${toolsDir}`);
  console.error("Run the one-time setup in this file's header.");
  process.exit(2);
}

const CDP = process.env.LIGHTPANDA_CDP ?? "ws://127.0.0.1:9222/";
const ORIGIN = process.env.SITE_ORIGIN ?? "http://127.0.0.1:8899";

function targets() {
  const args = process.argv.slice(2);
  if (args.length) return args.map((a) => (a.startsWith("http") ? a : ORIGIN + a));
  return JSON.parse(readFileSync(new URL("../.pa11yci", import.meta.url), "utf8")).urls;
}

const urls = targets();
console.log(
  `Structural pre-flight only — contrast is NOT checked (see the header\n` +
    `of this script). CI's pa11y-ci under Chrome is the real gate.\n`,
);

let browser;
try {
  browser = await puppeteer.connect({ browserWSEndpoint: CDP, defaultViewport: null });
} catch (e) {
  console.error(`Cannot reach Lightpanda at ${CDP} — is "lightpanda serve" running?`);
  console.error(String(e.message));
  process.exit(2);
}

let total = 0;
let errored = 0;
const started = Date.now();
for (const url of urls) {
  const page = await browser.newPage();
  try {
    const res = await pa11y(url, { browser, page, standard: "WCAG2AAA", timeout: 25000 });
    total += res.issues.length;
    const label = url.replace(ORIGIN, "") || "/";
    console.log(`${res.issues.length ? "FAIL" : " ok "} ${String(res.issues.length).padStart(3)}  ${label}`);
    for (const i of res.issues) console.log(`        ${i.code}\n        ${i.selector}`);
  } catch (e) {
    errored++;
    console.log(`ERR       ${url.replace(ORIGIN, "")} — ${String(e.message).slice(0, 70)}`);
  } finally {
    await page.close().catch(() => {});
  }
}
await browser.disconnect();

const secs = ((Date.now() - started) / 1000).toFixed(1);
console.log(`\n${urls.length} url(s), ${total} structural issue(s), ${errored} error(s), ${secs}s`);
// An unreachable page is a failure; a clean structural run is not a pass.
process.exit(total || errored ? 1 : 0);
