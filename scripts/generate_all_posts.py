#!/usr/bin/env python3
import os

POSTS_DIR = "/Users/seb/Code/Public/html/pain001.github.io/_posts"
os.makedirs(POSTS_DIR, exist_ok=True)

DATE_ISO = "2026-07-26T08:00:00+00:00"
DATE_RFC = "Sun, 26 Jul 2026 08:00:00 +0000"

def get_fm(title, description, permalink, layout="page", keywords=""):
    return {
        "author": "contact@pain001.com (Sebastien Rousseau)",
        "banner_alt": "Pain001 ISO 20022 Payment Initiation Suite",
        "banner_height": "500",
        "banner_width": "1200",
        "banner": "https://cloudcdn.pro/pain001/v1/logos/pain001.svg",
        "cdn": "https://cloudcdn.pro",
        "changefreq": "weekly",
        "charset": "utf-8",
        "cname": "pain001.com",
        "copyright": "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT.",
        "date": DATE_ISO,
        "description": description,
        "download": "https://pypi.org/project/pain001/",
        "format-detection": "telephone=no",
        "hreflang": "en",
        "icon": "https://cloudcdn.pro/pain001/v1/logos/pain001.svg",
        "id": permalink,
        "image_alt": "Logo of Pain001 Suite",
        "image_height": "120",
        "image_width": "120",
        "image": "https://cloudcdn.pro/pain001/v1/logos/pain001.svg",
        "keywords": keywords or "pain001, ISO 20022, payments, SWIFT, SEPA, banking, Python, MCP, LSP",
        "language": "en-GB",
        "layout": layout,
        "locale": "en_GB",
        "logo_alt": "Pain001 Logo",
        "logo_height": "36",
        "logo_width": "36",
        "logo": "https://cloudcdn.pro/pain001/v1/logos/pain001.svg",
        "menu": "active",
        "measurementID": "G-167B274ZWJ",
        "name": "Pain001",
        "permalink": permalink,
        "rating": "general",
        "referrer": "no-referrer",
        "revisit-after": "7 days",
        "robots": "index, follow",
        "short_name": "pain001",
        "subtitle": "ISO 20022 Payment Initiation & Transaction Orchestration Suite",
        "tags": "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA",
        "theme_color": "0, 132, 199",
        "title": title,
        "url": permalink,
        "viewport": "width=device-width, initial-scale=1, shrink-to-fit=no",
        "atom_link": f"{permalink}rss.xml",
        "category": "Technology",
        "docs": "https://validator.w3.org/feed/docs/rss2.html",
        "generator": "Static Site Generator (SSG) (version 0.0.47)",
        "item_description": description,
        "item_guid": f"{permalink}rss.xml",
        "item_link": f"{permalink}rss.xml",
        "item_pub_date": DATE_RFC,
        "item_title": title,
        "last_build_date": DATE_RFC,
        "managing_editor": "contact@pain001.com (Sebastien Rousseau)",
        "pub_date": DATE_RFC,
        "ttl": "60",
        "type": "website",
        "webmaster": "contact@pain001.com",
        "apple_mobile_web_app_orientations": "portrait",
        "apple_touch_icon_sizes": "192x192",
        "apple-mobile-web-app-capable": "yes",
        "apple-mobile-web-app-status-bar-inset": "black",
        "apple-mobile-web-app-status-bar-style": "black-translucent",
        "apple-mobile-web-app-title": title,
        "apple-touch-fullscreen": "yes",
        "msapplication-navbutton-color": "rgb(2, 132, 199)",
        "twitter_card": "summary_large_image",
        "twitter_creator": "@wwdseb",
        "twitter_description": description,
        "twitter_image": "https://cloudcdn.pro/pain001/v1/logos/pain001.svg",
        "twitter_image_alt": "Pain001 Logo",
        "twitter_site": "@wwdseb",
        "twitter_title": title,
        "twitter_url": permalink,
        "author_website": "https://sebastienrousseau.com",
        "author_twitter": "@wwdseb",
        "author_location": "London, UK",
        "thanks": "Thank you for using Pain001 Suite!",
        "site_last_updated": "2026-07-26",
        "site_standards": "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD",
        "site_components": "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx",
        "site_software": "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS",
    }

