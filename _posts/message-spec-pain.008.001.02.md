---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Every element of ISO 20022 pain.008.001.02: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Every element of ISO 20022 pain.008.001.02: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/message-spec-pain.008.001.02/"
image_alt: "Every element of ISO 20022 pain.008.001.02: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.008.001.02, ISO 20022, element reference, cardinality, code lists, XML path, message specification, pain.001"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/message-spec-pain.008.001.02/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "All 46 elements of pain.008.001.02 with cardinality, types and code lists, generated from the official ISO schema."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.008.001.02 — complete element reference"
url: "https://pain001.com/message-spec-pain.008.001.02/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/message-spec-pain.008.001.02/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Every element of ISO 20022 pain.008.001.02: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
item_guid: "https://pain001.com/message-spec-pain.008.001.02/"
item_link: "https://pain001.com/message-spec-pain.008.001.02/"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.008.001.02 — complete element reference"
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
apple-mobile-web-app-title: "pain.008.001.02 — complete element reference"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Every element of ISO 20022 pain.008.001.02: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.008.001.02 — complete element reference"
twitter_url: "https://pain001.com/message-spec-pain.008.001.02/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message specification"
excerpt: "Every element of ISO 20022 pain.008.001.02: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
last_reviewed: "2026-07-26"


---

This is the complete element reference for `pain.008.001.02`, generated directly from the official ISO 20022 XSD that Pain001 validates against — not transcribed by hand. Every cardinality, type and code value below can be checked against ISO's own publication.

**46 elements** · **46 required** · **0 types** · **0 code lists**

Cardinality is shown as ISO writes it: `0..1` optional, `1..1` required, `0..*` repeating. Required elements are **bold** — those are the ones whose absence makes the document invalid before any bank sees it.

## CstmrDrctDbtInitn

| Element | Path | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `CstmrDrctDbtInitn` | `CstmrDrctDbtInitn` | **1..1** | `(inline)` |  |

## GrpHdr

*Group Header — one per message*

| Element | Path | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| &nbsp;&nbsp;`GrpHdr` | `CstmrDrctDbtInitn/GrpHdr` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`MsgId` | `CstmrDrctDbtInitn/GrpHdr/MsgId` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`CreDtTm` | `CstmrDrctDbtInitn/GrpHdr/CreDtTm` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`NbOfTxs` | `CstmrDrctDbtInitn/GrpHdr/NbOfTxs` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`CtrlSum` | `CstmrDrctDbtInitn/GrpHdr/CtrlSum` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`InitgPty` | `CstmrDrctDbtInitn/GrpHdr/InitgPty` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Nm` | `CstmrDrctDbtInitn/GrpHdr/InitgPty/Nm` | **1..1** | `xs:string` |  |

## PmtInf

*Payment Information — one per debtor account and execution date*

| Element | Path | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| &nbsp;&nbsp;`PmtInf` | `CstmrDrctDbtInitn/PmtInf` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`PmtInfId` | `CstmrDrctDbtInitn/PmtInf/PmtInfId` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`PmtMtd` | `CstmrDrctDbtInitn/PmtInf/PmtMtd` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`BtchBookg` | `CstmrDrctDbtInitn/PmtInf/BtchBookg` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`NbOfTxs` | `CstmrDrctDbtInitn/PmtInf/NbOfTxs` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`CtrlSum` | `CstmrDrctDbtInitn/PmtInf/CtrlSum` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`PmtTpInf` | `CstmrDrctDbtInitn/PmtInf/PmtTpInf` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`SvcLvl` | `CstmrDrctDbtInitn/PmtInf/PmtTpInf/SvcLvl` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`ReqdColltnDt` | `CstmrDrctDbtInitn/PmtInf/ReqdColltnDt` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`Cdtr` | `CstmrDrctDbtInitn/PmtInf/Cdtr` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Nm` | `CstmrDrctDbtInitn/PmtInf/Cdtr/Nm` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`CdtrAcct` | `CstmrDrctDbtInitn/PmtInf/CdtrAcct` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Id` | `CstmrDrctDbtInitn/PmtInf/CdtrAcct/Id` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`CdtrAgt` | `CstmrDrctDbtInitn/PmtInf/CdtrAgt` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FinInstnId` | `CstmrDrctDbtInitn/PmtInf/CdtrAgt/FinInstnId` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`ChrgBr` | `CstmrDrctDbtInitn/PmtInf/ChrgBr` | **1..1** | `xs:string` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`DrctDbtTxInf` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf` | **1..*** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PmtId` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf/PmtId` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`InstdAmt` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf/InstdAmt` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`DrctDbtTx` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf/DrctDbtTx` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`DbtrAgt` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf/DbtrAgt` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Dbtr` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf/Dbtr` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`DbtrAcct` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf/DbtrAcct` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`RmtInf` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf/RmtInf` | **1..1** | `(inline)` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`SeqTp` | `CstmrDrctDbtInitn/PmtInf/DrctDbtTxInf/SeqTp` | **1..1** | `xs:string` |  |

*13 further nested elements sit below this depth — every one of them is defined in the type reference below, which lists each type once instead of repeating it under every party.*

## Generate and validate this version

```bash
pain001 -t pain.008.001.02 -d payments.csv -o out/ --dry-run
```

See the [compatibility matrix](/compatibility/) for supported input formats and gates.
