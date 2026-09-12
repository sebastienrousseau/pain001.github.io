/* Pain001 browser demo — page wiring.
 *
 * Input handling lives in ./try-demo.js (pure, unit-tested); the
 * verdicts come from the pain001 library itself, loaded into a Python
 * runtime (WebAssembly) by ./try-engine.js. This file binds the DOM,
 * drives the state machine and shows what the library said. No network
 * request in this file ever carries user data: the only fetches are
 * same-origin GETs for the runtime, the library and its dependencies.
 */

import {
  parseCsv, errorReportCsv, decodeBuffer,
  DELIMITER_NAMES, SAMPLES, SCENARIOS, fillTemplate,
} from "./try-demo.js";
import { loadEngine, runEngine, MESSAGE_TYPE } from "./try-engine.js";

/* ==== Runtime i18n ====
 * Locale demo pages carry a non-executable JSON table keyed by the
 * English template; English pages have none and fall through. */
const I18N = (() => {
  try {
    return JSON.parse(
      document.getElementById("try-i18n")?.textContent || "{}");
  } catch { return {}; }
})();
function t(template, params) {
  return fillTemplate(I18N[template] || template, params || {});
}
function tFinding(f) {
  return f.template && I18N[f.template]
    ? fillTemplate(I18N[f.template], f.params) : f.message;
}

/* ==== State machine ====
 * empty → loaded → running → valid | invalid. The engine has its own
 * state (idle → loading → ready | failed) and every control's enabled
 * state derives from the two — nothing toggles buttons ad hoc. */

const state = {
  phase: "empty",        // empty | loaded | running | valid | invalid
  engine: "idle",        // idle | loading | ready | failed
  findings: [],
  xml: "",
  pristine: "",          // sample before a scenario broke it
  scenarioActive: false,
  xsdVerdict: null,      // null | "valid" | "invalid"
  schemeVerdict: null,   // null | { scheme, valid, violations }
  version: "",           // pain001 version reported by the runtime
};

/** Scheme rulebooks the library ships that fit a credit-transfer batch. */
const SCHEMES = [
  "sepa-sct", "sepa-inst", "sepa-b2b", "cbpr-cross-border", "uk-fps", "uk-chaps",
  "uk-bacs", "us-ach", "us-wire", "us-rtp", "ch-domestic", "se-bankgiro", "de-ccu",
  "hk-fps", "sg-fast", "anti-duplicate",
];

const $ = (id) => document.getElementById(id);
const els = {
  dropzone: $("dropzone"), fileInput: $("file-input"),
  sampleSelect: $("sample-select"), scenarioSelect: $("scenario-select"),
  schemeSelect: $("scheme-select"),
  pasteBtn: $("paste-btn"), editorBlock: $("editor-block"),
  input: $("csv-input"), dialectNote: $("dialect-note"),
  runBtn: $("run-btn"), fixBtn: $("fix-btn"),
  status: $("status"), tableWrap: $("error-table-wrap"),
  tbody: $("error-tbody"), overflow: $("error-overflow"),
  runProgress: $("run-progress"), runProgressBar: $("run-progress-bar"),
  xmlOut: $("xml-out"), copyBtn: $("copy-btn"),
  downloadBtn: $("download-btn"), reportBtn: $("report-btn"),
  xsdBtn: $("xsd-btn"), xsdStatus: $("xsd-status"),
  xsdErrors: $("xsd-errors"), xsdHash: $("xsd-hash"),
  xsdProgress: $("xsd-progress"), xsdProgressBar: $("xsd-progress-bar"),
  layerSummary: $("layer-summary"),
  layerIso: $("layer-state-iso"), layerData: $("layer-state-data"),
  layerScheme: $("layer-state-scheme"),
};

const MAX_FILE_BYTES = 2 * 1024 * 1024;
const MAX_ROWS_WARN = 10000;
const MAX_VISIBLE_ERRORS = 50;