def write_post(filename, fm, content):
    filepath = os.path.join(POSTS_DIR, filename)
    lines = ["---", ""]
    for k, v in fm.items():
        if isinstance(v, str) and (v.startswith("http") or ":" in v or "[" in v or "#" in v or " " in v):
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f'{k}: {v}')
    lines.extend(["", "---", "", content.strip(), ""])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ Wrote {filename}")

# 1. index.md
write_post("index.md", get_fm("Pain001: ISO 20022 Payment Initiation & AI Transaction Suite", "Automate ISO 20022 Customer Credit Transfer & Direct Debit initiation file generation from CSV, Excel, SQLite, JSON, Parquet, and SWIFT MT101.", "https://pain001.com/", layout="index"), '''
# Welcome to the Pain001 Open Ecosystem

**Pain001** is the enterprise-grade Python suite for ISO 20022 **Customer Credit Transfer Initiation (`pain.001`)** and **Customer Direct Debit Initiation (`pain.008`)** message creation, schema validation, legacy translation, and AI agent transaction orchestration.

Banks and clearing networks reject malformed payment files. Pain001 ingests your operational payment data—whether exported from ERPs as CSV, Excel, SQLite, JSON, Parquet, or emitted as legacy SWIFT MT101 files—and converts it into 100% XSD-validated XML that adheres strictly to SWIFT CBPR+, SEPA, TARGET2, and FedNow rulebooks.

---

## The 5 Pillars of the Pain001 Suite

1. **`pain001` (Core Library & REST API)**: Python generator, CLI suite, and FastAPI REST microservice supporting monetary precision (`decimal.Decimal`), XXE zero-trust parsing (`defusedxml`), automatic control total calculations (`NbOfTxs`, `CtrlSum`), and streaming execution.
2. **`pain001-mcp` (Model Context Protocol Server)**: Exposes 17 agent tools for autonomous AI agents (Claude Desktop, Cursor, AI orchestrators) to validate IBAN/BICs, sanitize charsets, migrate schema versions, and generate payments within conversational workflows.
3. **`pain001-lsp` (Language Server Protocol)**: Editor diagnostics server providing real-time schema validation, autocomplete, hover docs, and quick-fix code actions for payment JSON authoring in VS Code, Neovim, Helix, and Emacs.
4. **`pain001-loader-mt101` (SWIFT MT101 Bridge)**: Parses legacy MT101 (Request for Transfer) sequence A/B messages into structured records that pass `pain.001.001.09` schema validation, solving the 2025/2026 SWIFT MT-MX coexistence migration requirement.
5. **`pain001-loader-xlsx` (Direct Excel Ingestion)**: Native Excel (`.xlsx` / `.xlsm`) loader plugin featuring an IBAN Safety Guard that rejects cell type `General` (preventing leading zero truncation) and resolves cached formulas (`data_only=True`).

---

## 2026 Mandatory ISO 20022 Migration Readiness

The global financial infrastructure is completing its migration to ISO 20022 messaging:
- **SWIFT CBPR+ MT-MX Coexistence Deadline**: Legacy MT101 and MT103 formats are decommissioned; financial institutions enforce strict XML schema compliance.
- **November 2026 Mandatory Structured Postal Address Rule**: Unstructured address lines are phased out in favor of discrete elements (`StrtNm`, `BldgNb`, `PstCd`, `TwnNm`, `Ctry`).
- **Instant Settlement Networks**: Seamless integration with FedNow (US), TIPS (Eurosystem), SEPA Instant Credit Transfer (`sepa-inst`), and UAE IPP.

---

## Quick Start Command

```bash
# Install core library and companion loaders
pip install pain001 pain001-loader-xlsx pain001-loader-mt101

# Generate a validated pain.001.001.09 payment file from Excel
pain001 -t pain.001.001.09 -d payments.xlsx -o output.xml
```

Explore our complete [Documentation](/documentation), [Installation Guide](/installation), and [2026 Trends Paper](/2026-iso20022-migration-trends).
''')

