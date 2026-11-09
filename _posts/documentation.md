---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Documentation pages for the Pain001 command-line interface and REST API, the working reference for teams generating ISO 20022 payment files."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complete reference for pain001 v0.0.83: CLI subcommands and flags, Python API, REST endpoints under /api/v1, scheme rulebooks, input normalisation, and plugin architecture."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/documentation/"
image_alt: "Documentation pages for the Pain001 command-line interface and REST API, the working reference for teams generating ISO 20022 payment files."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001 documentation, pain.001 CLI, ISO 20022 Python library, pain001 REST API, XSD validation, SEPA scheme validation, pain.002 parser, camt.053 parser"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/documentation/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Every flag, endpoint, and behaviour of pain001 v0.0.83, taken from the shipped code, not from aspiration."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 Technical Reference: CLI, Python API and REST"
url: "https://pain001.com/documentation/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/documentation/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.75)"
item_description: "Complete reference for pain001 v0.0.83: CLI subcommands and flags, Python API, REST endpoints under /api/v1, scheme rulebooks, input normalisation, and plugin architecture."
item_guid: "https://pain001.com/documentation/rss.xml"
item_link: "https://pain001.com/documentation/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 Technical Reference: CLI, Python API and REST"
last_build_date: "Sun, 26 Jul 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
ttl: 60
type: website
webmaster: contact@pain001.com
apple_mobile_web_app_orientations: portrait
apple_touch_icon_sizes: 192x192
apple-mobile-web-app-capable: yes
apple-mobile-web-app-status-bar-inset: black
apple-mobile-web-app-status-bar-style: black-translucent
apple-mobile-web-app-title: "Pain001 Technical Reference: CLI, Python API and REST"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "Complete reference for pain001 v0.0.83: CLI subcommands and flags, Python API, REST endpoints under /api/v1, scheme rulebooks, input normalisation, and plugin architecture."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "Pain001 Technical Reference: CLI, Python API and REST"
twitter_url: "https://pain001.com/documentation/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-11-07
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Reference"
excerpt: "The complete technical reference for the Pain001 core: CLI subcommands and generate flags, the Python API and its three-layer validation pipeline, REST endpoints under /api/v1 including async jobs and Prometheus metrics, input normalisation rules, the plugin architecture, and the quality gates the project holds itself to."
last_reviewed: "2026-11-07"

---

This reference documents the command-line interface, Python API, REST microservice, and validation pipeline for **pain001 v0.0.83**. Every flag, endpoint, and behaviour listed here is taken from the shipped code, not from aspiration.

Pain001 supports **13 ISO 20022 message definitions**: `pain.001.001.03` through `pain.001.001.13` (Customer Credit Transfer Initiation, eleven versions) and `pain.008.001.02` / `pain.008.001.08` (Customer Direct Debit Initiation).

---

## 1. Command-Line Interface

The `pain001` executable groups its functionality into subcommands. Running it with only generation flags invokes `generate` implicitly, so existing automation keeps working.

| Subcommand | Purpose |
| :--- | :--- |
| `generate` | Convert a data file into schema-validated ISO 20022 XML (default command). |
| `validate` | Validate input data without writing XML. |
| `check <file>... [--scheme] [--format]` | Check pain.001 or pain.008 files you already have: the XSD of the message type each file declares, the message definition's cross-element rules, and any scheme profiles, policy or Schematron rulebook you name. |
| `verify-signature <file>... --cert <PEM>` | Verify the XML-DSig signature on each file against the signer's certificate or public key; `--trust-embedded-cert` checks integrity only (requires the `sign` extra). |
| `versions [--json]` | List all 13 supported message definitions. |
| `inspect <type> [--json]` | Show the bundled template, schema, example data and accepted input formats for a message type. |
| `init <type> [-o FILE]` | Scaffold a starter CSV template for a message type. |
| `serve [--host] [--port] [--reload]` | Launch the FastAPI REST microservice (requires the `api` extra). |
| `mcp` | Launch the core library's built-in Model Context Protocol server over stdio (requires the `mcp` extra); the full server ships as [`pain001-mcp`](/pain001-mcp/). |
| `plugins list / show / disable` | List the discovered loader, validator, scheme and writer plugins, show one, or print how to disable third-party discovery. |
| `face <file> [--face] [--bindings] [-o] [--loss-report]` | Project a pain.001 XML file into another standard's JSON shape, with a report of every element not carried. |
| `upload [<file>] --sftp <url>` | Deliver a file atomically to an SFTP server you trust explicitly (requires the `upload` extra). |

### `generate` options

