// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* Shared fixture for the demo page tests: the page's markup, a fake
 * Python runtime, a fake network, and the browser globals the page module
 * reads. try-page.js is an ES module with top-level wiring, so each test
 * file imports it once, in its own process. */
"use strict";
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const FIXTURE = `
  <script type="application/json" id="try-i18n">{"Run": "Lancer", "{n} record(s)": "{n} enregistrement(s)",
    "row {row} has {cells} field(s), header has {header}": "ligne {row} : {cells} champ(s), en-tête {header}"}</script>
  <div id="dropzone" tabindex="0">Drop</div><input type="file" id="file-input">
  <select id="sample-select"><option value="">Choose</option></select>
  <select id="scenario-select"><option value="">Break it</option></select>
  <select id="scheme-select"><option value="">No scheme</option></select>
  <button id="paste-btn">Paste</button>
  <div id="editor-block" hidden><textarea id="csv-input"></textarea></div>
  <p id="dialect-note"></p>
  <button id="run-btn">Run</button><button id="fix-btn" hidden>Fix</button>
  <p id="status" class="status"></p>
  <div id="run-progress" hidden><div id="run-progress-bar"></div></div>
  <div id="error-table-wrap" hidden><table><tbody id="error-tbody"></tbody></table></div>
  <p id="error-overflow" hidden></p>
  <button id="tab-xml">XML</button><button id="tab-twin">JSON</button>
  <pre id="xml-out"></pre>
  <button id="copy-btn">Copy XML</button><button id="download-btn">Download</button>
  <button id="download-json-btn">JSON</button><button id="report-btn" hidden>Report</button>
  <button id="xsd-btn">Re-run XSD</button><p id="xsd-status"></p><ul id="xsd-errors"></ul><p id="xsd-hash"></p>
  <div id="xsd-progress"><div id="xsd-progress-bar"></div></div>
  <table id="layer-summary" hidden><tbody>
    <tr data-layer="iso"><td class="layer-state" id="layer-state-iso"></td></tr>
    <tr data-layer="data"><td class="layer-state" id="layer-state-data"></td></tr>
    <tr data-layer="scheme"><td class="layer-state" id="layer-state-scheme"></td></tr>
    <tr data-layer="bank"><td class="layer-state">Not evaluated</td></tr>
    <tr data-layer="channel"><td class="layer-state">Not evaluated</td></tr>
  </tbody></table>
  <div class="content-note"><pre>pip install pain001</pre></div>`;

const CORPUS_CSV = "payment_id,payment_amount\nP1,10";
const PAGE_URL = pathToFileURL(path.resolve(__dirname, "../../static/js/try-page.js")).href;

/** Expose the jsdom window's globals the module reads at import and run time. */
function installGlobals(win) {
  win.HTMLElement.prototype.scrollIntoView = function () {};
  for (const [name, value] of Object.entries({
    window: win, document: win.document, navigator: win.navigator, location: win.location, Event: win.Event,
    FileReader: win.FileReader, requestAnimationFrame: (fn) => win.requestAnimationFrame(fn),
  })) {
    Object.defineProperty(globalThis, name, { configurable: true, writable: true, value });
  }
}

/** A fake Pyodide whose answers each step sets. */
function fakeRuntime() {
  const runtime = {
    answer: { findings: [], scheme: null, xml: "<Document/>", twin: { Document: {} }, xsd_errors: [], records: 2, version: "0.0.71" },
    xsdErrors: [],
    throwOnRun: null,
    throwOnXsd: null,
    throwOnHash: false,
  };
  const py = {
    globals: { set() {} },
    loadPackage: async () => {},
    runPython(code) {
      if (code.startsWith("warm(")) return "0.0.71";
      if (code.startsWith("xsd_sha256(")) { if (runtime.throwOnHash) throw new Error("no hash"); return "ab12"; }
      if (code.startsWith("run(")) { if (runtime.throwOnRun) throw runtime.throwOnRun; return JSON.stringify(runtime.answer); }
      if (code.startsWith("xsd_errors(")) { if (runtime.throwOnXsd) throw runtime.throwOnXsd; return JSON.stringify(runtime.xsdErrors); }
      return undefined;
    },
  };
  runtime.loadPyodide = async () => py;
  return runtime;
}

/** Same-origin GETs only: the corpus index and the runtime files. */
function fakeFetch(state) {
  return async (url) => {
    if (url === "/corpus/try-samples.json") {
      if (state.corpus === "missing") return { ok: false };
      return { ok: true, json: async () => ({ samples: [{ id: "gb.fps", country: "gb", records: 1, csv: CORPUS_CSV, scheme: "uk-fps" }] }) };
    }
    if (url.endsWith("pain001-runtime.json")) {
      if (state.manifestFails) throw new Error("offline");
      return { ok: true, json: async () => ({ runtime: [{ file: "a", bytes: 2 }], packages: [], wheels: [{ file: "w.whl", bytes: 0 }] }) };
    }
    return { ok: true, body: null, arrayBuffer: async () => new ArrayBuffer(1) };
  };
}

module.exports = { FIXTURE, CORPUS_CSV, PAGE_URL, installGlobals, fakeRuntime, fakeFetch };