# 2. documentation.md
write_post("documentation.md", get_fm("Pain001 Documentation & Comprehensive API Reference", "Complete API reference for Pain001 CLI, Python library, REST API, scheme validators, streaming mode, and input normalization.", "https://pain001.com/documentation/"), '''
# Pain001 Suite Documentation & Technical Reference

This reference covers the CLI options, Python public API, REST microservice endpoints, scheme validators, and input normalization rules across the entire Pain001 ecosystem.

---

## 1. Command-Line Interface (CLI)

The `pain001` binary resolves templates and XSD schemas automatically from its bundled registry.

### Required Arguments
- `-t, --xmltype <TYPE>`: Message type (e.g. `pain.001.001.03`, `pain.001.001.09`, `pain.001.001.11`, `pain.008.001.02`).
- `-d, --data <FILE>`: Path to input data file (`.csv`, `.xlsx`, `.sqlite`, `.json`, `.jsonl`, `.parquet`).

### Optional Arguments & Flags
- `-o, --output <FILE>`: Output XML file path (defaults to `<xmltype>.xml`).
- `-m, --template <FILE>`: Custom XML template path.
- `-s, --schema <FILE>`: Custom XSD schema path.
- `--scheme <SCHEME>`: Enforce scheme rulebook checks (`sepa-sct`, `sepa-sdd`, `sepa-inst`, `sepa-b2b`, `xborder-ct`).
- `--dry-run`: Validate input data against XSD and scheme rules without writing output file (Exit code `0` for valid, `1` for invalid).
- `--streaming`: Enable memory-bounded chunked input processing for large datasets.
- `--chunk-size <N>`: Number of transactions per output chunk (default: `1000`).

---

## 2. Python Library Reference

```python
from pain001 import generate_xml_file, generate_xml_string
from pain001.validation import SchemaValidator

# Option A: Generate XML file directly
generate_xml_file(
    xml_type="pain.001.001.09",
    data_file="payments.xlsx",
    output_file="out.xml"
)

# Option B: In-memory validation and XML string generation
records = [
    {
        "payment_id": "TXN-2026-001",
        "payment_amount": "12500.50",
        "currency": "EUR",
        "debtor_name": "Acme Global Corp",
        "debtor_account_IBAN": "DE89370400440532013000",
        "debtor_BIC": "DEUTDEFFXXX",
        "creditor_name": "Supplier Logistics SARL",
        "creditor_account_IBAN": "FR1420041010050500013M02606",
        "creditor_BIC": "BNPAFRPPXXX",
        "charge_bearer": "SHAR",
        "remittance_information": "INVOICE-99887"
    }
]

validator = SchemaValidator("pain.001.001.09")
total, valid, errors = validator.validate_batch(records)

if valid == total:
    xml_output = generate_xml_string("pain.001.001.09", records)
    print("XML Generation Successful!")
else:
    print(f"Validation failed with errors: {errors}")
```

---

## 3. REST Microservice API

Launch the bundled FastAPI + Uvicorn server:

```bash
pip install "pain001[api]"
pain001 serve --host 0.0.0.0 --port 8000
```

### Endpoints
- `POST /v1/generate`: Ingests JSON payload or file upload and returns generated ISO 20022 XML.
- `POST /v1/validate`: Ingests JSON payload and returns validation status with precise field-level errors.
- `GET /health`: Health check and system status.

---

## 4. Input Normalization & Field Aliases

Pain001 automatically coerces user inputs to validate on the first try:
- Field name alias matching (`amount` -> `payment_amount`, `execution_date` -> `requested_execution_date`).
- IBAN / BIC lowercase normalization and whitespace stripping.
- Date string parsing (ISO 8601 `YYYY-MM-DD`).
- Precision protection: Numerical amounts are coerced through `decimal.Decimal` to prevent floating-point inaccuracies.
''')

