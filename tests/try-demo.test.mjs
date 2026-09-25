import { test } from "node:test";
import assert from "node:assert/strict";
import {
  sniffDelimiter, splitCsvLine, normaliseHeader, parseCsv,
  errorReportCsv, decodeBuffer, fillTemplate, SAMPLES, SCENARIOS, REQUIRED_COLUMNS,
} from "../static/js/try-demo.js";





/* ==== BIC ==== */


/* ==== CSV parsing ==== */

test("delimiter sniffing", () => {
  assert.equal(sniffDelimiter("a,b,c"), ",");
  assert.equal(sniffDelimiter("a;b;c"), ";");
  assert.equal(sniffDelimiter("a\tb\tc"), "\t");
  assert.equal(sniffDelimiter("a;b;c,d"), ";");
  assert.equal(sniffDelimiter("header"), ",");
});

test("quoted fields with embedded delimiters and quotes", () => {
  assert.deepEqual(
    splitCsvLine('1,"Smith & Sons, Ltd","He said ""hi"""', ","),
    ["1", "Smith & Sons, Ltd", 'He said "hi"'],
  );
  assert.deepEqual(splitCsvLine('ab"cd,ef', ","), ['ab"cd', "ef"]);
});

test("header normalisation is case-insensitive and reports unknowns", () => {
  const { headers, unknown } = normaliseHeader([" Payment_ID ", "CURRENCY", "custom_ref"]);
  assert.deepEqual(headers, ["payment_id", "currency", "custom_ref"]);
  assert.deepEqual(unknown, ["custom_ref"]);
  assert.deepEqual(normaliseHeader([" "]).unknown, []);
});

test("parseCsv rejects input without both a header and record", () => {
  assert.deepEqual(parseCsv("header-only"), {
    error: "Need a header row and at least one record.",
  });
});

test("message templates preserve unknown placeholders", () => {
  assert.equal(fillTemplate("row {row}: {missing}", { row: 2 }), "row 2: {missing}");
  assert.equal(fillTemplate("{value}", null), "{value}");
});

test("parseCsv: semicolon dialect and BOM", () => {
  const csv = "﻿id;payment_id\n1;T-1";
  const out = parseCsv(csv);
  assert.equal(out.delimiter, ";");
  assert.equal(out.rows.length, 1);
  assert.equal(out.rows[0].payment_id, "T-1");
});

test("parseCsv: ragged rows reported, not silently dropped", () => {
  const out = parseCsv("a,b\n1,2\n3");
  assert.equal(out.rows.length, 1);
  assert.equal(out.structural.length, 1);
  assert.equal(out.structural[0].rule, "row-shape");
});

/* ==== Control totals & XML ==== */




/* ==== Report + decoding ==== */

test("error report CSV quotes fields and names each finding's layer", () => {
  const report = errorReportCsv([
    { layer: "data", row: 3, column: "debtor_account_IBAN", rule: "iban-checksum", value: 'X"Y', message: "fails, badly" },
  ]);
  assert.ok(report.startsWith("layer,row,column,rule,value,message\n"));
  assert.ok(report.includes('"data",3,"debtor_account_IBAN"'));
  assert.ok(report.includes('"X""Y"'));
  assert.ok(report.includes('"fails, badly"'));
  assert.equal(errorReportCsv([]), "layer,row,column,rule,value,message\n");
});

test("error report leads with the layer summary, including the layers Pain001 cannot evaluate", () => {
  const summary = [
    { layer: "iso", state: "fail", text: "1 issue(s) the schema would reject" },
    { layer: "data", state: "pass", text: "No identifier or format problems found" },
    { layer: "scheme", state: "not-run", text: "Not run: choose a scheme rulebook in step 1" },
    { layer: "bank", state: "not-evaluated", text: 'Not evaluated: "no" bank profiles' },
    { layer: "channel", state: "not-evaluated", text: "Not evaluated: decided by your bank, not the file" },
  ];
  const finding = { layer: "iso", row: 2, column: "currency", rule: "required", value: undefined, message: "missing" };
  const lines = errorReportCsv([finding], summary).split("\n");
  assert.equal(lines.length, 1 + summary.length + 1);
  assert.equal(lines[1], '"iso",,,"summary","fail","1 issue(s) the schema would reject"');
  assert.equal(lines[4], '"bank",,,"summary","not-evaluated","Not evaluated: ""no"" bank profiles"');
  assert.equal(lines[5], '"channel",,,"summary","not-evaluated","Not evaluated: decided by your bank, not the file"');
  // a finding follows the summary; a missing value is an empty field, not "undefined"
  assert.equal(lines[6], '"iso",2,"currency","required","","missing"');
});

test("windows-1252 fallback decoding", () => {
  const utf8 = new TextEncoder().encode("Müller");
  assert.deepEqual(decodeBuffer(utf8), { text: "Müller", converted: false });
  const cp1252 = new Uint8Array([0x4d, 0xfc, 0x6c, 0x6c, 0x65, 0x72]); // "Müller" in 1252
  const out = decodeBuffer(cp1252);
  assert.equal(out.text, "Müller");
  assert.equal(out.converted, true);
});


/* ==== Validation layers ====
 * The layer of a finding is what the result summary reports, so it must
 * be right: an "iso" finding is one the XSD would also catch, a "data"
 * finding is one it would not. Getting these backwards would make the
 * demo claim credit for checks the schema already does, or hide the
 * checks that are actually the product's value.
 */

test("every sample parses with every column the library requires", () => {
  for (const [key, sample] of Object.entries(SAMPLES)) {
    const parsed = parseCsv(sample.csv);
    assert.equal(parsed.error, undefined, key);
    assert.ok(parsed.rows.length > 0, key);
    for (const col of REQUIRED_COLUMNS) assert.ok(col in parsed.rows[0], `${key} lacks ${col}`);
    assert.equal(parsed.structural.length, 0, key);
  }
});

test("every scenario changes the pristine sample (the library judges the result)", () => {
  const base = SAMPLES["sepa-sct"].csv;
  for (const [key, scenario] of Object.entries(SCENARIOS)) {
    assert.notEqual(scenario.apply(base), base, key);
  }
  const quoted = 'a,b,c,d,e,f\n"one,two",2,3,4,5,6';
  assert.match(SCENARIOS["missing-column"].apply(quoted), /"one,two"/);
});
