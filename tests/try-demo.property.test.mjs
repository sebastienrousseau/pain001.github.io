// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* Property-based fuzzing of the demo's input handling.
 *
 * The demo parses whatever a visitor pastes or drops, so its parser gets
 * generated input rather than hand-picked cases: arbitrary text must never
 * throw, and what the report writer quotes must parse back exactly. These
 * run with the unit tests (`npm test`) on every push. */
import { test } from "node:test";
import assert from "node:assert/strict";
import fc from "fast-check";
import {
  splitCsvLine, parseCsv, sniffDelimiter, errorReportCsv, decodeBuffer, fillTemplate,
} from "../static/js/try-demo.js";

const RUNS = { numRuns: 500 };
const DELIMITERS = [",", ";", "\t"];
const delimiter = fc.constantFrom(...DELIMITERS);
// One CSV line: any text without a line break (the parser works line by line).
const lineText = fc.string({ unit: "grapheme", maxLength: 60 }).map((s) => s.replace(/[\r\n]/g, " "));
const quote = (s) => '"' + s.replace(/"/g, '""') + '"';

test("splitting any line never throws and yields at least one field", () => {
  fc.assert(fc.property(fc.string({ unit: "binary", maxLength: 200 }), delimiter, (line, d) => {
    const cells = splitCsvLine(line, d);
    assert.ok(Array.isArray(cells) && cells.length >= 1);
    assert.ok(cells.every((c) => typeof c === "string"));
  }), RUNS);
});

test("fields quoted the RFC 4180 way split back to exactly the same fields", () => {
  fc.assert(fc.property(fc.array(lineText, { minLength: 1, maxLength: 12 }), delimiter, (fields, d) => {
    assert.deepEqual(splitCsvLine(fields.map(quote).join(d), d), fields);
  }), RUNS);
});

test("parsing any pasted text never throws, and every accepted row matches the header", () => {
  fc.assert(fc.property(fc.string({ unit: "binary", maxLength: 400 }), (text) => {
    const out = parseCsv(text);
    if (out.error) return;
    assert.ok(DELIMITERS.includes(out.delimiter));
    for (const row of out.rows) assert.equal(typeof row, "object");
    const widths = new Set(out.rows.map((r) => Object.keys(r).length));
    assert.ok(widths.size <= 1, "rows of one parse share one header");
  }), RUNS);
});

test("CSV-shaped input: rows either match the header or are reported, never dropped silently", () => {
  const table = fc.tuple(delimiter, fc.integer({ min: 1, max: 6 })).chain(([d, width]) =>
    fc.tuple(fc.constant(d), fc.array(fc.array(lineText, { minLength: 1, maxLength: width + 1 }), { minLength: 2, maxLength: 8 })));
  fc.assert(fc.property(table, ([d, lines]) => {
    const text = lines.map((cells) => cells.map(quote).join(d)).join("\n");
    const out = parseCsv(text);
    if (out.error) return;
    const records = text.split("\n").filter((l) => l.trim() !== "").length - 1;
    assert.equal(out.rows.length + out.structural.length, records,
      "every record line is either a row or a structural finding");
  }), RUNS);
});

test("the delimiter sniffer only ever answers comma, semicolon or tab", () => {
  fc.assert(fc.property(fc.string({ unit: "binary", maxLength: 200 }), (header) => {
    assert.ok(DELIMITERS.includes(sniffDelimiter(header)));
  }), RUNS);
});

test("every error-report line parses back to the six fields that were written", () => {
  const finding = fc.record({
    layer: fc.constantFrom("iso", "data", "scheme", "input"),
    row: fc.nat({ max: 99999 }),
    column: lineText, rule: lineText, value: fc.option(lineText, { nil: undefined }), message: lineText,
  });
  const summary = fc.record({
    layer: fc.constantFrom("iso", "data", "scheme", "bank", "channel"),
    state: fc.constantFrom("pass", "fail", "not-run", "not-evaluated"),
    text: lineText,
  });
  fc.assert(fc.property(fc.array(finding, { maxLength: 8 }), fc.array(summary, { maxLength: 5 }), (findings, rows) => {
    const lines = errorReportCsv(findings, rows).split("\n");
    assert.deepEqual(splitCsvLine(lines[0], ","), ["layer", "row", "column", "rule", "value", "message"]);
    rows.forEach((s, i) => {
      assert.deepEqual(splitCsvLine(lines[1 + i], ","), [s.layer, "", "", "summary", s.state, s.text]);
    });
    findings.forEach((f, i) => {
      assert.deepEqual(splitCsvLine(lines[1 + rows.length + i], ","),
        [f.layer, String(f.row), f.column, f.rule, f.value ?? "", f.message]);
    });
  }), RUNS);
});

test("decoding any uploaded bytes never throws and always yields text", () => {
  fc.assert(fc.property(fc.uint8Array({ maxLength: 300 }), (bytes) => {
    const out = decodeBuffer(bytes.buffer);
    assert.equal(typeof out.text, "string");
    assert.equal(typeof out.converted, "boolean");
  }), RUNS);
});

test("filling a message template never throws and leaves unknown placeholders intact", () => {
  fc.assert(fc.property(lineText, fc.dictionary(fc.string({ minLength: 1, maxLength: 8 }), lineText), (tpl, params) => {
    const out = fillTemplate(tpl + " {definitely_missing_key}", params);
    assert.ok(out.endsWith("{definitely_missing_key}"));
  }), RUNS);
});