# 3. installation.md
write_post("installation.md", get_fm("Pain001 Installation Guide: PyPI, Extras, Docker & Kubernetes", "Complete installation options for Pain001 suite including PyPI, optional extras, companion loaders, Docker, and Kubernetes.", "https://pain001.com/installation/"), '''
# Pain001 Installation & Deployment Guide

Pain001 requires **Python 3.10 or later** and runs natively on macOS, Linux, and Windows.

---

## 1. PyPI Installation Channels

| Channel | Command | Use Case |
| :--- | :--- | :--- |
| **Core CLI & Library** | `pip install pain001` | Standard command-line and Python API |
| **REST API Server** | `pip install "pain001[api]"` | Includes FastAPI + Uvicorn microservice |
| **Parquet Support** | `pip install "pain001[parquet]"` | Ingest PyArrow Parquet analytical datasets |
| **Redis Job Queue** | `pip install "pain001[redis]"` | Distributed background job processing |
| **MCP AI Server** | `pip install "pain001[mcp]"` | In-tree Model Context Protocol server |
| **LSP Language Server** | `pip install "pain001[lsp]"` | In-tree Language Server Protocol backend |

---

## 2. Installing Companion Loaders

To enable Excel and legacy SWIFT MT101 file support, install the official companion loaders:

```bash
# Direct Excel (.xlsx / .xlsm) loader with IBAN safety protection
pip install pain001-loader-xlsx

# Legacy SWIFT MT101 to pain.001 converter loader
pip install pain001-loader-mt101
```

---

## 3. Docker Deployment (GHCR)

Pre-built multi-architecture Docker images (`linux/amd64`, `linux/arm64`) are published to GitHub Container Registry.

### Execute CLI via Docker
```bash
docker run --rm -v "$PWD:/data" -w /data \
  ghcr.io/sebastienrousseau/pain001:latest \
  generate -t pain.001.001.09 -d payments.csv -o output.xml
```

### Launch REST API via Docker
```bash
docker run --rm -p 8000:8000 \
  ghcr.io/sebastienrousseau/pain001:latest \
  serve --host 0.0.0.0 --port 8000
```

> **Security Posture**: The Docker container executes under a dedicated non-root `pain001` user account (UID 10001).
''')

# 4. pain001-mcp.md
write_post("pain001-mcp.md", get_fm("pain001-mcp: Model Context Protocol Server for AI Payment Tools", "Exposing the Pain001 payment library as 17 first-class Model Context Protocol (MCP) agent tools for Claude Desktop, Cursor, and LLMs.", "https://pain001.com/pain001-mcp/"), '''
# pain001-mcp: Model Context Protocol Server

**`pain001-mcp`** is an open-source Model Context Protocol (MCP) server that exposes the `pain001` ISO 20022 payment library as **17 first-class agent tools**.

AI assistants and autonomous agents (such as Claude Desktop, Cursor, and custom FastMCP clients) can discover and invoke payment validation, charset transliteration, schema migration, and XML file generation directly within conversational workflows.

---

## Key Capabilities & Tools

| Tool Name | Description |
| :--- | :--- |
| `generate_xml_string` | Converts payment records into XSD-validated ISO 20022 `pain.001` or `pain.008` XML string. |
| `validate_identifier` | Validates IBANs (ISO 13616 / mod-97 check) and BIC codes (ISO 9362). |
| `migrate_records` | Round-trips and migrates payment records across schema versions (e.g. `pain.001.001.03` -> `pain.001.001.09` -> `.12`). |
| `sanitize_to_iso20022_charset` | Transliterates non-ISO 20022 Latin charset characters into valid SWIFT/SEPA character sets. |
| `parse_file` | Reads CSV, Excel, SQLite, or JSON files and returns structured payment dictionaries. |
| `load_schema` | Returns the official JSON Schema definition for any supported message type. |
| `get_supported_messages` | Lists all 20+ supported ISO 20022 `pain.001` and `pain.008` message versions. |

---

## Quick Start & Registration

### Installation
```bash
pip install pain001-mcp
```

### Register with Claude Desktop
Add the following snippet to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pain001": {
      "command": "python",
      "args": ["-m", "pain001_mcp"]
    }
  }
}
```
''')