function render() {
  const hasXml = state.phase === "valid";
  const busy = state.phase === "running";
  els.copyBtn.disabled = !hasXml;
  els.downloadBtn.disabled = !hasXml;
  els.copyBtn.title = hasXml ? "" : t("Add valid data in step 1 first");
  els.downloadBtn.title = hasXml ? "" : t("Add valid data in step 1 first");
  els.reportBtn.hidden = state.findings.length === 0;
  els.fixBtn.hidden = !state.scenarioActive;
  els.runBtn.disabled = busy;
  els.xsdBtn.disabled = !hasXml || busy;
  els.xsdBtn.title = hasXml ? "" : t("Generate XML in step 2 first");
}

/* ==== Layered result summary ====
 * Three rows now carry live verdicts from the library: the official XSD
 * gate, the data-quality checks a schema cannot make (IBAN mod-97, BIC
 * structure), and the scheme rulebook chosen in step 1. The bank and
 * channel rows stay static: nothing local can evaluate them. */
function setLayerState(el, kind, text) {
  if (!el) return;
  el.className = "layer-state" + (kind ? " is-" + kind : "");
  el.textContent = text;
}

function updateLayerSummary(findings) {
  if (!els.layerSummary) return;
  const shown = state.phase !== "empty";
  els.layerSummary.hidden = !shown;
  if (!shown) return;

  const count = (layer) => findings.filter((f) => f.layer === layer).length;
  const isoIssues = count("iso") + count("input");
  const dataIssues = count("data");

  if (state.xsdVerdict === "valid") {
    setLayerState(els.layerIso, "pass", t("Passed the official XSD"));
  } else if (state.xsdVerdict === "invalid") {
    setLayerState(els.layerIso, "fail", t("Rejected by the official XSD"));
  } else if (isoIssues > 0) {
    setLayerState(els.layerIso, "fail", t("{n} issue(s) the schema would reject", { n: isoIssues }));
  } else {
    setLayerState(els.layerIso, null, t("Not reached — fix the findings above first"));
  }

  setLayerState(els.layerData, dataIssues ? "fail" : "pass",
    dataIssues
      ? t("{n} issue(s) a schema would accept but a bank would not", { n: dataIssues })
      : t("No identifier or format problems found"));

  const verdict = state.schemeVerdict;
  if (!verdict) {
    setLayerState(els.layerScheme, null, t("Not run — choose a scheme rulebook in step 1"));
  } else if (verdict.valid) {
    setLayerState(els.layerScheme, "pass", t("Passed {scheme}", { scheme: verdict.scheme }));
  } else {
    setLayerState(els.layerScheme, "fail",
      t("{n} violation(s) against {scheme}", { n: verdict.violations.length, scheme: verdict.scheme }));
  }
}

function showFindings(findings) {
  els.tbody.innerHTML = "";
  if (findings.length === 0) {
    els.tableWrap.hidden = true;
    els.overflow.hidden = true;
    return;
  }
  findings.slice(0, MAX_VISIBLE_ERRORS).forEach((f) => {
    const tr = document.createElement("tr");
    [["td", f.row], ["td", f.column], ["td", f.rule, "cell-rule"],
     ["td", f.value, "cell-value"], ["td", tFinding(f), "cell-problem"]]
      .forEach(([tag, text, cls]) => {
        const td = document.createElement(tag);
        td.textContent = text === undefined || text === "" ? "—" : String(text);
        if (cls) td.className = cls;
        tr.appendChild(td);
      });
    els.tbody.appendChild(tr);
  });
  els.tableWrap.hidden = false;
  const rest = findings.length - MAX_VISIBLE_ERRORS;
  els.overflow.hidden = rest <= 0;
  if (rest > 0) els.overflow.textContent = t("…and {n} more — download the full error report below.", { n: rest });
}

function setXml(xml) {
  state.xml = xml;
  if (xml) {
    els.xmlOut.textContent = xml;
  } else {
    els.xmlOut.innerHTML = "";
    const span = document.createElement("span");
    span.className = "xml-placeholder";
    span.textContent = state.phase === "invalid"
      ? t("No XML generated — validation is a hard gate. Fix the findings above and re-validate.")
      : t("The validated pain.001.001.09 document will appear here — add data in step 1.");
    els.xmlOut.appendChild(span);
  }
}

