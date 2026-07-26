---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "An open reference book of ISO 20022 payments terminology, from pain.001 to Verification of Payee, defined in plain English."
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "pain.001, pacs.008, camt.053, CBPR+, VoP, UETR, hybrid addresses, control sums — the payments vocabulary defined for treasurers and operations teams, not just developers."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/glossary/"
image_alt: "An open reference book of ISO 20022 payments terminology, from pain.001 to Verification of Payee, defined in plain English."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "ISO 20022 glossary, pain.001 meaning, pacs.008 vs pain.001, camt.053 definition, CBPR+ meaning, UETR, verification of payee, payments terminology"
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
permalink: "https://pain001.com/glossary/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The payments vocabulary in plain English — for the people who sign off on files, not just the people who generate them."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "ISO 20022 Payments Glossary in Plain English"
url: "https://pain001.com/glossary/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/glossary/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "pain.001, pacs.008, camt.053, CBPR+, VoP, UETR, hybrid addresses, control sums — the payments vocabulary defined for treasurers and operations teams, not just developers."
item_guid: "https://pain001.com/glossary/rss.xml"
item_link: "https://pain001.com/glossary/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "ISO 20022 Payments Glossary in Plain English"
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
apple-mobile-web-app-title: "ISO 20022 Payments Glossary in Plain English"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "pain.001, pacs.008, camt.053, CBPR+, VoP, UETR, hybrid addresses, control sums — the payments vocabulary defined for treasurers and operations teams, not just developers."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "ISO 20022 Payments Glossary in Plain English"
twitter_url: "https://pain001.com/glossary/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Glossary"
excerpt: "Every term this site and your bank's channel documentation lean on: the pain, pacs, and camt message families, SEPA schemes and CBPR+, Verification of Payee, IBAN and BICFI and LEI and UETR, structured and hybrid addresses, control sums, charge bearers, and the tooling standards — MCP, LSP, XSD, SBOM — defined without jargon."
last_reviewed: "2026-07-26"

---

Plain-English definitions of the terms that appear across this site and in your bank's channel documentation. Written for treasurers and operations teams first, engineers second.

---

## Messages

**pain.001 — Customer Credit Transfer Initiation.** The XML message a customer sends its bank to order one or more credit transfers. The "pain" family is *payment initiation*; `.001` is the message number; the trailing version (`.001.09`) pins the schema.

**pain.002 — Customer Payment Status Report.** The bank's answer to your `pain.001` or `pain.008`: accepted, partially accepted, or rejected, with ISO reason codes per transaction.

**pain.008 — Customer Direct Debit Initiation.** The collection-side twin of `pain.001`: you pull funds owed to you under a mandate rather than pushing funds out.

**pacs.008 / pacs.009.** The interbank settlement messages your instruction becomes once the bank accepts it. Corporates never author these; banks exchange them.

**camt.052 / camt.053 / camt.054.** Account reporting: intraday report, end-of-day statement, and debit/credit notification respectively. `camt.053` is what reconciliation teams consume each morning.

**MT101.** The legacy SWIFT "Request for Transfer" text message that `pain.001` replaces. The interbank MT101 relay is decommissioned on 14 November 2026 in favour of `pain.001.001.09`; corporate-to-bank MT101 persists only at each bank's discretion.

## Schemes and rulebooks

**SEPA SCT / SCT Inst.** The euro credit-transfer schemes (standard and instant) governed by the European Payments Council rulebooks. Instant transfers settle in seconds, around the clock.

**SEPA SDD Core / B2B.** The euro direct-debit schemes — Core for consumers (with refund rights), B2B for businesses (no refund right, stricter mandate checks).

**CBPR+.** Cross-Border Payments and Reporting Plus: the usage guidelines that profile ISO 20022 messages for SWIFT correspondent banking. When people say "the SWIFT ISO 20022 migration", they mean CBPR+.

**HVPS+.** The equivalent profiling for high-value payment systems (T2, CHAPS, Fedwire and peers).

**CGI-MP.** Common Global Implementation — Market Practice: the group harmonising how corporates use `pain` messages across banks, so one file format can serve many banking partners.

**Verification of Payee (VoP).** The EU-mandated name/IBAN match check applied to all SEPA credit transfers since 9 October 2025. Done by the PSP at execution time; clean creditor data determines whether it matches.

## Identifiers and data

**IBAN.** International Bank Account Number (ISO 13616), self-checking via a mod-97 checksum — which is why a single transposed digit is detectable *before* submission.

**BIC / BICFI.** The ISO 9362 Business Identifier Code of a financial institution. The XML element is `<BIC>` in `pain.001.001.03` but `<BICFI>` from version 9 — a rename that causes real-world rejections during version upgrades.

**LEI.** Legal Entity Identifier (ISO 17442) — the 20-character global company identifier. Over 3 million are active, and regulators increasingly mandate them in payments.

**UETR.** Unique End-to-end Transaction Reference — the UUID that lets a payment be traced across the correspondent chain (SWIFT gpi).

**Structured / hybrid address.** Postal addresses as discrete XML elements (street, town, postcode, country) versus free-text lines. From 14 November 2026, CBPR+ rejects fully unstructured addresses; *hybrid* — structured town and country plus up to two 70-character address lines — remains valid.

**NbOfTxs / CtrlSum.** The group-header control totals: transaction count and amount sum. Banks recompute them; if yours disagree, the file bounces. Pain001 always derives them from the validated records.

**Charge bearer.** Who pays the fees: `DEBT` (sender), `CRED` (receiver), `SHAR` (shared), `SLEV` (per scheme rules). Legacy MT `OUR`/`BEN`/`SHA` map to the first three.

**Remittance information.** The "what this payment is for" field — free text (140 characters) or structured references. The thing reconciliation teams wish everyone filled in properly.

## Tooling terms used on this site

**XSD validation.** Checking XML against the official ISO 20022 schema definition. Pain001 treats it as a hard gate before any file is written.

**MCP — Model Context Protocol.** The open standard through which AI assistants call external tools. [`pain001-mcp`](/pain001-mcp/) exposes 17 payment tools to any MCP client, locally over stdio.

**LSP — Language Server Protocol.** The editor-integration standard behind IDE diagnostics. [`pain001-lsp`](/pain001-lsp/) uses it to validate payment files as you type.

**SBOM.** Software Bill of Materials — a machine-readable inventory of every dependency in a release, generated in CycloneDX format for Pain001 core releases.

---

Something missing? [Suggest a term](https://github.com/sebastienrousseau/pain001/issues) — this glossary grows with the questions people actually ask.