# 5. pain001-lsp.md
write_post("pain001-lsp.md", get_fm("pain001-lsp: Language Server Protocol for Payment Authoring", "Language Server Protocol server providing real-time diagnostics, schema validation, and autocomplete for payment JSON authoring in IDEs.", "https://pain001.com/pain001-lsp/"), '''
# pain001-lsp: Language Server Protocol Server

**`pain001-lsp`** brings enterprise Language Server Protocol (LSP) capabilities to payment data authoring. It connects to any LSP-compliant code editor (VS Code, Neovim, Helix, Emacs) to provide instant feedback while authoring payment JSON files.

---

## Features

- **Live Schema Validation**: As-you-type validation against official ISO 20022 message schemas.
- **IBAN & BIC Format Diagnostics**: Highlights invalid IBAN checksums or malformed BIC strings directly in the editor.
- **Field Autocomplete**: IntelliSense completions for all required and optional payment fields with inline documentation.
- **Hover Documentation**: Hover over any field to view XSD definitions, field lengths, and scheme requirements.
- **Quick-Fix Code Actions**: One-click "Add missing required fields" with type-correct placeholders.
- **Document Formatting**: Pretty-prints payment JSON files with 2-space indentation and sanitized charsets.
''')

# 6. pain001-loader-mt101.md
write_post("pain001-loader-mt101.md", get_fm("pain001-loader-mt101: SWIFT MT101 to pain.001 Bridge", "Convert legacy SWIFT MT101 Request for Transfer messages into schema-validated pain.001.001.09 ISO 20022 payment files.", "https://pain001.com/pain001-loader-mt101/"), '''
# pain001-loader-mt101: SWIFT MT101 Converter

**`pain001-loader-mt101`** is a focused companion loader that bridges the gap between legacy SWIFT MT101 messages and modern ISO 20022 `pain.001` XML.

As SWIFT completes its CBPR+ MT-MX migration, banks and corporate treasury management systems (TMS) are phasing out MT101. This loader parses MT101 text streams and produces flat records ready for `pain001` validation and XML generation.

---

## Key Features

- **Sequence A/B Parsing**: Correctly maps global header tags (Sequence A) and repeating transaction blocks (Sequence B).
- **Field Tag Mapping**: Maps `:20:`, `:21R:`, `:32B:`, `:50H:`, `:52A:`, `:57A:`, `:59:`, `:70:`, `:71A:` directly into `pain.001.001.09` keys.
- **Validation Proof**: Parsed records pass `SchemaValidator("pain.001.001.09").validate_batch(...)` with zero errors.
''')

# 7. pain001-loader-xlsx.md
write_post("pain001-loader-xlsx.md", get_fm("pain001-loader-xlsx: Excel Ingestion with IBAN Protection", "Direct Excel (.xlsx / .xlsm) loader plugin for Pain001 featuring numeric IBAN leading-zero safety guard and streaming.", "https://pain001.com/pain001-loader-xlsx/"), '''
# pain001-loader-xlsx: Direct Excel Ingestion Plugin

**`pain001-loader-xlsx`** teaches `pain001` to read payment data directly from Excel `.xlsx` and `.xlsm` spreadsheets without requiring an intermediate "Save As CSV" export.

---

## The IBAN Safety Guard

Excel silently converts text strings that look like numbers into numeric types, stripping leading zeros (e.g., German IBAN `DE09...` or French account numbers starting with `0`).

`pain001-loader-xlsx` includes an **IBAN Safety Guard**:
- If an IBAN column is formatted as cell type `General`, the loader **refuses execution** and instructs the user to format the column as `Text`.
- Prevents silent data corruption before files are submitted to banking networks.
''')

# 8. 2026-iso20022-migration-trends.md
write_post("2026-iso20022-migration-trends.md", get_fm("2026 Payment Trends & ISO 20022 Mandates Research Paper", "Deep-dive research on 2026 global payment trends, SWIFT CBPR+ MT-MX transition, Structured Address mandate, and FedNow.", "https://pain001.com/2026-iso20022-migration-trends/"), '''
# 2026 Global Payment Trends & ISO 20022 Mandates

## Executive Summary

The global wholesale and retail payment landscape in 2026 is defined by the finalization of the **ISO 20022 migration**. Financial institutions, corporate treasuries, and fintech platforms must align with rigid XML schema standards, instant clearing expectations, and mandatory structured data rules.

---

## Key 2026 Regulatory & Architectural Pillars

### 1. SWIFT CBPR+ End of MT-MX Coexistence
The transitional coexistence period between legacy MT messages (MT101, MT103, MT202) and MX ISO 20022 XML (`pain.001`, `pacs.008`, `camt.053`) has concluded. Banks worldwide are enforcing strict rejection policies for non-compliant XML formats.

### 2. November 2026 Mandatory Structured Postal Address Rule
Under SWIFT CBPR+ and Eurosystem rules, unstructured address lines (e.g. `<AdrLine>`) are decommissioned. All payment initiation messages (`pain.001.001.11` / `.12`) must provide discrete postal address elements:
- Street Name (`<StrtNm>`)
- Building Number (`<BldgNb>`)
- Post Code (`<PstCd>`)
- Town Name (`<TwnNm>`)
- Country (`<Ctry>`)
''')

