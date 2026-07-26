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
description: "Convert legacy SWIFT MT101 Request for Transfer messages into schema-validated pain.001.001.09 ISO 20022 payment files."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pain001-loader-mt101/"
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
permalink: "https://pain001.com/pain001-loader-mt101/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "ISO 20022 Payment Initiation & Transaction Orchestration Suite"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "pain001-loader-mt101: SWIFT MT101 to pain.001 Bridge"
url: "https://pain001.com/pain001-loader-mt101/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-loader-mt101/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Convert legacy SWIFT MT101 Request for Transfer messages into schema-validated pain.001.001.09 ISO 20022 payment files."
item_guid: "https://pain001.com/pain001-loader-mt101/rss.xml"
item_link: "https://pain001.com/pain001-loader-mt101/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain001-loader-mt101: SWIFT MT101 to pain.001 Bridge"
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
apple-mobile-web-app-title: "pain001-loader-mt101: SWIFT MT101 to pain.001 Bridge"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Convert legacy SWIFT MT101 Request for Transfer messages into schema-validated pain.001.001.09 ISO 20022 payment files."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain001-loader-mt101: SWIFT MT101 to pain.001 Bridge"
twitter_url: "https://pain001.com/pain001-loader-mt101/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"

---

# pain001-loader-mt101: SWIFT MT101 Converter

**`pain001-loader-mt101`** is a focused companion loader that bridges the gap between legacy SWIFT MT101 messages and modern ISO 20022 `pain.001` XML.

As SWIFT completes its CBPR+ MT-MX migration, banks and corporate treasury management systems (TMS) are phasing out MT101. This loader parses MT101 text streams and produces flat records ready for `pain001` validation and XML generation.

---

## Key Features

- **Sequence A/B Parsing**: Correctly maps global header tags (Sequence A) and repeating transaction blocks (Sequence B).
- **Field Tag Mapping**: Maps `:20:`, `:21R:`, `:32B:`, `:50H:`, `:52A:`, `:57A:`, `:59:`, `:70:`, `:71A:` directly into `pain.001.001.09` keys.
- **Validation Proof**: Parsed records pass `SchemaValidator("pain.001.001.09").validate_batch(...)` with zero errors.