| Flag | Description |
| :--- | :--- |
| `-t, --xml-message-type <TYPE>` | Message definition, e.g. `pain.001.001.09`. |
| `-d, --data <FILE>` | Input data: `.csv`, `.json`, `.jsonl`, `.db` / `.sqlite`, `.parquet`, or PGP-encrypted `.gpg` / `.asc`. |
| `-o, --output-dir <DIR>` | Directory that receives the generated XML. |
| `-m, --template <FILE>` / `-s, --schema <FILE>` | Override the bundled Jinja2 template or XSD schema. |
| `-c, --config <FILE>` | Load defaults from a configuration profile (`--profile`, `--show-config`). |
| `--dry-run` (alias `--validate-only`) | Validate input against the JSON Schema, XSD, and scheme rulebook without writing output. |
| `--scheme <NAME[,NAME]>` | Enforce one or more scheme rulebooks, comma-separated. `pain001 plugins list` names every installed rulebook. |
| `--explain --scheme-format {text,json}` | With `--scheme`, print a remediation hint for each violation, as text or JSON. |
| `--rules <FILE>` | Enforce a private YAML CEL policy before generation (requires the `rules` extra). |
| `--schematron <PRESET or FILE>` | Apply Schematron business rules: the `sepa`, `fednow` or `cbpr` preset, or your own `.sch` file. |
| `--decrypt-key <FILE>` / `--decrypt-passphrase-env <VAR>` | Import a GPG private key, and name the variable that holds its passphrase, for `.gpg` / `.asc` input (requires the `gpg` extra). |
| `--streaming` / `--chunk-size <N>` | Memory-bounded chunked processing for large batches (default 1,000 transactions per chunk; each chunk becomes its own XML file with recomputed `NbOfTxs` and `CtrlSum`). |
| `--emit-metrics` | Emit machine-readable run metrics for observability pipelines. |
| `--envelop-bah` | Wrap generated payment XML into an ISO 20022 Business Application Header (`head.001.001.03`) and `BizData` (`head.003.001.01`) envelope. |
| `--bah-sender <BIC/ID>` | Sender financial institution BIC or organisation identifier for BAH `<Fr>`. |
| `--bah-receiver <BIC/ID>` | Receiver financial institution BIC or organisation identifier for BAH `<To>`. |
| `--bah-msg-id <ID>` | Business Message Identifier for BAH `<BizMsgIdr>` (defaults to generated UUID). |
| `--xml-sign-key <FILE>` | PEM private key (RSA, or EC P-256/P-384) for a W3C XML Digital Signature (XML-DSig); the algorithm follows the key. |
| `--xml-sign-cert <FILE>` | Optional PEM X.509 certificate to embed in XML-DSig `<ds:KeyInfo>`. |
| `--xml-sign-alg <ALG>` | `rsa-sha256`, `rsa-pss-sha256`, `ecdsa-sha256` or `ecdsa-sha384`; by default an RSA key signs `rsa-sha256`. |
| `--xml-sign-passphrase-env <VAR>` | Environment variable holding the passphrase for `--xml-sign-key`. |
| `--list-templates` / `--show-template <TYPE>` | List the bundled templates, or show one template's metadata, and exit. |

Exit codes are CI-friendly: `0` success, `1` validation failure, `2` usage error.

XML signing and `verify-signature` need the `sign` extra (`pip install "pain001[sign]"`, which installs `cryptography` and `lxml`).

### Signatures: `pain001 verify-signature`

`pain001 verify-signature` checks the signature on files you received or wrote. Pass the signer's certificate or public key with `--cert`; that is the trust anchor. `--trust-embedded-cert` verifies with each file's own certificate instead, which proves the file is unchanged since it was signed but not who signed it. It exits `0` when every file verifies, `1` when any does not, and `2` when it cannot run; `--format json` prints one report per file. Verification uses exclusive C14N 1.0 and accepts only RSA-SHA256, RSA-PSS and ECDSA signatures with SHA-256 to SHA-512 digests over the whole document; the certificate's chain and validity dates are not checked.

### Faces: `pain001 face`

A face projects a validated pain.001 document into another standard's JSON request body. `--face uk_open_banking` targets the Open Banking Read/Write API v4.0.1 domestic payment, `--face berlin_group` targets NextGenPSD2 v1.3.16 payment initiation, and `--face iso_2018` renames every element to its ISO 20022 name in snake_case. A face refuses a document that lacks an element its target requires instead of inventing a value; `--loss-report` lists every source element it did not carry. Faces are outbound only.

### Delivery: `pain001 upload`

`pain001 upload` sends a finished file to an SFTP server you name, and only after you have trusted its host key: from a `known_hosts` file (`--known-hosts`) or an OpenSSH SHA256 fingerprint you verified independently (`--accept-host-key`). `--print-host-key` shows the server's fingerprint without logging in. It logs in with a private key (`--identity-file`, with `--passphrase-env`), a password read from an environment variable (`--password-env`), or your SSH agent. The file is written under a temporary name and renamed on the server, so the receiving side never sees a partial file.

---

## 2. Python API

```python
from pain001.core.core import process_files

# Generate a validated pain.001.001.09 file from CSV
process_files(
    xml_message_type="pain.001.001.09",
    xml_template_file_path="template.xml",
    xsd_schema_file_path="schema.xsd",
    data_file_path="payments.csv",
    output_path="out/payments.xml",
)
```

Every generated document passes three layers before it is written:

