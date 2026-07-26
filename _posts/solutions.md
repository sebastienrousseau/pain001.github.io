---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Pain001 explained for four audiences — treasury, CFO and board, payment operations, and engineering — each with its own entry point."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Treasury, CFO and board, payment operations, engineering and AI — the problem in your vocabulary, what Pain001 changes, and your next click, in 150 words per role."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "en"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/solutions/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "ISO 20022 for treasury, payment operations tools, CFO payments compliance, pain.001 for developers, AI agents payments, corporate treasury software"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/solutions/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Four roles, four vocabularies, one pipeline — find your problem, then your next click."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Who Pain001 Is For"
url: "https://pain001.com/solutions/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/solutions/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Treasury, CFO and board, payment operations, engineering and AI — the problem in your vocabulary, what Pain001 changes, and your next click, in 150 words per role."
item_guid: "https://pain001.com/solutions/rss.xml"
item_link: "https://pain001.com/solutions/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Who Pain001 Is For"
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
apple-mobile-web-app-title: "Who Pain001 Is For"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Treasury, CFO and board, payment operations, engineering and AI — the problem in your vocabulary, what Pain001 changes, and your next click, in 150 words per role."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Who Pain001 Is For"
twitter_url: "https://pain001.com/solutions/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Who it's for"
excerpt: "Pain001 mapped to the four people who touch a payment file: treasurers who need files that pass first time, CFOs and boards weighing deadline exposure and cost, payment-operations teams closing the pain.002 loop, and engineers or AI teams integrating the pipeline. Each section states the problem in that role's vocabulary and routes to the right depth."
last_reviewed: "2026-07-26"


---

## Treasury & finance

Your bank rejects files for reasons your ERP never warned you about: a transposed IBAN digit, a control total that no longer matches, an address format that stopped being acceptable. Pain001 makes those failures happen at your desk instead — every file is proven against the bank's official rulebook (ISO 20022 XSD) before submission, and the [payment-lifecycle guide](/payments/) shows where each check sits between origination and reconciliation. Start with the [glossary](/glossary/) if the vocabulary is new; the plain-English definitions were written for your side of the desk, not the engineers'.

## CFO & board

Two numbers frame the decision. **14 November 2026**: the date cross-border payments with unstructured addresses start bouncing at network level — exposure that lives in your customer master data, not your bank connection. **€10,000–30,000 per year**: the public list price of the nearest commercial translation SDK, against Pain001's permanent zero at any scale under open licences. The governance questions — auditability, data locality, supply-chain evidence — are answered with artefacts, not assurances: published [SBOM](/sbom.cdx.json), [security policy](/security.txt), and processing that never leaves your infrastructure. The [one-page executive brief](/executive-brief/) is written to be forwarded.

## Payment operations

You live in the response files. Pain001 closes the loop end to end: `--dry-run` pre-submission checks that pass or fail cleanly in CI, scheme rulebooks (SEPA and cross-border) explained rule by rule, the [pain.002 reason-code reference](/pain002-reason-codes/) for decoding what came back, and parsers that turn bank responses and camt.053 statements into structured data your pipeline can route. The [browser demo](/try/) is the fastest way to see the failure classes it eliminates — including the one-click "introduce an error" scenarios.

## Engineering & AI

A typed Python API, a CLI with meaningful exit codes, a REST microservice, and plugin points for loaders, validators, schemes, and writers — [the technical reference](/documentation/) covers every flag and endpoint, and the code carries 100% line-and-branch coverage as a hard CI gate. If you are building with agents: [pain001-mcp](/pain001-mcp/) is the category's only Model Context Protocol server — seventeen read-only tools your agents call locally, with editor diagnostics from [pain001-lsp](/pain001-lsp/) while humans stay in the loop.
