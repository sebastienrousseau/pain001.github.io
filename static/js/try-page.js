/* Pain001 browser demo — page wiring.
 *
 * All validation/parsing/XML logic lives in ./try-demo.js (pure,
 * unit-tested). This file only binds DOM, drives the state machine,
 * and runs the optional WASM XSD gate. No network request in this
 * file ever carries user data: the only fetches are same-origin GETs
 * for the Pyodide runtime and the official schema.
 */

import {
  parseCsv, validateRecords, toXml, errorReportCsv, decodeBuffer,
  DELIMITER_NAMES, SAMPLES, SCENARIOS, fillTemplate,
} from "./try-demo.js";

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
 * empty → loaded → valid | invalid ; valid → xsd-running → xsd-valid | xsd-invalid
 * Every control's enabled state derives from here — nothing toggles
 * buttons ad hoc. */
const state = {
  phase: "empty",        // empty | loaded | valid | invalid
  xsd: "idle",           // idle | running | valid | invalid
  findings: [],
  xml: "",
  pristine: "",          // sample before a scenario broke it
  scenarioActive: false,
};

const $ = (id) => document.getElementById(id);
const els = {
  dropzone: $("dropzone"), fileInput: $("file-input"),
  sampleSelect: $("sample-select"), scenarioSelect: $("scenario-select"),
  pasteBtn: $("paste-btn"), editorBlock: $("editor-block"),
  input: $("csv-input"), dialectNote: $("dialect-note"),
  runBtn: $("run-btn"), fixBtn: $("fix-btn"),
  status: $("status"), tableWrap: $("error-table-wrap"),
  tbody: $("error-tbody"), overflow: $("error-overflow"),
  xmlOut: $("xml-out"), copyBtn: $("copy-btn"),
  downloadBtn: $("download-btn"), reportBtn: $("report-btn"),
  xsdBtn: $("xsd-btn"), xsdStatus: $("xsd-status"),
  xsdErrors: $("xsd-errors"), xsdHash: $("xsd-hash"),
  xsdProgress: $("xsd-progress"), xsdProgressBar: $("xsd-progress-bar"),
};

const MAX_FILE_BYTES = 2 * 1024 * 1024;
const MAX_ROWS_WARN = 10000;
const MAX_VISIBLE_ERRORS = 50;

