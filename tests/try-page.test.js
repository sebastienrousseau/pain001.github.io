// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The demo page's wiring (try-page.js), driven end to end in a jsdom page
 * with a fake Python runtime: loading data every way a visitor can, the
 * validation state machine, the layered summary, the outputs and the
 * XSD re-run. The module keeps state across a visit, so the steps run in
 * order inside one test, as a visit would. */
"use strict";
const { test, mock } = require("node:test");
const assert = require("node:assert/strict");
const { makeDom, settle } = require("./helpers/browser.js");
const { FIXTURE, CORPUS_CSV, PAGE_URL, installGlobals, fakeRuntime, fakeFetch } = require("./helpers/try-page.js");

function installPage() {
  const dom = makeDom(FIXTURE, { url: "https://pain001.com/try/#sample=corpus:gb.fps" });
  const win = dom.window;
  const clip = [];
  const downloads = [];
  Object.defineProperty(win.navigator, "clipboard", { configurable: true, value: { writeText: async (s) => { clip.push(s); } } });
  Object.defineProperty(win.navigator, "serviceWorker", { configurable: true, value: { register: async () => { throw new Error("offline"); } } });
  win.HTMLAnchorElement.prototype.click = function () { downloads.push({ name: this.download, href: this.href }); };
  installGlobals(win);
  return { dom, win, doc: win.document, clip, downloads, $: (id) => win.document.getElementById(id) };
}


