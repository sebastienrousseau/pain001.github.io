import { test } from "node:test";
import assert from "node:assert/strict";
import {
  ibanChecksumValid, ibanLengthValid, bicValid,
  sniffDelimiter, splitCsvLine, normaliseHeader, parseCsv,
  validateRecords, controlSum, toXml, xmlEscape,
  errorReportCsv, decodeBuffer, SAMPLES, SCENARIOS, layerFor,
} from "../static/js/try-demo.js";

/* ==== IBAN vectors (published valid examples per country) ==== */

const VALID_IBANS = [
  "DE89370400440532013000", "FR1420041010050500013M02606",
  "GB29NWBK60161331926819", "NL91ABNA0417164300",
  "ES9121000418450200051332", "IT60X0542811101000000123456",
  "BE68539007547034", "CH9300762011623852957",
  "DE89 3704 0044 0532 0130 00", // spaces are tolerated
];

const INVALID_IBANS = [
  "DE88370400440532013000",  // flipped check digit
  "DE89370400440532013001",  // flipped last digit
  "GB29NWBK60161331926810",  // flipped last digit
  "XX00INVALID",             // nonsense
  "",                        // empty
  "DE8937040044053201300",   // truncated (also fails checksum)
];

test("valid IBANs pass mod-97", () => {
  for (const iban of VALID_IBANS) {
    assert.equal(ibanChecksumValid(iban), true, iban);
  }
});

test("invalid IBANs fail mod-97", () => {
  for (const iban of INVALID_IBANS) {
    assert.equal(ibanChecksumValid(iban), false, iban);
  }
});

test("IBAN country length table", () => {
  assert.equal(ibanLengthValid("DE89370400440532013000"), true);   // 22 = DE
  assert.equal(ibanLengthValid("DE893704004405320130"), false);    // 20 != 22
  assert.equal(ibanLengthValid("ZZ12345678901234"), true);         // unknown country: pass-through
});

/* ==== BIC ==== */

test("BIC structure", () => {
  for (const good of ["DEUTDEFF", "DEUTDEFFXXX", "NWBKGB2LXXX", "BNPAFRPP"]) {
    assert.equal(bicValid(good), true, good);
  }
  for (const bad of ["DEUTDE1", "DEUTDEFFXX", "12345678", "DEUTDEFFXXXX", ""]) {
    assert.equal(bicValid(bad), false, bad);
  }
});

/* ==== CSV parsing ==== */

test("delimiter sniffing", () => {
  assert.equal(sniffDelimiter("a,b,c"), ",");
  assert.equal(sniffDelimiter("a;b;c"), ";");
  assert.equal(sniffDelimiter("a\tb\tc"), "\t");
  assert.equal(sniffDelimiter("a;b;c,d"), ";");
});

test("quoted fields with embedded delimiters and quotes", () => {
  assert.deepEqual(
    splitCsvLine('1,"Smith & Sons, Ltd","He said ""hi"""', ","),
    ["1", "Smith & Sons, Ltd", 'He said "hi"'],
  );
});

