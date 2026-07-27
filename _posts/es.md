---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Suite Python de código abierto para generar ficheros pain.001 y pain.008 validados por XSD desde CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con herramientas MCP para agentes de IA y servidor LSP."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Suite Python de código abierto para generar ficheros pain.001 y pain.008 validados por XSD desde CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con herramientas MCP para agentes de IA y servidor LSP."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "es"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/es/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, transferencia SEPA, fichero pain.001, generador XML SEPA, pagos, Python, España"
language: "es"
layout: "page"
locale: "es_ES"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/es/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "La suite de código abierto que convierte sus datos de pago en XML ISO 20022 validado — probado antes de llegar al banco."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — Iniciación de pagos ISO 20022 en código abierto"
url: "https://pain001.com/es/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/es/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Suite Python de código abierto para generar ficheros pain.001 y pain.008 validados por XSD desde CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con herramientas MCP para agentes de IA y servidor LSP."
item_guid: "https://pain001.com/es/rss.xml"
item_link: "https://pain001.com/es/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — Iniciación de pagos ISO 20022 en código abierto"
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
apple-mobile-web-app-title: "Pain001 — Iniciación de pagos ISO 20022 en código abierto"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Suite Python de código abierto para generar ficheros pain.001 y pain.008 validados por XSD desde CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con herramientas MCP para agentes de IA y servidor LSP."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — Iniciación de pagos ISO 20022 en código abierto"
twitter_url: "https://pain001.com/es/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 en español"
excerpt: "Suite Python de código abierto para generar ficheros pain.001 y pain.008 validados por XSD desde CSV, Excel, SQLite, JSON, Parquet o SWIFT MT101 — con herramientas MCP para agentes de IA y servidor LSP."
last_reviewed: "2026-07-26"


---

## Ficheros de pago que su banco no rechazará

**Pain001** es una suite Python de código abierto para la iniciación de pagos ISO 20022. Convierte los datos que ya tiene — CSV, Excel, SQLite, JSON, Parquet o mensajes SWIFT MT101 heredados — en XML `pain.001` (transferencias) y `pain.008` (adeudos domiciliados) validados contra los esquemas XSD oficiales.

Cada fichero pasa tres niveles de validación antes de escribirse: esquema JSON por registro (con verificación mod-97 del IBAN y estructura del BIC), reglamentos de scheme (SEPA SCT, SEPA Inmediato, adeudos Core y B2B, transferencias transfronterizas CBPR+) y validación XSD del documento final. Los totales de control (`NbOfTxs`, `CtrlSum`) se recalculan — nunca se copian de la fuente. Todo se ejecuta en local: ningún dato de pago sale de su infraestructura.

## Pruébelo en su navegador

Valide un lote de ejemplo directamente en su navegador — no se sube nada — y pruebe el resultado contra el esquema XSD oficial: [probar Pain001](/try/). Hay ficheros CSV de ejemplo descargables como plantillas para sus propias exportaciones.

## La fecha límite del 14 de noviembre de 2026

Desde el fin de la coexistencia MT–MX el 22 de noviembre de 2025, la próxima fecha clave es el **14 de noviembre de 2026**: las direcciones postales totalmente no estructuradas serán rechazadas en los pagos CBPR+, y el relé interbancario MT101 será sustituido por `pain.001` versión 9. Pain001 genera direcciones estructuradas e híbridas hoy mismo — y convierte MT101 con un solo comando.

## Empezar

```bash
pip install pain001
pain001 -t pain.001.001.09 -d pagos.csv -o salida/ --dry-run
```

Para profundizar: [guía de instalación](/installation/), [referencia técnica](/documentation/), [hoja de ruta ISO 20022 hasta 2028](/iso20022-roadmap/), [códigos de rechazo pain.002](/pain002-reason-codes/), [centro de confianza](/trust/) — y el [resumen ejecutivo de una página](/es/executive-brief/), en español. La documentación completa está en inglés. El núcleo tiene doble licencia Apache-2.0 / MIT — uso comercial libre a cualquier escala.