1. **Input validation**: each record is checked against the message type's JSON Schema, with field-alias normalisation and IBAN/BIC syntax checks.
2. **Scheme rulebook** (optional): the rules of the rail you name, from SEPA (SCT, Instant, SDD Core, B2B) to national rails such as UK Faster Payments, CHAPS and Bacs, US ACH and wires, and Swift CBPR+; `pain001 plugins list` names them all.
3. **XSD validation**: the rendered XML is validated against the official ISO 20022 schema via `xmlschema` before a single byte is written to disk. With the optional `fast` extra (lxml) installed, libxml2 accepts valid documents faster; a document it rejects is checked again by `xmlschema`, whose verdict is final.

Monetary amounts are handled as `decimal.Decimal` during XML generation and scheme validation (never IEEE 754 floats), and `NbOfTxs` / `CtrlSum` control totals are recomputed from the validated records rather than trusted from input.

Beyond pain.001 generation, the core library also ships a **pain.002 status-report parser and generator** (so you can read the bank's accept/reject response) and a **camt.053 statement parser and generator** for end-of-day reconciliation, plus a `VersionMapper` that migrates records between message versions.

`pain001.faces.project_face` is the Python entry point for faces. `sign_xml_document` signs a document with XML-DSig, and `verify_signature(signed_xml, trust_anchor=cert_pem)` verifies one and returns a `SignatureReport` (`valid`, `trust`, `algorithm`, `signer`, `reason`); both need the `sign` extra. `verify_xml_signature` without a key or certificate still trusts the certificate inside the document, with a `DeprecationWarning`; pain001 0.0.84 refuses it.

Runnable, self-checking scripts for the public API and the CLI live in the library's [`examples/`](https://github.com/sebastienrousseau/pain001/tree/main/examples) directory.

---

## 3. REST Microservice

```bash
pip install "pain001[api]"
pain001 serve --host 0.0.0.0 --port 8000
```

All endpoints are mounted under `/api/v1` (with an unversioned `/api` alias):

| Method & Path | Purpose |
| :--- | :--- |
| `GET /api/v1/health` | Liveness probe. |
| `POST /api/v1/validate` | Validate records; returns field-level errors. |
| `POST /api/v1/generate` | Synchronous XML generation. |
| `POST /api/v1/generate/async` | Queue a large batch for background generation. |
| `GET /api/v1/status/{job_id}` | Poll an async job. |
| `GET /api/v1/download/{job_id}` | Download the finished XML. |
| `DELETE /api/v1/jobs/{job_id}` | Clean up a completed job. |
| `GET /api/v1/faces` | List the faces and the binding keys each accepts. |
| `POST /api/v1/faces/{face}` | Project a pain.001 document sent as XML text; returns the payload and the loss report, or `422` with the reason the face refused it. |
| `GET /metrics` | Prometheus metrics. |

Interactive documentation is served at `/api/docs` (Swagger UI), `/api/redoc`, and `/api/reference` (Scalar), with the OpenAPI document at `/openapi.json`.

When the `PAIN001_API_KEY` environment variable is set, every endpoint except `/health` and `/metrics` requires it as a bearer token; when it is unset, the API is open. `pain001 serve` binds to `127.0.0.1` unless you pass `--host`.

---

## 4. Input Normalisation

Pain001 coerces real-world exports into valid records before validation:

- **Field aliases**: common ERP column names map onto canonical fields (for example `amount` → `payment_amount`).
- **IBAN / BIC normalisation**: whitespace stripped, case folded, then checked (ISO 13616 mod-97 for IBANs, ISO 9362 structure for BICs).
- **Dates**: ISO 8601 `YYYY-MM-DD` parsing for execution dates.
- **Amounts**: routed through `decimal.Decimal`; malformed amounts fail validation instead of silently rounding.
- **Character set**: transliteration helpers reduce content to the ISO 20022 Latin character set accepted by SWIFT and SEPA.
- **Formula cells**: CSV cells that start with `=`, `+`, `-` or `@` are kept as supplied by default, so phone numbers and references survive; `load_csv_data(path, sanitize_formula=True)` escapes them with a leading quote instead.

---

## 5. Plugin Architecture

The suite is extensible through four entry-point groups: `pain001.loaders`, `pain001.validators`, `pain001.schemes`, and `pain001.writers`. [`pain001-loader-xlsx`](/pain001-loader-xlsx/) registers through this mechanism and is auto-discovered on install; [`pain001-loader-mt101`](/pain001-loader-mt101/) is a standalone parsing library consumed directly (and by the MCP server's `convert_mt101` tool). A kill switch, `PAIN001_DISABLE_PLUGINS=1`, disables third-party plugin discovery entirely in locked-down environments.

---

## 6. Quality Gates

The core library is developed against strict, verifiable gates: 100% line **and** branch coverage enforced in CI (`--cov-fail-under=100`), strict mypy typing, 100% docstring coverage, and security linting (Bandit, pip-audit). A CycloneDX SBOM is generated for every release build.

Continue with the [Installation Guide](/installation/), the [MCP server for AI agents](/pain001-mcp/), or the [payments glossary](/glossary/).
