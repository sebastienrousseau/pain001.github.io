---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "The ISO 20022 pain.001.001.06 message structure — group header, payment information, and credit transfer transaction blocks rendered as validated XML."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "pain.001.001.06 — maintenance release. Element structure, version-specific notes, generation and inspection commands, and version migration with Pain001."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/pain.001.001.06/"
image_alt: "The ISO 20022 pain.001.001.06 message structure — group header, payment information, and credit transfer transaction blocks rendered as validated XML."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001.001.06, pain.001.001.06 XSD, pain.001.001.06 example, customer credit transfer initiation, pain.001 versions, ISO 20022 message version"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/pain.001.001.06/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "pain.001.001.06 — a maintenance release some TMS platforms export. Element structure, version notes, and version migration."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.001.001.06 Reference: Generate and Validate"
url: "https://pain001.com/pain.001.001.06/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain.001.001.06/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "pain.001.001.06 — maintenance release. Element structure, version-specific notes, generation and inspection commands, and version migration with Pain001."
item_guid: "https://pain001.com/pain.001.001.06/rss.xml"
item_link: "https://pain001.com/pain.001.001.06/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.001.001.06 Reference: Generate and Validate"
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
apple-mobile-web-app-title: "pain.001.001.06 Reference: Generate and Validate"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "pain.001.001.06 — maintenance release. Element structure, version-specific notes, generation and inspection commands, and version migration with Pain001."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.001.001.06 Reference: Generate and Validate"
twitter_url: "https://pain001.com/pain.001.001.06/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message reference"
excerpt: "The reference page for pain.001.001.06, a maintenance release some TMS platforms export: what distinguishes this Customer Credit Transfer Initiation version, the shared GrpHdr/PmtInf/CdtTrfTxInf element skeleton, generation and inspection commands, and how Pain001's VersionMapper reshapes records between any of the eleven supported pain.001 versions."
last_reviewed: "2026-07-26"

---

`pain.001.001.06` is a stepping-stone version between the 2009 classic and the 2019 rework. Some treasury management systems export it natively, which is the main reason to generate it.

## What to know about this version

- Supported end-to-end: JSON Schema, Jinja2 template, official XSD, scheme rulebooks.
- Consider `.09` for new integrations unless your channel says otherwise.

## Element structure (all versions share this skeleton)

- **`<GrpHdr>` Group Header** — message id, creation timestamp, `NbOfTxs`, `CtrlSum`, initiating party. Pain001 recomputes the control totals from validated records.
- **`<PmtInf>` Payment Information** — debtor, debtor account and agent, requested execution date, payment method, charge bearer; one block can carry many transactions.
- **`<CdtTrfTxInf>` Credit Transfer Transaction** — amount and currency, creditor, creditor account and agent, remittance information, end-to-end reference.

## Generate and inspect

```bash
pain001 init pain.001.001.06 -o work/         # scaffold a starter CSV
pain001 inspect pain.001.001.06               # list required + optional fields
pain001 -t pain.001.001.06 -d payments.csv -o out/ --dry-run
```

Records can be reshaped between supported versions. The mapper renames and defaults fields to match the target version; elements the target does not model are not carried over, so re-validate after migrating:

```python
from pain001.migration import VersionMapper
rows = VersionMapper().migrate_rows(
    rows, "pain.001.001.06", "pain.001.001.09"
)
```

See the full [version catalogue](/documentation/), or the [glossary](/glossary/) for the vocabulary used here.
