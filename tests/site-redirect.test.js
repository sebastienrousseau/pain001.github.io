// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* The legacy-URL redirect with a stamped redirect table (issue #53).
 *
 * static/js/redirect.js ships with an empty table; the build's post-build
 * pass (stamp_redirect_map in scripts/postbuild_fix.py) replaces
 * `var REDIRECTS = {};` with the retired-path map, written by Python's
 * json.dumps(..., sort_keys=True). These tests stamp a copy the same way.
 *
 * Coverage: Node maps V8's byte ranges onto the file on disk, so a longer
 * stamped copy run under redirect.js's URL would shift every range after
 * the table and credit the wrong code. For the coverage-credited runs the
 * table is therefore stamped as `_R`, a two-character name bound to the
 * same parsed table, so every offset matches the committed file. The
 * build's exact output is run too, under its own name, and must behave the
 * same. */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { pathToFileURL } = require("node:url");

const FILE = path.resolve(__dirname, "../static/js/redirect.js");
const SOURCE = fs.readFileSync(FILE, "utf8");
const PLACEHOLDER = "var REDIRECTS = {};";

/** Python's json.dumps(table, sort_keys=True): ", " and ": " separators. */
function pyJson(table) {
  const pairs = Object.keys(table).sort().map((k) => `${JSON.stringify(k)}: ${JSON.stringify(table[k])}`);
  return `{${pairs.join(", ")}}`;
}

/** redirect.js exactly as the build stamps it. */
function stamped(table) {
  assert.ok(SOURCE.includes(PLACEHOLDER), "redirect.js keeps the placeholder the build stamps");
  return SOURCE.replace(PLACEHOLDER, `var REDIRECTS = ${pyJson(table)};`);
}

/** redirect.js stamped with `_R` (same length as `{}`), bound to the table. */
const ALIGNED = SOURCE.replace(PLACEHOLDER, "var REDIRECTS = _R;");

/** Run a version of redirect.js for a visitor at `pathname`; return where it sent them. */
function visit(source, pathname, { filename = pathToFileURL(FILE).href, table } = {}) {
  const calls = [];
  const window = { location: { pathname, replace: (to) => calls.push(to) } };
  const context = { window };
  if (table) context._R = JSON.parse(pyJson(table));
  new vm.Script(source, { filename }).runInContext(vm.createContext(context));
  return calls;
}

// The table postbuild_fix.py stamps today (LEGACY_REDIRECTS, keyed "/old/").
const TABLE = {
  "/executive-brief-de/": "/de/executive-brief/",
  "/executive-brief-es/": "/es/executive-brief/",
  "/executive-brief-fr/": "/fr/executive-brief/",
  "/made-with-shokunin/": "/made-with-ssg/",
};

test("the coverage copy differs from the committed file only in the table", () => {
  assert.equal(ALIGNED.length, SOURCE.length);
  assert.equal(ALIGNED.replace("var REDIRECTS = _R;", PLACEHOLDER), SOURCE);
});

test("the build's exact output redirects a retired path", () => {
  const filename = pathToFileURL(path.join(__dirname, "redirect.stamped.js")).href;
  assert.deepEqual(visit(stamped(TABLE), "/made-with-shokunin/", { filename }), ["/made-with-ssg/"]);
  assert.deepEqual(visit(stamped(TABLE), "/documentation/", { filename }), []);
  assert.deepEqual(visit(stamped(TABLE), "toString", { filename }), []);
});

test("a retired path is sent to its new page, once", () => {
  assert.deepEqual(visit(ALIGNED, "/made-with-shokunin/", { table: TABLE }), ["/made-with-ssg/"]);
  assert.deepEqual(visit(ALIGNED, "/executive-brief-fr/", { table: TABLE }), ["/fr/executive-brief/"]);
});

test("a path that is not in the table stays where it is", () => {
  assert.deepEqual(visit(ALIGNED, "/documentation/", { table: TABLE }), []);
  assert.deepEqual(visit(ALIGNED, "/made-with-shokunin", { table: TABLE }), [], "the table keys carry a trailing slash");
});

test("a path named like an inherited property does not redirect", () => {
  for (const pathname of ["/toString", "toString", "constructor", "__proto__", "hasOwnProperty"]) {
    assert.deepEqual(visit(ALIGNED, pathname, { table: TABLE }), [], pathname);
  }
});

test("the unstamped script, as committed, never redirects", () => {
  assert.deepEqual(visit(SOURCE, "/made-with-shokunin/"), []);
});
