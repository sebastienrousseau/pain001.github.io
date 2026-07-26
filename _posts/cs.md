---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Open-source sada v Pythonu generující XSD-validované soubory pain.001 a pain.008 z CSV, Excelu, SQLite, JSON, Parquet nebo SWIFT MT101 — s nástroji MCP pro AI agenty a LSP serverem."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Open-source sada v Pythonu generující XSD-validované soubory pain.001 a pain.008 z CSV, Excelu, SQLite, JSON, Parquet nebo SWIFT MT101 — s nástroji MCP pro AI agenty a LSP serverem."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "cs"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/cs/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, Čeština"
language: "cs"
layout: "page"
locale: "cs_CZ"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/cs/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Open-source sada, která promění vaše platební data ve validované XML ISO 20022 — prokazatelně správné dřív, než je uvidí banka."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — open-source iniciace plateb ISO 20022"
url: "https://pain001.com/cs/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/cs/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Open-source sada v Pythonu generující XSD-validované soubory pain.001 a pain.008 z CSV, Excelu, SQLite, JSON, Parquet nebo SWIFT MT101 — s nástroji MCP pro AI agenty a LSP serverem."
item_guid: "https://pain001.com/cs/rss.xml"
item_link: "https://pain001.com/cs/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — open-source iniciace plateb ISO 20022"
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
apple-mobile-web-app-title: "Pain001 — open-source iniciace plateb ISO 20022"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Open-source sada v Pythonu generující XSD-validované soubory pain.001 a pain.008 z CSV, Excelu, SQLite, JSON, Parquet nebo SWIFT MT101 — s nástroji MCP pro AI agenty a LSP serverem."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — open-source iniciace plateb ISO 20022"
twitter_url: "https://pain001.com/cs/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 česky"
excerpt: "Open-source sada v Pythonu generující XSD-validované soubory pain.001 a pain.008 z CSV, Excelu, SQLite, JSON, Parquet nebo SWIFT MT101 — s nástroji MCP pro AI agenty a LSP serverem."
last_reviewed: "2026-07-26"


---

## Platební soubory, které banka neodmítne

**Pain001** je open-source sada v Pythonu pro iniciaci plateb ISO 20022. Převádí data, která už máte — CSV, Excel, SQLite, JSON, Parquet nebo starší zprávy SWIFT MT101 — na XML `pain.001` (úhrady) a `pain.008` (inkasa), validované oficiálními schématy XSD.

Každý soubor projde třemi vrstvami validace: JSON schéma pro každý záznam (včetně kontroly mod-97 IBAN a struktury BIC), pravidla scheme (SEPA a přeshraniční CBPR+) a závěrečná validace XSD. Kontrolní součty se přepočítávají, nikdy nekopírují. Vše běží lokálně: žádná platební data neopouštějí vaši infrastrukturu.

## Termín 14. listopadu 2026

Po konci koexistence MT–MX 22. listopadu 2025 je dalším termínem **14. listopad 2026**: zcela nestrukturované poštovní adresy budou v platbách CBPR+ odmítány a mezibankovní přenos MT101 nahradí `pain.001` verze 9. Pain001 už dnes generuje strukturované i hybridní adresy — a MT101 převede jedním příkazem.

## Začínáme

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

Kompletní dokumentace je v angličtině: [instalační příručka](/installation/), [technická reference](/documentation/), [demo v prohlížeči](/try/) a [briefing ISO 20022 pro rok 2026](/2026-iso20022-migration-trends/). Jádro má dvojí licenci Apache-2.0 / MIT — volné komerční použití v jakémkoli měřítku.
