#!/usr/bin/env node
/*
 * Every built page, not a sample: WAVE's error, contrast and alert rules
 * plus the full axe rule set, in light and dark.
 *
 * Why this exists
 * ---------------
 * a11y_modes.mjs audits 13 representative URLs (pa11y-ci audited 19 until
 * v0.0.7, when this scan replaced it). The
 * taxonomy pages shipped with no site header and a browser-default serif
 * because no audited URL was a taxonomy page. The bar for this site is
 * "every page, zero WAVE errors or alerts, AAA", so the audit has to open
 * every page.
 *
 * WAVE itself has no command-line runner without a WebAIM API key, so the
 * `wave` checks below implement WAVE's documented rules (errors, alerts,
 * and the structural checks behind them) directly against the rendered
 * DOM. Contrast is left to axe's `color-contrast-enhanced` (7:1, AAA),
 * which is stricter than WAVE's AA contrast check. Confirm a sample with
 * the WAVE extension; a rule WAVE reports that this misses is a bug here.
 *
 * Usage:
 *   (cd site && python3 -m http.server 8899 &)
 *   node scripts/audit_site.mjs                 # every page, light + dark
 *   PAGES=/,/try/ node scripts/audit_site.mjs   # a subset
 *   CONCURRENCY=8 node scripts/audit_site.mjs
 */
import { createRequire } from "node:module";
import { existsSync, readdirSync, statSync } from "node:fs";
import { join, relative, sep } from "node:path";

const root = new URL("../.a11y-tools/", import.meta.url).pathname;
const require = createRequire(root + "resolve.cjs");
const puppeteer = require("puppeteer-core");
const { AxePuppeteer } = require("@axe-core/puppeteer");

const origin = process.env.SITE_ORIGIN || "http://127.0.0.1:8899";
const siteDir = new URL("../site/", import.meta.url).pathname;
const concurrency = Number(process.env.CONCURRENCY || 4);
const modes = (process.env.MODES || "light,dark").split(",");
const chrome = [
  process.env.CHROME_PATH,
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
].filter(Boolean).find(existsSync);
if (!chrome) throw new Error("Chrome not found; set CHROME_PATH");

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    if (name.startsWith(".") || name === "_csp") continue;
    const full = join(dir, name);
    if (statSync(full).isDirectory()) out.push(...walk(full));
    else if (name === "index.html") out.push(full);
  }
  return out;
}

const pages = process.env.PAGES
  ? process.env.PAGES.split(",")
  : walk(siteDir).map((f) => "/" + relative(siteDir, f).split(sep).slice(0, -1).join("/") + "/")
      .map((p) => p.replace(/\/+/g, "/"))
      .sort();

