---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Suite Python open source per generare file pain.001 e pain.008 validati XSD da CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con strumenti MCP per agenti IA e server LSP."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Suite Python open source per generare file pain.001 e pain.008 validati XSD da CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con strumenti MCP per agenti IA e server LSP."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "it"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/it/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, Italiano"
language: "it"
layout: "page"
locale: "it_IT"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/it/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "La suite open source che trasforma i vostri dati di pagamento in XML ISO 20022 validato — verificato prima di raggiungere la banca."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — Iniziazione di pagamenti ISO 20022 open source"
url: "https://pain001.com/it/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/it/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Suite Python open source per generare file pain.001 e pain.008 validati XSD da CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con strumenti MCP per agenti IA e server LSP."
item_guid: "https://pain001.com/it/rss.xml"
item_link: "https://pain001.com/it/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — Iniziazione di pagamenti ISO 20022 open source"
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
apple-mobile-web-app-title: "Pain001 — Iniziazione di pagamenti ISO 20022 open source"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Suite Python open source per generare file pain.001 e pain.008 validati XSD da CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con strumenti MCP per agenti IA e server LSP."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — Iniziazione di pagamenti ISO 20022 open source"
twitter_url: "https://pain001.com/it/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 in italiano"
excerpt: "Suite Python open source per generare file pain.001 e pain.008 validati XSD da CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con strumenti MCP per agenti IA e server LSP."
last_reviewed: "2026-07-26"


---

## File di pagamento che la vostra banca non respingerà

**Pain001** è una suite Python open source per l'iniziazione di pagamenti ISO 20022. Converte i dati che avete già — CSV, Excel, SQLite, JSON, Parquet o messaggi SWIFT MT101 — in XML `pain.001` (bonifici) e `pain.008` (addebiti diretti), validati con gli schemi XSD ufficiali.

Ogni file supera tre livelli di validazione prima di essere scritto: schema JSON per record (con verifica mod-97 dell'IBAN e struttura del BIC), regole di scheme (SEPA e CBPR+ transfrontaliero) e validazione XSD finale. I totali di controllo vengono ricalcolati, mai copiati. Tutto gira in locale: nessun dato di pagamento lascia la vostra infrastruttura.

## Provalo nel browser

Validate un lotto di esempio direttamente nel browser — nulla viene caricato — e provate il risultato con lo schema XSD ufficiale: [provare Pain001](/try/). File CSV di esempio sono scaricabili come modelli per le vostre esportazioni.

## La scadenza del 14 novembre 2026

Dopo la fine della coesistenza MT–MX il 22 novembre 2025, la prossima scadenza è il **14 novembre 2026**: gli indirizzi postali interamente non strutturati saranno respinti nei pagamenti CBPR+ e il relay interbancario MT101 sarà sostituito da `pain.001` versione 9. Pain001 genera già oggi indirizzi strutturati e ibridi — e converte MT101 con un solo comando.

## Per iniziare

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

Per approfondire: [guida all'installazione](/installation/), [riferimento tecnico](/documentation/), [roadmap ISO 20022 fino al 2028](/iso20022-roadmap/), [codici di rifiuto pain.002](/pain002-reason-codes/), [centro fiducia](/trust/) e [sintesi per dirigenti](/executive-brief/). La documentazione completa è in inglese. Doppia licenza Apache-2.0 / MIT — uso commerciale libero su qualsiasi scala.
