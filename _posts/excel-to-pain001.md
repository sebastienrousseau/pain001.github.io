---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Read payment batches straight from .xlsx and .xlsm workbooks with pain001-loader-xlsx: no Save As CSV, numeric-IBAN corruption caught at load, one command to a schema-validated pain.001 file."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-09-18T08:00:00+00:00"
description: "Read payment batches straight from .xlsx and .xlsm workbooks with pain001-loader-xlsx: no Save As CSV, numeric-IBAN corruption caught at load, one command to a schema-validated pain.001 file."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/excel-to-pain001/"
image_alt: "Read payment batches straight from .xlsx and .xlsm workbooks with pain001-loader-xlsx: no Save As CSV, numeric-IBAN corruption caught at load, one command to a schema-validated pain.001 file."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "Excel to pain.001, xlsx SEPA XML, Excel payment file ISO 20022, pain001 loader xlsx, spreadsheet to pain.001, treasury payment batch Excel"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/excel-to-pain001/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The spreadsheet is where the batch starts. One command takes it to a bank-ready, schema-validated pain.001 file."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "From Excel to a validated pain.001 file"
url: "https://pain001.com/excel-to-pain001/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/excel-to-pain001/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Read payment batches straight from .xlsx and .xlsm workbooks with pain001-loader-xlsx: no Save As CSV, numeric-IBAN corruption caught at load, one command to a schema-validated pain.001 file."
item_guid: "https://pain001.com/excel-to-pain001/"
item_link: "https://pain001.com/excel-to-pain001/"
item_pub_date: "Fri, 18 Sep 2026 08:00:00 +0000"
item_title: "From Excel to a validated pain.001 file"
last_build_date: "Fri, 18 Sep 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Fri, 18 Sep 2026 08:00:00 +0000"
ttl: 60
type: website
webmaster: contact@pain001.com
apple_mobile_web_app_orientations: portrait
apple_touch_icon_sizes: 192x192
apple-mobile-web-app-capable: yes
apple-mobile-web-app-status-bar-inset: black
apple-mobile-web-app-status-bar-style: black-translucent
apple-mobile-web-app-title: "From Excel to a validated pain.001 file"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Read payment batches straight from .xlsx and .xlsm workbooks with pain001-loader-xlsx: no Save As CSV, numeric-IBAN corruption caught at load, one command to a schema-validated pain.001 file."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "From Excel to a validated pain.001 file"
twitter_url: "https://pain001.com/excel-to-pain001/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "On-ramp"
excerpt: "Read payment batches straight from .xlsx and .xlsm workbooks with pain001-loader-xlsx: no Save As CSV, numeric-IBAN corruption caught at load, one command to a schema-validated pain.001 file."
last_reviewed: "2026-07-26"


---

Most payment batches start life in a spreadsheet. A treasury analyst builds the payroll or the supplier run in Excel, checks it, and then has to get it to the bank as a `pain.001` file. The usual bridge is "Save As CSV", and that is where the damage happens: leading zeros vanish, an IBAN typed into a `General` cell has already been turned into a number, the encoding drifts, and the first sign of any of it is a rejection from the bank days later.

`pain001-loader-xlsx` removes the bridge. Install it, and `pain001` reads the workbook directly.

## One command

```bash
pip install pain001 pain001-loader-xlsx

pain001 -t pain.001.001.09 -d payments.xlsx -o out/
```

The loader registers itself with `pain001` at install time; no configuration, no flag. The first worksheet is the batch, row 1 is the header, every row after it is a payment. Column names are the [flat-record vocabulary](/documentation/) every other `pain001` input uses, so a workbook and a CSV describe the same payment the same way.

## What it protects you from

- **Numeric IBANs.** If any cell in an IBAN column arrives as a number, the load stops with a clear error naming the row. A debtor account that Excel reformatted is exactly the corruption the bank cannot detect and you cannot afford.
- **Formulas and macros.** Formulas resolve to their last-saved values; macros in `.xlsm` files are never executed. The loader reads, it does not run.
- **Large batches.** Workbooks open read-only and stream in fixed-size chunks, so a multi-hundred-thousand-row batch never has to fit in memory.
- **Ambiguity.** One sheet, one batch. A workbook with no sheets or no header row is an error, not an empty file.

After the load, every record goes through the same three checks as any other input: the JSON Schema, the rail rulebook you name (SEPA, Faster Payments, CHAPS, ACH and the rest) and the official XSD. Full IBAN checksum validation happens there, so the type guard at load and the mod-97 check after it are two independent layers.

## Try it before you install anything

The [browser demo](/try/?sample=corpus:de.sepa.sct-salary) runs the real `pain001` library in your browser on a salary batch from the [example corpus](/example-corpus/): the same flat records a workbook produces, validated in three layers, with the ISO 20022 JSON twin beside the XML. Paste your own rows, in the same columns, and break it on purpose; the verdicts are the library's own words. Nothing is uploaded.

## What comes next

When the workbook is the source of truth, the next step is usually to stop retyping it: the same command runs from a scheduler, a [REST API](/documentation/) or an [AI agent](/pain001-mcp/), and the [LSP server](/pain001-lsp/) checks a batch inside the editor before anyone runs anything. If your bank's own guideline needs to be applied on top of the public rulebook, that is [private profile work](/enterprise/), done around the free software rather than inside it.

[Loader reference](/pain001-loader-xlsx/) · [Technical reference](/documentation/) · [Example corpus](/example-corpus/)
