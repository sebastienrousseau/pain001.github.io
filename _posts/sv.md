---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Python-svit med öppen källkod som genererar XSD-validerade pain.001- och pain.008-filer från CSV, Excel, SQLite, JSON, Parquet eller SWIFT MT101 — med MCP-verktyg för AI-agenter och LSP-server."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Python-svit med öppen källkod som genererar XSD-validerade pain.001- och pain.008-filer från CSV, Excel, SQLite, JSON, Parquet eller SWIFT MT101 — med MCP-verktyg för AI-agenter och LSP-server."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "sv"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/sv/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, Svenska"
language: "sv"
layout: "page"
locale: "sv_SE"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/sv/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Sviten med öppen källkod som förvandlar dina betalningsdata till validerad ISO 20022-XML — bevisat korrekt innan banken ser den."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — ISO 20022-betalningsinitiering med öppen källkod"
url: "https://pain001.com/sv/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/sv/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Python-svit med öppen källkod som genererar XSD-validerade pain.001- och pain.008-filer från CSV, Excel, SQLite, JSON, Parquet eller SWIFT MT101 — med MCP-verktyg för AI-agenter och LSP-server."
item_guid: "https://pain001.com/sv/rss.xml"
item_link: "https://pain001.com/sv/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — ISO 20022-betalningsinitiering med öppen källkod"
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
apple-mobile-web-app-title: "Pain001 — ISO 20022-betalningsinitiering med öppen källkod"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Python-svit med öppen källkod som genererar XSD-validerade pain.001- och pain.008-filer från CSV, Excel, SQLite, JSON, Parquet eller SWIFT MT101 — med MCP-verktyg för AI-agenter och LSP-server."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — ISO 20022-betalningsinitiering med öppen källkod"
twitter_url: "https://pain001.com/sv/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 på svenska"
excerpt: "Python-svit med öppen källkod som genererar XSD-validerade pain.001- och pain.008-filer från CSV, Excel, SQLite, JSON, Parquet eller SWIFT MT101 — med MCP-verktyg för AI-agenter och LSP-server."
last_reviewed: "2026-07-26"


---

## Betalfiler som din bank inte avvisar

**Pain001** är en Python-svit med öppen källkod för ISO 20022-betalningsinitiering. Den omvandlar data du redan har — CSV, Excel, SQLite, JSON, Parquet eller äldre SWIFT MT101-meddelanden — till `pain.001`- (betalningar) och `pain.008`-XML (autogiro), validerad mot de officiella XSD-schemana.

Varje fil passerar tre valideringsnivåer innan den skrivs: JSON-schema per post (med mod-97-kontroll av IBAN och BIC-struktur), scheme-regler (SEPA och gränsöverskridande CBPR+) samt slutlig XSD-validering. Kontrollsummor räknas om, kopieras aldrig. Allt körs lokalt: inga betalningsdata lämnar din infrastruktur.

## Prova i webbläsaren

Validera en exempelbatch direkt i webbläsaren — inget laddas upp — och bevisa resultatet mot det officiella XSD-schemat: [prova Pain001](/try/). Exempel-CSV-filer kan laddas ner som mallar för egna exporter.

## Deadline 14 november 2026

Sedan MT–MX-samexistensen upphörde den 22 november 2025 är nästa deadline **14 november 2026**: helt ostrukturerade postadresser avvisas i CBPR+-betalningar och det interbankära MT101-reläet ersätts av `pain.001` version 9. Pain001 stödjer strukturerade och hybrida adresser redan i dag — och konverterar MT101 med ett kommando.

## Kom igång

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

Vidare: [installationsguide](/installation/), [teknisk referens](/documentation/), [ISO 20022-färdplan till 2028](/iso20022-roadmap/), [pain.002-avvisningskoder](/pain002-reason-codes/), [förtroendecenter](/trust/) och [ledningssammanfattning](/executive-brief/). Fullständig dokumentation på engelska. Dubbellicens Apache-2.0 / MIT — fri kommersiell användning i valfri skala.
