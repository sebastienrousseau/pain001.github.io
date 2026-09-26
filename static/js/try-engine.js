/*
 * SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 */
/* Pain001 browser demo: the engine.
 *
 * Loads a Python runtime (Pyodide, WebAssembly) and the pain001 library
 * itself from this origin, then runs the library's own validation,
 * scheme rules, XML generation and official-XSD gate on the records the
 * page hands over. Nothing here talks to any other host: every URL is a
 * same-origin path listed in /pyodide/pain001-runtime.json.
 *
 * Exports are environment-agnostic (browser or Node) so the same code is
 * exercised by tests/engine.integration.mjs against the vendored runtime.
 */

export const MESSAGE_TYPE = "pain.001.001.09";

/** Package names Pyodide's own lock knows; loaded before the pure wheels. */
export const PYODIDE_PACKAGES = [
  "markupsafe", "pyyaml", "rpds-py", "pyrsistent", "attrs", "six", "typing-extensions",
  "referencing", "jsonschema-specifications", "jsonschema", "click", "jinja2",
];

/** The Python side. One module, three entry points: warm, run, version. */
export const BRIDGE = `
import json
import pain001
import xmlschema
from pain001.templates import DEFAULT_TEMPLATE_REGISTRY
from pain001.validation.schema_validator import SchemaValidator
from pain001.validation.bic_validator import validate_bic
from pain001.validation.iban_validator import validate_iban
from pain001.validation.schemes import validate_scheme
from pain001.twins import to_iso_json
from pain001.xml.generate_xml import generate_xml_string, normalize_payment_records

_SCHEMAS = {}
_VALIDATORS = {}


def _meta(message_type):
    return DEFAULT_TEMPLATE_REGISTRY.get_template(message_type)


def _schema(message_type):
    if message_type not in _SCHEMAS:
        _SCHEMAS[message_type] = xmlschema.XMLSchema(str(_meta(message_type).xsd_path))
    return _SCHEMAS[message_type]


def _validator(message_type):
    if message_type not in _VALIDATORS:
        _VALIDATORS[message_type] = SchemaValidator(message_type)
    return _VALIDATORS[message_type]


def warm(message_type):
    """Build the schema and the validator once, so the first run is fast."""
    _schema(message_type)
    _validator(message_type)
    return pain001.__version__


def xsd_sha256(message_type):
    """Hash of the bundled official schema, for readers who want to compare it."""
    import hashlib
    return hashlib.sha256(_meta(message_type).xsd_path.read_bytes()).hexdigest()


def xsd_errors_text(xml_text, message_type):
    """The official schema's first ten objections to a document, as JSON text."""
    return json.dumps([str(e.reason or e) for e in _schema(message_type).iter_errors(xml_text)][:10])


def xsd_errors(xml_text, message_type):
    """Alias kept for the page's re-run button."""
    return xsd_errors_text(xml_text, message_type)


def _finding(row, column, rule, value, message, layer):
    return {
        "row": row, "column": column, "rule": rule,
        "value": "" if value is None else str(value)[:60],
        "message": str(message), "layer": layer,
    }


def _identifiers(rows):
    """The library's own IBAN and BIC checks, per row: findings a schema cannot make."""
    found = []
    for index, row in enumerate(rows, 1):
        for column, value in row.items():
            if not value:
                continue
            if column.endswith("_IBAN"):
                try:
                    validate_iban(str(value))
                except Exception as exc:  # InvalidIBANError carries the reason
                    found.append(_finding(index, column, "iban", value, exc, "data"))
            elif column.endswith("_BIC"):
                try:
                    validate_bic(str(value))
                except Exception as exc:  # InvalidBICError carries the reason
                    found.append(_finding(index, column, "bic", value, exc, "data"))
    return found


def run(rows_json, message_type, scheme):
    """Validate records, apply a scheme rulebook, generate and XSD-check the file."""
    # A blank CSV cell is an absent value, as it is for the CLI's loaders.
    rows = [
        {key: value for key, value in row.items() if str(value).strip() != ""}
        for row in json.loads(rows_json)
    ]
    findings = []
    if not rows:
        findings.append(_finding("", "", "empty", "", "No records to process", "input"))
    try:
        rows = normalize_payment_records(rows) if rows else rows
    except Exception as exc:  # the library reports the row; the page shows it
        findings.append(_finding("", "", "normalise", "", exc, "input"))
    _total, _valid, errors = _validator(message_type).validate_batch(rows)
    for index, entries in errors:
        for entry in entries:
            field = str(entry.path).lstrip("$").lstrip(".")
            data_layer = field.endswith(("_IBAN", "_BIC")) or entry.rule == "pattern"
            findings.append(_finding(
                index + 1, field, entry.rule, entry.value, entry.message,
                "data" if data_layer else "iso",
            ))
    findings.extend(_identifiers(rows))
    scheme_result = None
    if scheme:
        result = validate_scheme(rows, scheme)
        violations = [v.as_dict() for v in result.violations]
        scheme_result = {"scheme": scheme, "valid": result.is_valid, "violations": violations}
        for v in violations:
            if v.get("severity", "error") == "error":
                findings.append(_finding(
                    (v.get("index") or 0) + 1, v.get("field", ""), v.get("rule", ""),
                    "", v.get("message", ""), "scheme",
                ))
    xml = ""
    xsd_errors = []
    twin = None
    if not findings:
        meta = _meta(message_type)
        try:
            xml = generate_xml_string(rows, message_type, str(meta.template_path), str(meta.xsd_path))
        except Exception as exc:  # any failure to produce a file is a verdict, not a crash
            findings.append(_finding("", "", "generate", "", exc, "iso"))
        else:
            xsd_errors = json.loads(xsd_errors_text(xml, message_type))
            if not xsd_errors:
                twin = to_iso_json(xml, message_type)
    return json.dumps({
        "findings": findings, "scheme": scheme_result, "xml": xml, "twin": twin,
        "xsd_errors": xsd_errors, "records": len(rows), "version": pain001.__version__,
    })
`;

