---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Suite Python open source pour générer des fichiers pain.001 et pain.008 validés par XSD à partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — avec outils MCP pour agents IA et serveur LSP."
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Suite Python open source pour générer des fichiers pain.001 et pain.008 validés par XSD à partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — avec outils MCP pour agents IA et serveur LSP."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "fr"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/fr/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, virement SEPA, fichier pain.001, générateur XML SEPA, paiements, Python, France"
language: "fr"
layout: "page"
locale: "fr_FR"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/fr/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "La suite open source qui transforme vos données de paiement en XML ISO 20022 validé — prouvé conforme avant même d'atteindre votre banque."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — Initiation de paiements ISO 20022 en open source"
url: "https://pain001.com/fr/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/fr/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Suite Python open source pour générer des fichiers pain.001 et pain.008 validés par XSD à partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — avec outils MCP pour agents IA et serveur LSP."
item_guid: "https://pain001.com/fr/rss.xml"
item_link: "https://pain001.com/fr/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — Initiation de paiements ISO 20022 en open source"
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
apple-mobile-web-app-title: "Pain001 — Initiation de paiements ISO 20022 en open source"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Suite Python open source pour générer des fichiers pain.001 et pain.008 validés par XSD à partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — avec outils MCP pour agents IA et serveur LSP."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — Initiation de paiements ISO 20022 en open source"
twitter_url: "https://pain001.com/fr/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 en français"
excerpt: "Suite Python open source pour générer des fichiers pain.001 et pain.008 validés par XSD à partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — avec outils MCP pour agents IA et serveur LSP."
last_reviewed: "2026-07-26"


---

## Des fichiers de paiement que votre banque n'aura pas à rejeter

**Pain001** est une suite Python open source pour l'initiation de paiements ISO 20022. Elle convertit les données que vous avez déjà — CSV, Excel, SQLite, JSON, Parquet, ou messages SWIFT MT101 hérités — en XML `pain.001` (virements) et `pain.008` (prélèvements) validés par les schémas XSD officiels.

Chaque fichier passe trois niveaux de validation avant d'être écrit : schéma JSON par enregistrement (avec contrôle mod-97 des IBAN et structure des BIC), règles de scheme (SEPA SCT, SEPA Instantané, prélèvement Core et B2B, virements transfrontaliers CBPR+), puis validation XSD du document final. Les totaux de contrôle (`NbOfTxs`, `CtrlSum`) sont recalculés — jamais copiés de la source. Tout s'exécute localement : aucune donnée de paiement ne quitte votre infrastructure.

## L'échéance du 14 novembre 2026

Depuis la fin de la coexistence MT–MX le 22 novembre 2025, l'échéance suivante est le **14 novembre 2026** : les adresses postales entièrement non structurées seront rejetées dans les paiements CBPR+, et le relais interbancaire MT101 sera remplacé par `pain.001` version 9. Pain001 gère dès aujourd'hui les adresses structurées et hybrides, et convertit vos MT101 en une commande.

## Démarrer

```bash
pip install pain001
pain001 -t pain.001.001.09 -d paiements.csv -o sortie/ --dry-run
```

La documentation détaillée est en anglais : [guide d'installation](/installation/), [référence technique](/documentation/), [essai dans le navigateur](/try/), et [briefing 2026 sur ISO 20022](/2026-iso20022-migration-trends/). Le cœur est sous double licence Apache-2.0 / MIT — utilisation commerciale libre, à toute échelle.
