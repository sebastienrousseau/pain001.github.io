---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Documentation pages for the Pain001 command-line interface and REST API — the working reference for teams generating ISO 20022 payment files."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complete reference for pain001 v0.0.56 — CLI subcommands and flags, Python API, REST endpoints under /api/v1, scheme rulebooks, input normalisation, and plugin architecture."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/documentation/"
image_alt: "Documentation pages for the Pain001 command-line interface and REST API — the working reference for teams generating ISO 20022 payment files."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001 documentation, pain.001 CLI, ISO 20022 Python library, pain001 REST API, XSD validation, SEPA scheme validation, pain.002 parser, camt.053 parser"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/documentation/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Every flag, endpoint, and behaviour of pain001 v0.0.56 — taken from the shipped code, not from aspiration."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 Technical Reference: CLI, Python API and REST"
url: "https://pain001.com/documentation/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/documentation/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Complete reference for pain001 v0.0.56 — CLI subcommands and flags, Python API, REST endpoints under /api/v1, scheme rulebooks, input normalisation, and plugin architecture."
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
twitter_creator: @wwdseb
twitter_description: "Complete reference for pain001 v0.0.56 — CLI subcommands and flags, Python API, REST endpoints under /api/v1, scheme rulebooks, input normalisation, and plugin architecture."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 Technical Reference: CLI, Python API and REST"
twitter_url: "https://pain001.com/documentation/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Reference"
excerpt: "The complete technical reference for the Pain001 core: CLI subcommands and generate flags, the Python API and its three-layer validation pipeline, REST endpoints under /api/v1 including async jobs and Prometheus metrics, input normalisation rules, the plugin architecture, and the quality gates the project holds itself to."
last_reviewed: "2026-07-26"

---

This reference documents the command-line interface, Python API, REST microservice, and validation pipeline for **pain001 v0.0.56**. Every flag, endpoint, and behaviour listed here is taken from the shipped code, not from aspiration.

Pain001 supports **11 ISO 20022 message definitions**: `pain.001.001.03` through `pain.001.001.12` (Customer Credit Transfer Initiation, ten versions) and `pain.008.001.02` (Customer Direct Debit Initiation).

---

## 1. Command-Line Interface

The `pain001` executable groups its functionality into subcommands. Running it with only generation flags invokes `generate` implicitly, so existing automation keeps working.

| Subcommand | Purpose |
| :--- | :--- |
| `generate` | Convert a data file into schema-validated ISO 20022 XML (default command). |
| `validate` | Validate input data without writing XML. |
| `versions [--json]` | List all 11 supported message definitions. |
| `inspect <type> [--json]` | Show the required and optional fields for a message type. |
| `init <type> [-o DIR]` | Scaffold a starter CSV template for a message type. |
| `serve [--host] [--port] [--reload]` | Launch the FastAPI REST microservice (requires the `api` extra). |
| `mcp` | Launch the in-tree Model Context Protocol server (5 tools; the full 17-tool server ships as [`pain001-mcp`](/pain001-mcp/)). |
| `plugins list / show / disable` | Inspect and manage discovered loader, validator, scheme, and writer plugins. |

### `generate` options

| Flag | Description |
| :--- | :--- |
| `-t, --xml-message-type <TYPE>` | Message definition, e.g. `pain.001.001.09`. |
| `-d, --data <FILE>` | Input data: `.csv`, `.json`, `.jsonl`, `.db` / `.sqlite`, `.parquet`, or PGP-encrypted `.gpg` / `.asc`. |
| `-o, --output-dir <DIR>` | Directory that receives the generated XML. |
| `-m, --template <FILE>` / `-s, --schema <FILE>` | Override the bundled Jinja2 template or XSD schema. |
| `-c, --config <FILE>` | Load defaults from a configuration profile (`--profile`, `--show-config`). |
| `--dry-run` (alias `--validate-only`) | Validate input against the JSON Schema, XSD, and scheme rulebook without writing output. |
| `--scheme <NAME>` | Enforce a scheme rulebook: `sepa-sct`, `sepa-inst`, `sepa-sdd`, `sepa-b2b`, or `xborder-ct`. |
| `--explain --scheme-format {text,json}` | Report each scheme rule that passed or failed, human- or machine-readable. |
| `--streaming` / `--chunk-size <N>` | Memory-bounded chunked processing for large batches (default 1,000 transactions per chunk; each chunk becomes its own XML file with recomputed `NbOfTxs` and `CtrlSum`). |
| `--emit-metrics` | Emit machine-readable run metrics for observability pipelines. |

Exit codes are CI-friendly: `0` success, `1` validation failure, `2` usage error.

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
    output_dir="out",
)
```

Every generated document passes three layers before it is written:

1. **Input validation** — each record is checked against the message type's JSON Schema, with field-alias normalisation and IBAN/BIC syntax checks.
2. **Scheme rulebook** (optional) — SEPA SCT, SEPA Instant, SEPA SDD Core, SEPA B2B, or cross-border credit transfer rules.
3. **XSD validation** — the rendered XML is validated against the official ISO 20022 schema via `xmlschema` before a single byte is written to disk.

Monetary amounts are handled as `decimal.Decimal` during XML generation and scheme validation — never IEEE 754 floats — and `NbOfTxs` / `CtrlSum` control totals are recomputed from the validated records rather than trusted from input.

Beyond pain.001 generation, the core library also ships a **pain.002 status-report parser and generator** (so you can read the bank's accept/reject response) and a **camt.053 statement parser and generator** for end-of-day reconciliation, plus a `VersionMapper` that migrates records between message versions.

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
| `GET /metrics` | Prometheus metrics. |

Interactive documentation is served at `/api/docs` (Swagger UI), `/api/redoc`, and `/api/reference` (Scalar), with the OpenAPI document at `/openapi.json`.

---

## 4. Input Normalisation

Pain001 coerces real-world exports into valid records before validation:

- **Field aliases** — common ERP column names map onto canonical fields (for example `amount` → `payment_amount`).
- **IBAN / BIC normalisation** — whitespace stripped, case folded, then checked (ISO 13616 mod-97 for IBANs, ISO 9362 structure for BICs).
- **Dates** — ISO 8601 `YYYY-MM-DD` parsing for execution dates.
- **Amounts** — routed through `decimal.Decimal`; malformed amounts fail validation instead of silently rounding.
- **Character set** — transliteration helpers reduce content to the ISO 20022 Latin character set accepted by SWIFT and SEPA.

---

## 5. Plugin Architecture

The suite is extensible through four entry-point groups: `pain001.loaders`, `pain001.validators`, `pain001.schemes`, and `pain001.writers`. [`pain001-loader-xlsx`](/pain001-loader-xlsx/) registers through this mechanism and is auto-discovered on install; [`pain001-loader-mt101`](/pain001-loader-mt101/) is a standalone parsing library consumed directly (and by the MCP server's `convert_mt101` tool). A kill switch — `PAIN001_DISABLE_PLUGINS=1` — disables third-party plugin discovery entirely in locked-down environments.

---

## 6. Quality Gates

The core library is developed against strict, verifiable gates: 100% line **and** branch coverage enforced in CI (`--cov-fail-under=100`), strict mypy typing, 100% docstring coverage, and security linting (Bandit, pip-audit). A CycloneDX SBOM is generated for every release build.

Continue with the [Installation Guide](/installation/), the [MCP server for AI agents](/pain001-mcp/), or the [payments glossary](/glossary/).
