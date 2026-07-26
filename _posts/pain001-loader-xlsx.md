---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A spreadsheet of payment instructions flowing into validated ISO 20022 XML, with the IBAN column protected from Excel's silent numeric conversion."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Read payment batches straight from .xlsx/.xlsm with an IBAN safety guard that stops Excel's numeric coercion corrupting account numbers before the bank ever sees them."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pain001-loader-xlsx/"
image_alt: "A spreadsheet of payment instructions flowing into validated ISO 20022 XML, with the IBAN column protected from Excel's silent numeric conversion."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "Excel to pain.001, xlsx payment file, Excel SEPA XML, IBAN leading zero Excel, exceltopain001 alternative, payment batch spreadsheet"
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
permalink: "https://pain001.com/pain001-loader-xlsx/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Read payment batches straight from .xlsx and .xlsm — with a safety guard that stops Excel corrupting account numbers."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Excel to pain.001: pain001-loader-xlsx"
url: "https://pain001.com/pain001-loader-xlsx/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-loader-xlsx/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Read payment batches straight from .xlsx/.xlsm with an IBAN safety guard that stops Excel's numeric coercion corrupting account numbers before the bank ever sees them."
item_guid: "https://pain001.com/pain001-loader-xlsx/rss.xml"
item_link: "https://pain001.com/pain001-loader-xlsx/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Excel to pain.001: pain001-loader-xlsx"
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
apple-mobile-web-app-title: "Excel to pain.001: pain001-loader-xlsx"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Read payment batches straight from .xlsx/.xlsm with an IBAN safety guard that stops Excel's numeric coercion corrupting account numbers before the bank ever sees them."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Excel to pain.001: pain001-loader-xlsx"
twitter_url: "https://pain001.com/pain001-loader-xlsx/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Excel ingestion"
excerpt: "pain001-loader-xlsx teaches the Pain001 core to ingest Excel workbooks directly: no CSV export step, cached formula values resolved, macros never executed, and streaming for very large sheets. Its IBAN safety guard halts the load if account-number columns arrive as numeric cells — catching Excel's silent coercion before it reaches a bank."
last_reviewed: "2026-07-26"

---

**`pain001-loader-xlsx` v0.0.54** teaches the Pain001 core to read payment batches straight from Excel `.xlsx` and `.xlsm` workbooks. No "Save As CSV" step, no encoding surprises, no silently corrupted account numbers.

Install it and it just works: the loader registers under the `pain001.loaders` entry point and is auto-discovered — `pain001 -t pain.001.001.09 -d payments.xlsx -o out/` needs no further configuration.

```bash
pip install pain001 pain001-loader-xlsx
```

---

## 01. The IBAN safety guard

Excel converts anything that looks like a number into a number. An IBAN pasted into a `General`-formatted cell can lose structure before you ever export it — and a corrupted debtor account is exactly the kind of error that surfaces as a bank-side rejection days later.

The loader refuses to let that happen. If any cell in the `debtor_account_IBAN`, `creditor_account_IBAN`, or `charge_account_IBAN` columns arrives as a numeric type, the load **stops with a clear error** telling you to re-format the column as Text. Matching is case-insensitive, and the failure happens before a single record is validated — fail fast, fail loud.

---

## 02. Behaviour, precisely

- **Formats:** `.xlsx` and `.xlsm`. Legacy `.xls` (BIFF) is not supported.
- **Formulas:** resolved to their last-saved cached values (`data_only=True`); macros in `.xlsm` files are **never executed**.
- **Structure:** first worksheet only; row 1 is the header, rows 2..N are records.
- **Memory:** workbooks are opened read-only, and `load_streaming(path, chunk_size)` yields fixed-size chunks so multi-hundred-thousand-row batches never load fully into memory — pairing naturally with the core CLI's `--streaming` mode.
- **Failure modes:** a workbook with no sheets or a first sheet with no header row raises a precise `ValueError` rather than producing an empty batch.

---

## 03. A well-behaved plugin

The loader conforms structurally to the core's `AbstractLoader` protocol — no subclassing, no tight coupling — and declares its plugin API version so the core can refuse incompatible combinations cleanly. Like every package in the suite, it is tested to 100% line and branch coverage in CI.

---

## FAQ

**Why not just export CSV from Excel?**

CSV export is where leading zeros die and encodings drift. Reading the workbook directly preserves cell types, catches numeric-IBAN corruption at load time, and removes a manual step from a process that runs on deadlines.

**Does it validate the IBANs themselves?**

The guard is a type-level defence at ingestion. Full IBAN checksum validation (ISO 13616 mod-97) happens immediately afterwards in the [core validation pipeline](/documentation/) — two layers, each doing one job.

**What about multi-sheet workbooks?**

Out of scope by design. One sheet, one batch keeps the audit trail unambiguous. Split multi-sheet workbooks upstream, or convert per sheet.
