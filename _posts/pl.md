---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Otwartoźródłowy pakiet Python generujący pliki pain.001 i pain.008 zwalidowane XSD z CSV, Excel, SQLite, JSON, Parquet lub SWIFT MT101 — z narzędziami MCP dla agentów AI i serwerem LSP."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Otwartoźródłowy pakiet Python generujący pliki pain.001 i pain.008 zwalidowane XSD z CSV, Excel, SQLite, JSON, Parquet lub SWIFT MT101 — z narzędziami MCP dla agentów AI i serwerem LSP."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "pl"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pl/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, Polski"
language: "pl"
layout: "page"
locale: "pl_PL"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/pl/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Otwartoźródłowy pakiet, który zamienia dane płatnicze w zwalidowany XML ISO 20022 — sprawdzony, zanim trafi do banku."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — inicjowanie płatności ISO 20022 w open source"
url: "https://pain001.com/pl/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pl/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Otwartoźródłowy pakiet Python generujący pliki pain.001 i pain.008 zwalidowane XSD z CSV, Excel, SQLite, JSON, Parquet lub SWIFT MT101 — z narzędziami MCP dla agentów AI i serwerem LSP."
item_guid: "https://pain001.com/pl/rss.xml"
item_link: "https://pain001.com/pl/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — inicjowanie płatności ISO 20022 w open source"
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
apple-mobile-web-app-title: "Pain001 — inicjowanie płatności ISO 20022 w open source"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Otwartoźródłowy pakiet Python generujący pliki pain.001 i pain.008 zwalidowane XSD z CSV, Excel, SQLite, JSON, Parquet lub SWIFT MT101 — z narzędziami MCP dla agentów AI i serwerem LSP."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — inicjowanie płatności ISO 20022 w open source"
twitter_url: "https://pain001.com/pl/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 po polsku"
excerpt: "Otwartoźródłowy pakiet Python generujący pliki pain.001 i pain.008 zwalidowane XSD z CSV, Excel, SQLite, JSON, Parquet lub SWIFT MT101 — z narzędziami MCP dla agentów AI i serwerem LSP."
last_reviewed: "2026-07-26"


---

## Pliki płatności, których bank nie odrzuci

**Pain001** to otwartoźródłowy pakiet Python do inicjowania płatności ISO 20022. Przekształca dane, które już masz — CSV, Excel, SQLite, JSON, Parquet lub komunikaty SWIFT MT101 — w XML `pain.001` (przelewy) i `pain.008` (polecenia zapłaty), walidowany oficjalnymi schematami XSD.

Każdy plik przechodzi trzy poziomy walidacji: schemat JSON dla każdego rekordu (z kontrolą mod-97 IBAN i strukturą BIC), reguły scheme (SEPA i transgraniczne CBPR+) oraz końcową walidację XSD. Sumy kontrolne są przeliczane, nigdy kopiowane. Wszystko działa lokalnie: żadne dane płatnicze nie opuszczają Twojej infrastruktury.

## Wypróbuj w przeglądarce

Zwaliduj przykładową partię bezpośrednio w przeglądarce — nic nie jest przesyłane — i potwierdź wynik oficjalnym schematem XSD: [wypróbuj Pain001](/try/). Przykładowe pliki CSV można pobrać jako szablony własnych eksportów.

## Termin 14 listopada 2026

Po zakończeniu koegzystencji MT–MX 22 listopada 2025 następny termin to **14 listopada 2026**: całkowicie nieustrukturyzowane adresy pocztowe będą odrzucane w płatnościach CBPR+, a międzybankowy przekaz MT101 zostanie zastąpiony przez `pain.001` w wersji 9. Pain001 już dziś generuje adresy ustrukturyzowane i hybrydowe — i konwertuje MT101 jednym poleceniem.

## Jak zacząć

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

Dalej: [instalacja](/installation/), [dokumentacja techniczna](/documentation/), [mapa drogowa ISO 20022 do 2028](/iso20022-roadmap/), [kody odrzuceń pain.002](/pain002-reason-codes/), [centrum zaufania](/trust/) i [streszczenie dla zarządu](/executive-brief/). Pełna dokumentacja po angielsku. Podwójna licencja Apache-2.0 / MIT — darmowe użycie komercyjne w dowolnej skali.
