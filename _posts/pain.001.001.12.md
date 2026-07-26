---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "The ISO 20022 pain.001.001.12 message structure — group header, payment information, and credit transfer transaction blocks rendered as validated XML."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "pain.001.001.12 — the newest supported version. Element structure, version-specific notes, generation and inspection commands, and lossless migration to other versions with Pain001."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pain.001.001.12/"
image_alt: "The ISO 20022 pain.001.001.12 message structure — group header, payment information, and credit transfer transaction blocks rendered as validated XML."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain.001.001.12, pain.001.001.12 XSD, pain.001.001.12 example, customer credit transfer initiation, pain.001 versions, ISO 20022 message version"
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
permalink: "https://pain001.com/pain.001.001.12/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "pain.001.001.12 — the newest version Pain001 supports. Element structure, version notes, and lossless migration."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.001.001.12 Reference: Generate and Validate"
url: "https://pain001.com/pain.001.001.12/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain.001.001.12/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "pain.001.001.12 — the newest supported version. Element structure, version-specific notes, generation and inspection commands, and lossless migration to other versions with Pain001."
item_guid: "https://pain001.com/pain.001.001.12/rss.xml"
item_link: "https://pain001.com/pain.001.001.12/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.001.001.12 Reference: Generate and Validate"
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
apple-mobile-web-app-title: "pain.001.001.12 Reference: Generate and Validate"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "pain.001.001.12 — the newest supported version. Element structure, version-specific notes, generation and inspection commands, and lossless migration to other versions with Pain001."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.001.001.12 Reference: Generate and Validate"
twitter_url: "https://pain001.com/pain.001.001.12/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message reference"
excerpt: "The reference page for pain.001.001.12, the newest version Pain001 supports: what distinguishes this Customer Credit Transfer Initiation version, the shared GrpHdr/PmtInf/CdtTrfTxInf element skeleton, generation and inspection commands, and how Pain001's VersionMapper migrates records to and from any of the ten supported pain.001 versions."
last_reviewed: "2026-07-26"

---

`pain.001.001.12` is the most recent Customer Credit Transfer Initiation version bundled with Pain001. It represents the current edge of the standard — ahead of most bank channel adoption, and exactly where forward-looking format work happens.

## What to know about this version

- Ideal for future-proofing internal formats: generate `.12` internally, down-convert per bank with `migrate_records`.
- As with every version, the official XSD is the acceptance gate — nothing unvalidated is written.

## Element structure (all versions share this skeleton)

- **`<GrpHdr>` Group Header** — message id, creation timestamp, `NbOfTxs`, `CtrlSum`, initiating party. Pain001 recomputes the control totals from validated records.
- **`<PmtInf>` Payment Information** — debtor, debtor account and agent, requested execution date, payment method, charge bearer; one block can carry many transactions.
- **`<CdtTrfTxInf>` Credit Transfer Transaction** — amount and currency, creditor, creditor account and agent, remittance information, end-to-end reference.

## Generate and inspect

```bash
pain001 init pain.001.001.12 -o work/         # scaffold a starter CSV
pain001 inspect pain.001.001.12               # list required + optional fields
pain001 -t pain.001.001.12 -d payments.csv -o out/ --dry-run
```

Records migrate losslessly between supported versions:

```python
from pain001.migration import VersionMapper
records_v9 = VersionMapper("pain.001.001.12", "pain.001.001.09").migrate(records)
```

See the full [version catalogue](/documentation/), or the [glossary](/glossary/) for the vocabulary used here.
