// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The demo page's less travelled paths, in their own process (the module
 * keeps state across a visit): an English page with no translation table,
 * a summary row with no state cell, a corpus index that throws, a visitor
 * who breaks the default sample before loading one, a runtime with
 * nothing to download, a batch over the size warning, reduced motion,
 * and error reports whose layers passed or never ran. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { makeDom, settle } = require("./helpers/browser.js");
const { FIXTURE, PAGE_URL, installGlobals, fakeRuntime } = require("./helpers/try-page.js");

/* The corpus index throws; the runtime manifest lists only empty files,
 * so the download reports a total of zero bytes. */
async function emptyRuntimeFetch(url) {
  if (url === "/corpus/try-samples.json") throw new Error("offline");
  if (url.endsWith("pain001-runtime.json")) {
    return { ok: true, json: async () => ({ runtime: [{ file: "a", bytes: 0 }], packages: [], wheels: [] }) };
  }
  return { ok: true, body: null, arrayBuffer: async () => new ArrayBuffer(0) };
}

function installPage() {
  const markup = FIXTURE
    .replace(/<script type="application\/json" id="try-i18n">[\s\S]*?<\/script>/, "")
    .replace('<td class="layer-state" id="layer-state-scheme"></td>', '<td class="layer-state"></td>');
  const dom = makeDom(markup, {
    url: "https://pain001.com/try/",
    media: { "(prefers-reduced-motion: reduce)": true },
  });
  const win = dom.window;
  const reports = [];
  const blobs = [];
  const RealBlob = globalThis.Blob;
  globalThis.Blob = class extends RealBlob {
    constructor(parts, opts) { super(parts, opts); blobs.push(parts.join("")); }
  };
  win.HTMLAnchorElement.prototype.click = function () { reports.push({ name: this.download, body: blobs.at(-1) }); };
  installGlobals(win);
  return { win, doc: win.document, reports, $: (id) => win.document.getElementById(id) };
}

test("try-page: the less travelled paths", async (t) => {
  const { win, doc, $, reports } = installPage();
  const scrolls = [];
  win.HTMLElement.prototype.scrollIntoView = function (opts) { scrolls.push(opts.behavior); };
  globalThis.fetch = emptyRuntimeFetch;
  const runtime = fakeRuntime();
  const click = (el) => el.dispatchEvent(new win.MouseEvent("click", { bubbles: true }));
  const change = (el) => el.dispatchEvent(new win.Event("change"));

  await import(PAGE_URL);
  await settle();

  await t.test("a corpus index that throws leaves the built-in samples", () => {
    assert.equal($("sample-select").querySelector("optgroup"), null);
    assert.ok($("sample-select").querySelector('option[value="sepa-sct"]'));
  });

  await t.test("choosing a scheme before any data validates nothing", () => {
    $("scheme-select").value = "sepa-sct";
    change($("scheme-select"));
    assert.equal(doc.head.querySelector('script[src="/pyodide/pyodide.js"]'), null);
    assert.equal($("status").textContent, "");
  });

  await t.test("breaking the data before loading any starts from the default sample", async () => {
    $("scenario-select").value = "iban-checksum";
    change($("scenario-select"));
    assert.match($("csv-input").value, /DE79/);
    assert.deepEqual(scrolls, ["auto"], "reduced motion scrolls without animation");
  });

  await t.test("a runtime that fails while warming is swallowed by the prefetch", async () => {
    $("csv-input").dispatchEvent(new win.FocusEvent("focus"));
    doc.head.querySelector('script[src="/pyodide/pyodide.js"]').onerror();
    await settle();
    assert.match($("status").textContent, /Engine failed to load: runtime script failed to load/);
  });

  await t.test("a runtime with nothing to download, and a batch over the size warning", async () => {
    win.loadPyodide = runtime.loadPyodide;
    const rows = Array.from({ length: 10001 }, (_, i) => `P${i}`);
    $("csv-input").value = ["payment_id", ...rows].join("\n");
    click($("run-btn"));
    await settle();
    assert.match($("dialect-note").textContent, /large batch; the CLI streams batches of any size/);
    assert.match($("status").textContent, /^✓ 2 record\(s\) valid/);
    assert.equal($("layer-state-iso").className, "layer-state is-pass");
  });

  await t.test("changing the scheme of a failed file re-validates it", async () => {
    runtime.answer = { ...runtime.answer, findings: [{ row: 1, column: "x", rule: "r", value: "", message: "m", layer: "data" }] };
    click($("run-btn"));
    await settle();
    assert.match($("status").textContent, /Validation failed: 1 issue/);
    runtime.answer = { ...runtime.answer, findings: [{ row: 1, column: "x", rule: "r", value: "", message: "m", layer: "iso" }] };
    $("scheme-select").value = "uk-fps";
    change($("scheme-select"));
    await settle();
    assert.match($("layer-state-iso").textContent, /1 issue\(s\) the schema would reject/);
  });

  await t.test("the error report records layers that passed and layers that never ran", async () => {
    click($("report-btn"));
    assert.equal($("layer-state-data").className, "layer-state is-pass");
    runtime.answer = { ...runtime.answer, findings: [{ row: 1, column: "x", rule: "r", value: "", message: "m", layer: "data" }] };
    click($("run-btn"));
    await settle();
    assert.equal($("layer-state-iso").className, "layer-state", "iso was not reached");
    click($("report-btn"));
    assert.equal(reports.length, 2);
    assert.ok(reports.every((r) => /^pain001-error-report-/.test(r.name)));
    assert.match(reports[0].body, /data.*pass/, "the data layer passed");
    assert.match(reports[1].body, /iso.*not-run/, "the schema layer was not reached");
    assert.match(reports[1].body, /scheme.*not-run/, "no scheme cell state: not run");
    assert.match(reports[1].body, /bank.*not-evaluated/);
  });
});
