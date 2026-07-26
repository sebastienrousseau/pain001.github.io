---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A legacy SWIFT MT101 message beside its regenerated ISO 20022 pain.001 XML — the migration path for the November 2026 interbank relay decommission."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Parse legacy SWIFT MT101 messages into records that pass pain.001.001.09 validation — full field-mapping table, strict error handling, ready for the 14 Nov 2026 relay cutover."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pain001-loader-mt101/"
image_alt: "A legacy SWIFT MT101 message beside its regenerated ISO 20022 pain.001 XML — the migration path for the November 2026 interbank relay decommission."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "MT101 to pain.001, MT101 mapping, SWIFT MT101 converter, MT101 decommission 2026, request for transfer, MT-MX migration, pain.001.001.09"
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
permalink: "https://pain001.com/pain001-loader-mt101/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "One function that parses legacy SWIFT MT101 into records that pass pain.001.001.09 validation — ready for the 14 November 2026 relay cutover."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "MT101 to pain.001 Conversion: pain001-loader-mt101"
url: "https://pain001.com/pain001-loader-mt101/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-loader-mt101/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Parse legacy SWIFT MT101 messages into records that pass pain.001.001.09 validation — full field-mapping table, strict error handling, ready for the 14 Nov 2026 relay cutover."
item_guid: "https://pain001.com/pain001-loader-mt101/rss.xml"
item_link: "https://pain001.com/pain001-loader-mt101/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "MT101 to pain.001 Conversion: pain001-loader-mt101"
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
apple-mobile-web-app-title: "MT101 to pain.001 Conversion: pain001-loader-mt101"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Parse legacy SWIFT MT101 messages into records that pass pain.001.001.09 validation — full field-mapping table, strict error handling, ready for the 14 Nov 2026 relay cutover."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "MT101 to pain.001 Conversion: pain001-loader-mt101"
twitter_url: "https://pain001.com/pain001-loader-mt101/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Legacy migration"
excerpt: "pain001-loader-mt101 bridges legacy SWIFT MT101 Request for Transfer messages and modern ISO 20022 pain.001 XML. It maps every supported field tag with published semantics, refuses to guess on out-of-scope instruction codes, raises precise errors on malformed input, and hands its records to the same validation pipeline as every other Pain001 input."
last_reviewed: "2026-07-26"

---

**`pain001-loader-mt101` v0.0.2** parses legacy SWIFT MT101 (Request for Transfer) messages into flat records that pass `pain.001.001.09` validation. One function, zero third-party dependencies, 100% branch-covered.

SWIFT retired the MT category 1, 2 and 9 payment messages on the FIN network for cross-border payment instructions in November 2025. Treasury systems, however, still hold years of MT101 templates, archives, and file-based bank integrations. This loader is the bridge: parse the MT, regenerate as MX, validate against the official XSD, move on.

---

## 01. One function

```python
from pain001_loader_mt101 import parse_mt101

records = parse_mt101(mt101_text)   # one dict per Sequence B transaction
```

The output is shaped for `pain.001.001.09` and passes the core library's `SchemaValidator` unchanged. The MCP server exposes the same capability to AI agents as the `convert_mt101` tool.

---

## 02. Field mapping reference

| MT101 tag | Meaning | pain.001 field |
| :--- | :--- | :--- |
| `:20:` (Seq A) | Sender's reference | `id`, `payment_information_id` |
| `:30:` (Seq A) | Requested execution date (YYMMDD) | `date`, `requested_execution_date` |
| `:21:` (Seq B) | Transaction reference | `payment_id` |
| `:32B:` | Currency + amount | `currency`, `payment_amount` |
| `:50H:` `:50G:` `:50F:` `:50K:` `:50A:` `:50:` | Ordering customer | `debtor_name`, `debtor_account_IBAN`, `initiator_name` |
| `:52A:` `:52C:` `:52D:` | Account servicing institution | `debtor_agent_BIC` |
| `:57A:` `:57C:` `:57D:` (Seq B) | Account with institution | `creditor_agent_BIC` |
| `:59:` `:59A:` `:59F:` (Seq B) | Beneficiary | `creditor_name`, `creditor_account_IBAN` |
| `:70:` | Remittance information | `remittance_information` (truncated to 140 chars) |
| `:71A:` | Details of charges | `charge_bearer` (`OUR`→`DEBT`, `BEN`→`CRED`, `SHA`→`SHAR`) |

Party tags set in Sequence B override their Sequence A defaults, matching MT101 semantics. A raw `{4:...-}` block-4 envelope is unwrapped automatically; block 1/2/3 headers are ignored. Control fields are synthesised: `nb_of_txs` from the Sequence B count, `ctrl_sum` from the transaction amounts, `payment_method` fixed to `TRF`.

**Deliberately out of scope:** `:23E:`, `:25:`, `:28D:`, `:33B:`, `:36:`, `:21F:`, `:56a:`, `:51A:`, `:77B:`, `:25A:`. Instruction codes, FX and intermediary routing need human judgement; the loader refuses to guess.

---

## 03. Strict where it counts

Malformed input raises `ValueError` with a precise message rather than emitting a half-converted file: missing `:20:` or `:30:`, no Sequence B transactions, a transaction without `:21:` or `:32B:`, or an unnamed beneficiary all stop the conversion. Amounts are re-validated and control sums recomputed downstream by the core library's `decimal.Decimal` pipeline before any XML is written.

---

## FAQ

**Is MT101 actually decommissioned?**

The many-to-one *relay* use of MT101 on SWIFT FIN follows the same retirement path as the rest of the MT payment category; corporate-to-bank channels (SCORE) retain MT for longer, at each bank's discretion. Either way, every receiving bank is now MX-native — regenerating legacy instructions as validated `pain.001` removes a translation dependency you no longer control. See the [2026 migration briefing](/2026-iso20022-migration-trends/).

**Why records instead of direct XML?**

Because conversion without validation is how malformed files reach banks. Records flow through the same JSON Schema → scheme rulebook → XSD pipeline as every other Pain001 input. The XML you get is provably valid, not merely translated.

**Install:**

```bash
pip install pain001 pain001-loader-mt101
```
