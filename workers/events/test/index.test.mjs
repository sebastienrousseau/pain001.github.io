// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// The events Worker's handler, run under node:test with a fake
// Analytics Engine binding that records each data point.

import assert from "node:assert/strict";
import { test } from "node:test";

import worker, {
  EVENTS,
  MAX_BODY_BYTES,
  cleanPage,
  countryOf,
  handle,
  optedOut,
  parseEvent,
  readCapped,
  sameSite,
} from "../src/index.js";

const URL_E = "https://pain001.com/e";

function fakeEnv() {
  const points = [];
  return { points, EVENTS: { writeDataPoint: (p) => points.push(p) } };
}

function post(body, headers = {}, init = {}) {
  return new Request(URL_E, {
    method: "POST",
    body: typeof body === "string" ? body : JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
      Origin: "https://pain001.com",
      "Sec-Fetch-Site": "same-origin",
      ...headers,
    },
    ...init,
  });
}

test("a valid same-origin event writes one data point and returns 204", async () => {
  const env = fakeEnv();
  const response = await handle(
    post({ event: "sandbox_start", page: "/try/?sample=sepa#x", label: "sepa-sct" }),
    env,
  );
  assert.equal(response.status, 204);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
  assert.deepEqual(env.points, [
    {
      blobs: ["sandbox_start", "/try/", "sepa-sct", ""],
      doubles: [1],
      indexes: ["sandbox_start"],
    },
  ]);
});

test("every allow-listed event is accepted", async () => {
  for (const event of EVENTS) {
    const env = fakeEnv();
    const response = await handle(post({ event, page: "/" }), env);
    assert.equal(response.status, 204, event);
    assert.equal(env.points.length, 1, event);
    assert.equal(env.points[0].blobs[2], "", event);
  }
  assert.equal(EVENTS.size, 12);
});

test("nothing identifying is written", async () => {
  const env = fakeEnv();
  const request = post(
    { event: "xml_copy", page: "/try/" },
    {
      "User-Agent": "UA-should-not-appear",
      Referer: "https://pain001.com/try/?token=secret",
      "CF-Connecting-IP": "203.0.113.9",
      Cookie: "id=should-not-appear",
    },
  );
  await handle(request, env);
  const stored = JSON.stringify(env.points);
  for (const leak of ["UA-should-not-appear", "203.0.113.9", "secret", "should-not-appear"]) {
    assert.ok(!stored.includes(leak), leak);
  }
});

test("the country comes only from Cloudflare's two-letter code", async () => {
  const request = post({ event: "install_copy", page: "/" });
  Object.defineProperty(request, "cf", { value: { country: "GB" } });
  const env = fakeEnv();
  await handle(request, env);
  assert.equal(env.points[0].blobs[3], "GB");
  assert.equal(countryOf({ cf: { country: "gb1" } }), "");
  assert.equal(countryOf({ cf: { country: 7 } }), "");
  assert.equal(countryOf({}), "");
});

test("Do Not Track and Global Privacy Control drop the event with 204", async () => {
  for (const headers of [{ DNT: "1" }, { "Sec-GPC": "1" }]) {
    const env = fakeEnv();
    const response = await handle(post({ event: "xml_copy", page: "/" }, headers), env);
    assert.equal(response.status, 204);
    assert.equal(env.points.length, 0);
  }
  assert.equal(optedOut(new Headers({ DNT: "0" })), false);
});

test("cross-site posts are dropped with 204 and never written", async () => {
  for (const headers of [
    { Origin: "https://evil.example" },
    { "Sec-Fetch-Site": "cross-site" },
    { "Sec-Fetch-Site": "same-site" },
  ]) {
    const env = fakeEnv();
    const response = await handle(post({ event: "xml_copy", page: "/" }, headers), env);
    assert.equal(response.status, 204);
    assert.equal(env.points.length, 0);
  }
  assert.equal(sameSite(new Headers()), true);
});

