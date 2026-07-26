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
description: "Automate ISO 20022 Customer Credit Transfer & Direct Debit initiation file generation from CSV, Excel, SQLite, JSON, Parquet, and SWIFT MT101."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/"
image_alt: "Logo of Pain001 Suite"
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, payments, SWIFT, SEPA, banking, Python, MCP, LSP"
language: en-GB
layout: index
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "ISO 20022 Payment Initiation & Transaction Orchestration Suite"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "Pain001: ISO 20022 Payment Initiation & AI Transaction Suite"
url: "https://pain001.com/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Automate ISO 20022 Customer Credit Transfer & Direct Debit initiation file generation from CSV, Excel, SQLite, JSON, Parquet, and SWIFT MT101."
item_guid: "https://pain001.com/rss.xml"
item_link: "https://pain001.com/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001: ISO 20022 Payment Initiation & AI Transaction Suite"
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
apple-mobile-web-app-title: "Pain001: ISO 20022 Payment Initiation & AI Transaction Suite"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Automate ISO 20022 Customer Credit Transfer & Direct Debit initiation file generation from CSV, Excel, SQLite, JSON, Parquet, and SWIFT MT101."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001: ISO 20022 Payment Initiation & AI Transaction Suite"
twitter_url: "https://pain001.com/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"

---

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
