/* Pain001 browser demo — core logic.
 *
 * ES module, zero dependencies, hand-auditable by design: a security
 * reviewer should be able to read this file top to bottom and confirm
 * that no function performs any network I/O. The only fetches on the
 * demo page are for same-origin assets (the page, this file, and the
 * optional WASM engine), and none of them carry user data.
 *
 * Exported pure functions are unit-tested in tests/try-demo.test.mjs.
 */

/* ==== Constants ==== */

export const REQUIRED_COLUMNS = [
  "id", "payment_id", "requested_execution_date", "payment_amount",
  "currency", "debtor_name", "debtor_account_IBAN", "debtor_agent_BIC",
  "creditor_name", "creditor_account_IBAN", "creditor_agent_BIC",
];

export const OPTIONAL_COLUMNS = ["remittance_information"];

const BIC_RE = /^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$/;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const AMOUNT_RE = /^\d+(\.\d+)?$/;
const CCY_RE = /^[A-Z]{3}$/;

/* ISO 13616 registry lengths for common countries; checksum-only
 * fallback for countries not listed. */
export const IBAN_LENGTHS = {
  AT: 20, BE: 16, CH: 21, CZ: 24, DE: 22, DK: 18, EE: 20, ES: 24,
  FI: 18, FR: 27, GB: 22, GR: 27, HR: 21, HU: 28, IE: 22, IT: 27,
  LT: 20, LU: 20, LV: 21, NL: 18, NO: 15, PL: 28, PT: 25, RO: 24,
  SE: 24, SI: 19, SK: 24,
};

/* ISO 4217 zero-decimal currencies (subset). */
export const ZERO_DECIMAL_CCY = ["JPY", "KRW", "VND", "CLP", "ISK"];

/* ==== IBAN / BIC ==== */

export function ibanChecksumValid(iban) {
  const s = String(iban).replace(/\s+/g, "").toUpperCase();
  if (!/^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$/.test(s)) return false;
  const r = s.slice(4) + s.slice(0, 4);
  let expanded = "";
  for (let i = 0; i < r.length; i++) {
    const c = r.charCodeAt(i);
    expanded += c >= 65 ? String(c - 55) : r[i];
  }
  let mod = 0;
  for (let j = 0; j < expanded.length; j += 7) {
    mod = parseInt(String(mod) + expanded.slice(j, j + 7), 10) % 97;
  }
  return mod === 1;
}

export function ibanLengthValid(iban) {
  const s = String(iban).replace(/\s+/g, "").toUpperCase();
  const expected = IBAN_LENGTHS[s.slice(0, 2)];
  return expected === undefined || s.length === expected;
}

export function bicValid(bic) {
  return BIC_RE.test(String(bic).trim().toUpperCase());
}

/* ==== CSV parsing ==== */

export function sniffDelimiter(headerLine) {
  const counts = {
    ",": (headerLine.match(/,/g) || []).length,
    ";": (headerLine.match(/;/g) || []).length,
    "\t": (headerLine.match(/\t/g) || []).length,
  };
  let best = ",";
  for (const d of [";", "\t"]) if (counts[d] > counts[best]) best = d;
  return counts[best] > 0 ? best : ",";
}

export const DELIMITER_NAMES = { ",": "comma", ";": "semicolon", "\t": "tab" };

/* Minimal RFC 4180 line parser: quoted fields, embedded delimiters,
 * doubled quotes. One line at a time (multi-line quoted fields are out
 * of scope for the demo and reported as errors by the caller). */
export function splitCsvLine(line, delimiter) {
  const cells = [];
  let cur = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"') {
        if (line[i + 1] === '"') { cur += '"'; i++; }
        else inQuotes = false;
      } else cur += ch;
    } else if (ch === '"' && cur === "") {
      inQuotes = true;
    } else if (ch === delimiter) {
      cells.push(cur); cur = "";
    } else {
      cur += ch;
    }
  }
  cells.push(cur);
  return cells;
}

/* Case-insensitive canonical header matching, whitespace-trimmed. */
export function normaliseHeader(rawHeaders) {
  const canon = {};
  for (const c of REQUIRED_COLUMNS.concat(OPTIONAL_COLUMNS)) {
    canon[c.toLowerCase()] = c;
  }
  const headers = [];
  const unknown = [];
  for (const raw of rawHeaders) {
    const key = String(raw).trim();
    const mapped = canon[key.toLowerCase()];
    if (mapped) headers.push(mapped);
    else { headers.push(key); if (key) unknown.push(key); }
  }
  return { headers, unknown };
}

