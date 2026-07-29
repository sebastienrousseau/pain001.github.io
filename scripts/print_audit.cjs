/*
 * Print/PDF audit.
 *
 * Renders each page with print media emulated at the real A4 content
 * width (210mm minus the @page margins) and looks for the things that
 * ruin a printed page: content wider than the sheet, scroll boxes
 * (which crop rather than scroll on paper), and headings or table rows
 * that would be split across a page boundary.
 *
 * A4 = 210mm; at 96 CSS px/in that is 793.7px. The stylesheet uses
 * 18mm margins, leaving 174mm = 657.6px of content.
 */
const { createRequire } = require("node:module");
// puppeteer-core lives in the gitignored .a11y-tools/ so it never becomes
// a project dependency; CI installs it there too. See scripts/a11y_local.mjs.
const toolsDir = process.env.A11Y_MODULES ?? __dirname + "/../.a11y-tools/";
let pc;
try {
  pc = createRequire(toolsDir + "resolve.cjs")("puppeteer-core");
} catch {
  console.error(`puppeteer-core not found under ${toolsDir}`);
  console.error("  mkdir -p .a11y-tools && cd .a11y-tools");
  console.error("  echo '{\"name\":\"a11y-tools\",\"private\":true}' > package.json");
  console.error("  PUPPETEER_SKIP_DOWNLOAD=1 npm install puppeteer-core@23");
  process.exit(2);
}
const fs = require("node:fs");

const fs2 = require("node:fs");
// GitHub runners have Chrome at /usr/bin/google-chrome; macOS has the app
// bundle. pa11y's own bundled Chromium will not launch on this Mac, which
// is why every browser check here points at an installed Chrome.
function findChrome() {
  const candidates = [
    process.env.CHROME_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
  ].filter(Boolean);
  for (const c of candidates) { try { if (fs2.existsSync(c)) return c; } catch {} }
  throw new Error("no Chrome found; set CHROME_PATH");
}
const CHROME = findChrome();
const ORIGIN = process.env.SITE_ORIGIN ?? "http://127.0.0.1:8899";
const OUT = process.env.OUT ?? "/tmp/print.jsonl";
const MM = 96 / 25.4;
const MARGIN_MM = Number(process.env.MARGIN_MM ?? 18);
const CONTENT_PX = Math.round((210 - 2 * MARGIN_MM) * MM);
const PAGE_H_PX = Math.round((297 - 2 * MARGIN_MM) * MM);

const PAGES = process.env.PAGES
  ? process.env.PAGES.split(",")
  : [
      "/", "/executive-brief/", "/documentation/", "/installation/", "/faqs/",
      "/glossary/", "/message-specs/", "/message-spec-pain.001.001.13/",
      "/message-spec-pain.001.001.13-types/", "/message-spec-code-lists/",
      "/compatibility/", "/pain002-reason-codes/", "/competitors-comparison/",
      "/trust/", "/try/", "/contact/", "/fr/executive-brief/", "/tags/iso-20022/",
    ];

function probe(contentPx, pageH) {
  const out = { tooWide: [], scrollBoxes: [], splits: [], docWidth: 0 };
  const sel = (el) => {
    if (el.id) return "#" + el.id;
    const c = typeof el.className === "string" && el.className.trim()
      ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".")
      : "";
    return el.tagName.toLowerCase() + c;
  };
  out.docWidth = document.documentElement.scrollWidth;
  for (const el of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (r.width > contentPx + 2) {
      out.tooWide.push({ sel: sel(el), width: Math.round(r.width), over: Math.round(r.width - contentPx) });
    }
    // On paper a scroll box cannot scroll: whatever overflows is lost.
    if (["auto", "scroll"].includes(cs.overflowX) && el.scrollWidth - el.clientWidth > 1) {
      out.scrollBoxes.push({ sel: sel(el), lost: el.scrollWidth - el.clientWidth });
    }
    // Would this box straddle a page boundary?
    if (/^(H[1-4]|TR|PRE|FIGURE)$/.test(el.tagName)) {
      const top = r.top + window.scrollY;
      const startPage = Math.floor(top / pageH);
      const endPage = Math.floor((top + r.height - 1) / pageH);
      if (endPage > startPage && cs.breakInside !== "avoid") {
        out.splits.push({ sel: sel(el), height: Math.round(r.height), breakInside: cs.breakInside });
      }
    }
  }
  // A4 content is 658px, below the 720px card breakpoint, so tables
  // silently printed as stacked cards — 15 pages instead of 4, mostly
  // blank. Every width/overflow measure said "clean"; only looking at a
  // rendered PDF showed it. Assert the real table layout instead.
  out.cardTables = [];
  for (const t of document.querySelectorAll(".content-body table")) {
    const d = getComputedStyle(t).display;
    const row = t.querySelector("tbody tr");
    const rd = row ? getComputedStyle(row).display : "table-row";
    if (d !== "table" || rd !== "table-row") {
      out.cardTables.push({ table: d, row: rd });
    }
  }
  out.cardTables = out.cardTables.slice(0, 3);
  out.tooWide = out.tooWide.slice(0, 6);
  out.scrollBoxes = out.scrollBoxes.slice(0, 6);
  out.splits = out.splits.slice(0, 6);
  return out;
}

(async () => {
  fs.writeFileSync(OUT, "");
  const browser = await pc.launch({
    executablePath: CHROME, headless: "new",
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"],
  });
  for (const path of PAGES) {
    const page = await browser.newPage();
    try {
      await page.setViewport({ width: CONTENT_PX, height: PAGE_H_PX });
      await page.emulateMediaType("print");
      await page.goto(ORIGIN + path, { waitUntil: "networkidle2", timeout: 30000 });
      const r = await page.evaluate(probe, CONTENT_PX, PAGE_H_PX);
      fs.appendFileSync(OUT, JSON.stringify({ path, contentPx: CONTENT_PX, ...r }) + "\n");
    } catch (e) {
      fs.appendFileSync(OUT, JSON.stringify({ path, error: String(e.message).slice(0, 90) }) + "\n");
    } finally {
      await page.close().catch(() => {});
    }
  }
  await browser.close();
  console.log(`content width ${CONTENT_PX}px (A4 minus ${MARGIN_MM}mm margins)`);
  const rows = fs.readFileSync(OUT, "utf8").trim().split("\n").map(JSON.parse);
  let bad = 0;
  for (const r of rows) {
    const probs = [];
    if (r.error) probs.push(`error: ${r.error}`);
    for (const x of r.tooWide ?? []) probs.push(`too wide: ${x.sel} +${x.over}px`);
    for (const x of r.scrollBoxes ?? []) probs.push(`cropped on paper: ${x.sel} loses ${x.lost}px`);
    for (const x of r.splits ?? []) probs.push(`splits across pages: ${x.sel} h=${x.height}`);
    for (const x of r.cardTables ?? []) probs.push(`printing as cards: table=${x.table} row=${x.row}`);
    if (probs.length) { bad++; console.log(`  ${r.path}`); probs.forEach((p) => console.log(`      ${p}`)); }
  }
  console.log(bad ? `result: ${bad} page(s) with print problems` : `result: CLEAN (${rows.length} pages)`);
  process.exit(bad ? 1 : 0);
})();