test("other paths and methods are refused, with no CORS headers", async () => {
  const env = fakeEnv();
  const other = await handle(new Request("https://pain001.com/x", { method: "POST" }), env);
  assert.equal(other.status, 404);
  for (const method of ["GET", "OPTIONS", "PUT"]) {
    const response = await handle(new Request(URL_E, { method }), env);
    assert.equal(response.status, 405, method);
    assert.equal(response.headers.get("Allow"), "POST");
    assert.equal(response.headers.get("Access-Control-Allow-Origin"), null);
  }
  assert.equal(env.points.length, 0);
});

test("malformed or disallowed bodies get 400 and are not written", async () => {
  const bad = [
    "not json",
    "[]",
    "null",
    '"string"',
    { event: "pageview", page: "/" },
    { event: 1, page: "/" },
    { event: "xml_copy" },
    { event: "xml_copy", page: "https://evil.example/" },
    { event: "xml_copy", page: "//evil.example/" },
    { event: "xml_copy", page: "relative" },
    { event: "xml_copy", page: "/<script>" },
    { event: "xml_copy", page: "/" + "a".repeat(200) },
    { event: "xml_copy", page: "" },
    { event: "xml_copy", page: "/", label: "x".repeat(65) },
    { event: "xml_copy", page: "/", label: "<b>" },
    { event: "xml_copy", page: "/", label: 3 },
    { event: "xml_copy", page: "/", extra: "field" },
  ];
  for (const body of bad) {
    const env = fakeEnv();
    const response = await handle(post(body), env);
    assert.equal(response.status, 400, JSON.stringify(body));
    assert.equal(await response.text(), "");
    assert.equal(env.points.length, 0, JSON.stringify(body));
  }
});

test("an oversized body is refused before it is parsed", async () => {
  const big = JSON.stringify({ event: "xml_copy", page: "/", label: "x".repeat(MAX_BODY_BYTES) });
  const env = fakeEnv();
  const declared = await handle(post(big, { "Content-Length": String(big.length) }), env);
  assert.equal(declared.status, 400);
  // A body that understates its length is still cut off at the cap.
  const streamed = new Request(URL_E, {
    method: "POST",
    body: new ReadableStream({
      start(controller) {
        controller.enqueue(new TextEncoder().encode("x".repeat(MAX_BODY_BYTES)));
        controller.enqueue(new TextEncoder().encode("yy"));
        controller.close();
      },
    }),
    duplex: "half",
    headers: { Origin: "https://pain001.com" },
  });
  assert.equal(await readCapped(streamed), null);
  assert.equal(env.points.length, 0);
});

test("readCapped joins chunks and handles an empty body", async () => {
  const chunked = new Request(URL_E, {
    method: "POST",
    body: new ReadableStream({
      start(controller) {
        controller.enqueue(new TextEncoder().encode('{"event":'));
        controller.enqueue(new TextEncoder().encode('"xml_copy","page":"/"}'));
        controller.close();
      },
    }),
    duplex: "half",
  });
  assert.equal(await readCapped(chunked), '{"event":"xml_copy","page":"/"}');
  assert.equal(await readCapped(new Request(URL_E, { method: "POST" })), "");
});

test("a failed write is logged without request data and still returns 204", async (t) => {
  const logged = [];
  t.mock.method(console, "error", (line) => logged.push(line));
  const env = {
    EVENTS: {
      writeDataPoint() {
        throw new Error("binding unavailable");
      },
    },
  };
  const response = await handle(post({ event: "xml_copy", page: "/try/" }), env);
  assert.equal(response.status, 204);
  assert.equal(logged.length, 1);
  assert.deepEqual(JSON.parse(logged[0]), {
    message: "events write failed",
    error: "Error: binding unavailable",
  });
});

test("the module's fetch handler delegates to handle", async () => {
  const env = fakeEnv();
  const response = await worker.fetch(post({ event: "outbound_pypi", page: "/" }), env);
  assert.equal(response.status, 204);
  assert.equal(env.points.length, 1);
});

test("the helpers reject non-objects and keep clean paths", () => {
  assert.equal(parseEvent(undefined), null);
  assert.equal(cleanPage(5), null);
  assert.equal(cleanPage("/docs/a-b_c.d~e/"), "/docs/a-b_c.d~e/");
  assert.equal(cleanPage("?only=query"), null);
});
