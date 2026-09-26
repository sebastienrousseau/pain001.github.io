// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The site chrome: navigation disclosure, mega-menu panels and the theme
 * control (prism.js), and the Pain001 layer on top of it
 * (pain001-prism.js): current-page marking, contents rails, the motion
 * toggle, scrollable tables and bookmarks. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const {
  makeDom, runScript, blockStorage, stillLoading, installIntersectionObserver, manualTimers,
} = require("./helpers/browser.js");

const WIDE = "(min-width: 64rem)";
const HOVER = "(hover: hover)";
const DARK = "(prefers-color-scheme: dark)";

const CHROME = `
  <div data-ssg-search></div>
  <header>
    <button id="navToggle" aria-expanded="false">Menu</button>
    <nav id="navMenu">
      <ul>
        <li class="nav-item has-panel" id="item-a">
          <a class="nav-link" href="/solutions/">Solutions</a>
          <button class="nav-disclosure" aria-expanded="false">More</button>
          <div class="nav-panel"><a href="/a/" id="panel-a-link">A</a></div>
        </li>
        <li class="nav-item has-panel" id="item-b">
          <a class="nav-link" href="/documentation/">Docs</a>
          <button class="nav-disclosure" aria-expanded="false">More</button>
          <div class="nav-panel"><a href="/b/">B</a></div>
        </li>
        <li class="nav-item has-panel" id="item-broken"><a href="/x/">No panel</a></li>
      </ul>
    </nav>
    <button id="mode-toggle" data-label-light="Clair" data-label-dark="Sombre"><span id="mode-state"> System </span></button>
  </header>
  <main><p id="outside">Body</p></main>
  <button id="ssg-search-btn">Search</button>`;

function chrome(opts) {
  const dom = makeDom(CHROME, opts);
  runScript(dom, "prism.js");
  const $ = (id) => dom.window.document.getElementById(id);
  const click = (el) => el.dispatchEvent(new dom.window.MouseEvent("click", { bubbles: true }));
  return { dom, $, click, doc: dom.window.document };
}

test("prism: the search trigger moves into its header slot", () => {
  const { doc, $ } = chrome();
  assert.equal(doc.querySelector("[data-ssg-search]"), null);
  assert.equal($("ssg-search-btn").parentElement.tagName, "BODY");
  assert.ok(doc.querySelector("header").previousElementSibling === $("ssg-search-btn"));
});

test("prism: the navigation disclosure opens, closes on Escape and on an outside click", () => {
  const { dom, $, click } = chrome();
  const toggle = $("navToggle");
  const menu = $("navMenu");
  assert.equal(toggle.getAttribute("aria-expanded"), "false");
  click(toggle);
  assert.equal(toggle.getAttribute("aria-expanded"), "true");
  assert.equal(menu.getAttribute("data-open"), "true");
  menu.dispatchEvent(new dom.window.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  assert.equal(toggle.getAttribute("aria-expanded"), "false");
  assert.equal(dom.window.document.activeElement, toggle);
  click(toggle);
  click($("outside"));
  assert.equal(toggle.getAttribute("aria-expanded"), "false");
  click(toggle);
  menu.dispatchEvent(new dom.window.KeyboardEvent("keydown", { key: "a", bubbles: true }));
  assert.equal(toggle.getAttribute("aria-expanded"), "true", "other keys leave it open");
});

test("prism: panels open one at a time by click and close by click, Escape and focus leaving", () => {
  const { dom, $, click, doc } = chrome();
  const [a, b] = ["item-a", "item-b"].map($);
  const btnA = a.querySelector(".nav-disclosure");
  const btnB = b.querySelector(".nav-disclosure");
  const panelA = a.querySelector(".nav-panel");
  assert.equal(panelA.hidden, true);
  click(btnA);
  assert.equal(btnA.getAttribute("aria-expanded"), "true");
  assert.equal(panelA.hidden, false);
  assert.ok(a.classList.contains("is-open"));
  click(btnB);
  assert.equal(btnA.getAttribute("aria-expanded"), "false", "opening B closes A");
  click(btnB);
  assert.equal(btnB.getAttribute("aria-expanded"), "false", "a second click closes it");

  click(btnA);
  const esc = new dom.window.KeyboardEvent("keydown", { key: "Escape", bubbles: true, cancelable: true });
  $("panel-a-link").dispatchEvent(esc);
  assert.equal(btnA.getAttribute("aria-expanded"), "false");
  assert.equal(doc.activeElement, btnA);
  assert.equal(esc.defaultPrevented, true);
  a.dispatchEvent(new dom.window.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));

  click(btnA);
  a.dispatchEvent(new dom.window.FocusEvent("focusout", { relatedTarget: $("panel-a-link") }));
  assert.equal(btnA.getAttribute("aria-expanded"), "true", "focus moving inside keeps it open");
  a.dispatchEvent(new dom.window.FocusEvent("focusout", { relatedTarget: $("outside") }));
  assert.equal(btnA.getAttribute("aria-expanded"), "false");

  click(btnA);
  click($("outside"));
  assert.equal(btnA.getAttribute("aria-expanded"), "false", "an outside click closes every panel");
});

