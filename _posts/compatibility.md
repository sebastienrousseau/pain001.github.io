---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A compatibility matrix listing every ISO 20022 message version, input format, and scheme rulebook the Pain001 suite supports."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Exactly what Pain001 supports: every message definition with generate/validate/migrate coverage, input formats, scheme rulebooks, address models, and the known limitations — verified against the shipped code."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/compatibility/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001 compatibility, pain.001 versions supported, pain.008 support, input formats, SEPA schemes, MT101 fields, supported message definitions"
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
permalink: "https://pain001.com/compatibility/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The exact support surface — message versions, formats, schemes, and the limitations — verified against shipped code, not marketing."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Compatibility Matrix"
url: "https://pain001.com/compatibility/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/compatibility/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Exactly what Pain001 supports: every message definition with generate/validate/migrate coverage, input formats, scheme rulebooks, address models, and the known limitations — verified against the shipped code."
item_guid: "https://pain001.com/compatibility/rss.xml"
item_link: "https://pain001.com/compatibility/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Compatibility Matrix"
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
apple-mobile-web-app-title: "Compatibility Matrix"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Exactly what Pain001 supports: every message definition with generate/validate/migrate coverage, input formats, scheme rulebooks, address models, and the known limitations — verified against the shipped code."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Compatibility Matrix"
twitter_url: "https://pain001.com/compatibility/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Compatibility"
excerpt: "Pain001's compatibility matrix: eleven message definitions with per-capability coverage for generation, validation, and migration; seven input formats and their gates; five scheme rulebooks; structured and hybrid address support; response-side parsers; and the known limitations stated as plainly as the capabilities."
last_reviewed: "2026-07-26"


---

Everything on this page is verified against the shipped code of **pain001 v0.0.56** and its companions — the same discipline as the [technical reference](/documentation/). If a cell says no, that is a statement, not an omission.

## 01. Message definitions

| Message definition | Generate | XSD-validate | Migrate to/from | Notes |
| :--- | :--- | :--- | :--- | :--- |
| pain.001.001.03 | Yes | Yes | Yes | SEPA/CGI workhorse; `<BIC>` element naming |
| pain.001.001.04 – .08 | Yes | Yes | Yes | Channel-specific maintenance versions |
| pain.001.001.09 | Yes | Yes | Yes | CBPR+ version; MT101-relay successor; `<BICFI>` |
| pain.001.001.10 – .12 | Yes | Yes | Yes | Post-2019 refinements |
| pain.008.001.02 | Yes | Yes | — | The only pain.008 version supported — others are not |
| pain.002 (responses) | No | — | — | **Parsed**, not generated-for-submission: status/reason extraction |
| camt.053 (statements) | No | — | — | **Parsed** for reconciliation |

## 02. Input formats

| Format | Support | Gate |
| :--- | :--- | :--- |
| CSV | Built-in | Field-alias normalisation, JSON Schema per record |
| JSON / JSONL | Built-in | Same pipeline |
| SQLite (`.db`/`.sqlite`) | Built-in | Table `pain001` by default |
| Parquet | `pain001[parquet]` extra | PyArrow |
| PGP-encrypted (`.gpg`/`.asc`) | `pain001[gpg]` extra | Decrypted in-process |
| Excel `.xlsx`/`.xlsm` | [`pain001-loader-xlsx`](/pain001-loader-xlsx/) | IBAN safety guard; formulas resolve, macros never execute; `.xls` (legacy BIFF) **not** supported |
| SWIFT MT101 | [`pain001-loader-mt101`](/pain001-loader-mt101/) | Sequence A/B field map published; out-of-scope tags refuse rather than guess |

## 03. Scheme rulebooks

`sepa-sct` (SEPA Credit Transfer) · `sepa-inst` (SEPA Instant) · `sepa-sdd` (SEPA Direct Debit Core) · `sepa-b2b` (SEPA B2B) · `xborder-ct` (cross-border credit transfer). Each supports `--explain` rule-by-rule output. Bank-*specific* profile packs beyond these five do not exist yet — that is the roadmap's rule-pack architecture, not a shipped feature.

## 04. Address models

Structured and hybrid postal address elements are generated today, meeting the [14 November 2026 CBPR+ requirement](/iso20022-roadmap/). Unstructured `AdrLine` output remains available for channels that still accept it.

## 05. Known limitations

- **No bank connectivity** — Pain001 stops at the validated file; submission is your channel (by design — see [scope](/competitors-comparison/)).
- **pain.008 is one version** — `.001.02` only.
- **MT101 loader excludes** `:23E:`, `:25:`, `:28D:`, `:33B:`, `:36:`, `:21F:`, `:56a:`, `:51A:`, `:77B:`, `:25A:` — instruction codes and FX routing need human judgement.
- **Streaming semantics** — `--streaming` emits one independently valid file per chunk with recomputed totals, not a single monolithic document.
- **Python 3.10–3.12** — nothing newer is CI-tested yet.
- **The browser demo** implements the fail-fast layer plus the official XSD gate for v09; the full JSON-Schema/rulebook pipeline is CLI-side.

Corrections welcome — this page follows the [corrections policy](/governance/#corrections-and-editorial-policy).
