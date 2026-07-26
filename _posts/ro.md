---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Suită Python open source care generează fișiere pain.001 și pain.008 validate XSD din CSV, Excel, SQLite, JSON, Parquet sau SWIFT MT101 — cu instrumente MCP pentru agenți AI și server LSP."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Suită Python open source care generează fișiere pain.001 și pain.008 validate XSD din CSV, Excel, SQLite, JSON, Parquet sau SWIFT MT101 — cu instrumente MCP pentru agenți AI și server LSP."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "ro"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/ro/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, Română"
language: "ro"
layout: "page"
locale: "ro_RO"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/ro/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Suita open source care transformă datele dumneavoastră de plată în XML ISO 20022 validat — verificat înainte să ajungă la bancă."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — Inițierea plăților ISO 20022 în open source"
url: "https://pain001.com/ro/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/ro/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Suită Python open source care generează fișiere pain.001 și pain.008 validate XSD din CSV, Excel, SQLite, JSON, Parquet sau SWIFT MT101 — cu instrumente MCP pentru agenți AI și server LSP."
item_guid: "https://pain001.com/ro/rss.xml"
item_link: "https://pain001.com/ro/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — Inițierea plăților ISO 20022 în open source"
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
apple-mobile-web-app-title: "Pain001 — Inițierea plăților ISO 20022 în open source"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Suită Python open source care generează fișiere pain.001 și pain.008 validate XSD din CSV, Excel, SQLite, JSON, Parquet sau SWIFT MT101 — cu instrumente MCP pentru agenți AI și server LSP."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — Inițierea plăților ISO 20022 în open source"
twitter_url: "https://pain001.com/ro/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 în română"
excerpt: "Suită Python open source care generează fișiere pain.001 și pain.008 validate XSD din CSV, Excel, SQLite, JSON, Parquet sau SWIFT MT101 — cu instrumente MCP pentru agenți AI și server LSP."
last_reviewed: "2026-07-26"


---

## Fișiere de plată pe care banca nu le va respinge

**Pain001** este o suită Python open source pentru inițierea plăților ISO 20022. Convertește datele pe care le aveți deja — CSV, Excel, SQLite, JSON, Parquet sau mesaje SWIFT MT101 — în XML `pain.001` (transferuri) și `pain.008` (debitări directe), validate cu schemele XSD oficiale.

Fiecare fișier trece prin trei niveluri de validare: schema JSON per înregistrare (cu verificarea mod-97 a IBAN-ului și structura BIC), regulile de scheme (SEPA și CBPR+ transfrontalier) și validarea XSD finală. Totalurile de control sunt recalculate, niciodată copiate. Totul rulează local: nicio dată de plată nu părăsește infrastructura dumneavoastră.

## Termenul-limită: 14 noiembrie 2026

După încheierea coexistenței MT–MX la 22 noiembrie 2025, următorul termen este **14 noiembrie 2026**: adresele poștale complet nestructurate vor fi respinse în plățile CBPR+, iar releul interbancar MT101 va fi înlocuit de `pain.001` versiunea 9. Pain001 generează deja adrese structurate și hibride — și convertește MT101 cu o singură comandă.

## Primii pași

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

Documentația completă este în engleză: [ghid de instalare](/installation/), [referință tehnică](/documentation/), [demo în browser](/try/) și [briefingul ISO 20022 pentru 2026](/2026-iso20022-migration-trends/). Nucleul are licență dublă Apache-2.0 / MIT — utilizare comercială liberă la orice scară.
