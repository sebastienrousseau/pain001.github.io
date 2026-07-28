---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Open-source Python-suite voor XSD-gevalideerde pain.001- en pain.008-bestanden uit CSV, Excel, SQLite, JSON, Parquet of SWIFT MT101 — met MCP-tools voor AI-agenten en een LSP-server."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Open-source Python-suite voor XSD-gevalideerde pain.001- en pain.008-bestanden uit CSV, Excel, SQLite, JSON, Parquet of SWIFT MT101 — met MCP-tools voor AI-agenten en een LSP-server."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "nl"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/nl/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, Nederlands"
language: "nl"
layout: "page"
locale: "nl_NL"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/nl/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "De open-source suite die uw betaalgegevens omzet in gevalideerde ISO 20022-XML — aantoonbaar correct vóór de bank het ziet."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — Open-source ISO 20022-betalingsinitiatie"
url: "https://pain001.com/nl/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/nl/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Open-source Python-suite voor XSD-gevalideerde pain.001- en pain.008-bestanden uit CSV, Excel, SQLite, JSON, Parquet of SWIFT MT101 — met MCP-tools voor AI-agenten en een LSP-server."
item_guid: "https://pain001.com/nl/rss.xml"
item_link: "https://pain001.com/nl/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — Open-source ISO 20022-betalingsinitiatie"
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
apple-mobile-web-app-title: "Pain001 — Open-source ISO 20022-betalingsinitiatie"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Open-source Python-suite voor XSD-gevalideerde pain.001- en pain.008-bestanden uit CSV, Excel, SQLite, JSON, Parquet of SWIFT MT101 — met MCP-tools voor AI-agenten en een LSP-server."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — Open-source ISO 20022-betalingsinitiatie"
twitter_url: "https://pain001.com/nl/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 in het Nederlands"
excerpt: "Open-source Python-suite voor XSD-gevalideerde pain.001- en pain.008-bestanden uit CSV, Excel, SQLite, JSON, Parquet of SWIFT MT101 — met MCP-tools voor AI-agenten en een LSP-server."
last_reviewed: "2026-07-26"


---

## Ontdek fouten in betaalbestanden voordat uw bank dat doet

**Pain001** is een open-source Python-suite voor ISO 20022-betalingsinitiatie. Ze zet de gegevens die u al heeft — CSV, Excel, SQLite, JSON, Parquet of oude SWIFT MT101-berichten — om in `pain.001`- (overboekingen) en `pain.008`-XML (incasso's), gevalideerd tegen de officiële XSD-schema's.

Elk bestand doorloopt drie validatielagen vóór het wordt weggeschreven: JSON-schema per record (met mod-97-controle van het IBAN en BIC-structuur), scheme-regels (SEPA en grensoverschrijdend CBPR+) en XSD-eindvalidatie. Controletotalen worden herberekend, nooit overgenomen. Alles draait lokaal: geen betaalgegevens verlaten uw infrastructuur.

## Probeer het in uw browser

Valideer een voorbeeldbatch rechtstreeks in uw browser — er wordt niets geüpload — en bewijs het resultaat tegen het officiële XSD-schema: [Pain001 proberen](/try/). Voorbeeld-CSV-bestanden zijn te downloaden als sjablonen voor uw eigen exports.

## De deadline van 14 november 2026

Sinds het einde van de MT–MX-coëxistentie op 22 november 2025 is de volgende deadline **14 november 2026**: volledig ongestructureerde adressen worden in CBPR+-betalingen geweigerd en de interbancaire MT101-relay wordt vervangen door `pain.001` versie 9. Pain001 ondersteunt gestructureerde en hybride adressen vandaag al — en converteert MT101 met één commando.

## Aan de slag

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

Verder lezen: [installatiegids](/installation/), [technische referentie](/documentation/), [ISO 20022-routekaart tot 2028](/iso20022-roadmap/), [pain.002-afwijzingscodes](/pain002-reason-codes/), [Trust Centre](/trust/) en [managementsamenvatting](/executive-brief/). De volledige documentatie is Engels. Dubbele licentie Apache-2.0 / MIT — vrij commercieel gebruik op elke schaal.
