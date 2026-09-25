/* Pain001 browser demo: input handling.
 *
 * ES module, zero dependencies, hand-auditable by design: a security
 * reviewer should be able to read this file top to bottom and confirm
 * that no function performs any network I/O. It reads CSV text into
 * records, ships the sample batches and the error scenarios, and writes
 * the error report. Every verdict comes from the pain001 library itself,
 * running in the browser through try-engine.js: there is no second rule
 * engine here to drift from the one in the package.
 *
 * Exported pure functions are unit-tested in tests/try-demo.test.mjs.
 */

/* ==== Constants ==== */

export const REQUIRED_COLUMNS = [
  "id", "date", "initiator_name", "payment_id", "requested_execution_date",
  "payment_amount", "currency", "debtor_name", "debtor_account_IBAN",
  "debtor_agent_BIC", "creditor_name", "creditor_account_IBAN", "creditor_agent_BIC",
];

export const OPTIONAL_COLUMNS = ["remittance_information"];

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
        layer: "input",
      });
      continue;
    }
    const rec = {};
    headers.forEach((h, idx) => { rec[h] = cells[idx].trim(); });
    rows.push(rec);
  }
  return { rows, delimiter, unknown, structural };
}

/* Fill "{x}" placeholders in a message template. Exported so the page
 * layer can re-fill translated templates with the same params. */
export function fillTemplate(template, params) {
  return template.replace(/\{(\w+)\}/g, (m, k) =>
    params && k in params ? String(params[k]) : m);
}


/* ==== Sample data ==== */

const HEADER = "id,date,initiator_name,payment_id,requested_execution_date,payment_amount,currency," +
  "debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name," +
  "creditor_account_IBAN,creditor_agent_BIC,remittance_information";

export const SAMPLES = {
  "sepa-sct": {
    label: "SEPA credit transfer (2 records, EUR)",
    csv: HEADER + "\n" +
      "1,2026-08-01,Acme Global Corp,TXN-001,2026-08-03,1250.00,EUR,Acme Global Corp,DE89370400440532013000,DEUTDEFFXXX,Supplier SARL,FR1420041010050500013M02606,BNPAFRPPXXX,INVOICE-2026-4411\n" +
      "2,2026-08-01,Acme Global Corp,TXN-002,2026-08-03,890.50,EUR,Acme Global Corp,DE89370400440532013000,DEUTDEFFXXX,Northwind Ltd,GB29NWBK60161331926819,NWBKGB2LXXX,INVOICE-2026-4412",
  },
  "cross-border": {
    label: "Cross-border (GBP, escaped chars)",
    csv: HEADER + "\n" +
      '1,2026-08-01,Acme Global Corp,XB-001,2026-08-05,4500.00,GBP,Acme Global Corp,DE89370400440532013000,DEUTDEFFXXX,"Smith & Sons <Holdings> Ltd",GB29NWBK60161331926819,NWBKGB2LXXX,PO-2026-889 R&D',
  },
  "batch-20": {
    label: "Larger batch (20 records)",
    get csv() {
      const rows = [];
      for (let i = 1; i <= 20; i++) {
        const amt = (100 + i * 7) + "." + String((i * 13) % 100).padStart(2, "0");
        rows.push([
          i, "2026-08-01", "Acme Global Corp", "BATCH-" + String(i).padStart(3, "0"),
          "2026-08-07", amt, "EUR", "Acme Global Corp",
          "DE89370400440532013000", "DEUTDEFFXXX", "Payee " + i,
          "FR1420041010050500013M02606", "BNPAFRPPXXX", "BATCH-INV-" + i,
        ].join(","));
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
      cells.splice(4, 1);
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

/* The report carries the same layer structure as the on-screen summary,
 * so a downloaded file keeps the boundary with it: the first rows state
 * what each layer concluded (rule "summary", the state in the value
 * column, the visitor's own wording in the message column), including
 * the bank and channel layers that no local tool can evaluate. Each
 * finding then names its layer. `summary` is [{layer, state, text}]. */
export function errorReportCsv(findings, summary = []) {
  const head = "layer,row,column,rule,value,message";
  const q = (v) => '"' + String(v ?? "").replace(/"/g, '""') + '"';
  const lines = summary.map((s) =>
    [q(s.layer), "", "", q("summary"), q(s.state), q(s.text)].join(","));
  for (const f of findings) {
    lines.push([q(f.layer), f.row, q(f.column), q(f.rule), q(f.value), q(f.message)].join(","));
  }
  return head + "\n" + lines.join("\n");
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