export function parseCsv(text) {
  const clean = String(text).replace(/^﻿/, "");
  const lines = clean.split(/\r\n|\r|\n/).filter((l) => l.trim() !== "");
  if (lines.length < 2) {
    return { error: "Need a header row and at least one record." };
  }
  const delimiter = sniffDelimiter(lines[0]);
  const { headers, unknown } = normaliseHeader(splitCsvLine(lines[0], delimiter));
  const rows = [];
  const structural = [];
  for (let i = 1; i < lines.length; i++) {
    const cells = splitCsvLine(lines[i], delimiter);
    if (cells.length !== headers.length) {
      structural.push({
        row: i, column: "", rule: "row-shape", value: "",
        message: fillTemplate("row {row} has {cells} field(s), header has {header}",
          { row: i, cells: cells.length, header: headers.length }),
        template: "row {row} has {cells} field(s), header has {header}",
        params: { row: i, cells: cells.length, header: headers.length },
        layer: layerFor("row-shape"),
      });
      continue;
    }
    const rec = {};
    headers.forEach((h, idx) => { rec[h] = cells[idx].trim(); });
    rows.push(rec);
  }
  return { rows, delimiter, unknown, structural };
}

/* ==== Validation rules ====
 * Each finding: { row, column, rule, value, message }. Row numbers are
 * 1-based data rows (header excluded), matching what an ops person
 * counts in a spreadsheet. */


/* Fill "{x}" placeholders in a message template. Exported so the page
 * layer can re-fill translated templates with the same params. */
/* Which validation layer each rule belongs to, for the layered result
 * summary. The distinction matters and is the product's actual value:
 *
 *   "iso"   the XSD would also reject this — we just say so faster and
 *           in plainer language than a schema parser does.
 *   "data"  the XSD would ACCEPT this. A mistyped IBAN digit is a valid
 *           string to a schema; the bank rejects it days later. These
 *           are the findings that justify "before your bank does".
 *   "input" the file could not be read as tabular data at all.
 *
 * Scheme rulebooks (SEPA, CBPR+) are not evaluated in the browser — the
 * CLI does that with --scheme. The summary says so rather than implying
 * a clean run means scheme-clean.
 */
export const RULE_LAYERS = {
  "row-shape": "input",
  "required-field": "iso",
  "amount-format": "iso",
  "amount-precision": "iso",
  "currency-code": "iso",
  "date-format": "iso",
  "date-value": "iso",
  "iban-length": "data",
  "iban-checksum": "data",
  "bic-structure": "data",
};

export function layerFor(rule) {
  return RULE_LAYERS[rule] || "data";
}

export function fillTemplate(template, params) {
  return template.replace(/\{(\w+)\}/g, (m, k) =>
    params && k in params ? String(params[k]) : m);
}

export function validateRecords(rows) {
  const errors = [];
  const add = (row, column, rule, value, template, params) =>
    errors.push({ row, column, rule, value: String(value),
      message: fillTemplate(template, params), template, params,
      layer: layerFor(rule) });

  rows.forEach((rec, idx) => {
    const row = idx + 1;
    for (const f of REQUIRED_COLUMNS) {
      if (!rec[f]) add(row, f, "required-field", "", "missing required value", {});
    }
    const amt = rec.payment_amount;
    if (amt) {
      if (/^\d{1,3}(\.\d{3})*,\d+$/.test(amt) || /^\d+,\d+$/.test(amt)) {
        add(row, "payment_amount", "amount-format", amt,
          "comma-decimal amount — expected point-decimal (e.g. 1234.56)", {});
      } else if (!AMOUNT_RE.test(amt)) {
        add(row, "payment_amount", "amount-format", amt,
          "not a valid decimal amount (expected e.g. 1234.56)", {});
      } else {
        const decimals = (amt.split(".")[1] || "").length;
        const ccy = (rec.currency || "").toUpperCase();
        if (ZERO_DECIMAL_CCY.includes(ccy) && decimals > 0) {
          add(row, "payment_amount", "amount-precision", amt,
            "{ccy} is a zero-decimal currency — no fractional part allowed", { ccy });
        } else if (decimals > 2) {
          add(row, "payment_amount", "amount-precision", amt,
            "more than 2 decimal places", {});
        }
      }
    }
    if (rec.currency && !CCY_RE.test(rec.currency.toUpperCase())) {
      add(row, "currency", "currency-code", rec.currency,
        "not a 3-letter ISO 4217 code", {});
    }
    if (rec.requested_execution_date) {
      const d = rec.requested_execution_date;
      if (!DATE_RE.test(d)) {
        add(row, "requested_execution_date", "date-format", d,
          "expected ISO 8601 YYYY-MM-DD", {});
      } else {
        const [y, m, day] = d.split("-").map(Number);
        const dt = new Date(Date.UTC(y, m - 1, day));
        if (dt.getUTCMonth() !== m - 1 || dt.getUTCDate() !== day) {
          add(row, "requested_execution_date", "date-value", d,
            "not a real calendar date", {});
        }
      }
    }
    for (const f of ["debtor_account_IBAN", "creditor_account_IBAN"]) {
      const v = rec[f];
      if (!v) continue;
      if (!ibanLengthValid(v)) {
        add(row, f, "iban-length", v,
          "wrong length for country {cc} (expected {len} characters)",
          { cc: v.slice(0, 2).toUpperCase(),
            len: IBAN_LENGTHS[v.slice(0, 2).toUpperCase()] });
      } else if (!ibanChecksumValid(v)) {
        add(row, f, "iban-checksum", v,
          "fails the ISO 13616 mod-97 checksum — likely a mistyped digit", {});
      }
    }
    for (const f of ["debtor_agent_BIC", "creditor_agent_BIC"]) {
      if (rec[f] && !bicValid(rec[f])) {
        add(row, f, "bic-structure", rec[f],
          "not a valid ISO 9362 BIC (8 or 11 characters, AAAAAA00[XXX])", {});
      }
    }
  });
  return errors;
}

