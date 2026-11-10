---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Turn your bank's usage guideline into a validated pain001 profile in-house, with the guideline never leaving your network. Free, step by step, with the library's own tooling."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-11-10T08:00:00+00:00"
description: "Turn your bank's usage guideline into a validated pain001 profile in-house, with the guideline never leaving your network. Free, step by step, with the library's own tooling."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/docs/bank-profiles/"
image_alt: "Turn your bank's usage guideline into a validated pain001 profile in-house, with the guideline never leaving your network. Free, step by step, with the library's own tooling."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001 bank profile, bank usage guideline, ISO 20022 overlay, private validation profile, pain.001 bank rules"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/docs/bank-profiles/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Your bank's rules are the third layer. Your team can encode them itself, privately, with the library's tooling."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Build your own bank profile for pain001"
url: "https://pain001.com/docs/bank-profiles/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/docs/bank-profiles/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.75)"
item_description: "Turn your bank's usage guideline into a validated pain001 profile in-house, with the guideline never leaving your network. Free, step by step, with the library's own tooling."
item_guid: "https://pain001.com/docs/bank-profiles/rss.xml"
item_link: "https://pain001.com/docs/bank-profiles/rss.xml"
item_pub_date: "Tue, 10 Nov 2026 08:00:00 +0000"
item_title: "Build your own bank profile for pain001"
last_build_date: "Tue, 10 Nov 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Tue, 10 Nov 2026 08:00:00 +0000"
ttl: 60
type: website
webmaster: contact@pain001.com
apple_mobile_web_app_orientations: portrait
apple_touch_icon_sizes: 192x192
apple-mobile-web-app-capable: yes
apple-mobile-web-app-status-bar-inset: black
apple-mobile-web-app-status-bar-style: black-translucent
apple-mobile-web-app-title: "Build your own bank profile for pain001"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "Turn your bank's usage guideline into a validated pain001 profile in-house, with the guideline never leaving your network. Free, step by step, with the library's own tooling."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "Build your own bank profile for pain001"
twitter_url: "https://pain001.com/docs/bank-profiles/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Bank profiles"
excerpt: "Turn your bank's usage guideline into a validated pain001 profile in-house, with the guideline never leaving your network. Free, step by step, with the library's own tooling."
last_reviewed: "2026-11-10"

---
Pain001 checks two of the four layers that decide whether a bank accepts a file: the ISO 20022 schema and the scheme rulebook. The third is your bank's own **message usage guideline**: which elements it requires, which it ignores and which values it accepts. That guideline is your bank's document, licensed to you, so it never enters the public project. Your team encodes it as a private profile instead, inside your own environment.

## What the library gives you

- An **overlay grammar** that expresses a guideline as a short list of rules: an element that must be present, one that must be absent, a value that must be one of a set.
- `scripts/derive_overlay.py`, which reads a guideline's schema and drafts those rules for you to review.
- The corpus builder, which renders any [example scenario](/example-corpus/) the way your bank wants it, so you can see the profile at work before your own data goes through it.

## The step-by-step guide

The guide, with a template, a validator and worked examples, lives in the core repository: [docs/bank-profiles.md](https://github.com/sebastienrousseau/pain001/blob/main/docs/bank-profiles.md). The [corpus guide](https://github.com/sebastienrousseau/pain001/blob/main/docs/corpus.md) walks through the overlay tooling it builds on.

## What stays private, and what can be shared

Your bank's guideline and the profile derived from it stay in your environment; nothing in the tooling sends them anywhere. A profile built only from public, non-confidential material, such as a scheme's published rulebook, may be contributed to the repository as a pull request.

Questions go to [GitHub Discussions](https://github.com/sebastienrousseau/pain001/discussions).
