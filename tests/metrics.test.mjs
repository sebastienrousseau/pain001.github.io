import { test } from "node:test";
import assert from "node:assert/strict";
import { EVENTS, configured, optedOut, classify, payload } from "../static/js/metrics-core.js";

const el = (attrs = {}, dataset = {}) => ({
  dataset, getAttribute: (k) => (k in attrs ? attrs[k] : null),
});

test("exactly five events exist and nothing else is counted", () => {
  assert.deepEqual([...EVENTS], ["try_run", "try_download_xml", "corpus_zip_download", "install_click", "contact_submit"]);
  assert.equal(classify(el({}, { track: "made_up" })), null);
  assert.equal(classify(el({ href: "/documentation/" })), null);
});

test("measurement is off until a real website id is configured", () => {
  assert.equal(configured("00000000-0000-0000-0000-000000000000", "https://metrics.pain001.com"), false);
  assert.equal(configured("", "https://metrics.pain001.com"), false);
  assert.equal(configured("3f2c1b0a-9d8e-4f7a-b6c5-d4e3f2a1b0c9", "http://metrics.pain001.com"), false);
  assert.equal(configured("3f2c1b0a-9d8e-4f7a-b6c5-d4e3f2a1b0c9", "https://metrics.pain001.com"), true);
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
  assert.deepEqual(classify(el({ href: "/corpus/pain001-example-corpus-0.0.69.zip" })), { name: "corpus_zip_download", label: "pain001-example-corpus-0.0.69.zip" });
  assert.deepEqual(classify(el({ href: "https://pypi.org/project/pain001-mcp/" })), { name: "install_click", label: "pain001-mcp" });
  assert.equal(classify(el({ href: "https://example.com/x.zip" })), null);
});

test("the collector body carries no identifiers and drops same-site referrers", () => {
  const page = { origin: "https://pain001.com", hostname: "pain001.com", pathname: "/try/" };
  const body = payload({ websiteId: "id", name: "try_run", label: "csv", page, referrer: "https://pain001.com/", language: "en-GB", screen: "1440x900", title: "Try" });
  assert.equal(body.type, "event");
  assert.deepEqual(Object.keys(body.payload).sort(), ["data", "hostname", "language", "name", "referrer", "screen", "title", "url", "website"]);
  assert.equal(body.payload.referrer, "");
  assert.deepEqual(body.payload.data, { label: "csv" });
  const view = payload({ websiteId: "id", page, referrer: "https://duckduckgo.com/", language: "en", screen: "", title: "" });
  assert.equal(view.payload.referrer, "https://duckduckgo.com/");
  assert.equal("name" in view.payload, false);
});