/* ==== The engine: the library, loaded once ==== */

let engineReady = null;

function setRunProgress(pct) {
  if (!els.runProgress) return;
  if (pct === null) { els.runProgress.hidden = true; return; }
  els.runProgress.hidden = false;
  els.runProgressBar.style.width = pct + "%";
}

function reportProgress(p) {
  const mb = (n) => (n / 1e6).toFixed(1);
  if (p.phase === "download") {
    setRunProgress(p.total ? Math.round((p.done / p.total) * 100) : 0);
    els.status.textContent = t("Starting a private Python runtime in your browser — {done} of {total} MB; nothing leaves your machine.",
      { done: mb(p.done), total: mb(p.total) });
  } else if (p.phase === "boot") {
    els.status.textContent = t("Booting Python runtime…");
  } else if (p.phase === "install") {
    els.status.textContent = t("Installing pain001 and its dependencies…");
  } else if (p.phase === "warm") {
    els.status.textContent = t("Warming the official schema (once per visit)…");
  }
}

function ensureEngine() {
  if (engineReady) return engineReady;
  state.engine = "loading";
  engineReady = (async () => {
    await new Promise((resolve, reject) => {
      if (window.loadPyodide) { resolve(); return; }
      const s = document.createElement("script");
      s.src = "/pyodide/pyodide.js";
      s.onload = resolve;
      s.onerror = () => reject(new Error("runtime script failed to load"));
      document.head.appendChild(s);
    });
    const engine = await loadEngine({ base: "", loadPyodide: window.loadPyodide, onProgress: reportProgress });
    state.engine = "ready";
    state.version = engine.version;
    setRunProgress(null);
    try {
      const hex = engine.py.runPython(`xsd_sha256(${JSON.stringify(MESSAGE_TYPE)})`);
      els.xsdHash.textContent = t("Schema SHA-256: {hex} — compare it against the copy published for pain.001.001.09.", { hex });
    } catch (_) { /* informational only */ }
    return engine;
  })();
  engineReady.catch(() => { engineReady = null; state.engine = "failed"; setRunProgress(null); });
  return engineReady;
}

/* Warm the runtime the moment intent is clear: data has been loaded. */
function prefetchEngine() { ensureEngine().catch(() => {}); }

function showXsd(errors, secs) {
  els.xsdErrors.innerHTML = "";
  if (errors.length === 0) {
    state.xsdVerdict = "valid";
    els.xsdStatus.className = "status pass";
    els.xsdStatus.textContent = t("✓ VALID against the official ISO 20022 pain.001.001.09 XSD ({s}s).", { s: secs });
  } else {
    state.xsdVerdict = "invalid";
    els.xsdStatus.className = "status fail";
    els.xsdStatus.textContent = t("✗ Official schema rejected the document — {n} error(s) ({s}s).", { n: errors.length, s: secs });
    for (const e of errors) {
      const li = document.createElement("li");
      li.textContent = e;
      els.xsdErrors.appendChild(li);
    }
  }
}

