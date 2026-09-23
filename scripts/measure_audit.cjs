#!/usr/bin/env node
/* Reading-measure audit: every built page, in real Chrome, at phone,
 * tablet, laptop and desktop widths. The layout audit catches cropping,
 * overflow and misalignment; this one catches the opposite failure, a
 * page whose text is technically fine but squashed: a reading column
 * that uses under half of its container on a laptop, a title wrapped
 * over three or more lines, a paragraph narrower than a phone screen on
 * a desktop, or a page that scrolls sideways.
 *
 * Usage: SITE_ORIGIN=http://127.0.0.1:8899 node scripts/measure_audit.cjs [--all]
 * Without --all it audits one page per layout family plus every English
 * page (fast); with --all it audits all 668 pages. Exits 1 on a finding. */
const { createRequire } = require("node:module");
const fs = require("node:fs");
const pathModule = require("node:path");
const toolsDir = process.env.A11Y_MODULES ?? __dirname + "/../.a11y-tools/";
let pc;
try { pc = createRequire(toolsDir + "resolve.cjs")("puppeteer-core"); }
catch { console.error("puppeteer-core not found under .a11y-tools; see layout_audit.cjs"); process.exit(2); }

function findChrome() {
  for (const c of [process.env.CHROME_PATH, "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium-browser", "/usr/bin/chromium"]) {
    try { if (c && fs.existsSync(c)) return c; } catch {}
  }
  console.error("No Chrome found; set CHROME_PATH"); process.exit(2);
}
const ORIGIN = process.env.SITE_ORIGIN ?? "http://127.0.0.1:8899";
const SITE = pathModule.resolve(__dirname, "..", "site");
const ALL = process.argv.includes("--all");
const WIDTHS = [390, 820, 1440, 1920];
const CONCURRENCY = Number(process.env.CONCURRENCY ?? 4);

function pages() {
  const out = [];
  (function walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = pathModule.join(dir, e.name);
      if (e.isDirectory()) { if (!e.name.startsWith(".") && e.name !== "_csp") walk(p); }
      else if (e.name === "index.html") out.push("/" + pathModule.relative(SITE, dir).split(pathModule.sep).join("/").replace(/^\.$/, "") + (dir === SITE ? "" : "/"));
    }
  })(SITE);
  out.sort();
  if (ALL) return out;
  // English pages plus one locale copy per family: /<locale>/… is a copy of the English page.
  const locale = /^\/[a-z]{2}(-[a-z]+)?\//;
  const en = out.filter((p) => !locale.test(p) && !/^\/[a-z]{2}-corpus-/.test(p));
  const sample = out.filter((p) => /^\/(fr|ar|zh-hans)\//.test(p)).filter((p, i) => i % 9 === 0);
  return [...en, ...sample];
}

const probe = (vw) => {
  const root = document.querySelector("main") || document.body;
  const container = root.querySelector(".container") || root;
  const cw = container.getBoundingClientRect().width;
  // Only article pages have a reading column; grid layouts (home,
  // enterprise, comparison) are judged on overflow and narrow blocks alone.
  const column = root.querySelector(".content-body");
  const colw = column ? column.getBoundingClientRect().width : cw;
  const h1 = document.querySelector(".page-hero h1"); // the home hero is a headline, not a title
  let h1Lines = 0;
  if (h1) {
    const cs = getComputedStyle(h1);
    const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
    h1Lines = Math.round(h1.getBoundingClientRect().height / lh);
  }
  const narrow = [];
  const inScrollBox = (el) => {
    for (let a = el.parentElement; a && a !== root; a = a.parentElement) {
      const o = getComputedStyle(a).overflowX;
      if ((o === "auto" || o === "scroll") && a.scrollWidth > a.clientWidth + 1) return true;
    }
    return false;
  };
  for (const el of root.querySelectorAll("p, li:not(nav li), td, th, dd")) {
    const r = el.getBoundingClientRect();
    // A cell in a table that scrolls sideways is governed by the layout
    // audit's scroll-box rules, not by this one.
    const cell = el.tagName === "TD" || el.tagName === "TH";
    const floor = cell ? 144 : (vw >= 1024 ? 240 : 200); // 9rem per column; a phone's width for prose
    if (r.width > 0 && r.height > 0 && (el.textContent || "").trim().length > 40 && r.width < floor && !inScrollBox(el)) {
      narrow.push({ tag: el.tagName.toLowerCase(), w: Math.round(r.width), text: (el.textContent || "").trim().slice(0, 40) });
      if (narrow.length >= 4) break;
    }
  }
  return {
    container: Math.round(cw), column: Math.round(colw), ratio: cw ? Math.round((colw / cw) * 100) / 100 : 1,
    h1Lines, narrow, docOverflow: document.documentElement.scrollWidth - window.innerWidth,
    family: column ? "article" : ((root.firstElementChild || {}).className || "grid").split(/\s+/)[0],
  };
};

