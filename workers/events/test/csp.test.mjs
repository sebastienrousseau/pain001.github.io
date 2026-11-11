// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// CSP violation reports on /e/csp, run under node:test with the same
// fake Analytics Engine binding as the events tests.

import assert from "node:assert/strict";
import { test } from "node:test";

import {
  MAX_CSP_BODY_BYTES,
  blockedOrigin,
  parseViolation,
  recordViolations,
  violations,
} from "../src/csp.js";
import worker, { handleCsp } from "../src/index.js";

const URL_CSP = "https://pain001.com/e/csp";

function fakeEnv() {
  const points = [];
  return { points, EVENTS: { writeDataPoint: (p) => points.push(p) } };
}

function report(body, headers = {}, method = "POST") {
  return new Request(URL_CSP, {
    method,
    body:
      method === "POST"
        ? typeof body === "string"
          ? body
          : JSON.stringify(body)
        : undefined,
    headers: { "Content-Type": "application/csp-report", ...headers },
  });
}

const LEGACY = {
  "csp-report": {
    "document-uri": "https://pain001.com/for-banks/?q=secret#x",
    "effective-directive": "form-action",
    "violated-directive": "form-action 'self'",
    "blocked-uri": "https://evil.example/collect?id=42",
    "original-policy": "form-action 'self'",
  },
};

const MODERN = {
  type: "csp-violation",
  body: {
    documentURL: "https://pain001.com/",
    effectiveDirective: "object-src",
    blockedURL: "inline",
  },
};

test("a report-uri report is stored without the path or query", async () => {
  const env = fakeEnv();
  const response = await worker.fetch(report(LEGACY), env);
  assert.equal(response.status, 204);
  assert.deepEqual(env.points, [
    {
      blobs: [
        "csp_violation",
        "/for-banks/",
        "form-action",
        "",
        "https://evil.example",
      ],
      doubles: [1],
      indexes: ["csp_violation"],
    },
  ]);
});

test("a Reporting API list stores each csp-violation entry", async () => {
  const env = fakeEnv();
  const other = { type: "deprecation", body: {} };
  const response = await handleCsp(report([MODERN, other, MODERN]), env);
  assert.equal(response.status, 204);
  assert.equal(env.points.length, 2);
  assert.deepEqual(env.points[0].blobs, [
    "csp_violation",
    "/",
    "object-src",
    "",
    "inline",
  ]);
});

test("only the first ten entries of a list are read", () => {
  assert.equal(violations(Array(20).fill(MODERN)).length, 10);
});

test("the violated directive is used when no effective one is given", () => {
  const body = { ...LEGACY["csp-report"] };
  delete body["effective-directive"];
  assert.equal(parseViolation({ "csp-report": body }).directive, "form-action");
});

test("reports for other sites or malformed fields are dropped", () => {
  const bad = (patch) =>
    parseViolation({ "csp-report": { ...LEGACY["csp-report"], ...patch } });
  assert.equal(bad({ "document-uri": "https://other.example/" }), null);
  assert.equal(bad({ "document-uri": "not a url" }), null);
  assert.equal(bad({ "document-uri": 7 }), null);
  assert.equal(bad({ "document-uri": "https://pain001.com//x" }), null);
  assert.equal(
    bad({ "effective-directive": 3, "violated-directive": undefined }),
    null,
  );
  assert.equal(bad({ "effective-directive": "Script Src!" }), null);
  assert.equal(parseViolation(null), null);
  assert.equal(parseViolation("x"), null);
  assert.equal(parseViolation({ type: "csp-violation" }), null);
  assert.equal(parseViolation({}), null);
});

test("blocked URIs keep only a keyword, a scheme or an origin", () => {
  assert.equal(blockedOrigin("eval"), "eval");
  assert.equal(
    blockedOrigin("http://a.example:8080/p?q"),
    "http://a.example:8080",
  );
  assert.equal(blockedOrigin("data:text/html,hi"), "data");
  assert.equal(
    blockedOrigin("chrome-extension://abc/x.js"),
    "chrome-extension",
  );
  assert.equal(blockedOrigin("no scheme"), "other");
  assert.equal(blockedOrigin(""), "other");
  assert.equal(blockedOrigin(undefined), "other");
});

test("opted-out visitors are dropped with 204", async () => {
  const env = fakeEnv();
  const response = await handleCsp(report(LEGACY, { "Sec-GPC": "1" }), env);
  assert.equal(response.status, 204);
  assert.equal(env.points.length, 0);
});

test("only POST is accepted", async () => {
  const response = await handleCsp(report(null, {}, "GET"), fakeEnv());
  assert.equal(response.status, 405);
  assert.equal(response.headers.get("Allow"), "POST");
});

test("an oversized or malformed body is refused with 400", async () => {
  const big = "x".repeat(MAX_CSP_BODY_BYTES + 1);
  assert.equal((await handleCsp(report(big), fakeEnv())).status, 400);
  assert.equal((await handleCsp(report("{not json"), fakeEnv())).status, 400);
});

test("a report the parser rejects still answers 204 and stores nothing", async () => {
  const env = fakeEnv();
  const response = await handleCsp(report({ hello: "world" }), env);
  assert.equal(response.status, 204);
  assert.equal(env.points.length, 0);
});

test("a failed write is logged without request data", () => {
  const logged = [];
  const original = console.error;
  console.error = (line) => logged.push(line);
  try {
    const env = {
      EVENTS: {
        writeDataPoint: () => {
          throw new Error("down");
        },
      },
    };
    recordViolations([parseViolation(LEGACY)], new Request(URL_CSP), env);
  } finally {
    console.error = original;
  }
  assert.equal(logged.length, 1);
  assert.match(logged[0], /csp write failed/);
  assert.doesNotMatch(logged[0], /evil|for-banks/);
});
