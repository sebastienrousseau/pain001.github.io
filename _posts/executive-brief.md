---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A one-page executive brief on Pain001 and the ISO 20022 structured-data requirements, formatted for print."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "One page for decision-makers: the rejected-file problem, the structured-address requirement and its new timing, what Pain001 does, what it costs, the safety evidence, and the one ask. Print-ready."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "en"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/executive-brief/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation, covering the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001 executive brief, ISO 20022 executive summary, payments compliance brief, CFO briefing ISO 20022, 2026 deadline briefing"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/executive-brief/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "One page. Five facts. One ask. Also available in French, German, and Spanish, and print-ready from your browser."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 Executive Brief"
url: "https://pain001.com/executive-brief/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/executive-brief/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.63)"
item_description: "One page for decision-makers: the rejected-file problem, the structured-address requirement and its new timing, what Pain001 does, what it costs, the safety evidence, and the one ask. Print-ready."
item_guid: "https://pain001.com/executive-brief/rss.xml"
item_link: "https://pain001.com/executive-brief/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 Executive Brief"
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
apple-mobile-web-app-title: "Pain001 Executive Brief"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "One page for decision-makers: the rejected-file problem, the structured-address requirement and its new timing, what Pain001 does, what it costs, the safety evidence, and the one ask. Print-ready."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "Pain001 Executive Brief"
twitter_url: "https://pain001.com/executive-brief/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Executive brief"
excerpt: "A one-page executive brief on Pain001: why payment files get rejected and what that costs, the structured-address requirement Swift deferred in August 2026, what the suite does, its zero cost against the €10–30k/yr commercial reference, the verifiable safety posture, and the single ask: have your payments team run the 60-second demo."
last_reviewed: "2026-07-26"


---

> **To print or save as PDF:** use your browser's print function (⌘P / Ctrl+P). This page carries a print stylesheet that produces a clean single page, with no navigation, no footer, and links written out in full.

Read in: [Français](/fr/executive-brief/) · [Deutsch](/de/executive-brief/) · [Español](/es/executive-brief/)

## The problem

Banks reject malformed payment files. Every rejection costs a repair cycle; a repair that misses the day's cut-off costs a settlement day. The rejection reasons are knowable in advance, and therefore preventable.

## The deadline

**Deferred, not dropped.** In August 2026 Swift postponed the rule that rejects cross-border payments (CBPR+) with fully unstructured addresses, and the move from interbank MT101 to ISO 20022 `pain.001` version 9. The new timing comes by December 2026. The exposure still sits in customer master data, and dates already set remain: June 2027 (investigations), November 2027 (CHAPS purpose codes), November 2028 (MT statements). Sources: Swift and central banks, cited in full at pain001.com/2026-iso20022-migration-trends.

## What Pain001 does

An open-source suite that converts existing data (spreadsheets, ERP exports, legacy SWIFT files) into bank-ready ISO 20022 payment files, and proves each file against the bank's official rulebook (ISO 20022 XSD) *before* submission. It runs entirely on your own infrastructure: no upload, no vendor cloud, no telemetry.

## What it costs

Nothing, at any scale, under open licences (Apache-2.0 / MIT). Commercial reference point: SWIFT's translation SDK is publicly listed at €10,000–30,000 per year.

Support, an LTS line and private profile work for your bank's guideline are offered separately, without changing the licences: [enterprise page](/enterprise/).

## The evidence

Published dependency inventory (SBOM) · 100% branch-covered code as a CI gate · independently scored supply chain (OpenSSF Scorecard) · WCAG 2.2 AAA accessible documentation · security policy with private disclosure. All verifiable at pain001.com.

## The ask

Have your payments engineering team run the 60-second demo at **pain001.com/try**. It validates a sample batch and proves it against the official ISO 20022 schema, in the browser, with nothing uploaded. If it holds up, the installation guide takes minutes.