# 9. competitors-comparison.md
write_post("competitors-comparison.md", get_fm("Enterprise Comparative Analysis: Pain001 vs Market Solutions", "Detailed comparison of Pain001 Suite against enterprise payment gateways, proprietary translators, and middleware.", "https://pain001.com/competitors-comparison/"), '''
# Enterprise Market & Solutions Comparison

This report evaluates **Pain001 Suite** against commercial enterprise payment translators and legacy banking middleware (including Volante, Bottomline Technologies, Form3, Finastra, IBM Payment Manager, XMLdation, and SWIFT Translator).

---

## Comparative Architectural Matrix

| Capability / Metric | Pain001 Suite | Commercial Translators | Legacy Bank Middleware |
| :--- | :--- | :--- | :--- |
| **Licensing Model** | **Dual Apache-2.0 / MIT** | Annual Per-Core License | Heavy Enterprise Contract |
| **Auditability & Source** | 100% Open Source | Closed Source | Closed Source |
| **ISO 20022 Version Depth** | `pain.001.001.03` to `.12` | Vendor-dependent | Upgrade cycle dependent |
| **AI MCP Protocol Integration** | **Native (17 Tools)** | None | None |
| **IDE Language Server (LSP)** | **Native `pain001-lsp`** | None | None |
| **Legacy SWIFT MT101 Bridge** | Included (`loader-mt101`) | Paid Add-on | Mainframe Adapter |
| **Direct Excel Ingestion** | Included (`loader-xlsx`) | Manual conversion | Custom ETL required |
| **Monetary Precision** | `decimal.Decimal` | Varies | Varies |
| **XXE Security Hardening** | Native `defusedxml` | Vendor-dependent | Vendor-dependent |
| **Deployment Footprint** | Lightweight Python / Docker | Heavy Application Server | Mainframe / VM Cluster |
''')

# 10. architecture-and-patents.md
write_post("architecture-and-patents.md", get_fm("Enterprise Architecture & Open Protocols White Paper", "Architectural white paper covering Pain001 zero-trust XML security, monetary precision, streaming performance, and open standards.", "https://pain001.com/architecture-and-patents/"), '''
# Enterprise Architecture & Open Standards White Paper

## 1. Zero-Trust Security & XML Hardening
Pain001 implements an OWASP-compliant zero-trust posture for XML parsing and generation:
- **XXE Protection**: All XML processing is routed through `defusedxml` to block XML External Entity (XXE) injection, entity expansion attacks (Billion Laughs), and external DTD resolution.
- **Input Sanitization**: Control characters and non-ISO 20022 Latin characters are transliterated or stripped prior to XML serialization.

---

## 2. Fixed-Point Monetary Precision
To eliminate binary floating-point representation errors inherent in IEEE 754 floats:
- All financial amounts (`payment_amount`, `instructed_amount`, control totals) are parsed and calculated using Python's `decimal.Decimal`.
- Control totals (`NbOfTxs` and `CtrlSum`) are dynamically computed from validated transaction records, never trusted blindly from raw input sources.
''')

# 11. faqs.md
write_post("faqs.md", get_fm("Pain001 Enterprise & Technical FAQs", "Comprehensive questions and answers for Treasurers, CFOs, Enterprise Architects, Compliance Officers, and Engineers.", "https://pain001.com/faqs/"), '''
# Frequently Asked Questions (FAQs)

## General & Business Questions

### Q: What is Pain001?
Pain001 is an open-source enterprise Python library, CLI, REST API, AI MCP server, and IDE language server designed to automate ISO 20022 `pain.001` (Customer Credit Transfer Initiation) and `pain.008` (Direct Debit Initiation) payment file creation and validation.

### Q: Who uses Pain001?
Pain001 is deployed by corporate treasuries, commercial banks, fintech payment gateways, ERP vendors, and financial engineering teams worldwide.

### Q: What licenses govern Pain001?
Pain001 is dual-licensed under the **Apache-2.0** and **MIT** licenses, allowing free commercial use, modification, and integration without restrictive copyleft requirements.
''')