test("prism: on a wide hover-capable screen panels follow the pointer and stay inside the viewport", () => {
  const { dom, $, click } = chrome({ media: { [WIDE]: true, [HOVER]: true } });
  const timers = manualTimers(dom);
  const a = $("item-a");
  const btn = a.querySelector(".nav-disclosure");
  const panel = a.querySelector(".nav-panel");
  panel.getBoundingClientRect = () => ({ right: dom.window.innerWidth + 40 });
  a.dispatchEvent(new dom.window.MouseEvent("mouseenter"));
  assert.equal(btn.getAttribute("aria-expanded"), "true");
  assert.equal(panel.style.left, `-${40 + 16}px`, "pulled back inside the viewport");
  a.dispatchEvent(new dom.window.MouseEvent("mouseenter"));
  click(btn);
  assert.equal(btn.getAttribute("aria-expanded"), "true", "a click pins a hovered panel");
  a.dispatchEvent(new dom.window.MouseEvent("mouseleave"));
  timers.flush();
  assert.equal(btn.getAttribute("aria-expanded"), "false", "leaving closes it after the delay");

  panel.getBoundingClientRect = () => ({ right: 10 });
  click(btn);
  assert.equal(panel.style.left, "", "no offset when it fits");

  dom.setMedia(WIDE, false);
  assert.equal(btn.getAttribute("aria-expanded"), "false", "a layout change resets the menu");
  a.dispatchEvent(new dom.window.MouseEvent("mouseenter"));
  assert.equal(btn.getAttribute("aria-expanded"), "false", "no hover behaviour on the narrow layout");
  a.dispatchEvent(new dom.window.MouseEvent("mouseleave"));
  assert.equal(timers.queue.length, 0);
});

test("prism: the theme control cycles system, light and dark and remembers the choice", () => {
  const { dom, $, click } = chrome();
  const root = dom.window.document.documentElement;
  const label = $("mode-state");
  assert.equal(label.textContent, "System");
  click($("mode-toggle"));
  assert.equal(root.getAttribute("data-theme"), "light");
  assert.equal(label.textContent, "Clair");
  assert.equal(dom.window.localStorage.getItem("theme"), "light");
  click($("mode-toggle"));
  assert.equal(root.getAttribute("data-theme"), "dark");
  assert.equal(label.textContent, "Sombre");
  click($("mode-toggle"));
  assert.equal(root.hasAttribute("data-theme"), false);
  assert.equal(dom.window.localStorage.getItem("theme"), null);
  label.textContent = "stale";
  dom.setMedia(DARK, true);
  assert.equal(label.textContent, "System", "follows OS changes while on system");
  click($("mode-toggle"));
  label.textContent = "kept";
  dom.setMedia(DARK, false);
  assert.equal(label.textContent, "kept", "an explicit choice is not overwritten");
});

