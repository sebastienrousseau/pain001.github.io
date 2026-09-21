#!/usr/bin/env node
/* Axe + structural checks in system, light, and dark colour modes. */
import { createRequire } from "node:module";
import { existsSync } from "node:fs";

const root = new URL("../.a11y-tools/", import.meta.url).pathname;
const require = createRequire(root + "resolve.cjs");
const puppeteer = require("puppeteer-core");
const { AxePuppeteer } = require("@axe-core/puppeteer");

const chromeCandidates = [
  process.env.CHROME_PATH,
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
].filter(Boolean);
const executablePath = chromeCandidates.find(existsSync);
if (!executablePath) throw new Error("Chrome not found; set CHROME_PATH");

const origin = process.env.SITE_ORIGIN || "http://127.0.0.1:8899";
const pages = (process.env.PAGES || [
  "/", "/try/", "/documentation/", "/compliance-toolkit/", "/contact/",
  "/message-specs/", "/message-spec-pain.001.001.13/", "/example-corpus/",
  "/pain001-mcp/", "/faqs/", "/fr/", "/ar/try/", "/tags/iso-20022/",
].join(",")).split(",");
const modes = ["system", "light", "dark"];

let failures = 0;

for (const path of pages) {
  const browser = await puppeteer.launch({
    executablePath,
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  });
  try {
    for (const mode of modes) {
      const page = await browser.newPage();
      try {
        await page.setViewport({ width: 1280, height: 800 });
        await page.goto(origin + path, { waitUntil: "networkidle0", timeout: 30000 });
        await page.evaluate((selected) => {
          if (selected === "system") document.documentElement.removeAttribute("data-theme");
          else document.documentElement.setAttribute("data-theme", selected);
        }, mode);

        const structural = await page.evaluate(() => {
          const descendants = document.querySelectorAll(
            "summary a, summary button, summary input, summary select, summary textarea, summary [tabindex]",
          ).length;
          const ids = [...document.querySelectorAll("[id]")].map((element) => element.id);
          const duplicates = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
          return { descendants, duplicates };
        });
        const result = await new AxePuppeteer(page).analyze();
        const count = result.violations.length + structural.descendants + structural.duplicates.length;
        failures += count;
        console.log(`${count ? "FAIL" : " ok "} ${mode.padEnd(6)} ${path}`);
        for (const violation of result.violations) {
          console.log(`  ${violation.id}: ${violation.help} (${violation.nodes.length})`);
          for (const node of violation.nodes) {
            console.log(`    ${node.target.join(" ")}: ${node.failureSummary || ""}`);
          }
        }
        if (structural.descendants) console.log(`  summary interactive descendants: ${structural.descendants}`);
        if (structural.duplicates.length) console.log(`  duplicate ids: ${structural.duplicates.join(", ")}`);
      } catch (error) {
        failures += 1;
        console.log(`ERR  ${mode.padEnd(6)} ${path}: ${String(error.message).slice(0, 160)}`);
      } finally {
        await page.close().catch(() => {});
      }
    }
  } finally {
    await browser.close().catch(() => {});
  }
}

console.log(`\n${pages.length * modes.length} page/mode checks; ${failures} finding(s)`);
process.exit(failures ? 1 : 0);
