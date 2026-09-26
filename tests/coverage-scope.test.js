// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* Node's coverage report only lists files a test loaded, so a new script
 * in static/js/ with no test would sit outside the coverage gate unseen.
 * Every shipped script except the vendored beacon must be loaded by a
 * test file. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const VENDORED = new Set(["cf-beacon.min.js"]);

test("every shipped script in static/js is exercised by a test", () => {
  const jsDir = path.resolve(__dirname, "../static/js");
  const scripts = fs.readdirSync(jsDir).filter((f) => f.endsWith(".js") && !VENDORED.has(f));
  const tests = fs.readdirSync(__dirname)
    .filter((f) => /\.test\.m?js$/.test(f))
    .map((f) => fs.readFileSync(path.join(__dirname, f), "utf8"))
    .concat(fs.readFileSync(path.join(__dirname, "helpers/try-page.js"), "utf8"))
    .join("\n");
  const untested = scripts.filter((f) => !tests.includes(f));
  assert.deepEqual(untested, [], `add tests for: ${untested.join(", ")}`);
});