test("prism: the theme control works with blocked storage and default labels", () => {
  const dom = makeDom(`<button id="mode-toggle"><span id="mode-state">Auto</span></button>`, { htmlClass: "" });
  dom.window.document.documentElement.setAttribute("data-theme", "dark");
  blockStorage(dom);
  stillLoading(dom);
  runScript(dom, "prism.js");
  dom.window.document.dispatchEvent(new dom.window.Event("DOMContentLoaded"));
  const btn = dom.window.document.getElementById("mode-toggle");
  const label = dom.window.document.getElementById("mode-state");
  assert.equal(label.textContent, "Dark");
  btn.click();
  assert.equal(dom.window.document.documentElement.hasAttribute("data-theme"), false);
  btn.click();
  assert.equal(label.textContent, "Light");
});

test("prism: a page without the chrome does nothing and clicks are harmless", () => {
  const dom = makeDom(`<p id="p">x</p>`);
  dom.window.matchMedia = (q) => ({ media: q, matches: false });
  runScript(dom, "prism.js");
  dom.window.document.getElementById("p").click();
});

/* ---------------- pain001-prism.js ---------------- */

const LAYER = `
  <nav>
    <a class="nav-link" href="/">Home</a>
    <a class="nav-link" href="/documentation/">Docs</a>
    <a class="nav-link" href="/faqs/">FAQs</a>
  </nav>
  <span class="ap-lang-current">??</span>
  <aside data-local-nav><a href="#one">One</a><a href="#two">Two</a><a href="#missing">Missing</a></aside>
  <main>
    <h2 id="one">Rates #</h2>
    <div class="table-responsive" id="t1"><table><tr><th>Scheme</th></tr></table></div>
    <div class="table-responsive" id="t2"><table><tr><th>Scheme</th></tr></table></div>
    <h3 id="two">Fees</h3>
    <div class="table-responsive" id="t3"><table><tr><td>no header</td></tr></table></div>
    <div class="table-responsive" id="t4"><table></table></div>
    <div class="table-responsive" id="t5" tabindex="0"></div>
    <div role="region"><div class="table-responsive" id="t6"></div></div>
  </main>
  <button id="motion-toggle">Reduce motion</button>
  <div data-reveal id="r1"></div>
  <button id="bookmark-page">Save page</button>`;

function layer({ url = "https://pain001.com/documentation", lang = "fr-FR", htmlClass = "", overflow = ["t1", "t2", "t3", "t4", "t5", "t6"], before } = {}) {
  const dom = makeDom(LAYER, { url, lang, htmlClass });
  const doc = dom.window.document;
  for (const id of overflow) {
    const el = doc.getElementById(id);
    Object.defineProperty(el, "scrollWidth", { configurable: true, value: 800 });
    Object.defineProperty(el, "clientWidth", { configurable: true, value: 300 });
  }
  if (before) before(dom);
  runScript(dom, "pain001-prism.js");
  return { dom, doc, $: (id) => doc.getElementById(id) };
}

test("pain001-prism: current page, locale label and scrollable tables", () => {
  let io;
  const { doc, $ } = layer({ before: (dom) => { io = installIntersectionObserver(dom); } });
  const current = [...doc.querySelectorAll('.nav-link[aria-current="page"]')].map((a) => a.getAttribute("href"));
  assert.deepEqual(current, ["/documentation/"]);
  assert.equal(doc.querySelector(".ap-lang-current").textContent, "FR");
  assert.equal($("t1").getAttribute("aria-label"), "Rates: Scheme");
  assert.equal($("t2").getAttribute("aria-label"), "Rates: Scheme (2)", "duplicate names are numbered");
  assert.equal($("t3").getAttribute("aria-label"), "Fees");
  assert.equal($("t1").getAttribute("role"), "region");
  assert.equal($("t5").hasAttribute("role"), false, "already focusable: left alone");
  assert.equal($("t6").hasAttribute("role"), false, "inside a region: left alone");

  io.fire($("two"));
  assert.equal(doc.querySelector('[data-local-nav] a[href="#two"]').getAttribute("aria-current"), "location");
  io.fire($("one"));
  assert.equal(doc.querySelector('[data-local-nav] a[href="#two"]').hasAttribute("aria-current"), false);
  io.fire($("one"), false);
  assert.equal(doc.querySelector('[data-local-nav] a[href="#one"]').getAttribute("aria-current"), "location");
});

