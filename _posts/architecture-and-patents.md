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
description: "Architectural white paper covering Pain001 zero-trust XML security, monetary precision, streaming performance, and open standards."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/architecture-and-patents/"
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
permalink: "https://pain001.com/architecture-and-patents/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "ISO 20022 Payment Initiation & Transaction Orchestration Suite"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "Enterprise Architecture & Open Protocols White Paper"
url: "https://pain001.com/architecture-and-patents/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/architecture-and-patents/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Architectural white paper covering Pain001 zero-trust XML security, monetary precision, streaming performance, and open standards."
item_guid: "https://pain001.com/architecture-and-patents/rss.xml"
item_link: "https://pain001.com/architecture-and-patents/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Enterprise Architecture & Open Protocols White Paper"
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
apple-mobile-web-app-title: "Enterprise Architecture & Open Protocols White Paper"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Architectural white paper covering Pain001 zero-trust XML security, monetary precision, streaming performance, and open standards."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Enterprise Architecture & Open Protocols White Paper"
twitter_url: "https://pain001.com/architecture-and-patents/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"

---

# Enterprise Architecture & Open Standards White Paper

## 1. Zero-Trust Security & XML Hardening
Pain001 implements an OWASP-compliant zero-trust posture for XML parsing and generation:
- **XXE Protection**: All XML processing is routed through `defusedxml` to block XML External Entity (XXE) injection, entity expansion attacks (Billion Laughs), and external DTD resolution.
- **Input Sanitization**: Control characters and non-ISO 20022 Latin characters are transliterated or stripped prior to XML serialization.

---

## 2. Fixed-Point Monetary Precision
To eliminate binary floating-point representation errors inherent in IEEE 754 floats:
- All financial amounts (`payment_amount`, `instructed_amount`, control totals) are parsed and calculated using Python's `decimal.Decimal`.
- Control totals (`NbOfTxs` and `CtrlSum`) are dynamically computed from validated transaction records, never trusted blindly from raw input sources.