test("header normalisation is case-insensitive and reports unknowns", () => {
  const { headers, unknown } = normaliseHeader([" Payment_ID ", "CURRENCY", "custom_ref"]);
  assert.deepEqual(headers, ["payment_id", "currency", "custom_ref"]);
  assert.deepEqual(unknown, ["custom_ref"]);
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

/* ==== Validation rules ==== */

function sampleRows() {
  return parseCsv(SAMPLES["sepa-sct"].csv).rows;
}

test("pristine sample validates clean", () => {
  assert.deepEqual(validateRecords(sampleRows()), []);
});

test("every scenario produces at least one finding with its rule", () => {
  const expectations = {
    "iban-checksum": "iban-checksum",
    "bic-structure": "bic-structure",
    "missing-column": "required-field",
    "amount-format": "amount-format",
    "date-value": "date-value",
  };
  for (const [name, scenario] of Object.entries(SCENARIOS)) {
    const broken = scenario.apply(SAMPLES["sepa-sct"].csv);
    const parsed = parseCsv(broken);
    const findings = validateRecords(parsed.rows)
      .concat(parsed.structural || []);
    assert.ok(findings.length > 0, name + " produced no findings");
    assert.ok(
      findings.some((f) => f.rule === expectations[name]),
      name + " expected rule " + expectations[name] + ", got " +
        JSON.stringify(findings.map((f) => f.rule)),
    );
  }
});

test("comma-decimal amounts are rejected with a naming message", () => {
  const rows = sampleRows();
  rows[0].payment_amount = "1.250,00";
  const findings = validateRecords(rows);
  assert.ok(findings.some((f) =>
    f.rule === "amount-format" && f.message.includes("point-decimal")));
});

test("zero-decimal currency precision", () => {
  const rows = sampleRows();
  rows[0].currency = "JPY";
  rows[0].payment_amount = "100.50";
  const findings = validateRecords(rows);
  assert.ok(findings.some((f) => f.rule === "amount-precision"));
});

/* ==== Control totals & XML ==== */

test("control sum is exact decimal arithmetic", () => {
  assert.equal(controlSum([
    { payment_amount: "0.10" }, { payment_amount: "0.20" },
  ]), "0.30"); // classic float trap: 0.1 + 0.2
  assert.equal(controlSum([
    { payment_amount: "1250.00" }, { payment_amount: "890.50" },
  ]), "2140.50");
});

test("XML escapes special characters and recomputes totals", () => {
  const rows = parseCsv(SAMPLES["cross-border"].csv).rows;
  const xml = toXml(rows, "TEST-1", "2026-07-26T12:00:00");
  assert.ok(xml.includes("Smith &amp; Sons &lt;Holdings&gt; Ltd"));
  assert.ok(xml.includes("<NbOfTxs>1</NbOfTxs>"));
  assert.ok(xml.includes("<CtrlSum>4500.00</CtrlSum>"));
  assert.ok(!/&(?!amp;|lt;|gt;|quot;)/.test(xml), "unescaped ampersand");
});

test("xmlEscape covers the XML special set", () => {
  assert.equal(xmlEscape('a&b<c>d"e'), "a&amp;b&lt;c&gt;d&quot;e");
});

/* ==== Report + decoding ==== */

test("error report CSV quotes fields", () => {
  const report = errorReportCsv([
    { row: 3, column: "debtor_account_IBAN", rule: "iban-checksum", value: 'X"Y', message: "fails, badly" },
  ]);
  assert.ok(report.startsWith("row,column,rule,value,message\n"));
  assert.ok(report.includes('"X""Y"'));
  assert.ok(report.includes('"fails, badly"'));
});

test("windows-1252 fallback decoding", () => {
  const utf8 = new TextEncoder().encode("Müller");
  assert.deepEqual(decodeBuffer(utf8), { text: "Müller", converted: false });
  const cp1252 = new Uint8Array([0x4d, 0xfc, 0x6c, 0x6c, 0x65, 0x72]); // "Müller" in 1252
  const out = decodeBuffer(cp1252);
  assert.equal(out.text, "Müller");
  assert.equal(out.converted, true);
});

test("all samples parse and validate clean", () => {
  for (const [name, sample] of Object.entries(SAMPLES)) {
    const parsed = parseCsv(sample.csv);
    assert.ok(!parsed.error, name);
    assert.equal(parsed.structural.length, 0, name);
    assert.deepEqual(validateRecords(parsed.rows), [], name);
  }
});

/* ==== Validation layers ====
 * The layer of a finding is what the result summary reports, so it must
 * be right: an "iso" finding is one the XSD would also catch, a "data"
 * finding is one it would not. Getting these backwards would make the
 * demo claim credit for checks the schema already does, or hide the
 * checks that are actually the product's value.
 */
test("IBAN checksum failures are data-layer: the XSD accepts them", () => {
  const csv = SAMPLES["sepa-sct"].csv.replace(/DE89370400440532013000/, "DE89370400440532013001");
  const parsed = parseCsv(csv);
  const findings = validateRecords(parsed.rows);
  const iban = findings.find((f) => f.rule === "iban-checksum");
  assert.ok(iban, "expected an iban-checksum finding");
  assert.equal(iban.layer, "data",
    "a mistyped IBAN digit is a valid string to a schema — it must not be reported as an ISO-layer finding");
});

test("missing required fields are iso-layer: the XSD would reject them too", () => {
  const parsed = parseCsv("payment_id,payment_amount\nP1,100.00\n");
  const findings = validateRecords(parsed.rows);
  const req = findings.find((f) => f.rule === "required-field");
  assert.ok(req, "expected a required-field finding");
  assert.equal(req.layer, "iso");
});

test("every finding carries a layer", () => {
  for (const key of Object.keys(SCENARIOS)) {
    const csv = SCENARIOS[key].apply(SAMPLES["sepa-sct"].csv);
    const parsed = parseCsv(csv);
    const findings = parsed.structural.concat(validateRecords(parsed.rows || []));
    for (const f of findings) {
      assert.ok(["input", "iso", "data"].includes(f.layer),
        `finding ${f.rule} has layer ${f.layer}`);
    }
  }
});

test("layerFor is total: unknown rules do not crash the summary", () => {
  assert.equal(layerFor("not-a-real-rule"), "data");
});