test("pain001-prism: the home link and an untitled table", () => {
  const { doc, $ } = layer({
    url: "https://pain001.com/", lang: "",
    before: (dom) => {
      dom.window.document.title = "Pain001";
      dom.window.document.querySelectorAll("main h2, main h3").forEach((h) => h.remove());
      dom.window.document.querySelectorAll("#t1 th, #t2 th").forEach((th) => th.remove());
    },
  });
  assert.equal(doc.querySelector('.nav-link[href="/"]').getAttribute("aria-current"), "page");
  assert.equal(doc.querySelector(".ap-lang-current").textContent, "EN");
  assert.equal($("t1").getAttribute("aria-label"), "Pain001", "falls back to the page title");
  assert.equal($("t2").getAttribute("aria-label"), "Pain001 (2)");
});

test("pain001-prism: tables that fit are not made focusable", () => {
  const { $ } = layer({ overflow: [] });
  assert.equal($("t1").hasAttribute("tabindex"), false);
});

test("pain001-prism: the motion toggle stores the choice and reveals content", () => {
  const { dom, doc, $ } = layer({ htmlClass: "js-motion" });
  const btn = $("motion-toggle");
  const root = doc.documentElement;
  assert.equal(btn.getAttribute("aria-pressed"), "false");
  btn.click();
  assert.equal(btn.getAttribute("aria-pressed"), "true");
  assert.ok(root.classList.contains("motion-off"));
  assert.equal(root.classList.contains("js-motion"), false);
  assert.ok($("r1").classList.contains("is-visible"));
  assert.equal(dom.window.localStorage.getItem("motion"), "off");
  btn.click();
  assert.equal(root.classList.contains("js-motion"), true);
  assert.equal(dom.window.localStorage.getItem("motion"), null);
  dom.setMedia("(prefers-reduced-motion: reduce)", true);
  btn.click();
  btn.click();
  assert.equal(root.classList.contains("js-motion"), false, "the OS preference still applies");
});

test("pain001-prism: bookmarks toggle and persist, and survive blocked storage", () => {
  const { dom, $ } = layer({ before: (d) => d.window.localStorage.setItem("pain001:bookmarks", "not json") });
  const btn = $("bookmark-page");
  assert.equal(btn.getAttribute("aria-pressed"), "false");
  btn.click();
  assert.equal(btn.getAttribute("aria-pressed"), "true");
  assert.deepEqual(JSON.parse(dom.window.localStorage.getItem("pain001:bookmarks")).map((b) => b.url), ["/documentation/"]);
  btn.click();
  assert.equal(btn.getAttribute("aria-pressed"), "false");

  const blocked = layer({ htmlClass: "motion-off", before: (d) => { blockStorage(d); stillLoading(d); } });
  blocked.dom.window.document.dispatchEvent(new blocked.dom.window.Event("DOMContentLoaded"));
  assert.equal(blocked.$("motion-toggle").getAttribute("aria-pressed"), "true");
  blocked.$("motion-toggle").click();
  blocked.$("bookmark-page").click();
  assert.equal(blocked.$("bookmark-page").getAttribute("aria-pressed"), "true", "works for this page view");
});

test("pain001-prism: a page without the optional controls", () => {
  const dom = makeDom(`<nav><a class="nav-link">No href</a></nav><aside data-local-nav></aside>`);
  dom.window.matchMedia = undefined;
  runScript(dom, "pain001-prism.js");
  assert.equal(dom.window.document.querySelector(".nav-link").hasAttribute("aria-current"), false);
});
