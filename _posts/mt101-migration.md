---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "SWIFT ended MT and MX coexistence in November 2025. Keep the MT101 your systems already emit, parse it into validated records with pain001-loader-mt101, and produce pain.001 XML proven clean before submission."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-09-18T08:00:00+00:00"
description: "SWIFT ended MT and MX coexistence in November 2025. Keep the MT101 your systems already emit, parse it into validated records with pain001-loader-mt101, and produce pain.001 XML proven clean before submission."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/mt101-migration/"
image_alt: "SWIFT ended MT and MX coexistence in November 2025. Keep the MT101 your systems already emit, parse it into validated records with pain001-loader-mt101, and produce pain.001 XML proven clean before submission."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "MT101 migration, MT101 to pain.001, MT to MX migration, SWIFT MT101 converter, ISO 20022 cross-border payments, request for transfer, pain001"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/mt101-migration/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Keep the MT101 your systems already produce; validate it into ISO 20022 pain.001 instead of rewriting every export."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "MT101 to pain.001: the migration path"
url: "https://pain001.com/mt101-migration/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/mt101-migration/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "SWIFT ended MT and MX coexistence in November 2025. Keep the MT101 your systems already emit, parse it into validated records with pain001-loader-mt101, and produce pain.001 XML proven clean before submission."
item_guid: "https://pain001.com/mt101-migration/"
item_link: "https://pain001.com/mt101-migration/"
item_pub_date: "Fri, 18 Sep 2026 08:00:00 +0000"
item_title: "MT101 to pain.001: the migration path"
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
apple-mobile-web-app-title: "MT101 to pain.001: the migration path"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "SWIFT ended MT and MX coexistence in November 2025. Keep the MT101 your systems already emit, parse it into validated records with pain001-loader-mt101, and produce pain.001 XML proven clean before submission."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "MT101 to pain.001: the migration path"
twitter_url: "https://pain001.com/mt101-migration/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Migration case"
excerpt: "SWIFT ended MT and MX coexistence in November 2025. Keep the MT101 your systems already emit, parse it into validated records with pain001-loader-mt101, and produce pain.001 XML proven clean before submission."
last_reviewed: "2026-07-26"


---

SWIFT ended MT and MX coexistence for cross-border payment instructions on the FIN network on 22 November 2025. The MT101 templates did not go anywhere: they sit in treasury workstations, ERP export jobs and bank-portal integrations that were built around them for twenty years. Every one of those systems now has to produce an ISO 20022 `pain.001` the bank will accept, and the [Swift Standards Release 2026](https://www.swift.com/standards/iso-20022) adds structured-address requirements on top.

There are two ways to get there. Rewrite each export so it emits `pain.001` directly, and re-test every field mapping by hand. Or keep the MT101 the system already emits, parse it into the flat records `pain001` validates, and let the same pipeline that checks every other input produce the XML. The second path is what `pain001-loader-mt101` is for.

## What the loader does

One function. `parse_mt101(text)` takes an MT101 message, with or without its `{4:...-}` block envelope, and returns one record per Sequence B transaction. The record keys are exactly the ones `pain001` validates against the `pain.001.001.09` JSON Schema, so the output passes `SchemaValidator` unchanged and flows through the scheme rulebook and the official XSD like any CSV batch.

```python
from pain001_loader_mt101 import parse_mt101

records = parse_mt101(mt101_text)   # one dict per transaction
```

The [field-mapping table](/pain001-loader-mt101/#02-field-mapping-reference) covers the mandatory and common-denominator tags: `:20:`, `:30:`, `:21:`, `:32B:`, the `:50a:`, `:52a:`, `:57a:` and `:59a:` party options, `:70:` remittance and `:71A:` charges. Sequence B overrides Sequence A, as the standard says. Tags that need human judgement, such as instruction codes, FX and intermediary routing, are deliberately out of scope and documented as such, so a file never leaves the loader half-converted: malformed input raises a precise error instead.

AI agents get the same capability as the `convert_mt101` tool in the [MCP server](/pain001-mcp/).

## Why records, not XML

Because conversion without validation is how malformed files reach banks. A converter that writes XML directly has to be trusted twice: once for the mapping and once for the output. Records go through the three layers every `pain001` input goes through, the JSON Schema, the rail rulebook and the official XSD, and the XML you get is proven clean before submission. That is the property the [example corpus](/example-corpus/) documents for 42 scenarios, with provenance.

## The migration in three steps

1. **Install both packages** (Python 3.10 or later, no other dependency):

   ```bash
   pip install pain001 pain001-loader-mt101
   ```

2. **Parse the MT101 you already produce**, keep the records, and generate the XML with `pain001` for the edition and rail your bank names. The records are plain dictionaries, so the fields MT101 does not carry and the schema requires, which the loader synthesises with documented defaults, can be set from your own master data before generation.

3. **Prove it before the first live file.** Run the result through the [browser demo](/try/?sample=corpus:gb.international.usd), which executes the real library in your browser and shows the three verdicts and the ISO 20022 JSON twin; nothing leaves your machine. The cross-border scenario loaded by that link is the shape most MT101 traffic takes.

## When to ask for help

The loader covers the public MT101 grammar. Your bank's usage guideline for `pain.001`, the elements it insists on and the ones it rejects, is a private document, and it is applied privately with the library's overlay tooling. If you want that derivation done for you, or a supported release channel while the migration runs, the [enterprise page](/enterprise/) describes both. The software stays free either way.

[Loader reference](/pain001-loader-mt101/) · [Technical reference](/documentation/) · [Example corpus](/example-corpus/)