test("try-page: a visit through every control", async (t) => {
  const page = installPage();
  const { win, doc, $, clip, downloads } = page;
  const net = { manifestFails: false };
  globalThis.fetch = fakeFetch(net);
  const runtime = fakeRuntime();
  const click = (el) => el.dispatchEvent(new win.MouseEvent("click", { bubbles: true }));
  const change = (el) => el.dispatchEvent(new win.Event("change"));

  await import(PAGE_URL);
  await settle();

  await t.test("the page fills its menus and opens the corpus sample named in the URL", async () => {
    assert.ok($("sample-select").querySelector('option[value="sepa-sct"]'));
    assert.ok($("scenario-select").querySelector('option[value="iban-checksum"]'));
    assert.ok($("sample-select").querySelector('optgroup option[value="corpus:gb.fps"]'));
    assert.equal($("scheme-select").value, "uk-fps", "the corpus sample's scheme is selected");
    assert.equal($("csv-input").value, CORPUS_CSV);
    assert.equal($("editor-block").hidden, false);
    assert.ok(doc.querySelector(".content-note pre + button"), "code samples get a copy button");
  });

  await t.test("the runtime script failing to load is reported, and the page recovers", async () => {
    const script = doc.head.querySelector('script[src="/pyodide/pyodide.js"]');
    assert.ok(script, "the runtime is requested only when data arrives");
    script.onerror();
    await settle();
    assert.match($("status").textContent, /Engine failed to load: runtime script failed to load/);
    assert.equal($("run-btn").disabled, false);
  });

  await t.test("a runtime download failure is reported as well", async () => {
    win.loadPyodide = runtime.loadPyodide;
    net.manifestFails = true;
    click($("run-btn"));
    await settle();
    assert.match($("status").textContent, /Engine failed to load: offline/);
    net.manifestFails = false;
  });

  await t.test("a clean file is generated, shown and XSD-checked", async () => {
    runtime.throwOnHash = true;
    click($("run-btn"));
    await settle();
    runtime.throwOnHash = false;
    assert.match($("status").textContent, /^✓ 2 record\(s\) valid\. pain001 0\.0\.71/);
    assert.equal($("xml-out").textContent, "<Document/>");
    assert.equal($("copy-btn").disabled, false);
    assert.equal($("xsd-status").className, "status pass");
    assert.equal($("layer-state-iso").className, "layer-state is-pass");
    assert.equal($("layer-state-data").className, "layer-state is-pass");
    assert.match($("layer-state-scheme").textContent, /Not run/);
    assert.match($("dialect-note").textContent, /comma-delimited · 1 enregistrement\(s\)/);
    assert.equal($("layer-summary").hidden, false);
  });

  await t.test("the output tabs switch between the XML and its JSON twin", () => {
    click($("tab-twin"));
    assert.equal($("xml-out").textContent, JSON.stringify({ Document: {} }, null, 2));
    assert.equal($("tab-twin").getAttribute("aria-selected"), "true");
    click($("tab-xml"));
    assert.equal($("xml-out").textContent, "<Document/>");
  });

  await t.test("copy and download the outputs", async () => {
    mock.timers.enable({ apis: ["setTimeout"] });
    try {
      click($("copy-btn"));
      await settle();
      assert.deepEqual(clip, ["<Document/>"]);
      assert.equal($("copy-btn").textContent, "Copied ✓");
      mock.timers.tick(1600);
      assert.equal($("copy-btn").textContent, "Copy XML");
      click(doc.querySelector(".content-note pre + button"));
      await settle();
      assert.equal(clip.at(-1), "pip install pain001");
      mock.timers.tick(1600);
      assert.equal(doc.querySelector(".content-note pre + button").textContent, "Copy command");
    } finally {
      mock.timers.reset();
    }
    click($("download-btn"));
    click($("download-json-btn"));
    assert.match(downloads[0].name, /^pain001-demo-\d{4}-\d{2}-\d{2}\.xml$/);
    assert.match(downloads[1].name, /\.iso\.json$/);
  });

  await t.test("the XSD gate re-runs on demand, with and without objections", async () => {
    runtime.xsdErrors = ["cvc-pattern-valid: bad IBAN"];
    click($("xsd-btn"));
    await settle();
    assert.equal($("xsd-status").className, "status fail");
    assert.equal($("xsd-errors").children.length, 1);
    assert.equal($("layer-state-iso").className, "layer-state is-fail");
    runtime.throwOnXsd = new Error("runtime gone");
    click($("xsd-btn"));
    await settle();
    assert.match($("xsd-status").textContent, /runtime gone/);
    runtime.throwOnXsd = null;
    runtime.xsdErrors = [];
    click($("xsd-btn"));
    await settle();
    assert.equal($("xsd-status").className, "status pass");
  });

  await t.test("choosing a scheme re-validates, and its verdict fills the scheme row", async () => {
    runtime.answer = { ...runtime.answer, scheme: { scheme: "sepa-sct", valid: true, violations: [] } };
    $("scheme-select").value = "sepa-sct";
    change($("scheme-select"));
    await settle();
    assert.equal($("layer-state-scheme").className, "layer-state is-pass");
    assert.match($("layer-state-scheme").textContent, /Passed sepa-sct/);
  });

  await t.test("findings fail the file, fill the table and the report", async () => {
    const findings = Array.from({ length: 52 }, (_, i) => ({
      row: i + 1, column: "debtor_account_IBAN", rule: "iban", value: "DE00", message: "bad checksum", layer: i % 2 ? "data" : "iso",
    }));
    findings[0].template = "Run";
    findings[1].template = "untranslated";
    runtime.answer = { ...runtime.answer, findings, xml: "", scheme: { scheme: "sepa-sct", valid: false, violations: [{}, {}] } };
    click($("run-btn"));
    await settle();
    assert.match($("status").textContent, /Validation failed: 52 issue/);
    assert.equal($("error-tbody").children.length, 50);
    assert.equal($("error-overflow").hidden, false);
    assert.match($("error-overflow").textContent, /and 2 more/);
    assert.equal($("error-tbody").children[0].lastChild.textContent, "Lancer", "translated finding");
    assert.equal($("error-tbody").children[1].lastChild.textContent, "bad checksum");
    assert.match($("layer-state-iso").textContent, /26 issue\(s\) the schema would reject/);
    assert.match($("layer-state-data").textContent, /26 issue\(s\)/);
    assert.match($("layer-state-scheme").textContent, /2 violation\(s\) against sepa-sct/);
    assert.match($("xml-out").textContent, /No XML generated/);
    assert.equal($("report-btn").hidden, false);
    click($("report-btn"));
    assert.match(downloads.at(-1).name, /^pain001-error-report-/);
    assert.equal($("copy-btn").disabled, true);
    click($("xsd-btn"));
    click($("download-json-btn"));
  });

  await t.test("a library exception is shown as a verdict, not a crash", async () => {
    runtime.throwOnRun = new Error("Traceback\nValueError: amount");
    click($("run-btn"));
    await settle();
    assert.match($("status").textContent, /library raised an error: ValueError: amount/);
    runtime.throwOnRun = null;
  });

  await t.test("unreadable input, unknown columns and ragged rows", async () => {
    $("csv-input").value = "only a header";
    click($("run-btn"));
    await settle();
    assert.match($("status").textContent, /^✗ Need a header row/);
    assert.equal($("layer-summary").hidden, false);
    runtime.answer = { ...runtime.answer, findings: [], xml: "<Document/>", scheme: null };
    $("csv-input").value = "payment_id;mystery\nP1;x\nP2";
    click($("run-btn"));
    await settle();
    assert.match($("dialect-note").textContent, /semicolon-delimited .* ignored column\(s\): mystery/);
    assert.match($("error-tbody").textContent, /ligne 2 : 1 champ\(s\), en-tête 2/);
  });

  await t.test("samples, scenarios, the fix button and paste mode", async () => {
    $("sample-select").value = "sepa-sct";
    change($("sample-select"));
    await settle();
    assert.equal($("sample-select").value, "");
    assert.match($("csv-input").value, /TXN-001/);
    $("scenario-select").value = "iban-checksum";
    change($("scenario-select"));
    await settle();
    assert.match($("csv-input").value, /DE79/);
    assert.equal($("fix-btn").hidden, false);
    click($("fix-btn"));
    await settle();
    assert.match($("csv-input").value, /DE89/);
    change($("scenario-select"));
    click($("paste-btn"));
    assert.equal($("csv-input").value, "");
    assert.match($("dialect-note").textContent, /Paste your CSV/);
    $("sample-select").value = "";
    change($("sample-select"));
  });

  await t.test("files arrive by picker and by drop; large and unreadable files are refused", async () => {
    const drop = $("dropzone");
    let picked = 0;
    $("file-input").click = () => { picked++; };
    click(drop);
    drop.dispatchEvent(new win.KeyboardEvent("keydown", { key: "Enter", cancelable: true }));
    drop.dispatchEvent(new win.KeyboardEvent("keydown", { key: " ", cancelable: true }));
    drop.dispatchEvent(new win.KeyboardEvent("keydown", { key: "a", cancelable: true }));
    assert.equal(picked, 3);
    drop.dispatchEvent(new win.Event("dragenter", { cancelable: true }));
    assert.ok(drop.classList.contains("dragover"));
    drop.dispatchEvent(new win.Event("dragleave", { cancelable: true }));
    assert.equal(drop.classList.contains("dragover"), false);

    const latin1 = new Uint8Array([...Buffer.from("payment_id,creditor_name\nP9,Soci"), 0xe9, ...Buffer.from("t"), 0xe9, ...Buffer.from("\n")]);
    Object.defineProperty($("file-input"), "files", { configurable: true, value: [new win.File([latin1], "a.csv")] });
    change($("file-input"));
    await settle(60);
    assert.match($("csv-input").value, /Société/);
    assert.match($("dialect-note").textContent, /converted from Windows-1252/);

    const dropEvent = new win.Event("drop", { cancelable: true });
    Object.defineProperty(dropEvent, "dataTransfer", { value: { files: [new win.File(["payment_id\nP10"], "b.csv")] } });
    drop.dispatchEvent(dropEvent);
    await settle(60);
    assert.match($("csv-input").value, /P10/);
    const bare = new win.Event("drop", { cancelable: true });
    drop.dispatchEvent(bare);

    Object.defineProperty($("file-input"), "files", {
      configurable: true, value: [{ size: 2 * 1024 * 1024 + 1 }],
    });
    change($("file-input"));
    assert.match($("status").textContent, /larger than 2 MB/);

    const RealReader = globalThis.FileReader;
    globalThis.FileReader = class { readAsArrayBuffer() { this.onerror(); } };
    Object.defineProperty($("file-input"), "files", { configurable: true, value: [{ size: 10 }] });
    change($("file-input"));
    globalThis.FileReader = RealReader;
    assert.match($("status").textContent, /Could not read that file/);
  });

  await t.test("focusing the editor warms the runtime, which is already loaded", async () => {
    $("csv-input").dispatchEvent(new win.FocusEvent("focus"));
    $("editor-block").dispatchEvent(new win.Event("input"));
    await settle();
    assert.equal($("run-btn").disabled, false);
  });
});
