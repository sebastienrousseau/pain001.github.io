/* Integration check for the browser engine, run in Node against the
 * vendored runtime under static/pyodide/. Needs the `pyodide` npm
 * package (npm i --no-save pyodide@0.27.2). Prints one JSON line per
 * case and exits non-zero on any failure. */
import { readFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import { createRequire } from "node:module";
import { loadEngine, runEngine } from "../static/js/try-engine.js";
import { parseCsv, SAMPLES, SCENARIOS } from "../static/js/try-demo.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const staticDir = path.resolve(here, "..", "static");
const require = createRequire(process.env.PYODIDE_NODE_MODULES ? path.join(process.env.PYODIDE_NODE_MODULES, "x.js") : import.meta.url);
const { loadPyodide } = require("pyodide");

// Node has fetch for http(s) only; serve local files through the same interface.
async function fetchImpl(url) {
  const file = url.startsWith("file:") ? fileURLToPath(url) : url;
  const body = await readFile(file);
  return { ok: true, status: 200, json: async () => JSON.parse(body.toString()), arrayBuffer: async () => body.buffer.slice(body.byteOffset, body.byteOffset + body.byteLength) };
}

const t0 = Date.now();
let last = "";
const engine = await loadEngine({
  base: staticDir, loadPyodide, fetchImpl,
  onProgress: (p) => { if (p.phase !== last) { last = p.phase; console.log(JSON.stringify({ phase: p.phase, mb: +(p.done / 1e6).toFixed(1), at_s: +((Date.now() - t0) / 1000).toFixed(1) })); } },
});
console.log(JSON.stringify({ loaded_s: +((Date.now() - t0) / 1000).toFixed(1), pain001: engine.version }));

let failures = 0;
function check(name, cond, extra) {
  console.log(JSON.stringify({ case: name, ok: !!cond, ...extra }));
  if (!cond) failures += 1;
}

for (const [key, sample] of Object.entries(SAMPLES)) {
  const parsed = parseCsv(sample.csv);
  const t = Date.now();
  let out;
  try {
    out = runEngine(engine, parsed.rows, { scheme: key === "sepa-sct" || key === "batch-20" ? "sepa-sct" : "" });
  } catch (err) {
    check(`sample ${key} clean`, false, { error: String(err.message).split("\n").filter((l) => /Error|error/.test(l)).slice(-3).join(" | ").slice(0, 400) });
    continue;
  }
  check(`sample ${key} clean`, out.findings.length === 0 && out.xml.length > 0 && out.xsd_errors.length === 0,
    { records: out.records, xml_bytes: out.xml.length, ms: Date.now() - t, scheme: out.scheme && out.scheme.valid });
}
for (const [key, scenario] of Object.entries(SCENARIOS)) {
  const csv = scenario.apply(SAMPLES["sepa-sct"].csv);
  const parsed = parseCsv(csv);
  let out;
  try {
    out = parsed.error ? { findings: [{ rule: "parse" }], xml: "" } : runEngine(engine, parsed.rows, {});
  } catch (err) {
    check(`scenario ${key} caught`, false, { error: String(err.message).split("\n").filter((l) => /Error|error/.test(l)).slice(-2).join(" | ").slice(0, 300) });
    continue;
  }
  const all = (parsed.structural || []).concat(out.findings);
  check(`scenario ${key} caught`, all.length > 0 && !out.xml, { rules: [...new Set(all.map((f) => f.rule))].slice(0, 4) });
}
// a scheme violation blocks generation
const usd = parseCsv(SAMPLES["cross-border"].csv);
const blocked = runEngine(engine, usd.rows, { scheme: "sepa-sct" });
check("non-EUR batch fails sepa-sct", blocked.findings.some((f) => f.layer === "scheme") && !blocked.xml, { rules: [...new Set(blocked.findings.map((f) => f.rule))] });

console.log(JSON.stringify({ failures, total_s: +((Date.now() - t0) / 1000).toFixed(1) }));
process.exit(failures ? 1 : 0);
