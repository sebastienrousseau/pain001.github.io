---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A payment batch moving through origination, validation, bank submission, acknowledgement, and statement reconciliation — the lifecycle Pain001 instruments end to end."
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "From ERP export to pain.002 acknowledgement to camt.053 reconciliation — designing batch, streaming, and API payment pipelines around validation gates that stop rejections."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/payments/"
image_alt: "A payment batch moving through origination, validation, bank submission, acknowledgement, and statement reconciliation — the lifecycle Pain001 instruments end to end."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "payment initiation pipeline, pain.002 status report, camt.053 reconciliation, payment batch processing, payment file automation, rejection handling"
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
permalink: "https://pain001.com/payments/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "From ERP export to pain.002 acknowledgement to camt.053 reconciliation — the full lifecycle, with validation gates at every step."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "Payment Initiation End to End with Pain001"
url: "https://pain001.com/payments/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/payments/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "From ERP export to pain.002 acknowledgement to camt.053 reconciliation — designing batch, streaming, and API payment pipelines around validation gates that stop rejections."
item_guid: "https://pain001.com/payments/rss.xml"
item_link: "https://pain001.com/payments/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Payment Initiation End to End with Pain001"
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
apple-mobile-web-app-title: "Payment Initiation End to End with Pain001"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "From ERP export to pain.002 acknowledgement to camt.053 reconciliation — designing batch, streaming, and API payment pipelines around validation gates that stop rejections."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Payment Initiation End to End with Pain001"
twitter_url: "https://pain001.com/payments/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Guide"
excerpt: "Where Pain001 sits in a corporate payment flow: originate from the systems you have, generate validated pain.001, submit over your bank channel, parse the pain.002 response, reconcile against camt.053. Batch, streaming, REST, and agent-assisted patterns — and the four rejection classes your pipeline should make impossible."
last_reviewed: "2026-07-26"

---

Where Pain001 sits in a corporate payment flow, and how to design the pipeline around it — from ERP export to bank acknowledgement to statement reconciliation.

---

## 01. The lifecycle of one payment batch

1. **Origination.** Accounts payable, payroll, or treasury produces a batch — usually an ERP export, a spreadsheet, or rows in a database.
2. **Generation.** Pain001 ingests the batch (CSV, Excel, SQLite, JSON, JSONL, Parquet, or MT101), normalises fields, validates every record, and renders `pain.001` XML that passes the official XSD.
3. **Submission.** The file goes to the bank over your existing channel — host-to-host SFTP, EBICS, SWIFT FileAct, or a bank portal. Pain001 deliberately stops at the file boundary; connectivity is your bank relationship, not your toolchain.
4. **Acknowledgement.** The bank answers with `pain.002` status reports — accepted, partially accepted, or rejected with reason codes. Pain001's built-in **pain.002 parser** turns those into structured data your systems can route.
5. **Reconciliation.** End-of-day `camt.053` statements confirm what actually settled. Pain001 parses those too, closing the loop from instruction to statement.

Initiate, acknowledge, reconcile. One toolchain covers all three message legs.

## 02. Batch, streaming, or API

- **Scheduled batch** — the classic AP run: cron or CI invokes the CLI, `--dry-run` first, then generation; exit codes gate the pipeline.
- **Large-volume streaming** — `--streaming --chunk-size N` processes memory-bounded chunks, each emitted as an independently valid XML file with recomputed `NbOfTxs`/`CtrlSum`. Payroll-scale batches run in constant memory.
- **Service integration** — `pain001 serve` exposes the same pipeline as REST: synchronous `POST /api/v1/generate` for interactive flows, `POST /api/v1/generate/async` with job polling for heavy ones, Prometheus metrics for your observability stack.
- **Agent-assisted operations** — the [MCP server](/pain001-mcp/) lets an AI assistant run pre-flight checks, explain scheme failures, or convert legacy files, with every tool read-only and local.

## 03. Designing for rejection — so it never happens

Build the four bank-side rejection classes into your pipeline as pre-submission gates:

| Rejection class | Pain001 gate |
| :--- | :--- |
| Schema violation (wrong element/version/namespace) | XSD validation against the official schema, before write |
| Invalid identifiers (IBAN checksum, malformed BIC) | ISO 13616 mod-97 and ISO 9362 structure checks per record |
| Control-total mismatch | `NbOfTxs` / `CtrlSum` recomputed from validated records |
| Scheme-rule breach (SEPA field rules, currency, charge bearer) | `--scheme sepa-sct` / `sepa-inst` / `sepa-sdd` / `sepa-b2b` / `xborder-ct` with `--explain` |

A file that passes all four gates can still be rejected for business reasons — insufficient funds, sanctions screening, closed account. Those belong to the bank. Format-class rejections belong to you, and they are the ones this pipeline eliminates.

## 04. Which version should you generate?

Your bank's channel documentation decides — but the pattern in 2026: `pain.001.001.03` remains the SEPA and CGI workhorse; **`pain.001.001.09`** is the CBPR+ version and the MT101-relay successor, making it the default for anything cross-border; later versions add structured-data refinements banks adopt gradually. Pain001 generates all ten versions and migrates records between them (`migrate_records`, `VersionMapper`), so a version switch is a parameter change, not a project. See the [version reference pages](/pain.001.001.09/) for element-level detail.