async function runValidation() {
  state.xsdVerdict = null;
  state.schemeVerdict = null;
  els.xsdErrors.innerHTML = "";
  els.xsdStatus.className = "status";
  els.xsdStatus.textContent = t("Generate XML in step 2 first — the XSD gate runs on that output.");
  const parsed = parseCsv(els.input.value);
  if (parsed.error) {
    state.phase = "invalid";
    state.findings = [];
    els.status.textContent = "✗ " + t(parsed.error);
    els.status.className = "status fail";
    els.dialectNote.textContent = "";
    showFindings([]);
    setXml("");
    updateLayerSummary([]);
    render();
    return;
  }

  const notes = [t("Detected: {delim}-delimited", { delim: t(DELIMITER_NAMES[parsed.delimiter]) }),
    t("{n} record(s)", { n: parsed.rows.length })];
  if (parsed.unknown.length) notes.push(t("ignored column(s): {cols}", { cols: parsed.unknown.join(", ") }));
  if (parsed.rows.length > MAX_ROWS_WARN) notes.push(t("large batch — the CLI streams batches of any size"));
  els.dialectNote.textContent = notes.join(" · ");

  state.phase = "running";
  state.findings = [];
  els.status.className = "status";
  els.status.textContent = t("Running pain001 in your browser…");
  setXml("");
  render();

  let engine;
  try {
    engine = await ensureEngine();
  } catch (err) {
    state.phase = "loaded";
    els.status.className = "status fail";
    els.status.textContent = t("✗ Engine failed to load: {error}. Check your connection and try again.", { error: err.message });
    render();
    return;
  }

  const started = performance.now();
  let out;
  try {
    out = runEngine(engine, parsed.rows, { scheme: els.schemeSelect ? els.schemeSelect.value : "" });
  } catch (err) {
    state.phase = "invalid";
    els.status.className = "status fail";
    els.status.textContent = t("✗ The library raised an error: {error}", { error: String(err.message).split("\n").pop() });
    render();
    return;
  }
  const secs = ((performance.now() - started) / 1000).toFixed(1);
  const findings = parsed.structural.concat(out.findings);
  state.findings = findings;
  state.schemeVerdict = out.scheme;
  showFindings(findings);

  if (findings.length) {
    state.phase = "invalid";
    els.status.textContent = t("✗ Validation failed — {n} issue(s). This file would be rejected.", { n: findings.length });
    els.status.className = "status fail";
    setXml("");
  } else {
    state.phase = "valid";
    setXml(out.xml);
    showXsd(out.xsd_errors, secs);
    els.status.textContent = t("✓ {n} record(s) valid — pain001 {version} generated the file and the official XSD accepted it ({s}s).",
      { n: out.records, version: out.version, s: secs });
    els.status.className = "status pass";
  }
  updateLayerSummary(findings);
  render();
}

function loadData(text, opts) {
  opts = opts || {};
  state.scenarioActive = !!opts.scenario;
  if (!opts.scenario) state.pristine = text;
  els.input.value = String(text).trim();
  els.editorBlock.hidden = false;
  void runValidation();
  els.status.scrollIntoView({
    behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
    block: "center",
  });
}

function readFile(file) {
  if (!file) return;
  if (file.size > MAX_FILE_BYTES) {
    els.status.textContent = t("✗ File is larger than 2 MB — this demo caps input size; the CLI streams batches of any size.");
    els.status.className = "status fail";
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    const decoded = decodeBuffer(reader.result);
    loadData(decoded.text);
    if (decoded.converted) {
      els.dialectNote.textContent += " · converted from Windows-1252 encoding";
    }
  };
  reader.onerror = () => {
    els.status.textContent = t("✗ Could not read that file.");
    els.status.className = "status fail";
  };
  reader.readAsArrayBuffer(file);
}

/* ==== Step 1 controls ==== */

for (const [key, sample] of Object.entries(SAMPLES)) {
  const opt = document.createElement("option");
  opt.value = key;
  opt.textContent = t(sample.label);
  els.sampleSelect.appendChild(opt);
}
for (const [key, scenario] of Object.entries(SCENARIOS)) {
  const opt = document.createElement("option");
  opt.value = key;
  opt.textContent = t(scenario.label);
  els.scenarioSelect.appendChild(opt);
}

els.sampleSelect.addEventListener("change", () => {
  const key = els.sampleSelect.value;
  if (key) loadData(SAMPLES[key].csv);
  els.sampleSelect.value = "";
});

els.scenarioSelect.addEventListener("change", () => {
  const key = els.scenarioSelect.value;
  if (key) {
    const base = state.pristine || SAMPLES["sepa-sct"].csv;
    state.pristine = base;
    loadData(SCENARIOS[key].apply(base), { scenario: true });
  }
  els.scenarioSelect.value = "";
});

els.fixBtn.addEventListener("click", () => {
  if (state.pristine) loadData(state.pristine);
});

