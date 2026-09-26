// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* A jsdom window for testing the site's classic (non-module) scripts.
 *
 * The scripts are evaluated with node:vm inside jsdom's own context, under
 * their file URL, so Node's coverage attributes every line to the real
 * file in static/js/. jsdom lacks a few browser APIs the scripts use
 * (matchMedia, IntersectionObserver, clipboard); these helpers provide
 * small, controllable stand-ins. */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { pathToFileURL } = require("node:url");
const { JSDOM, VirtualConsole } = require("jsdom");

const JS_DIR = path.resolve(__dirname, "../../static/js");

/** A quiet virtual console: jsdom reports unimplemented navigation there. */
function quietConsole() {
  const vc = new VirtualConsole();
  vc.on("jsdomError", () => {});
  return vc;
}

/**
 * Build a page. ``media`` maps media queries to their initial `matches`;
 * `dom.setMedia(query, matches)` changes one and fires its listeners.
 */
function makeDom(body, { url = "https://pain001.com/", lang = "en", htmlClass = "no-js", media = {}, head = "" } = {}) {
  const dom = new JSDOM(
    `<!doctype html><html lang="${lang}" class="${htmlClass}"><head>${head}</head><body>${body}</body></html>`,
    { url, runScripts: "outside-only", pretendToBeVisual: true, virtualConsole: quietConsole() },
  );
  /* jsdom finishes loading on a later tick; the scripts under test see a
     parsed page, as they do in the browser when loaded with `defer`.
     `stillLoading()` restores the other path. */
  Object.defineProperty(dom.window.document, "readyState", { configurable: true, value: "complete" });
  const state = { ...media };
  const listeners = {};
  const lists = {};
  dom.window.matchMedia = (query) => {
    if (!lists[query]) {
      lists[query] = {
        media: query,
        get matches() { return !!state[query]; },
        addEventListener(type, fn) { (listeners[query] = listeners[query] || []).push(fn); },
        removeEventListener() {},
      };
    }
    return lists[query];
  };
  dom.setMedia = (query, matches) => {
    state[query] = matches;
    (listeners[query] || []).forEach((fn) => fn({ matches }));
  };
  return dom;
}

/** Evaluate static/js/<name> in the page, attributed to its real file. */
function runScript(dom, name) {
  const file = path.join(JS_DIR, name);
  new vm.Script(fs.readFileSync(file, "utf8"), { filename: pathToFileURL(file).href })
    .runInContext(dom.getInternalVMContext());
}

/** Make every localStorage access throw, as private modes and policies do. */
function blockStorage(dom) {
  Object.defineProperty(dom.window, "localStorage", {
    configurable: true,
    get() { throw new dom.window.DOMException("storage blocked", "SecurityError"); },
  });
}

/** Make the document look as if it were still parsing. */
function stillLoading(dom) {
  Object.defineProperty(dom.window.document, "readyState", { configurable: true, value: "loading" });
}

/** A controllable IntersectionObserver; `io.fire(target, isIntersecting)`. */
function installIntersectionObserver(dom) {
  const observers = [];
  dom.window.IntersectionObserver = class {
    constructor(callback, options) {
      this.callback = callback;
      this.options = options;
      this.targets = new Set();
      observers.push(this);
    }
    observe(el) { this.targets.add(el); }
    unobserve(el) { this.targets.delete(el); }
    disconnect() { this.targets.clear(); }
  };
  return {
    observers,
    fire(target, isIntersecting = true) {
      for (const o of observers) {
        if (o.targets.has(target)) o.callback([{ target, isIntersecting }], o);
      }
    },
  };
}

/** Replace the page's setTimeout with a queue the test flushes by hand. */
function manualTimers(dom) {
  const queue = [];
  dom.window.setTimeout = (fn, ms) => { queue.push({ fn, ms }); return queue.length; };
  dom.window.clearTimeout = (id) => { if (queue[id - 1]) queue[id - 1].fn = () => {}; };
  return {
    queue,
    flush() { while (queue.length) queue.shift().fn(); },
  };
}

/** Let promise chains and zero-delay timers run. */
async function settle(rounds = 25) {
  for (let i = 0; i < rounds; i++) await new Promise((resolve) => setImmediate(resolve));
}

module.exports = {
  JS_DIR, makeDom, runScript, blockStorage, stillLoading,
  installIntersectionObserver, manualTimers, settle, quietConsole,
};
