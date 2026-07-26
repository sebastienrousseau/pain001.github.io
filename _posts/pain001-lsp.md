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
description: "Language Server Protocol server providing real-time diagnostics, schema validation, and autocomplete for payment JSON authoring in IDEs."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pain001-lsp/"
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
permalink: "https://pain001.com/pain001-lsp/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "ISO 20022 Payment Initiation & Transaction Orchestration Suite"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "pain001-lsp: Language Server Protocol for Payment Authoring"
url: "https://pain001.com/pain001-lsp/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-lsp/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Language Server Protocol server providing real-time diagnostics, schema validation, and autocomplete for payment JSON authoring in IDEs."
item_guid: "https://pain001.com/pain001-lsp/rss.xml"
item_link: "https://pain001.com/pain001-lsp/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain001-lsp: Language Server Protocol for Payment Authoring"
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
apple-mobile-web-app-title: "pain001-lsp: Language Server Protocol for Payment Authoring"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Language Server Protocol server providing real-time diagnostics, schema validation, and autocomplete for payment JSON authoring in IDEs."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain001-lsp: Language Server Protocol for Payment Authoring"
twitter_url: "https://pain001.com/pain001-lsp/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"

---

# pain001-lsp: Language Server Protocol Server

**`pain001-lsp`** brings enterprise Language Server Protocol (LSP) capabilities to payment data authoring. It connects to any LSP-compliant code editor (VS Code, Neovim, Helix, Emacs) to provide instant feedback while authoring payment JSON files.

---

## Features

- **Live Schema Validation**: As-you-type validation against official ISO 20022 message schemas.
- **IBAN & BIC Format Diagnostics**: Highlights invalid IBAN checksums or malformed BIC strings directly in the editor.
- **Field Autocomplete**: IntelliSense completions for all required and optional payment fields with inline documentation.
- **Hover Documentation**: Hover over any field to view XSD definitions, field lengths, and scheme requirements.
- **Quick-Fix Code Actions**: One-click "Add missing required fields" with type-correct placeholders.
- **Document Formatting**: Pretty-prints payment JSON files with 2-space indentation and sanitized charsets.
