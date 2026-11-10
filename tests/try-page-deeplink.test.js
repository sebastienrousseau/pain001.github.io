// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* /try/#sample=<key> opens a built-in sample, not only a corpus one.
 * The homepage's primary button links /try/#sample=sepa-sct; before
 * this, only corpus:<id> keys were honoured and the link opened an empty
 * page. Loading a sample validates it, so the visitor lands on a result. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { makeDom, settle } = require("./helpers/browser.js");
const { FIXTURE, PAGE_URL, installGlobals, fakeRuntime, fakeFetch } = require("./helpers/try-page.js");

test("try-page: #sample=sepa-sct opens and validates the built-in sample", async () => {
  const dom = makeDom(FIXTURE, { url: "https://pain001.com/try/#sample=sepa-sct" });
  const win = dom.window;
  installGlobals(win);
  globalThis.fetch = fakeFetch({ corpus: "missing" });
  win.loadPyodide = fakeRuntime().loadPyodide;

  await import(PAGE_URL);
  await settle();
  const $ = (id) => win.document.getElementById(id);
  const { SAMPLES } = await import(PAGE_URL.replace("try-page.js", "try-demo.js"));
  assert.equal($("csv-input").value, SAMPLES["sepa-sct"].csv.trim());
  assert.equal($("editor-block").hidden, false);
  assert.match($("status").textContent, /^✓/, "the sample is validated on arrival");
});