function render() {
  const hasXml = state.phase === "valid";
  els.copyBtn.disabled = !hasXml;
  els.downloadBtn.disabled = !hasXml;
  els.copyBtn.title = hasXml ? "" : t("Add valid data in step 1 first");
  els.downloadBtn.title = hasXml ? "" : t("Add valid data in step 1 first");
  els.reportBtn.hidden = state.findings.length === 0;
  els.fixBtn.hidden = !state.scenarioActive;
  els.xsdBtn.disabled = !hasXml || state.xsd === "running";
  els.xsdBtn.title = hasXml ? "" : t("Generate XML in step 2 first");
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

function runValidation() {
  const parsed = parseCsv(els.input.value);
  if (parsed.error) {
    state.phase = "invalid";
    state.findings = [];
    els.status.textContent = "✗ " + t(parsed.error);
    els.status.className = "status fail";
    els.dialectNote.textContent = "";
    showFindings([]);
    setXml("");
    render();
    return;
  }

  const notes = [t("Detected: {delim}-delimited", { delim: t(DELIMITER_NAMES[parsed.delimiter]) }),
    t("{n} record(s)", { n: parsed.rows.length })];
  if (parsed.unknown.length) notes.push(t("ignored column(s): {cols}", { cols: parsed.unknown.join(", ") }));
  if (parsed.rows.length > MAX_ROWS_WARN) notes.push(t("large batch — the CLI streams batches of any size"));
  els.dialectNote.textContent = notes.join(" · ");

  const findings = parsed.structural.concat(validateRecords(parsed.rows));
  state.findings = findings;
  showFindings(findings);

  if (findings.length) {
    state.phase = "invalid";
    els.status.textContent = t("✗ Validation failed — {n} issue(s). This file would be rejected.", { n: findings.length });
    els.status.className = "status fail";
    setXml("");
  } else {
    state.phase = "valid";
    els.status.textContent = t("✓ {n} record(s) valid — control totals recomputed. Exit code 0.", { n: parsed.rows.length });
    els.status.className = "status pass";
    setXml(toXml(parsed.rows, "DEMO-" + Date.now(),
      new Date().toISOString().slice(0, 19)));
    prefetchEngine();
  }
  render();
}

function loadData(text, opts) {
  opts = opts || {};
  state.scenarioActive = !!opts.scenario;
  if (!opts.scenario) state.pristine = text;
  els.input.value = String(text).trim();
  els.editorBlock.hidden = false;
  runValidation();
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
  runValidation();
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

/* ==== Step 3: the WASM XSD gate ==== */

const WASM_URL = "/pyodide/pyodide.asm.wasm";
let pyodideReady = null;
let prefetched = false;

/* Warm the HTTP cache for the big payload the moment intent is clear
 * (valid XML exists, or the button is hovered/focused). loadPyodide's
 * own fetch then hits the cache. */
function prefetchEngine() {
  if (prefetched) return;
  prefetched = true;
  fetch(WASM_URL).catch(() => { prefetched = false; });
}
els.xsdBtn.addEventListener("mouseenter", prefetchEngine);
els.xsdBtn.addEventListener("focus", prefetchEngine);

function setProgress(pct) {
  if (pct === null) {
    els.xsdProgress.hidden = true;
    return;
  }
  els.xsdProgress.hidden = false;
  els.xsdProgressBar.style.width = pct + "%";
}

async function fetchWithProgress(url, onPct) {
  const resp = await fetch(url);
  const total = Number(resp.headers.get("Content-Length")) || 0;
  if (!resp.body || !total) { await resp.arrayBuffer(); onPct(100); return; }
  const reader = resp.body.getReader();
  let seen = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    seen += value.length;
    onPct(Math.min(100, Math.round((seen / total) * 100)));
  }
}

async function sha256Hex(url) {
  const buf = await fetch(url).then((r) => r.arrayBuffer());
  const digest = await crypto.subtle.digest("SHA-256", buf);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0")).join("");
}

function loadEngine() {
  if (pyodideReady) return pyodideReady;
  pyodideReady = (async () => {
    els.xsdStatus.textContent = t("Downloading the engine (~13 MB, first run only)…");
    await fetchWithProgress(WASM_URL, setProgress);
    setProgress(null);
    els.xsdStatus.textContent = t("Booting Python runtime…");
    await new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = "/pyodide/pyodide.js";
      s.onload = resolve;
      s.onerror = () => reject(new Error("engine script failed to load"));
      document.head.appendChild(s);
    });
    const py = await loadPyodide({ indexURL: "/pyodide/" });
    els.xsdStatus.textContent = t("Loading xmlschema…");
    await py.loadPackage([
      "/pyodide/elementpath-5.1.3-py3-none-any.whl",
      "/pyodide/xmlschema-4.3.2-py3-none-any.whl",
    ]);
    const xsdText = await fetch("/pyodide/pain.001.001.09.xsd").then((r) => r.text());
    py.FS.writeFile("/pain.001.001.09.xsd", xsdText);
    py.runPython("import xmlschema\nschema = xmlschema.XMLSchema('/pain.001.001.09.xsd')");
    sha256Hex("/pyodide/pain.001.001.09.xsd").then((hex) => {
      els.xsdHash.textContent = t("Schema SHA-256: {hex} — compare it against the copy published for pain.001.001.09.", { hex });
    }).catch(() => {});
    return py;
  })();
  pyodideReady.catch(() => { pyodideReady = null; });
  return pyodideReady;
}

els.xsdBtn.addEventListener("click", async () => {
  if (state.phase !== "valid") return;
  state.xsd = "running";
  render();
  els.xsdErrors.innerHTML = "";
  els.xsdStatus.className = "status";
  const started = performance.now();
  try {
    const py = await loadEngine();
    els.xsdStatus.textContent = t("Validating against the official schema…");
    py.globals.set("xml_text", state.xml);
    const result = py.runPython(
      "import json\n" +
      "errs = [str(e.reason or e) for e in schema.iter_errors(xml_text)]\n" +
      "json.dumps(errs[:10])"
    );
    const errs = JSON.parse(result);
    const secs = ((performance.now() - started) / 1000).toFixed(1);
    if (errs.length === 0) {
      state.xsd = "valid";
      els.xsdStatus.className = "status pass";
      els.xsdStatus.textContent = t("✓ VALID against the official ISO 20022 pain.001.001.09 XSD ({s}s).", { s: secs });
    } else {
      state.xsd = "invalid";
      els.xsdStatus.className = "status fail";
      els.xsdStatus.textContent = t("✗ Official schema rejected the document — {n} error(s) ({s}s).", { n: errs.length, s: secs });
      for (const e of errs) {
        const li = document.createElement("li");
        li.textContent = e;
        els.xsdErrors.appendChild(li);
      }
    }
  } catch (err) {
    state.xsd = "idle";
    setProgress(null);
    els.xsdStatus.className = "status fail";
    els.xsdStatus.textContent = t("✗ Engine failed to load: {error}. Check your connection and try again.", { error: err.message });
  }
  render();
});

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
