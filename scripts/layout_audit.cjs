/*
 * Layout audit: horizontal overflow, cropped content and gutter balance
 * across viewports, in real Chrome.
 *
 * Writes JSONL incrementally and uses a fresh browser per page, because
 * a single long-lived browser died with TargetCloseError partway through
 * the message-spec pages — those carry thousands of elements and the
 * original two-pass getComputedStyle walk was heavy enough to stall the
 * CDP session. One pass now, and a crash costs one page not the run.
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
const OUT = process.env.OUT ?? "/tmp/layout.jsonl";

const VIEWPORTS = [
  [320, 640], [375, 812], [390, 844], [414, 896], [768, 1024],
  [1024, 768], [1280, 800], [1440, 900], [1920, 1080], [2560, 1440],
];

const PAGES = process.env.PAGES
  ? process.env.PAGES.split(",")
  : [
      "/", "/try/", "/documentation/", "/installation/", "/faqs/", "/glossary/",
      "/message-specs/", "/message-spec-pain.001.001.13/",
      "/message-spec-pain.001.001.13-types/", "/message-spec-code-lists/",
      "/message-spec-changes/", "/compatibility/", "/pain002-reason-codes/",
      "/competitors-comparison/", "/executive-brief/", "/trust/", "/contact/",
      "/accessibility/", "/404/", "/fr/", "/fr/glossary/", "/ar/try/", "/ar/",
      "/tags/iso-20022/", "/iso20022-roadmap/", "/pain001-mcp/", "/languages/",
    ];

function probe() {
  const de = document.documentElement;
  const vw = window.innerWidth;
  const wide = [];
  const clipped = [];
  const sel = (el) => {
    if (el.id) return "#" + el.id;
    const c = typeof el.className === "string" && el.className.trim()
      ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".")
      : "";
    return el.tagName.toLowerCase() + c;
  };
  // Single walk: one getComputedStyle per element.
  for (const el of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") continue;
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 && cs.position !== "fixed" &&
        r.right > 0 && r.left < vw + 1 && r.right > vw + 1) {
      wide.push({ sel: sel(el), over: Math.round(r.right - vw), width: Math.round(r.width) });
    }
    // Cropped means unreachable, which is narrower than "overflows".
    // overflow-x:visible renders outside the box and stays readable —
    // a wide table deliberately exceeding the 68ch column is fine. The
    // real crop is a box that clips its own content, or content pushed
    // past an ancestor that clips. Flagging mere overflow reported 110
    // false positives the moment tables were allowed to break out.
    const hidden = el.scrollWidth - el.clientWidth;
    const selfClips = ["hidden", "clip"].includes(cs.overflowX);
    if (hidden > 1 && el.clientWidth > 2 && selfClips) {
      clipped.push({ sel: sel(el), hidden, clientWidth: el.clientWidth,
                     overflowX: cs.overflowX, why: "self-clips" });
    }
    // Ancestor clipping applies to every element, not only those with
    // visible overflow: a scrollable .table-responsive can itself be
    // cut off by a clipping parent, and restricting this branch to
    // overflow:visible missed exactly that case in testing.
    {
      for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
        const acs = getComputedStyle(a);
        // A scrollable ancestor makes the content reachable — stop and
        // treat it as fine. Checking only for clipping ancestors walked
        // straight past the scrollable <pre> to the hidden .terminal.
        if (["auto", "scroll"].includes(acs.overflowX)) break;
        if (!["hidden", "clip"].includes(acs.overflowX)) continue;
        // The visually-hidden pattern (1px box + clip) is deliberate
        // a11y furniture, not lost content — the mobile card layout
        // hides <thead> this way.
        if (a.clientWidth <= 1) break;
        const ab = a.getBoundingClientRect();
        const over = Math.round(r.right - ab.right);
        if (over > 1) {
          clipped.push({ sel: sel(el), hidden: over, clientWidth: el.clientWidth,
                         overflowX: "visible", why: "clipped by " + sel(a) });
        }
        break;
      }
    }
  }
  const main = document.querySelector("main");
  let gutters = null;
  if (main) {
    // Pick the first candidate that is actually rendered: the status
    // strip is a .wrap that goes display:none below 720px, and picking
    // it reported a 0-width column and a bogus full-viewport gutter.
    // Measure the text itself, not its container. A full-bleed section
    // band legitimately spans the viewport; the question is whether the
    // words inside it touch the screen edge. Take the first substantial
    // paragraph, falling back to the article column.
    let inner = null;
    for (const c of main.querySelectorAll("p, li")) {
      const b = c.getBoundingClientRect();
      if (b.width > 40 && b.height > 1 && (c.textContent || "").trim().length > 40) {
        inner = c; break;
      }
    }
    if (!inner) {
      for (const c of main.querySelectorAll(".content-body, article, .wrap")) {
        const b = c.getBoundingClientRect();
        if (b.width > 1 && b.height > 1) { inner = c; break; }
      }
    }
    if (!inner) inner = main;
    const r = inner.getBoundingClientRect();
    // Symmetry alone is not enough: 0/0 is perfectly symmetric and
    // means the text is touching both screen edges, which is exactly
    // what .content-shell's padding shorthand was doing on every phone.
    // Track the absolute gutter as well.
    gutters = {
      left: Math.round(r.left), right: Math.round(vw - r.right),
      width: Math.round(r.width),
      min: Math.round(Math.min(r.left, vw - r.right)),
    };
    // Symmetry is only an expectation where a centred reading column is
    // the intent — the article layout. Hero and demo copy is
    // deliberately left-aligned in a wider band, so measuring its
    // balance against the viewport says nothing.
    const col = main.querySelector(".content-body");
    if (col) {
      const c = col.getBoundingClientRect();
      if (c.width > 1) {
        gutters.colLeft = Math.round(c.left);
        gutters.colRight = Math.round(vw - c.right);
        gutters.delta = Math.round(Math.abs(c.left - (vw - c.right)));
      }
    }
  }
  // Every block inside the article shares the reading column's left
  // edge; wide tables grow rightwards only. A table that drifted left
  // (the symmetric-breakout attempt) looked broken next to the heading
  // above it, and no overflow or clipping check could see it.
  const strays = [];
  const col = main && main.querySelector(".content-body");
  if (col) {
    const colLeft = col.getBoundingClientRect().left;
    for (const el of col.children) {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.float !== "none") continue;
      const b = el.getBoundingClientRect();
      if (b.width < 2 || b.height < 2) continue;
      if (Math.abs(b.left - colLeft) > 2) {
        strays.push({ sel: sel(el), left: Math.round(b.left), colLeft: Math.round(colLeft) });
      }
    }
  }

  // The page title must sit on the article's left edge. Centring
  // .content-body without the header left the heading 140px adrift and
  // no existing check could see it — the page had no overflow, nothing
  // was cropped, and both columns were individually symmetric.
  let headerOffset = null;
  const hdr = document.querySelector(".page-header .wrap");
  if (hdr && col) {
    const h = hdr.getBoundingClientRect();
    const c = col.getBoundingClientRect();
    const pad = parseFloat(getComputedStyle(hdr).paddingLeft) || 0;
    if (h.width > 1 && c.width > 1) {
      headerOffset = Math.round(Math.abs(h.left + pad - c.left));
    }
  }

  return {
    headerOffset,
    strays: strays.slice(0, 6),
    docOverflow: de.scrollWidth - de.clientWidth,
    wide: wide.slice(0, 8),
    clipped: clipped.slice(0, 8),
    gutters,
  };
}

(async () => {
  fs.writeFileSync(OUT, "");
  for (const path of PAGES) {
    let browser;
    try {
      browser = await pc.launch({
        executablePath: CHROME, headless: "new",
        args: ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"],
      });
      const page = await browser.newPage();
      for (const [w, h] of VIEWPORTS) {
        try {
          await page.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
          await page.goto(ORIGIN + path, { waitUntil: "domcontentloaded", timeout: 30000 });
          const r = await page.evaluate(probe);
          fs.appendFileSync(OUT, JSON.stringify({ path, vw: w, ...r }) + "\n");
        } catch (e) {
          fs.appendFileSync(OUT, JSON.stringify({ path, vw: w, error: String(e.message).slice(0, 90) }) + "\n");
        }
      }
    } catch (e) {
      fs.appendFileSync(OUT, JSON.stringify({ path, fatal: String(e.message).slice(0, 90) }) + "\n");
    } finally {
      if (browser) await browser.close().catch(() => {});
    }
    process.stderr.write(`. ${path}\n`);
  }

  // Summarise and fail: an audit nobody can gate on is a report, not a
  // check. These five invariants each correspond to a defect that
  // shipped and that no other gate could see.
  const rows = fs.readFileSync(OUT, "utf8").trim().split("\n").map(JSON.parse);
  const g = rows.filter((r) => r.gutters);
  const counts = {
    errors: rows.filter((r) => r.error || r.fatal).length,
    pageOverflow: rows.filter((r) => (r.docOverflow ?? 0) > 1).length,
    cropped: rows.reduce((n, r) => n + (r.clipped?.length ?? 0), 0),
    tightGutter: g.filter((r) => r.gutters.min < 12).length,
    columnAsymmetry: g.filter((r) => "delta" in r.gutters && r.gutters.delta > 8).length,
    leftEdgeStrays: rows.reduce((n, r) => n + (r.strays?.length ?? 0), 0),
    headerMisaligned: rows.filter((r) => (r.headerOffset ?? 0) > 2).length,
  };
  console.log(`${rows.length} measurements over ${PAGES.length} page(s)`);
  for (const [k, v] of Object.entries(counts)) console.log(`  ${k}: ${v}`);
  const bad = Object.values(counts).reduce((a, b) => a + b, 0);
  if (bad) {
    for (const r of rows) {
      if ((r.docOverflow ?? 0) > 1) console.log(`  OVERFLOW ${r.path} @${r.vw} ${r.docOverflow}px`);
      for (const c of r.clipped ?? []) console.log(`  CROPPED  ${r.path} @${r.vw} ${c.sel} ${c.hidden}px (${c.why})`);
      for (const st of r.strays ?? []) console.log(`  STRAY    ${r.path} @${r.vw} ${st.sel} left=${st.left} col=${st.colLeft}`);
      if ((r.headerOffset ?? 0) > 2) console.log(`  HEADER   ${r.path} @${r.vw} title offset ${r.headerOffset}px from the article`);
      if (r.gutters && r.gutters.min < 12) console.log(`  GUTTER   ${r.path} @${r.vw} only ${r.gutters.min}px`);
    }
  }
  console.log(bad ? `result: ${bad} problem(s)` : "result: CLEAN");
  process.exit(bad ? 1 : 0);
})();