/* ==== XML generation ==== */

export function xmlEscape(v) {
  return String(v)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export function controlSum(rows) {
  const cents = rows.reduce((sum, r) => {
    const parts = String(r.payment_amount).split(".");
    return sum + parseInt(parts[0], 10) * 100 +
      (parts[1] ? parseInt((parts[1] + "0").slice(0, 2), 10) : 0);
  }, 0);
  return Math.floor(cents / 100) + "." + String(cents % 100).padStart(2, "0");
}

export function toXml(rows, msgId, creDtTm) {
  const ctrl = controlSum(rows);
  const first = rows[0];
  const tx = rows.map((r) => [
    "      <CdtTrfTxInf>",
    "        <PmtId><EndToEndId>" + xmlEscape(r.payment_id) + "</EndToEndId></PmtId>",
    '        <Amt><InstdAmt Ccy="' + xmlEscape(r.currency) + '">' + xmlEscape(r.payment_amount) + "</InstdAmt></Amt>",
    "        <CdtrAgt><FinInstnId><BICFI>" + xmlEscape(r.creditor_agent_BIC) + "</BICFI></FinInstnId></CdtrAgt>",
    "        <Cdtr><Nm>" + xmlEscape(r.creditor_name) + "</Nm></Cdtr>",
    "        <CdtrAcct><Id><IBAN>" + xmlEscape(r.creditor_account_IBAN) + "</IBAN></Id></CdtrAcct>",
    r.remittance_information
      ? "        <RmtInf><Ustrd>" + xmlEscape(r.remittance_information) + "</Ustrd></RmtInf>"
      : null,
    "      </CdtTrfTxInf>",
  ].filter(Boolean).join("\n")).join("\n");

  return ['<?xml version="1.0" encoding="UTF-8"?>',
    '<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09">',
    "  <CstmrCdtTrfInitn>",
    "    <GrpHdr>",
    "      <MsgId>" + xmlEscape(msgId) + "</MsgId>",
    "      <CreDtTm>" + xmlEscape(creDtTm) + "</CreDtTm>",
    "      <NbOfTxs>" + rows.length + "</NbOfTxs>",
    "      <CtrlSum>" + ctrl + "</CtrlSum>",
    "      <InitgPty><Nm>" + xmlEscape(first.debtor_name) + "</Nm></InitgPty>",
    "    </GrpHdr>",
    "    <PmtInf>",
    "      <PmtInfId>" + xmlEscape(first.id) + "</PmtInfId>",
    "      <PmtMtd>TRF</PmtMtd>",
    "      <NbOfTxs>" + rows.length + "</NbOfTxs>",
    "      <CtrlSum>" + ctrl + "</CtrlSum>",
    "      <ReqdExctnDt><Dt>" + xmlEscape(first.requested_execution_date) + "</Dt></ReqdExctnDt>",
    "      <Dbtr><Nm>" + xmlEscape(first.debtor_name) + "</Nm></Dbtr>",
    "      <DbtrAcct><Id><IBAN>" + xmlEscape(first.debtor_account_IBAN) + "</IBAN></Id></DbtrAcct>",
    "      <DbtrAgt><FinInstnId><BICFI>" + xmlEscape(first.debtor_agent_BIC) + "</BICFI></FinInstnId></DbtrAgt>",
    tx,
    "    </PmtInf>",
    "  </CstmrCdtTrfInitn>",
    "</Document>"].join("\n");
}

/* ==== Samples ==== */

const HEADER = "id,payment_id,requested_execution_date,payment_amount,currency," +
  "debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name," +
  "creditor_account_IBAN,creditor_agent_BIC,remittance_information";

export const SAMPLES = {
  "sepa-sct": {
    label: "SEPA credit transfer (2 records, EUR)",
    csv: HEADER + "\n" +
      "1,TXN-001,2026-08-03,1250.00,EUR,Acme Global Corp,DE89370400440532013000,DEUTDEFFXXX,Supplier SARL,FR1420041010050500013M02606,BNPAFRPPXXX,INVOICE-2026-4411\n" +
      "2,TXN-002,2026-08-03,890.50,EUR,Acme Global Corp,DE89370400440532013000,DEUTDEFFXXX,Northwind Ltd,GB29NWBK60161331926819,NWBKGB2LXXX,INVOICE-2026-4412",
  },
  "cross-border": {
    label: "Cross-border (GBP, escaped chars)",
    csv: HEADER + "\n" +
      '1,XB-001,2026-08-05,4500.00,GBP,Acme Global Corp,DE89370400440532013000,DEUTDEFFXXX,"Smith & Sons <Holdings> Ltd",GB29NWBK60161331926819,NWBKGB2LXXX,PO-2026-889 R&D',
  },
  "batch-20": {
    label: "Larger batch (20 records)",
    get csv() {
      const rows = [];
      for (let i = 1; i <= 20; i++) {
        const amt = (100 + i * 7) + "." + String((i * 13) % 100).padStart(2, "0");
        rows.push(i + ",BATCH-" + String(i).padStart(3, "0") +
          ",2026-08-07," + amt + ",EUR,Acme Global Corp," +
          "DE89370400440532013000,DEUTDEFFXXX,Payee " + i +
          ",FR1420041010050500013M02606,BNPAFRPPXXX,BATCH-INV-" + i);
      }
      return HEADER + "\n" + rows.join("\n");
    },
  },
};

/* ==== Error scenarios (Phase 1) ====
 * Each takes the pristine sample CSV and returns it with exactly one
 * deliberate flaw, so the corresponding rule fires on validation. */

export const SCENARIOS = {
  "iban-checksum": {
    label: "Flipped IBAN digit (mod-97 checksum)",
    apply: (csv) => csv.replace("DE89", "DE79"),
  },
  "bic-structure": {
    label: "Malformed BIC (wrong structure)",
    apply: (csv) => csv.replace("DEUTDEFFXXX", "DEUTDE1"),
  },
  "missing-column": {
    label: "Missing required column (execution date)",
    apply: (csv) => csv.split("\n").map((line, i) => {
      const cells = splitCsvLine(line, ",");
      cells.splice(2, 1);
      return cells.map((c) => (/[,"]/.test(c) ? '"' + c.replace(/"/g, '""') + '"' : c)).join(",");
    }).join("\n"),
  },
  "amount-format": {
    label: "European comma-decimal amount",
    apply: (csv) => csv.replace("1250.00", '"1.250,00"'),
  },
  "date-value": {
    label: "Impossible calendar date",
    apply: (csv) => csv.replace("2026-08-03", "2026-02-31"),
  },
};

/* ==== Error report export ==== */

export function errorReportCsv(findings) {
  const head = "row,column,rule,value,message";
  const q = (v) => '"' + String(v).replace(/"/g, '""') + '"';
  return head + "\n" + findings.map((f) =>
    [f.row, q(f.column), q(f.rule), q(f.value), q(f.message)].join(",")
  ).join("\n");
}

/* ==== Text decoding (UTF-8 with Windows-1252 fallback) ==== */

export function decodeBuffer(buffer) {
  try {
    return {
      text: new TextDecoder("utf-8", { fatal: true }).decode(buffer),
      converted: false,
    };
  } catch (e) {
    return {
      text: new TextDecoder("windows-1252").decode(buffer),
      converted: true,
    };
  }
}
