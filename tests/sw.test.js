// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The demo's service worker, static/sw.js (issue #52).
 *
 * The worker is loaded into a node:vm context under its real file URL, so
 * coverage is credited to static/sw.js, with small stand-ins for the
 * service-worker globals it uses: `self`, `caches` and `fetch`. Its
 * top-level `cacheable()` and `CACHE` are visible from the context. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { pathToFileURL } = require("node:url");

const FILE = path.resolve(__dirname, "../static/sw.js");
const ORIGIN = "https://pain001.com";

/** A response stand-in; `clone()` returns a distinguishable copy. */
function response(body, ok = true) {
  return { body, ok, clone() { return { body, ok, cloned: true }; } };
}

/** Load the worker with fresh fakes; returns the context and the fakes. */
function loadWorker({ cached = {}, network = {}, keys = [] } = {}) {
  const listeners = {};
  const calls = { skipWaiting: 0, claim: 0, deleted: [], put: [], fetched: [], opened: [] };
  const store = { ...cached };
  const cache = {
    match: async (request) => store[request.url],
    put: async (request, resp) => { calls.put.push([request.url, resp]); store[request.url] = resp; },
  };
  const context = {
    URL,
    self: {
      location: { origin: ORIGIN },
      addEventListener: (type, fn) => { listeners[type] = fn; },
      skipWaiting: () => { calls.skipWaiting += 1; },
      clients: { claim: async () => { calls.claim += 1; } },
    },
    caches: {
      keys: async () => keys,
      delete: async (name) => { calls.deleted.push(name); return true; },
      open: async (name) => { calls.opened.push(name); return cache; },
    },
    fetch: async (request) => {
      calls.fetched.push(request.url);
      return network[request.url] || response("network", true);
    },
  };
  vm.createContext(context);
  new vm.Script(fs.readFileSync(FILE, "utf8"), { filename: pathToFileURL(FILE).href }).runInContext(context);
  return { context, listeners, calls, store, CACHE: vm.runInContext("CACHE", context) };
}

/** Dispatch a fetch event; returns the promise given to respondWith, or null. */
function dispatchFetch(worker, url, method = "GET") {
  let responded = null;
  worker.listeners.fetch({ request: { url, method }, respondWith: (p) => { responded = p; } });
  return responded;
}

test("cacheable() takes only the demo and its same-origin assets", () => {
  const { context } = loadWorker();
  for (const url of [
    `${ORIGIN}/try/`, `${ORIGIN}/sw.js`, `${ORIGIN}/fr/try/`, `${ORIGIN}/pt-br/try/`,
    `${ORIGIN}/js/try-page.js`, `${ORIGIN}/pyodide/pyodide.asm.wasm`,
    `${ORIGIN}/samples/sepa.csv`, `${ORIGIN}/_csp/61bc2fae7f71ccad.js`,
  ]) assert.equal(context.cacheable(url), true, url);
  for (const url of [
    `${ORIGIN}/`, `${ORIGIN}/documentation/`, `${ORIGIN}/try`, `${ORIGIN}/fr/try/extra/`,
    `${ORIGIN}/FR/try/`, `${ORIGIN}/css/site.css`,
    "https://cdn.example.com/js/try-page.js", "https://cloudflareinsights.com/cdn-cgi/rum",
  ]) assert.equal(context.cacheable(url), false, url);
});

test("install activates the new worker at once", () => {
  const worker = loadWorker();
  worker.listeners.install({});
  assert.equal(worker.calls.skipWaiting, 1);
});

test("activate deletes every other cache, keeps the current one, then claims clients", async () => {
  const current = loadWorker().CACHE;
  const stale = ["pain001-try-old", "pain001-try-v7", "unrelated"];
  const worker = loadWorker({ keys: [stale[1], current, stale[2], stale[0]] });
  let waited = null;
  worker.listeners.activate({ waitUntil: (p) => { waited = p; } });
  await waited;
  assert.deepEqual([...worker.calls.deleted].sort(), stale);
  assert.ok(!worker.calls.deleted.includes(current));
  assert.equal(worker.calls.claim, 1);
});

test("requests outside the demo pass straight to the network, untouched", () => {
  const worker = loadWorker();
  assert.equal(dispatchFetch(worker, `${ORIGIN}/documentation/`), null);
  assert.equal(dispatchFetch(worker, "https://cloudflareinsights.com/cdn-cgi/rum"), null);
  assert.equal(dispatchFetch(worker, `${ORIGIN}/try/`, "POST"), null, "only GET is cached");
  assert.deepEqual(worker.calls.fetched, []);
  assert.deepEqual(worker.calls.opened, []);
});

test("a cached demo asset is served from the cache without a network request", async () => {
  const url = `${ORIGIN}/js/try-page.js`;
  const hit = response("cached");
  const worker = loadWorker({ cached: { [url]: hit } });
  assert.equal(await dispatchFetch(worker, url), hit);
  assert.deepEqual(worker.calls.fetched, []);
  assert.deepEqual(worker.calls.opened, [worker.CACHE]);
});

test("an uncached demo asset is fetched, stored as a clone, and returned", async () => {
  const url = `${ORIGIN}/try/`;
  const fresh = response("fresh");
  const worker = loadWorker({ network: { [url]: fresh } });
  assert.equal(await dispatchFetch(worker, url), fresh);
  assert.deepEqual(worker.calls.fetched, [url]);
  assert.equal(worker.calls.put.length, 1);
  assert.equal(worker.calls.put[0][0], url);
  assert.equal(worker.calls.put[0][1].cloned, true, "the cache gets a clone; the page gets the original");
});

test("a failed network response is returned but never cached", async () => {
  const url = `${ORIGIN}/samples/missing.csv`;
  const failed = response("not found", false);
  const worker = loadWorker({ network: { [url]: failed } });
  assert.equal(await dispatchFetch(worker, url), failed);
  assert.deepEqual(worker.calls.put, []);
});