(async () => {
  const list = pages();
  const browser = await pc.launch({ executablePath: findChrome(), headless: "new", args: ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"] });
  const rows = [];
  let next = 0;
  async function worker() {
    const page = await browser.newPage();
    while (next < list.length) {
      const path = list[next++];
      for (const vw of WIDTHS) {
        try {
          await page.setViewport({ width: vw, height: 900 });
          await page.goto(ORIGIN + path, { waitUntil: "domcontentloaded", timeout: 30000 });
          rows.push({ path, vw, ...(await page.evaluate(probe, vw)) });
        } catch (e) { rows.push({ path, vw, error: String(e.message).slice(0, 90) }); }
      }
    }
    await page.close();
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  await browser.close();
  if (process.env.MEASURE_OUT) fs.writeFileSync(process.env.MEASURE_OUT, rows.map((r) => JSON.stringify(r)).join("\n") + "\n");

  // Findings. Thresholds: a reading column under 55% of its container at
  // laptop width and above is squashed; a title on three or more lines at
  // laptop width is squashed; any paragraph narrower than a phone; any
  // sideways scroll at any width.
  const findings = [];
  for (const r of rows) {
    if (r.error) { findings.push(`${r.path} @${r.vw}: ${r.error}`); continue; }
    if (r.vw >= 1440 && r.ratio < 0.55) findings.push(`${r.path} @${r.vw}: reading column ${r.column}px is ${Math.round(r.ratio * 100)}% of its ${r.container}px container`);
    if (r.vw >= 1440 && r.h1Lines >= 3) findings.push(`${r.path} @${r.vw}: title wraps over ${r.h1Lines} lines`);
    if (r.narrow.length) findings.push(`${r.path} @${r.vw}: ${r.narrow.length} squashed block(s), e.g. <${r.narrow[0].tag}> ${r.narrow[0].w}px "${r.narrow[0].text}"`);
    if (r.docOverflow > 1) findings.push(`${r.path} @${r.vw}: page scrolls sideways by ${r.docOverflow}px`);
  }
  // Family summary at laptop width, so the shape of every layout is visible at a glance.
  const fam = new Map();
  for (const r of rows.filter((r) => !r.error && r.vw === 1440)) {
    const f = fam.get(r.family) || { n: 0, minRatio: 1, maxH1: 0, example: r.path };
    f.n += 1; f.minRatio = Math.min(f.minRatio, r.ratio); f.maxH1 = Math.max(f.maxH1, r.h1Lines); fam.set(r.family, f);
  }
  console.log(`${rows.length} measurements over ${list.length} page(s) at ${WIDTHS.join("/")}px`);
  console.log("layout families at 1440px (pages, narrowest column ratio, most title lines, example):");
  for (const [k, f] of [...fam.entries()].sort((a, b) => a[1].minRatio - b[1].minRatio)) console.log(`  ${f.n.toString().padStart(4)}  ${f.minRatio.toFixed(2)}  ${f.maxH1}  ${f.example}  [${k.slice(0, 60)}]`);
  const shown = findings.slice(0, 40);
  for (const f of shown) console.log("  - " + f);
  if (findings.length > shown.length) console.log(`  … and ${findings.length - shown.length} more`);
  console.log(findings.length ? `result: ${findings.length} finding(s)` : "result: CLEAN");
  process.exit(findings.length ? 1 : 0);
})();
