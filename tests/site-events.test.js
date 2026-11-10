// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* pain001-events.js: first-party, cookie-free event counts (decision D1).
 * Every beacon carries the event name, the page path and at most a short
 * label, and nothing is sent locally, under Do Not Track or GPC, or for a
 * name outside the list. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { makeDom, runScript } = require("./helpers/browser.js");

/** A page with a recording sendBeacon; `sent` holds each decoded payload. */
function page(body, { url = "https://pain001.com/", nav = {}, beacon = "record" } = {}) {
  const dom = makeDom(body, { url });
  const sent = [];
  const navigator = dom.window.navigator;
  for (const [key, value] of Object.entries(nav)) {
    Object.defineProperty(navigator, key, { configurable: true, value });
  }
  if (beacon === "record") {
    navigator.sendBeacon = (endpoint, blob) => {
      sent.push({ endpoint, blob });
      return true;
    };
  } else if (beacon === "throw") {
    navigator.sendBeacon = () => { throw new Error("blocked"); };
  } else {
    navigator.sendBeacon = undefined;
  }
  runScript(dom, "pain001-events.js");
  return { dom, sent, doc: dom.window.document };
}

async function payloads(sent) {
  return Promise.all(sent.map(async ({ endpoint, blob }) => ({ endpoint, ...JSON.parse(await blob.text()) })));
}

function click(doc, selector) {
  doc.querySelector(selector).dispatchEvent(new doc.defaultView.MouseEvent("click", { bubbles: true }));
}

test("events: a tagged element sends its name, the page and its label to /e", async () => {
  const { doc, sent } = page('<a id="cta" href="/try/" data-event="hero_cta_click" data-event-label="validate-sample">Go</a>');
  click(doc, "#cta");
  assert.deepEqual(await payloads(sent), [{ endpoint: "/e", event: "hero_cta_click", page: "/", label: "validate-sample" }]);
});

test("events: a label is cut to 64 characters and an unlabelled event has none", async () => {
  const { doc, sent } = page(`<button id="a" data-event="install_copy" data-event-label="${"x".repeat(80)}">a</button><button id="b" data-event="xml_copy">b</button>`, { url: "https://pain001.com/try/" });
  click(doc, "#a");
  click(doc, "#b");
  const [a, b] = await payloads(sent);
  assert.equal(a.label.length, 64);
  assert.deepEqual(b, { endpoint: "/e", event: "xml_copy", page: "/try/" });
});

test("events: links are counted by host: GitHub and PyPI", async () => {
  const { doc, sent } = page(`
    <a id="gh" href="https://github.com/sebastienrousseau/pain001">GitHub</a>
    <a id="pypi" href="https://pypi.org/project/pain001/"><span id="inner">PyPI</span></a>
    <a id="other" href="https://example.com/">Elsewhere</a>
    <a id="local" href="/documentation/">Docs</a>`);
  for (const id of ["#gh", "#inner", "#other", "#local"]) click(doc, id);
  assert.deepEqual((await payloads(sent)).map((p) => p.event), ["outbound_github", "outbound_pypi"]);
});

test("events: an unknown name, a link that cannot be parsed, or a non-element target sends nothing", () => {
  const { doc, sent, dom } = page('<button id="x" data-event="session_replay">x</button><a id="bad" href="http://[bad">bad</a>');
  click(doc, "#x");
  click(doc, "#bad");
  doc.dispatchEvent(new dom.window.MouseEvent("click", { bubbles: true }));
  assert.equal(sent.length, 0);
  assert.equal(dom.window.pain001Event("not_an_event"), false);
});

test("events: the demo's first interaction counts once, whatever it is", async () => {
  const { doc, sent } = page('<div data-event-start><textarea id="csv"></textarea><button id="sample">Load</button></div>', { url: "https://pain001.com/try/" });
  const win = doc.defaultView;
  doc.getElementById("csv").dispatchEvent(new win.Event("input", { bubbles: true }));
  click(doc, "#sample");
  doc.getElementById("csv").dispatchEvent(new win.Event("paste", { bubbles: true }));
  assert.deepEqual((await payloads(sent)).map((p) => p.event), ["sandbox_start"]);
});

test("events: opening the bank-profile guide counts a view", async () => {
  const { sent } = page("", { url: "https://pain001.com/docs/bank-profiles/" });
  assert.deepEqual(await payloads(sent), [{ endpoint: "/e", event: "profile_guide_view", page: "/docs/bank-profiles/" }]);
});

test("events: nothing is sent from a local preview", () => {
  for (const url of ["http://localhost:8099/", "http://127.0.0.1:8099/docs/bank-profiles/"]) {
    const { doc, sent } = page('<a id="cta" data-event="hero_cta_click">Go</a>', { url });
    click(doc, "#cta");
    assert.equal(sent.length, 0, url);
  }
});

test("events: Do Not Track and Global Privacy Control silence every event", () => {
  for (const nav of [{ doNotTrack: "1" }, { globalPrivacyControl: true }]) {
    const { doc, sent } = page('<a id="cta" data-event="hero_cta_click">Go</a>', { nav });
    click(doc, "#cta");
    assert.equal(sent.length, 0, JSON.stringify(nav));
  }
});

test("events: a browser without sendBeacon, or one that refuses it, is left alone", () => {
  for (const beacon of ["missing", "throw"]) {
    const { doc, dom } = page('<a id="cta" data-event="hero_cta_click">Go</a>', { beacon });
    assert.doesNotThrow(() => click(doc, "#cta"));
    assert.equal(dom.window.pain001Event("hero_cta_click"), false);
  }
});
