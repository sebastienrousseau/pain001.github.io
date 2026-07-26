---

author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Pain001 ISO 20022 Payment Initiation Suite"
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Direct Excel (.xlsx / .xlsm) loader plugin for Pain001 featuring numeric IBAN leading-zero safety guard and streaming."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pain001-loader-xlsx/"
image_alt: "Logo of Pain001 Suite"
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, payments, SWIFT, SEPA, banking, Python, MCP, LSP"
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
permalink: "https://pain001.com/pain001-loader-xlsx/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "ISO 20022 Payment Initiation & Transaction Orchestration Suite"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "pain001-loader-xlsx: Excel Ingestion with IBAN Protection"
url: "https://pain001.com/pain001-loader-xlsx/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-loader-xlsx/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Direct Excel (.xlsx / .xlsm) loader plugin for Pain001 featuring numeric IBAN leading-zero safety guard and streaming."
item_guid: "https://pain001.com/pain001-loader-xlsx/rss.xml"
item_link: "https://pain001.com/pain001-loader-xlsx/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain001-loader-xlsx: Excel Ingestion with IBAN Protection"
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
apple-mobile-web-app-title: "pain001-loader-xlsx: Excel Ingestion with IBAN Protection"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Direct Excel (.xlsx / .xlsm) loader plugin for Pain001 featuring numeric IBAN leading-zero safety guard and streaming."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain001-loader-xlsx: Excel Ingestion with IBAN Protection"
twitter_url: "https://pain001.com/pain001-loader-xlsx/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"

---

# pain001-loader-xlsx: Direct Excel Ingestion Plugin

**`pain001-loader-xlsx`** teaches `pain001` to read payment data directly from Excel `.xlsx` and `.xlsm` spreadsheets without requiring an intermediate "Save As CSV" export.

---

## The IBAN Safety Guard

Excel silently converts text strings that look like numbers into numeric types, stripping leading zeros (e.g., German IBAN `DE09...` or French account numbers starting with `0`).

`pain001-loader-xlsx` includes an **IBAN Safety Guard**:
- If an IBAN column is formatted as cell type `General`, the loader **refuses execution** and instructs the user to format the column as `Text`.
- Prevents silent data corruption before files are submitted to banking networks.
