---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Open-Source-Python-Suite zur Erzeugung XSD-validierter pain.001- und pain.008-Dateien aus CSV, Excel, SQLite, JSON, Parquet oder SWIFT MT101 — mit MCP-Tools für KI-Agenten und LSP-Server."
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Open-Source-Python-Suite zur Erzeugung XSD-validierter pain.001- und pain.008-Dateien aus CSV, Excel, SQLite, JSON, Parquet oder SWIFT MT101 — mit MCP-Tools für KI-Agenten und LSP-Server."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "de"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/de/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, SEPA Überweisung, pain.001 Datei, SEPA XML Generator, Zahlungsverkehr, Python, Deutschland"
language: "de"
layout: "page"
locale: "de_DE"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/de/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Die Open-Source-Suite, die Ihre Zahlungsdaten in validiertes ISO-20022-XML verwandelt — nachweislich korrekt, bevor die Bank es je sieht."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — Open-Source-Zahlungsinitiierung nach ISO 20022"
url: "https://pain001.com/de/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/de/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Open-Source-Python-Suite zur Erzeugung XSD-validierter pain.001- und pain.008-Dateien aus CSV, Excel, SQLite, JSON, Parquet oder SWIFT MT101 — mit MCP-Tools für KI-Agenten und LSP-Server."
item_guid: "https://pain001.com/de/rss.xml"
item_link: "https://pain001.com/de/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — Open-Source-Zahlungsinitiierung nach ISO 20022"
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
apple-mobile-web-app-title: "Pain001 — Open-Source-Zahlungsinitiierung nach ISO 20022"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Open-Source-Python-Suite zur Erzeugung XSD-validierter pain.001- und pain.008-Dateien aus CSV, Excel, SQLite, JSON, Parquet oder SWIFT MT101 — mit MCP-Tools für KI-Agenten und LSP-Server."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — Open-Source-Zahlungsinitiierung nach ISO 20022"
twitter_url: "https://pain001.com/de/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 auf Deutsch"
excerpt: "Open-Source-Python-Suite zur Erzeugung XSD-validierter pain.001- und pain.008-Dateien aus CSV, Excel, SQLite, JSON, Parquet oder SWIFT MT101 — mit MCP-Tools für KI-Agenten und LSP-Server."
last_reviewed: "2026-07-26"


---

## Zahlungsdateien, die Ihre Bank nicht ablehnen wird

**Pain001** ist eine Open-Source-Python-Suite für die ISO-20022-Zahlungsinitiierung. Sie wandelt vorhandene Daten — CSV, Excel, SQLite, JSON, Parquet oder Alt-SWIFT-MT101 — in `pain.001`- (Überweisungen) und `pain.008`-XML (Lastschriften) um, validiert gegen die offiziellen XSD-Schemata.

Jede Datei durchläuft drei Prüfebenen, bevor sie geschrieben wird: JSON-Schema je Datensatz (inklusive IBAN-Prüfziffern nach mod-97 und BIC-Struktur), Scheme-Regelwerke (SEPA SCT, SEPA Instant, Lastschrift Core und B2B, grenzüberschreitende CBPR+-Überweisungen) und abschließende XSD-Validierung. Kontrollsummen (`NbOfTxs`, `CtrlSum`) werden neu berechnet — nie aus der Quelle übernommen. Alles läuft lokal: Keine Zahlungsdaten verlassen Ihre Infrastruktur.

## Der Stichtag 14. November 2026

Seit dem Ende der MT–MX-Koexistenz am 22. November 2025 ist der nächste Stichtag der **14. November 2026**: Vollständig unstrukturierte Postadressen werden in CBPR+-Zahlungen abgelehnt, und das Interbanken-MT101-Relay wird durch `pain.001` Version 9 ersetzt. Pain001 unterstützt strukturierte und hybride Adressen bereits heute — und konvertiert MT101 mit einem Befehl.

## Loslegen

```bash
pip install pain001
pain001 -t pain.001.001.09 -d zahlungen.csv -o ausgabe/ --dry-run
```

Die ausführliche Dokumentation ist auf Englisch: [Installationsanleitung](/installation/), [Technische Referenz](/documentation/), [Browser-Demo](/try/) und [ISO-20022-Briefing 2026](/2026-iso20022-migration-trends/). Der Kern steht unter dualer Apache-2.0-/MIT-Lizenz — freie kommerzielle Nutzung in jedem Umfang.
