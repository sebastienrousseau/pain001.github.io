#!/usr/bin/env node
/*
 * Run the real accessibility gate locally, against installed Chrome.
 *
 * This mirrors the CI step (pa11y-ci, WCAG2AAA, the .pa11yci URL list)
 * rather than approximating it, so a clean run here means the same
 * thing CI means. Use it before pushing; CI still has the final word.
 *
 * Why an explicit executablePath: `npx -y pa11y@8` resolves its own
 * puppeteer and tries to launch a bundled Chromium, which on this
 * machine dies with "spawn Unknown system error -88". Pointing pa11y at
 * the installed Chrome avoids that entirely — the browser was never the
 * problem, the bundled download was. Override with CHROME_PATH.
 *
 * One-time setup (the repo intentionally has no package.json, so the
 * tools live in a gitignored corner rather than becoming a dependency
 * CI would have to install):
 *
 *   mkdir -p .a11y-tools && cd .a11y-tools
 *   echo '{"name":"pain001-a11y-tools","private":true}' > package.json
 *   PUPPETEER_SKIP_DOWNLOAD=1 npm install pa11y@8 puppeteer-core@23
 *
 * PUPPETEER_SKIP_DOWNLOAD matters: pa11y depends on full puppeteer,
 * which otherwise downloads a Chromium that will not run here anyway.
 *
 * Usage:
 *   (cd docs && python3 -m http.server 8899 &)
 *   node scripts/a11y_local.mjs            # the .pa11yci URL list
 *   node scripts/a11y_local.mjs /fr/try/   # one or more paths
 */
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";

const CHROME =
  process.env.CHROME_PATH ??
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const ORIGIN = process.env.SITE_ORIGIN ?? "http://127.0.0.1:8899";
const toolsDir =
  process.env.A11Y_MODULES ?? new URL("../.a11y-tools/", import.meta.url).pathname;

let pa11y;
try {
  pa11y = createRequire(toolsDir + "resolve.cjs")("pa11y");
} catch {
  console.error(`pa11y not found under ${toolsDir}`);
  console.error("Run the one-time setup in this file's header.");
  process.exit(2);
}

const args = process.argv.slice(2);
const urls = args.length
  ? args.map((a) => (a.startsWith("http") ? a : ORIGIN + a))
  : JSON.parse(readFileSync(new URL("../.pa11yci", import.meta.url), "utf8")).urls;

const options = {
  standard: "WCAG2AAA",
  timeout: 30000,
  wait: 500,
  chromeLaunchConfig: {
    executablePath: CHROME,
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  },
};

let total = 0;
let errored = 0;
const started = Date.now();
for (const url of urls) {
  try {
    const res = await pa11y(url, options);
    total += res.issues.length;
    console.log(
      `${res.issues.length ? "FAIL" : " ok "} ${String(res.issues.length).padStart(3)}  ${url.replace(ORIGIN, "") || "/"}`,
    );
    for (const i of res.issues) {
      console.log(`        ${i.code}`);
      console.log(`        ${i.selector}`);
      console.log(`        ${i.message.slice(0, 120)}`);
    }
  } catch (e) {
    errored++;
    console.log(`ERR       ${url.replace(ORIGIN, "")} — ${String(e.message).slice(0, 80)}`);
  }
}

const secs = ((Date.now() - started) / 1000).toFixed(1);
console.log(`\n${urls.length} url(s), ${total} issue(s), ${errored} error(s), ${secs}s`);
process.exit(total || errored ? 1 : 0);