els.pasteBtn.addEventListener("click", () => {
  state.scenarioActive = false;
  els.editorBlock.hidden = false;
  els.input.value = "";
  els.dialectNote.textContent = t("Paste your CSV records, then press Validate & generate.");
  els.input.focus();
  render();
});

els.dropzone.addEventListener("click", () => els.fileInput.click());
els.dropzone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") { e.preventDefault(); els.fileInput.click(); }
});
els.fileInput.addEventListener("change", () => {
  readFile(els.fileInput.files[0]);
  els.fileInput.value = "";
});

for (const ev of ["dragover", "dragenter"]) {
  els.dropzone.addEventListener(ev, (e) => { e.preventDefault(); els.dropzone.classList.add("dragover"); });
}
for (const ev of ["dragleave", "drop"]) {
  els.dropzone.addEventListener(ev, (e) => { e.preventDefault(); els.dropzone.classList.remove("dragover"); });
}
els.dropzone.addEventListener("drop", (e) => {
  readFile(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]);
});

els.runBtn.addEventListener("click", () => {
  state.scenarioActive = false;
  void runValidation();
});

/* ==== Step 2 outputs ==== */

els.copyBtn.addEventListener("click", () => {
  navigator.clipboard.writeText(state.xml).then(() => {
    els.copyBtn.textContent = t("Copied ✓");
    setTimeout(() => { els.copyBtn.textContent = t("Copy XML"); }, 1600);
  });
});

function downloadBlob(content, type, filename) {
  const blob = new Blob([content], { type });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(a.href);
}

els.downloadBtn.addEventListener("click", () => {
  downloadBlob(state.xml, "application/xml",
    "pain001-demo-" + new Date().toISOString().slice(0, 10) + ".xml");
});

els.reportBtn.addEventListener("click", () => {
  downloadBlob(errorReportCsv(state.findings), "text/csv",
    "pain001-error-report-" + new Date().toISOString().slice(0, 10) + ".csv");
});

/* ==== Step 3: re-run the official XSD gate on the XML shown ==== */

els.xsdBtn.addEventListener("click", async () => {
  if (state.phase !== "valid" || !state.xml) return;
  els.xsdStatus.className = "status";
  els.xsdStatus.textContent = t("Validating against the official schema…");
  const started = performance.now();
  try {
    const engine = await ensureEngine();
    engine.py.globals.set("_xml_text", state.xml);
    const errs = JSON.parse(engine.py.runPython(`xsd_errors(_xml_text, ${JSON.stringify(MESSAGE_TYPE)})`));
    showXsd(errs, ((performance.now() - started) / 1000).toFixed(1));
    updateLayerSummary(state.findings);
  } catch (err) {
    els.xsdStatus.className = "status fail";
    els.xsdStatus.textContent = t("✗ Engine failed to load: {error}. Check your connection and try again.", { error: err.message });
  }
  render();
});

/* ==== Scheme rulebook choice ==== */

if (els.schemeSelect) {
  for (const id of SCHEMES) {
    const opt = document.createElement("option");
    opt.value = id;
    opt.textContent = id;
    els.schemeSelect.appendChild(opt);
  }
  els.schemeSelect.addEventListener("change", () => {
    if (state.phase === "valid" || state.phase === "invalid") void runValidation();
  });
}

els.input.addEventListener("focus", prefetchEngine, { once: true });
els.editorBlock.addEventListener("input", prefetchEngine, { once: true });

/* ==== Copy buttons for code samples in the prose ==== */

document.querySelectorAll(".content-note pre").forEach((pre) => {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "pill pill-ghost";
  btn.style.marginTop = "0.5rem";
  btn.textContent = t("Copy command");
  btn.addEventListener("click", () => {
    navigator.clipboard.writeText(pre.textContent.trim()).then(() => {
      btn.textContent = t("Copied ✓");
      setTimeout(() => { btn.textContent = t("Copy command"); }, 1600);
    });
  });
  pre.insertAdjacentElement("afterend", btn);
});

/* ==== Offline support (see the "Verify it yourself" panel) ==== */

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js").catch(() => {});
}

render();