/* WAVE's documented rules, evaluated in the page. */
function waveRules() {
  const out = [];
  const add = (type, id, el, note) => out.push({
    type, id, note: note || "",
    where: el ? (el.outerHTML || "").replace(/\s+/g, " ").slice(0, 140) : "",
  });
  const text = (el) => (el.textContent || "").replace(/\s+/g, " ").trim();
  const byId = (id) => document.getElementById(id);
  const visible = (el) => {
    const s = getComputedStyle(el);
    return s.display !== "none" && s.visibility !== "hidden" && el.getClientRects().length > 0;
  };
  const accName = (el) => {
    const lb = el.getAttribute("aria-labelledby");
    if (lb) return lb.split(/\s+/).map((i) => byId(i)).filter(Boolean).map(text).join(" ").trim();
    const al = (el.getAttribute("aria-label") || "").trim();
    if (al) return al;
    const imgs = [...el.querySelectorAll("img[alt], svg[aria-label]")]
      .map((i) => (i.getAttribute("alt") || i.getAttribute("aria-label") || "").trim()).join(" ");
    return (text(el) + " " + imgs).trim();
  };

  // ---- Errors ----
  const html = document.documentElement;
  if (!/^[a-z]{2,3}(-[A-Za-z0-9]+)*$/.test(html.getAttribute("lang") || "")) add("error", "language_missing", html);
  if (!document.title.trim()) add("error", "title_invalid", null);
  for (const m of document.querySelectorAll('meta[http-equiv="refresh" i]')) add("error", "meta_refresh", m);
  for (const m of document.querySelectorAll('meta[name="viewport"]')) {
    const c = (m.getAttribute("content") || "").replace(/\s/g, "").toLowerCase();
    const max = /maximum-scale=([\d.]+)/.exec(c);
    if (/user-scalable=(no|0)/.test(c) || (max && Number(max[1]) < 2)) add("error", "meta_viewport", m);
  }
  for (const img of document.querySelectorAll("img")) {
    if (!img.hasAttribute("alt")) add("error", "alt_missing", img);
  }
  for (const i of document.querySelectorAll('input[type="image"]')) if (!i.getAttribute("alt")) add("error", "alt_input_missing", i);
  for (const a of document.querySelectorAll("area")) if (!a.hasAttribute("alt")) add("error", "alt_area_missing", a);
  for (const a of document.querySelectorAll("a[href]")) {
    if (!accName(a)) {
      const onlyImgs = a.querySelector("img") && !text(a);
      add("error", onlyImgs ? "alt_link_missing" : "link_empty", a);
    }
  }
  for (const b of document.querySelectorAll('button, input[type="button"], input[type="submit"], input[type="reset"]')) {
    const name = b.tagName === "INPUT" ? (b.value || b.getAttribute("aria-label") || "").trim() : accName(b);
    if (!name) add("error", "button_empty", b);
  }
  for (const h of document.querySelectorAll("h1,h2,h3,h4,h5,h6")) if (!accName(h)) add("error", "heading_empty", h);
  for (const th of document.querySelectorAll("th")) if (!accName(th)) add("error", "th_empty", th);
  for (const el of document.querySelectorAll("blink, marquee")) add("error", el.tagName.toLowerCase(), el);
  const controls = document.querySelectorAll('input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="reset"]):not([type="image"]), select, textarea');
  for (const c of controls) {
    const forLabels = c.id ? document.querySelectorAll(`label[for="${CSS.escape(c.id)}"]`) : [];
    const wrapped = c.closest("label");
    const aria = (c.getAttribute("aria-label") || "").trim() || c.getAttribute("aria-labelledby");
    if (forLabels.length > 1) add("error", "label_multiple", c);
    const labels = [...forLabels, ...(wrapped ? [wrapped] : [])];
    if (!labels.length && !aria) {
      if ((c.getAttribute("title") || "").trim()) add("alert", "label_title", c);
      else add("error", "label_missing", c);
    }
    for (const l of labels) if (!text(l) && !l.querySelector("img[alt]:not([alt=''])")) add("error", "label_empty", l);
  }
  for (const el of document.querySelectorAll("[aria-labelledby], [aria-describedby]")) {
    for (const attr of ["aria-labelledby", "aria-describedby"]) {
      const v = el.getAttribute(attr);
      if (v && v.split(/\s+/).some((i) => !byId(i))) add("error", "aria_reference_broken", el, attr);
    }
  }
  for (const m of document.querySelectorAll('[role="menu"]')) if (!m.querySelector('[role^="menuitem"]')) add("error", "aria_menu_broken", m);
  for (const a of document.querySelectorAll('a[href^="#"]')) {
    const id = decodeURIComponent(a.getAttribute("href").slice(1));
    if (id && !byId(id) && !document.getElementsByName(id).length) {
      add(/skip/i.test(text(a)) ? "error" : "alert", /skip/i.test(text(a)) ? "link_skip_broken" : "link_internal_broken", a);
    }
  }

  // ---- Alerts ----
  for (const img of document.querySelectorAll("img[alt]")) {
    const alt = img.getAttribute("alt").trim();
    if (alt.length > 100) add("alert", "alt_long", img);
    if (/^(image|graphic|photo|picture|spacer|img|icon)$|\.(png|jpe?g|gif|svg|webp|avif)$/i.test(alt)) add("alert", "alt_suspicious", img);
    const next = img.nextSibling && img.nextSibling.textContent ? img.nextSibling.textContent.trim() : "";
    if (alt && next && alt.toLowerCase() === next.toLowerCase()) add("alert", "alt_redundant", img);
  }
  for (const l of document.querySelectorAll("label[for]")) if (!byId(l.getAttribute("for"))) add("alert", "label_orphaned", l);
  const groups = {};
  for (const r of document.querySelectorAll('input[type="radio"][name], input[type="checkbox"][name]')) (groups[r.name] ||= []).push(r);
  for (const g of Object.values(groups)) if (g.length > 1 && !g[0].closest('fieldset, [role="group"], [role="radiogroup"]')) add("alert", "fieldset_missing", g[0]);
  for (const f of document.querySelectorAll("fieldset")) if (!f.querySelector("legend") || !text(f.querySelector("legend"))) add("alert", "legend_missing", f);
  const heads = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")];
  if (!heads.length) add("alert", "heading_missing", null);
  if (!document.querySelector("h1")) add("alert", "h1_missing", null);
  let prev = 0;
  for (const h of heads) {
    const lvl = Number(h.tagName[1]);
    if (prev && lvl > prev + 1) add("alert", "heading_skipped", h, `h${prev} -> h${lvl}`);
    prev = lvl;
  }
  for (const p of document.querySelectorAll("p")) {
    const t = text(p);
    if (!t || t.length >= 50 || !visible(p)) continue;
    const s = getComputedStyle(p);
    const size = parseFloat(s.fontSize);
    const bold = Number(s.fontWeight) >= 600 || [...p.querySelectorAll("strong, b")].some((b) => text(b) === t);
    const italic = s.fontStyle === "italic";
    if (size >= 20 || (size >= 16 && (bold || italic))) add("alert", "heading_possible", p);
  }
  for (const t of document.querySelectorAll("table")) {
    if (!t.querySelector("th") && t.getAttribute("role") !== "presentation") add("alert", "table_layout", t);
  }
  const suspicious = /^(click here|here|more|read more|learn more|link|this|continue|details|more info)$/i;
  const links = [...document.querySelectorAll("a[href]")];
  for (const a of links) {
    const t = accName(a);
    if (suspicious.test(t)) add("alert", "link_suspicious", a);
    const href = a.getAttribute("href") || "";
    const ext = /\.(pdf)(\?|#|$)/i.test(href) ? "link_pdf" : /\.(docx?)(\?|#|$)/i.test(href) ? "link_word"
      : /\.(xlsx?)(\?|#|$)/i.test(href) ? "link_excel" : /\.(pptx?)(\?|#|$)/i.test(href) ? "link_powerpoint" : "";
    if (ext) add("alert", ext, a);
    if ((a.getAttribute("title") || "").trim().toLowerCase() === t.toLowerCase() && t) add("alert", "title_redundant", a);
  }
  // Adjacent links to the same URL: consecutive links in document order
  // with no other text between them.
  for (let i = 0; i + 1 < links.length; i++) {
    const a = links[i], b = links[i + 1];
    if (a.href !== b.href || !a.href) continue;
    const range = document.createRange();
    range.setStartAfter(a); range.setEndBefore(b);
    const between = range.toString().replace(/[\s·|,;:/-]+/g, "");
    if (!between && !a.contains(b) && !b.contains(a)) add("alert", "link_redundant", b);
  }
  for (const el of document.querySelectorAll("[onmouseover], [onmouseout]")) {
    if (!el.hasAttribute("onfocus") && !el.hasAttribute("onblur")) add("alert", "event_handler", el);
  }
  for (const s of document.querySelectorAll("select[onchange]")) add("alert", "javascript_jumpmenu", s);
  for (const el of document.querySelectorAll("[accesskey]")) add("alert", "accesskey", el);
  for (const el of document.querySelectorAll("[tabindex]")) if (Number(el.getAttribute("tabindex")) > 0) add("alert", "tabindex", el);
  for (const el of document.querySelectorAll("noscript")) add("alert", "noscript", el);
  for (const el of document.querySelectorAll("video, audio")) add("alert", "html5_video_audio", el);
  for (const el of document.querySelectorAll('iframe[src*="youtube"], object, embed, applet')) add("alert", "plugin", el);
  if (!document.querySelector('main, [role="main"]') || !document.querySelector('header, [role="banner"], nav, [role="navigation"]')) add("alert", "region_missing", null);
  // Text styling
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const node = walker.currentNode;
    const el = node.parentElement;
    if (!el || seen.has(el) || !node.textContent.trim() || !visible(el)) continue;
    seen.add(el);
    const s = getComputedStyle(el);
    if (parseFloat(s.fontSize) < 10) add("alert", "text_small", el, s.fontSize);
    if (s.textAlign === "justify" && node.textContent.trim().length > 40) add("alert", "text_justified", el);
    const deco = s.textDecorationLine || s.textDecoration || "";
    if (/underline/.test(deco) && !el.closest("a, abbr[title], ins")) add("alert", "underline", el);
  }
  return out;
}

/* Layout: nothing may be drawn under the article contents rail. The
   first rail sat beside a 68ch column while tables widened past it, and
   no markup- or contrast-based check notices one box on top of another.
   Checked at 1280 and 1920 CSS px, where the rail is shown. */
function overlapRules() {
  const out = [];
  const rail = document.querySelector(".content-body > .article-toc");
  if (!rail) return out;
  const r = rail.getBoundingClientRect();
  if (!r.width || getComputedStyle(rail).display === "none") return out;
  const body = rail.parentElement;
  const hits = new Set();
  // What is painted, not the layout box: a wide table inside a scrolling
  // wrapper is clipped by it, and clipped overflow overlaps nothing.
  const clipRight = (el) => {
    let right = Infinity;
    for (let a = el.parentElement; a && a !== body.parentElement; a = a.parentElement) {
      if (getComputedStyle(a).overflowX !== "visible") right = Math.min(right, a.getBoundingClientRect().right);
    }
    return right;
  };
  for (const el of body.querySelectorAll("p, li, td, th, pre, img, h2, h3, h4, h5, blockquote, figure, table")) {
    if (rail.contains(el)) continue;
    const limit = clipRight(el);
    for (const raw of el.getClientRects()) {
      const b = { left: raw.left, right: Math.min(raw.right, limit), width: raw.width, height: raw.height };
      if (b.width < 1 || b.height < 1) continue;
      const overlapX = Math.min(b.right, r.right) - Math.max(b.left, r.left);
      // The rail spans the article's full height, so sharing any
      // horizontal band with it is an overlap.
      if (overlapX > 1) {
        hits.add(el);
        break;
      }
    }
  }
  for (const el of [...hits].slice(0, 5)) {
    out.push({ type: "layout", id: "overlaps_contents_rail", note: `${Math.round(window.innerWidth)}px`,
      where: el.outerHTML.replace(/\s+/g, " ").slice(0, 120) });
  }
  return out;
}

const browser = await puppeteer.launch({ executablePath: chrome, headless: "new" });
const results = [];
let cursor = 0;
async function worker() {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  while (cursor < pages.length) {
    const path = pages[cursor++];
    for (const mode of modes) {
      try {
        await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: mode }]);
        await page.goto(origin + path, { waitUntil: "networkidle0", timeout: 120000 });
        const wave = mode === modes[0] ? await page.evaluate(waveRules) : [];
        if (mode === modes[0]) {
          for (const width of [1920, 1280]) {
            await page.setViewport({ width, height: 900 });
            wave.push(...await page.evaluate(overlapRules));
          }
        }
        const axe = await new AxePuppeteer(page)
          .withTags(["wcag2a", "wcag2aa", "wcag2aaa", "wcag21a", "wcag21aa", "wcag21aaa", "wcag22aa", "wcag22aaa", "best-practice"])
          .analyze();
        results.push({ path, mode, wave, axe: axe.violations.map((v) => ({ id: v.id, nodes: v.nodes.length, target: v.nodes[0]?.target?.join(" ") })) });
      } catch (e) {
        results.push({ path, mode, wave: [], axe: [], fatal: String(e.message || e).slice(0, 160) });
      }
    }
  }
  await page.close();
}
await Promise.all(Array.from({ length: Math.min(concurrency, pages.length) }, worker));
await browser.close();

