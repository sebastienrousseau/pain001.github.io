/* Performance budgets, enforced in CI with Lighthouse (mobile emulation).
 *
 * Three routes, three thresholds each: performance score, accessibility
 * score and total transferred bytes. Timing metrics (LCP) are reported
 * but not gated, because a shared CI runner makes them noisy; bytes and
 * scores are stable. Usage: node scripts/perf_budget.mjs [origin] */
import { execFileSync } from "node:child_process";
import { readFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const ORIGIN = process.argv[2] || process.env.SITE_ORIGIN || "http://127.0.0.1:8899";
const BUDGETS = [
  { route: "/", perf: 90, a11y: 100, bytesKiB: 300 },
  { route: "/example-corpus/", perf: 90, a11y: 100, bytesKiB: 300 },
  { route: "/corpus-gb-fps-single/", perf: 90, a11y: 100, bytesKiB: 300 },
  { route: "/try/", perf: 90, a11y: 100, bytesKiB: 400 }, // before the runtime, which loads on intent
];
const chrome = process.env.CHROME_PATH || "";
const dir = mkdtempSync(join(tmpdir(), "lh-"));
let failures = 0;
for (const b of BUDGETS) {
  const out = join(dir, b.route.replace(/\W/g, "_") + ".json");
  execFileSync("npx", ["-y", "lighthouse@12", ORIGIN + b.route, "--quiet",
    "--chrome-flags=--headless=new --no-sandbox", "--only-categories=performance,accessibility",
    "--output=json", `--output-path=${out}`], { stdio: "ignore", env: { ...process.env, CHROME_PATH: chrome } });
  const r = JSON.parse(readFileSync(out, "utf8"));
  const perf = Math.round(r.categories.performance.score * 100);
  const a11y = Math.round(r.categories.accessibility.score * 100);
  const kib = Math.round(r.audits["total-byte-weight"].numericValue / 1024);
  const lcp = r.audits["largest-contentful-paint"].displayValue;
  const ok = perf >= b.perf && a11y >= b.a11y && kib <= b.bytesKiB;
  if (!ok) failures += 1;
  console.log(`${ok ? "ok  " : "FAIL"} ${b.route}  perf ${perf} (>= ${b.perf})  a11y ${a11y} (>= ${b.a11y})  ${kib} KiB (<= ${b.bytesKiB})  LCP ${lcp}`);
}
process.exit(failures ? 1 : 0);
