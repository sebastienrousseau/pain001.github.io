// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The demo engine's JavaScript half, against a fake runtime: the download
 * loop, progress reporting, package loading and the bridge calls. The
 * real Pyodide runtime is exercised by tests/engine.integration.mjs. */
import { test } from "node:test";
import assert from "node:assert/strict";
import {
  loadEngine, runEngine, MESSAGE_TYPE, PYODIDE_PACKAGES, BRIDGE,
} from "../static/js/try-engine.js";

const MANIFEST = {
  runtime: [{ file: "pyodide.asm.wasm", bytes: 6 }],
  packages: [{ file: "micropip.whl", bytes: 4 }],
  wheels: [{ file: "pain001-0.0.71-py3-none-any.whl", bytes: 5 }],
};

function fakeFetch({ streamed = true, failOn = "" } = {}) {
  const seen = [];
  const fetchImpl = async (url) => {
    seen.push(url);
    if (url.endsWith("pain001-runtime.json")) return { ok: true, json: async () => MANIFEST };
    const name = url.split("/").pop();
    if (name === failOn) return { ok: false, status: 404 };
    const size = [...MANIFEST.runtime, ...MANIFEST.packages, ...MANIFEST.wheels].find((f) => f.file === name).bytes;
    if (!streamed) return { ok: true, body: null, arrayBuffer: async () => new ArrayBuffer(size) };
    const chunks = [new Uint8Array(size - 1), new Uint8Array(1)];
    return {
      ok: true,
      body: { getReader: () => ({ read: async () => (chunks.length ? { done: false, value: chunks.shift() } : { done: true }) }) },
    };
  };
  return { fetchImpl, seen };
}

function fakePyodide() {
  const calls = { code: [], packages: null, indexURL: null, globals: {} };
  const py = {
    globals: { set: (k, v) => { calls.globals[k] = v; } },
    loadPackage: async (names, opts) => { calls.packages = names; opts.messageCallback("ignored"); },
    runPython: (code) => {
      calls.code.push(code);
      if (code.startsWith("warm(")) return "0.0.71";
      if (code.startsWith("run(")) return JSON.stringify({ findings: [], xml: "<Document/>", records: 1 });
      return undefined;
    },
  };
  const loadPyodide = async ({ indexURL }) => { calls.indexURL = indexURL; return py; };
  return { py, loadPyodide, calls };
}

test("loadEngine streams every runtime file, reports progress and boots the bridge", async () => {
  const { fetchImpl, seen } = fakeFetch();
  const { loadPyodide, calls } = fakePyodide();
  const progress = [];
  const engine = await loadEngine({ base: "/site", loadPyodide, fetchImpl, onProgress: (p) => progress.push(p) });
  assert.equal(engine.version, "0.0.71");
  assert.deepEqual(engine.manifest, MANIFEST);
  assert.deepEqual(seen, [
    "/site/pyodide/pain001-runtime.json", "/site/pyodide/pyodide.asm.wasm",
    "/site/pyodide/micropip.whl", "/site/pyodide/pain001-0.0.71-py3-none-any.whl",
  ]);
  assert.equal(calls.indexURL, "/site/pyodide/");
  assert.deepEqual(calls.packages, [...PYODIDE_PACKAGES, "/site/pyodide/pain001-0.0.71-py3-none-any.whl"]);
  assert.equal(calls.code[0], BRIDGE);
  assert.equal(calls.code[1], `warm(${JSON.stringify(MESSAGE_TYPE)})`);
  const phases = [...new Set(progress.map((p) => p.phase))];
  assert.deepEqual(phases, ["download", "boot", "install", "warm", "ready"]);
  const downloads = progress.filter((p) => p.phase === "download");
  assert.equal(downloads.at(-1).done, 15);
  assert.ok(downloads.every((p) => p.total === 15));
  assert.ok(downloads.length > 4, "progress per chunk, not per file");
});

test("loadEngine falls back to arrayBuffer without a streaming body, and to the global fetch", async () => {
  const { fetchImpl } = fakeFetch({ streamed: false });
  const { loadPyodide } = fakePyodide();
  const original = globalThis.fetch;
  globalThis.fetch = fetchImpl;
  try {
    const engine = await loadEngine({ base: "", loadPyodide });
    assert.equal(engine.version, "0.0.71");
  } finally {
    globalThis.fetch = original;
  }
});

test("loadEngine stops at the first file the server does not serve", async () => {
  const { fetchImpl } = fakeFetch({ failOn: "micropip.whl" });
  const { loadPyodide } = fakePyodide();
  await assert.rejects(loadEngine({ base: "", loadPyodide, fetchImpl }), /micropip\.whl: HTTP 404/);
});

test("runEngine hands the rows to the bridge and parses its answer", () => {
  const { py, calls } = fakePyodide();
  const rows = [{ payment_id: "P1" }];
  const out = runEngine({ py }, rows, { scheme: "sepa-sct" });
  assert.deepEqual(out, { findings: [], xml: "<Document/>", records: 1 });
  assert.equal(calls.globals._rows_json, JSON.stringify(rows));
  assert.equal(calls.code.at(-1), `run(_rows_json, ${JSON.stringify(MESSAGE_TYPE)}, "sepa-sct")`);
  runEngine({ py }, rows);
  assert.equal(calls.code.at(-1), `run(_rows_json, ${JSON.stringify(MESSAGE_TYPE)}, "")`);
});
