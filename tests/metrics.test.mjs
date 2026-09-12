import { test } from "node:test";
import assert from "node:assert/strict";
import { EVENTS, configured, optedOut, classify, countQuery } from "../static/js/metrics-core.js";

const el = (attrs = {}, dataset = {}) => ({
  dataset, getAttribute: (k) => (k in attrs ? attrs[k] : null),
});

test("exactly five events exist and nothing else is counted", () => {
  assert.deepEqual([...EVENTS], ["try_run", "try_download_xml", "corpus_zip_download", "install_click", "contact_submit"]);
  assert.equal(classify(el({}, { track: "made_up" })), null);
  assert.equal(classify(el({ href: "/documentation/" })), null);
});

test("measurement is off until the layout enables it against an https host", () => {
  assert.equal(configured("false", "https://metrics.pain001.com"), false);
  assert.equal(configured("true", "http://metrics.pain001.com"), false);
  assert.equal(configured(undefined, "https://metrics.pain001.com"), false);
  assert.equal(configured("true", "https://metrics.pain001.com"), true);
});

test("Do-Not-Track and Global Privacy Control switch it off", () => {
  assert.equal(optedOut({ doNotTrack: "1" }), true);
  assert.equal(optedOut({ globalPrivacyControl: true }), true);
  assert.equal(optedOut({ doNotTrack: "0" }), false);
  assert.equal(optedOut(undefined), true);
});

test("clicks map to events by data-track, corpus zip, or PyPI link", () => {
  assert.deepEqual(classify(el({}, { track: "try_run" })), { name: "try_run", label: "" });
  assert.deepEqual(classify(el({}, { track: "try_download_xml:pain.001.001.09" })), { name: "try_download_xml", label: "pain.001.001.09" });
  assert.deepEqual(classify(el({ href: "/corpus/pain001-example-corpus-0.0.70.zip" })), { name: "corpus_zip_download", label: "pain001-example-corpus-0.0.70.zip" });
  assert.deepEqual(classify(el({ href: "https://pypi.org/project/pain001-mcp/" })), { name: "install_click", label: "pain001-mcp" });
  assert.equal(classify(el({ href: "https://example.com/x.zip" })), null);
});

test("the count query carries no identifiers and drops same-site referrers", () => {
  const page = { origin: "https://pain001.com", pathname: "/try/" };
  const view = new URLSearchParams(countQuery({ page, referrer: "https://pain001.com/", screen: "1440,900,2", title: "Try" }));
  assert.equal(view.get("p"), "/try/");
  assert.equal(view.get("r"), "");
  assert.equal(view.get("e"), null);
  assert.deepEqual([...view.keys()].sort(), ["p", "r", "rnd", "s", "t"]);
  const ev = new URLSearchParams(countQuery({ name: "try_run", label: "csv", page, referrer: "https://duckduckgo.com/", screen: "", title: "" }));
  assert.equal(ev.get("p"), "try_run:csv");
  assert.equal(ev.get("e"), "true");
  assert.equal(ev.get("r"), "https://duckduckgo.com/");
});
