// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The demo page without its optional parts: no translation table (a
 * malformed one is ignored), no layered summary, no output tabs or JSON
 * download, no progress bar, no scheme selector, no corpus index and no
 * service worker. The page must still validate and generate. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { makeDom, settle } = require("./helpers/browser.js");
const { FIXTURE, PAGE_URL, installGlobals, fakeRuntime, fakeFetch } = require("./helpers/try-page.js");

test("try-page: a minimal page still validates and generates", async () => {
  const markup = FIXTURE
    .replace(/<script type="application\/json" id="try-i18n">[\s\S]*?<\/script>/, '<script type="application/json" id="try-i18n">{broken</script>')
    .replace(/<table id="layer-summary"[\s\S]*?<\/table>/, "")
    .replace('<button id="tab-xml">XML</button><button id="tab-twin">JSON</button>', "")
    .replace('<button id="download-json-btn">JSON</button>', "")
    .replace('<div id="run-progress" hidden><div id="run-progress-bar"></div></div>', "")
    .replace('<select id="scheme-select"><option value="">No scheme</option></select>', "");
  const dom = makeDom(markup, { url: "https://pain001.com/try/?sample=corpus:none" });
  const win = dom.window;
  const downloads = [];
  win.HTMLAnchorElement.prototype.click = function () { downloads.push(this.download); };
  installGlobals(win);
  globalThis.fetch = fakeFetch({ corpus: "missing" });
  win.loadPyodide = fakeRuntime().loadPyodide;

  await import(PAGE_URL);
  await settle();
  const $ = (id) => win.document.getElementById(id);
  assert.equal($("sample-select").querySelector("optgroup"), null, "no corpus index: built-in samples only");

  $("csv-input").value = "payment_id\nP1";
  $("run-btn").click();
  await settle();
  assert.match($("status").textContent, /^✓ 2 record\(s\) valid/);
  assert.equal($("xml-out").textContent, "<Document/>");
  $("download-btn").click();
  assert.equal(downloads.length, 1);

  $("csv-input").value = "";
  $("run-btn").click();
  await settle();
  assert.match($("status").textContent, /^✗ Need a header row/, "untranslated messages fall through");
});

test("try-page: a corpus index that cannot be fetched leaves the built-in samples", async () => {
  globalThis.fetch = async () => { throw new Error("offline"); };
  await settle();
  assert.ok(globalThis.document.getElementById("sample-select").querySelector('option[value="sepa-sct"]'));
});