/**
 * Load the runtime and the library. ``base`` is the directory holding
 * /pyodide/ (a URL path in the browser, an absolute path in Node);
 * ``loadPyodide`` is injected so browser and Node use their own copy.
 * ``onProgress({phase, done, total})`` is called as bytes arrive.
 */
export async function loadEngine({ base, loadPyodide, fetchImpl, onProgress }) {
  const progress = onProgress || (() => {});
  const fetcher = fetchImpl || globalThis.fetch;
  const manifest = await fetcher(`${base}/pyodide/pain001-runtime.json`).then((r) => r.json());
  const files = [...manifest.runtime, ...manifest.packages, ...manifest.wheels];
  const total = files.reduce((n, f) => n + f.bytes, 0);
  let done = 0;
  progress({ phase: "download", done, total });
  // Warm the HTTP cache file by file so the bar reflects real bytes; the
  // runtime's own loads then hit the cache.
  for (const file of files) {
    const resp = await fetcher(`${base}/pyodide/${file.file}`);
    if (!resp.ok) throw new Error(`${file.file}: HTTP ${resp.status}`);
    if (resp.body && resp.body.getReader) {
      const reader = resp.body.getReader();
      for (;;) {
        const { done: end, value } = await reader.read();
        if (end) break;
        done += value.length;
        progress({ phase: "download", done, total });
      }
    } else {
      done += (await resp.arrayBuffer()).byteLength;
      progress({ phase: "download", done, total });
    }
  }
  progress({ phase: "boot", done: total, total });
  const py = await loadPyodide({ indexURL: `${base}/pyodide/` });
  progress({ phase: "install", done: total, total });
  await py.loadPackage([
    ...PYODIDE_PACKAGES,
    ...manifest.wheels.map((w) => `${base}/pyodide/${w.file}`),
  ], { messageCallback: () => {} });
  progress({ phase: "warm", done: total, total });
  py.runPython(BRIDGE);
  const version = py.runPython(`warm(${JSON.stringify(MESSAGE_TYPE)})`);
  progress({ phase: "ready", done: total, total });
  return { py, version, manifest };
}

/** Run the library on parsed records. Returns the bridge's JSON, parsed. */
export function runEngine(engine, rows, { messageType = MESSAGE_TYPE, scheme = "" } = {}) {
  const { py } = engine;
  py.globals.set("_rows_json", JSON.stringify(rows));
  const out = py.runPython(`run(_rows_json, ${JSON.stringify(messageType)}, ${JSON.stringify(scheme)})`);
  return JSON.parse(out);
}
