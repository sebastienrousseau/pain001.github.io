// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The scripts every page runs first: the pre-paint theme and motion
 * choice, the analytics loader, and the legacy-URL redirect. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { makeDom, runScript, blockStorage } = require("./helpers/browser.js");

const REDUCE = "(prefers-reduced-motion: reduce)";

test("theme init: no stored choice follows the OS and enables motion", () => {
  const dom = makeDom("");
  runScript(dom, "prism-theme-init.js");
  const root = dom.window.document.documentElement;
  assert.equal(root.classList.contains("no-js"), false);
  assert.equal(root.hasAttribute("data-theme"), false);
  assert.equal(root.classList.contains("js-motion"), true);
  assert.equal(root.classList.contains("motion-off"), false);
});

test("theme init: a stored theme and a stored motion choice are applied", () => {
  const dom = makeDom("");
  dom.window.localStorage.setItem("theme", "dark");
  dom.window.localStorage.setItem("motion", "off");
  runScript(dom, "prism-theme-init.js");
  const root = dom.window.document.documentElement;
  assert.equal(root.getAttribute("data-theme"), "dark");
  assert.equal(root.classList.contains("motion-off"), true);
  assert.equal(root.classList.contains("js-motion"), false);
});

test("theme init: an unknown stored theme is ignored and the OS can ask for less motion", () => {
  const dom = makeDom("", { media: { [REDUCE]: true } });
  dom.window.localStorage.setItem("theme", "purple");
  runScript(dom, "prism-theme-init.js");
  const root = dom.window.document.documentElement;
  assert.equal(root.hasAttribute("data-theme"), false);
  assert.equal(root.classList.contains("js-motion"), false);
  assert.equal(root.classList.contains("motion-off"), false);
});

test("theme init: blocked storage falls back to the OS preference", () => {
  const dom = makeDom("");
  blockStorage(dom);
  runScript(dom, "prism-theme-init.js");
  const root = dom.window.document.documentElement;
  assert.equal(root.hasAttribute("data-theme"), false);
  assert.equal(root.classList.contains("js-motion"), true);
});

test("theme init: a browser without matchMedia still gets motion", () => {
  const dom = makeDom("");
  dom.window.matchMedia = undefined;
  runScript(dom, "prism-theme-init.js");
  assert.equal(dom.window.document.documentElement.classList.contains("js-motion"), true);
});

function analyticsPage(url, token) {
  const dom = makeDom(`<script id="loader"${token ? ` data-cf-token="${token}"` : ""}></script>`, { url });
  const doc = dom.window.document;
  Object.defineProperty(doc, "currentScript", { configurable: true, get: () => doc.getElementById("loader") });
  runScript(dom, "pain001-analytics.js");
  return doc.querySelector('script[src="/js/cf-beacon.min.js"]');
}

test("analytics: the beacon loads on the deployed host with its token", () => {
  const beacon = analyticsPage("https://pain001.com/", "abc123");
  assert.ok(beacon, "beacon script appended");
  assert.equal(beacon.defer, true);
  assert.deepEqual(JSON.parse(beacon.dataset.cfBeacon), { token: "abc123" });
});

test("analytics: no beacon without a token or on a local preview", () => {
  assert.equal(analyticsPage("https://pain001.com/", ""), null);
  assert.equal(analyticsPage("http://localhost:8099/", "abc123"), null);
  assert.equal(analyticsPage("http://127.0.0.1:8099/", "abc123"), null);
});

test("redirect: a page that is not a legacy stub stays where it is", () => {
  const dom = makeDom("", { url: "https://pain001.com/documentation/" });
  runScript(dom, "redirect.js");
  assert.equal(dom.window.location.pathname, "/documentation/");
});