const tally = {};
let failures = 0;
for (const r of results.sort((a, b) => a.path.localeCompare(b.path) || a.mode.localeCompare(b.mode))) {
  const bad = r.wave.length + r.axe.length + (r.fatal ? 1 : 0);
  if (!bad) continue;
  failures += bad;
  console.log(`FAIL ${r.mode.padEnd(5)} ${r.path}`);
  if (r.fatal) console.log(`  fatal: ${r.fatal}`);
  for (const w of r.wave) {
    tally[`wave:${w.type}:${w.id}`] = (tally[`wave:${w.type}:${w.id}`] || 0) + 1;
    console.log(`  ${w.type === "layout" ? "layout" : "wave"} ${w.type} ${w.id}${w.note ? " (" + w.note + ")" : ""}: ${w.where}`);
  }
  for (const v of r.axe) {
    tally[`axe:${v.id}`] = (tally[`axe:${v.id}`] || 0) + v.nodes;
    console.log(`  axe ${v.id} x${v.nodes}: ${v.target || ""}`);
  }
}
console.log("\n" + Object.entries(tally).sort((a, b) => b[1] - a[1]).map(([k, n]) => `${String(n).padStart(5)}  ${k}`).join("\n"));
console.log(`\n${pages.length} page(s) x ${modes.length} mode(s); ${failures} finding(s)`);
process.exit(failures ? 1 : 0);
