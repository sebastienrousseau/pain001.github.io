// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The homepage: recorded-run tabs, scroll reveals, the gallery, copy
 * buttons, and dated content checked against the visitor's clock. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const {
  makeDom, runScript, stillLoading, installIntersectionObserver, manualTimers, settle,
} = require("./helpers/browser.js");

const PAGE = `
  <div data-tabs>
    <button role="tab" id="t1" aria-controls="p1">One</button>
    <button role="tab" id="t2" aria-controls="p2">Two</button>
    <button role="tab" id="t3" aria-controls="missing">Three</button>
  </div>
  <div id="p1"></div><div id="p2"></div>
  <section data-reveal id="r1"></section><section data-settle id="r2"></section>
  <div data-gallery>
    <div class="gallery-track" id="track"><figure id="s0"></figure><figure id="s1"></figure><figure id="s2"></figure></div>
    <button data-gallery-prev id="prev"></button><button data-gallery-next id="next"></button>
    <button data-gallery-to="0" id="d0"></button><button data-gallery-to="1" id="d1"></button><button data-gallery-to="2" id="d2"></button>
  </div>
  <div data-gallery><div class="gallery-track"><figure></figure></div></div>
  <div data-copy-group>
    <pre id="cmd">pip install pain001</pre>
    <button data-copy="cmd" data-label-copied="Copié" id="copy">Copy</button>
    <span data-copy-status id="copy-status"></span>
  </div>
  <button data-copy="cmd" id="copy-bare">Copy</button>
  <button data-copy="nope" id="copy-missing">Copy</button>
  <p data-expires="2000-01-01" id="expired">old</p>
  <p data-expires="2999-01-01" id="current">new</p>
  <ol data-timeline>
    <li class="milestone" id="m1"><time datetime="2001-01-01"></time><span class="milestone-flag"></span></li>
    <li class="milestone" id="m2"><time datetime="2998-01-01"></time><span class="milestone-flag"></span></li>
    <li class="milestone" id="m3"><time datetime="2999-01-01"></time></li>
    <li class="milestone" id="m4"><span class="milestone-flag"></span></li>
  </ol>`;

function home({ htmlClass = "js-motion", io = true, clipboard = true, rtl = false, loading = false } = {}) {
  const dom = makeDom(PAGE, { htmlClass });
  const win = dom.window;
  const observer = io ? installIntersectionObserver(dom) : null;
  const timers = manualTimers(dom);
  const scrolls = [];
  win.HTMLElement.prototype.scrollTo = function (opts) { scrolls.push({ el: this.id, ...opts }); };
  if (rtl) win.document.getElementById("track").style.direction = "rtl";
  const written = [];
  if (clipboard) {
    Object.defineProperty(win.navigator, "clipboard", {
      configurable: true, value: { writeText: (text) => { written.push(text); return Promise.resolve(); } },
    });
  }
  if (loading) stillLoading(dom);
  runScript(dom, "home.js");
  if (loading) win.document.dispatchEvent(new win.Event("DOMContentLoaded"));
  const $ = (id) => win.document.getElementById(id);
  const key = (el, k) => {
    const e = new win.KeyboardEvent("keydown", { key: k, cancelable: true, bubbles: true });
    el.dispatchEvent(e);
    return e;
  };
  return { dom, win, $, observer, timers, scrolls, written, key };
}

test("home: tabs follow the WAI-ARIA pattern with click, arrows, Home and End", () => {
  const { win, $, key } = home();
  $("t2").click();
  assert.equal($("t2").getAttribute("aria-selected"), "true");
  assert.equal($("t1").tabIndex, -1);
  assert.equal($("p1").hidden, true);
  assert.equal($("p2").hidden, false);
  assert.equal(key($("t2"), "ArrowRight").defaultPrevented, true);
  assert.equal(win.document.activeElement, $("t3"));
  key($("t3"), "ArrowRight");
  assert.equal($("t1").getAttribute("aria-selected"), "true", "wraps to the first tab");
  key($("t1"), "ArrowLeft");
  assert.equal($("t3").getAttribute("aria-selected"), "true", "wraps to the last tab");
  key($("t3"), "Home");
  assert.equal($("t1").getAttribute("aria-selected"), "true");
  key($("t1"), "End");
  assert.equal($("t3").getAttribute("aria-selected"), "true");
  assert.equal(key($("t3"), "x").defaultPrevented, false);
});

test("home: reveals wait for the viewport when motion is on", () => {
  const { $, observer } = home();
  assert.equal($("r1").classList.contains("is-visible"), false);
  observer.fire($("r1"), false);
  assert.equal($("r1").classList.contains("is-visible"), false);
  observer.fire($("r1"));
  assert.ok($("r1").classList.contains("is-visible"));
});

test("home: without motion, or without IntersectionObserver, everything is visible at once", () => {
  assert.ok(home({ htmlClass: "" }).$("r2").classList.contains("is-visible"));
  assert.ok(home({ io: false, loading: true }).$("r1").classList.contains("is-visible"));
});

test("home: the gallery scrolls with its buttons and dots and marks the slide in view", () => {
  const { $, scrolls, observer } = home();
  $("next").click();
  $("d2").click();
  $("next").click();
  $("prev").click();
  $("d0").click();
  $("prev").click();
  assert.deepEqual(scrolls.map((s) => s.behavior), ["smooth", "smooth", "smooth", "smooth", "smooth", "smooth"]);
  observer.fire($("s2"));
  assert.equal($("d2").getAttribute("aria-current"), "true");
  assert.equal($("d0").hasAttribute("aria-current"), false);
  observer.fire($("s0"));
  assert.equal($("d0").getAttribute("aria-current"), "true");
});

test("home: a right-to-left gallery without motion scrolls instantly", () => {
  const { $, scrolls } = home({ rtl: true, htmlClass: "", io: false });
  $("next").click();
  assert.equal(scrolls[0].behavior, "auto");
  assert.equal(typeof scrolls[0].left, "number");
});

test("home: copy buttons copy, confirm, announce and reset", async () => {
  const { $, written, timers } = home();
  $("copy").click();
  await settle();
  assert.deepEqual(written, ["pip install pain001"]);
  assert.equal($("copy").textContent, "Copié");
  assert.equal($("copy-status").textContent, "Copié");
  assert.equal($("copy").hasAttribute("data-copied"), true);
  timers.flush();
  assert.equal($("copy").textContent, "Copy");
  assert.equal($("copy-status").textContent, "");

  $("copy-bare").click();
  await settle();
  assert.equal($("copy-bare").textContent, "Copied");
  timers.flush();
  assert.equal($("copy-bare").textContent, "Copy");
  $("copy-missing").click();
  await settle();
  assert.equal(written.length, 2, "a missing source copies nothing");
});

test("home: without the clipboard API the copy button does nothing", async () => {
  const { $ } = home({ clipboard: false });
  $("copy").click();
  await settle();
  assert.equal($("copy").textContent, "Copy");
});

test("home: expired content is removed and the next milestone is flagged", () => {
  const { $ } = home();
  assert.equal($("expired"), null);
  assert.ok($("current"));
  assert.ok($("m1").classList.contains("is-past"));
  assert.equal($("m1").querySelector(".milestone-flag").hidden, true);
  assert.ok($("m2").classList.contains("is-next"));
  assert.equal($("m2").querySelector(".milestone-flag").hidden, false);
  assert.equal($("m3").classList.contains("is-next"), false);
  assert.equal($("m4").classList.contains("is-past"), false, "undated items count as future");
  assert.equal($("m4").querySelector(".milestone-flag").hidden, true);
});