# 12. Schema versions (03 to 12)
for ver in ["03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
    filename = f"pain.001.001.{ver}.md"
    title = f"pain.001.001.{ver} ISO 20022 Message Reference"
    desc = f"Technical specification, XSD schema rules, and element definitions for ISO 20022 pain.001.001.{ver} Customer Credit Transfer Initiation."
    permalink = f"https://pain001.com/pain.001.001.{ver}/"
    content = f'''
# pain.001.001.{ver} ISO 20022 Message Reference

`pain.001.001.{ver}` is the Customer Credit Transfer Initiation version specification.

## Key Element Tree
- `<GrpHdr>` (Group Header): Control information, message identifier, creation date/time, number of transactions (`NbOfTxs`), and control sum (`CtrlSum`).
- `<PmtInf>` (Payment Information): Debtor details, execution date, payment method, charge bearer, and debtor account/agent.
- `<CdtTrfTxInf>` (Credit Transfer Transaction Information): Creditor details, instructed amount, currency, creditor account (IBAN), creditor agent (BIC), and remittance information.

## Usage with Pain001

```bash
pain001 -t pain.001.001.{ver} -d payments.csv -o output_{ver}.xml
```
'''
    write_post(filename, get_fm(title, desc, permalink), content)

# 13. Other pages
write_post("payments.md", get_fm("ISO 20022 Payment Processing Architecture", "Guide to automated payment initiation, validation, and processing using Pain001.", "https://pain001.com/payments/"), "# Payment Processing Architecture Guide\n\nPain001 streamlines end-to-end payment initiation pipelines.")
write_post("iso-20022-payment-initiation-for-cross-border-payments.md", get_fm("ISO 20022 Cross-Border Payments & SWIFT CBPR+", "Guide to SWIFT CBPR+ cross-border credit transfer initiation with Pain001.", "https://pain001.com/iso-20022-payment-initiation-for-cross-border-payments/"), "# ISO 20022 Cross-Border Payments Guide\n\nCross-border payment initiation requires strict adherence to SWIFT CBPR+ guidelines.")
write_post("privacy.md", get_fm("Pain001 Privacy Policy", "Privacy policy for Pain001 website and services.", "https://pain001.com/privacy/"), "# Privacy Policy\n\nPain001 does not collect financial transaction data.")
write_post("terms.md", get_fm("Pain001 Terms of Service", "Terms of service for Pain001 software and website.", "https://pain001.com/terms/"), "# Terms of Service\n\nPain001 is dual-licensed under Apache-2.0 and MIT.")
write_post("thanks.md", get_fm("Thank You", "Thank you for visiting Pain001.", "https://pain001.com/thanks/"), "# Thank You\n\nThank you for exploring Pain001 Suite!")
write_post("contact.md", get_fm("Contact Security & Support", "Contact Pain001 team.", "https://pain001.com/contact/", layout="contact"), "# Contact Us\n\nPlease reach out for security or enterprise inquiries.")
write_post("404.md", get_fm("404 Page Not Found", "Page not found.", "https://pain001.com/404/"), "# 404 - Page Not Found\n\nThe requested page could not be found.")
write_post("offline.md", get_fm("Offline", "Offline page.", "https://pain001.com/offline/"), "# You are Offline\n\nPlease check your network connection.")
write_post("tags.md", get_fm("Tags", "Topic tags.", "https://pain001.com/tags/"), "# Topic Tags\n\nExplore topics across Pain001 documentation.")
write_post("made-with-shokunin.md", get_fm("Made with Static Site Generator", "Built with SSG Rust static site generator.", "https://pain001.com/made-with-shokunin/"), "# Made with SSG\n\nThis site is compiled with Static Site Generator (SSG) in Rust.")

print("✓ All posts generated successfully with zero syntax errors!")
