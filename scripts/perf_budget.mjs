/* Lighthouse quality gate for every PRISM page type.
 *
 * Every audited route must score exactly 100 in all four public Lighthouse
 * categories on every profile: mobile, tablet, desktop, 4K and 8K. The
 * routes cover each layout and generator (home, article, reference, spec,
 * corpus, comparison, enterprise, taxonomy, a left-to-right and a
 * right-to-left locale, the demo). Transfer budgets remain an additional
 * guard against performance regressions.
 * Usage: node scripts/perf_budget.mjs [origin]
 */
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const origin = process.argv[2] || process.env.SITE_ORIGIN || "http://127.0.0.1:8899";
const allBudgets = [
  { route: "/", bytesKiB: 300 },
  { route: "/documentation/", bytesKiB: 300 },
  { route: "/compliance-toolkit/", bytesKiB: 300 },
  { route: "/example-corpus/", bytesKiB: 300 },
  { route: "/try/", bytesKiB: 400 },
  { route: "/why/", bytesKiB: 300 },
  { route: "/enterprise/", bytesKiB: 300 },
  { route: "/competitors-comparison/", bytesKiB: 300 },
  { route: "/message-spec-pain.001.001.09/", bytesKiB: 400 },
  { route: "/corpus-gb-fps-single/", bytesKiB: 300 },
  { route: "/tags/iso-20022/", bytesKiB: 300 },
  { route: "/fr/", bytesKiB: 300 },
  { route: "/ar/", bytesKiB: 300 },
];
/* Large screens use Lighthouse's desktop settings (throttling, form
   factor) with the emulated screen overridden. 4K and 8K are at a device
   pixel ratio of 1, the worst case for layout: the most CSS pixels. */
const screens = {
  tablet: ["--formFactor=mobile", "--screenEmulation.mobile", "--screenEmulation.width=820", "--screenEmulation.height=1180", "--screenEmulation.deviceScaleFactor=2"],
  "desktop-4k": ["--preset=desktop", "--screenEmulation.width=3840", "--screenEmulation.height=2160", "--screenEmulation.deviceScaleFactor=1"],
  "desktop-8k": ["--preset=desktop", "--screenEmulation.width=7680", "--screenEmulation.height=4320", "--screenEmulation.deviceScaleFactor=1"],
};
const selectedRoutes = (process.env.LIGHTHOUSE_ROUTES || "").split(",").filter(Boolean);
const budgets = selectedRoutes.length
  ? allBudgets.filter((budget) => selectedRoutes.includes(budget.route))
  : allBudgets;
const profiles = (process.env.LIGHTHOUSE_PROFILES || "mobile,tablet,desktop,desktop-4k,desktop-8k").split(",").filter(Boolean);
const localCli = resolve(".a11y-tools/node_modules/.bin/lighthouse");
const hasLocalCli = existsSync(localCli);
const command = hasLocalCli ? localCli : "npx";
const commandPrefix = hasLocalCli ? [] : ["-y", "lighthouse@12.8.2"];
const dir = mkdtempSync(join(tmpdir(), "pain001-lighthouse-"));
let failures = 0;

for (const profile of profiles) {
  for (const budget of budgets) {
    const stem = `${profile}-${budget.route.replace(/\W/g, "_") || "home"}`;
    const out = join(dir, `${stem}.json`);
    const args = [
      ...commandPrefix,
      origin + budget.route,
      "--quiet",
      "--chrome-flags=--headless=new --no-sandbox --disable-dev-shm-usage",
      "--only-categories=performance,accessibility,best-practices,seo",
      "--output=json",
      `--output-path=${out}`,
    ];
    if (profile === "desktop") args.push("--preset=desktop");
    if (screens[profile]) args.push(...screens[profile]);
    execFileSync(command, args, { stdio: "ignore", env: process.env });

    const report = JSON.parse(readFileSync(out, "utf8"));
    const scores = Object.fromEntries(
      ["performance", "accessibility", "best-practices", "seo"].map((name) => [
        name,
        Math.round(report.categories[name].score * 100),
      ]),
    );
    const kib = Math.round(report.audits["total-byte-weight"].numericValue / 1024);
    const scoresPerfect = Object.values(scores).every((score) => score === 100);
    const ok = scoresPerfect && kib <= budget.bytesKiB;
    if (!ok) failures += 1;
    console.log(
      `${ok ? "ok  " : "FAIL"} ${profile.padEnd(10)} ${budget.route}  ` +
      `perf ${scores.performance}  a11y ${scores.accessibility}  ` +
      `best ${scores["best-practices"]}  seo ${scores.seo}  ` +
      `${kib} KiB (<= ${budget.bytesKiB})`,
    );
    if (!scoresPerfect) {
      for (const audit of Object.values(report.audits)) {
        if (audit.scoreDisplayMode !== "notApplicable" && audit.score !== null && audit.score < 1) {
          console.log(`      ${audit.id}: ${audit.title} (${audit.displayValue || audit.score})`);
        }
      }
    }
  }
}
process.exit(failures ? 1 : 0);
