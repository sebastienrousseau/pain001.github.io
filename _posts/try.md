---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "An interactive browser demo validating payment records and generating ISO 20022 pain.001 XML entirely client-side."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Upload or paste payment CSV data and watch the validation gate work: IBAN mod-97, BIC structure, required fields, recomputed control totals, and the official XSD. Everything runs in your browser."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "en"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/try/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation, covering the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001 validator online, try pain001, SEPA XML generator online, IBAN checker, pain.001 example, ISO 20022 demo, payment file validator"
language: "en-GB"
layout: "try"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/try/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Drop in a CSV, use the sample, or paste your own records. Validation runs instantly, entirely in your browser, and nothing ever leaves your machine."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Try Pain001 in Your Browser"
url: "https://pain001.com/try/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/try/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.63)"
item_description: "Upload or paste payment CSV data and watch the validation gate work: IBAN mod-97, BIC structure, required fields, recomputed control totals, and the official XSD. Everything runs in your browser."
item_guid: "https://pain001.com/try/rss.xml"
item_link: "https://pain001.com/try/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Try Pain001 in Your Browser"
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
apple-mobile-web-app-title: "Try Pain001 in Your Browser"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "Upload or paste payment CSV data and watch the validation gate work: IBAN mod-97, BIC structure, required fields, recomputed control totals, and the official XSD. Everything runs in your browser."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "Try Pain001 in Your Browser"
twitter_url: "https://pain001.com/try/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Interactive demo"
excerpt: "An in-browser demonstration of the Pain001 validation gate: paste or edit CSV payment records, run IBAN mod-97 and BIC checks with recomputed control totals, and generate pain.001.001.09 XML. The full CLI adds JSON Schema, five scheme rulebooks, and official XSD validation."
last_reviewed: "2026-07-26"


---

## What this demo shows, and what the real pipeline adds

Each sample batch is also [downloadable as a CSV file](/samples/pain001-sample-sepa-sct.csv) to use as the template for your own ERP or spreadsheet export. The header row is the contract.

The demo above runs the pain001 library itself, not an imitation of it: required-field checks, ISO 13616 mod-97 IBAN checksums, ISO 9362 BIC structure, amount and date formats, control totals (`NbOfTxs`, `CtrlSum`) recomputed from the records rather than trusted, the scheme rulebook you choose, and the official XSD gate. Try the "Introduce an error…" menu. Each scenario plants exactly one realistic flaw (a flipped IBAN digit, a malformed BIC, a missing column, a European comma-decimal amount, an impossible date) and shows you the row-level finding a bank's gateway would otherwise report days later.

The installed toolchain adds what a browser tab cannot: files of any size; input from Excel, SQLite, JSON, Parquet and SWIFT MT101; all 29 scheme profiles, including direct debits and purpose-code mandates (the demo offers 16), with rule-by-rule `--explain` output; and every supported edition, eleven `pain.001` versions and two `pain.008` versions (`.02` and `.08`).

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --scheme sepa-sct --dry-run
```

Step 3 re-runs the schema gate on its own, so you can edit the XML above and check it again: [xmlschema](https://pypi.org/project/xmlschema/) against the official `pain.001.001.09` schema, served from this site. It is the same class of XSD gate the CLI applies.
