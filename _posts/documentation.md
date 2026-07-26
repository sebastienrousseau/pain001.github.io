---

author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Pain001 ISO 20022 Payment Initiation Suite"
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complete API reference for Pain001 CLI, Python library, REST API, scheme validators, streaming mode, and input normalization."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/documentation/"
image_alt: "Logo of Pain001 Suite"
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, payments, SWIFT, SEPA, banking, Python, MCP, LSP"
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
subtitle: "ISO 20022 Payment Initiation & Transaction Orchestration Suite"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "Pain001 Documentation & Comprehensive API Reference"
url: "https://pain001.com/documentation/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/documentation/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Complete API reference for Pain001 CLI, Python library, REST API, scheme validators, streaming mode, and input normalization."
item_guid: "https://pain001.com/documentation/rss.xml"
item_link: "https://pain001.com/documentation/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 Documentation & Comprehensive API Reference"
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
apple-mobile-web-app-title: "Pain001 Documentation & Comprehensive API Reference"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Complete API reference for Pain001 CLI, Python library, REST API, scheme validators, streaming mode, and input normalization."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 Documentation & Comprehensive API Reference"
twitter_url: "https://pain001.com/documentation/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"

---

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
