---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "The business case for Pain001 answered as five plain-English questions, each claim linked to verifiable evidence."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "What a rejected payment file costs, why 14 November 2026 is fixed, what Pain001 does about it, what it costs (nothing), and whether it is safe — each answer linked to its proof."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "en"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/why/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "why pain001, ISO 20022 business case, payment file rejected cost, ISO 20022 migration deadline 2026, CBPR+ structured address requirement, pain.001 vs MT101, open source payment software"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/why/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The five questions a CFO actually asks — answered in plain English, every claim linked to its evidence."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Why Pain001: the Business Case in Five Questions"
url: "https://pain001.com/why/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/why/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "What a rejected payment file costs, why 14 November 2026 is fixed, what Pain001 does about it, what it costs (nothing), and whether it is safe — each answer linked to its proof."
item_guid: "https://pain001.com/why/rss.xml"
item_link: "https://pain001.com/why/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Why Pain001: the Business Case in Five Questions"
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
apple-mobile-web-app-title: "Why Pain001: the Business Case in Five Questions"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "What a rejected payment file costs, why 14 November 2026 is fixed, what Pain001 does about it, what it costs (nothing), and whether it is safe — each answer linked to its proof."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Why Pain001: the Business Case in Five Questions"
twitter_url: "https://pain001.com/why/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "The business case"
excerpt: "The executive case for Pain001 in five questions: the operational cost of a rejected payment file, the fixed 14 November 2026 CBPR+ deadline, what the suite does about both, why it costs nothing at any scale against a €10–30k/yr commercial reference point, and the verifiable safety posture — local processing, no telemetry, published SBOM, 100% branch coverage."
last_reviewed: "2026-07-26"


---

## What does a rejected payment file cost?

A file the bank bounces does not fail quietly. Someone diagnoses the reason code, repairs the source data, regenerates, resubmits — and if the repair misses the day's cut-off, settlement slips. For payroll or supplier runs, a slipped day is a phone call you do not want to make. The [reason-code reference](/pain002-reason-codes/) lists what banks actually send back; almost every format-class entry on it is preventable before submission.

## Why is 14 November 2026 non-negotiable?

Because it is enforced at network level, not by policy. From that date, cross-border payments (CBPR+) carrying fully unstructured postal addresses are rejected, and the interbank MT101 relay retires in favour of `pain.001` version 9. The dates come from SWIFT, not from us — every one is cited in the [2026 briefing](/2026-iso20022-migration-trends/), and the schedule continues to 2028 on the [living roadmap](/iso20022-roadmap/).

## What does Pain001 do about it?

Three things. It turns the data you already have — spreadsheets, ERP exports, legacy SWIFT files — into bank-ready ISO 20022 payment files. It proves each file clean before submission: validation against the bank's official rulebook (ISO 20022 XSD), the account-number checksum your bank runs (ISO 13616 mod-97), and control totals recalculated from the records, never trusted. And it does all of this on your own infrastructure — nothing is uploaded anywhere.

## What does it cost?

Nothing, at any scale, permanently. The core is dual-licensed (Apache-2.0 or MIT); companion packages are Apache-2.0. The nearest commercial reference point — SWIFT's translation SDK — is publicly listed at €10,000–30,000 per year before integration effort. The full landscape, including where commercial platforms genuinely win, is in the [comparison](/competitors-comparison/).

## Is it safe?

Check rather than trust: payment data [never leaves your machines](/privacy/), the dependency inventory is a published [SBOM](/sbom.cdx.json), the code holds [100% branch coverage as a CI gate](/architecture-and-patents/), and the [browser demo](/try/) invites your security team to falsify the claims with DevTools open.

## What is the next step?

Watch it work: the [60-second demo](/try/) validates a payment batch and proves it against the official schema, in your browser. Then hand your team the [executive brief](/executive-brief/) — one page, print-ready, available in [French](/fr/executive-brief/), [German](/de/executive-brief/), and [Spanish](/es/executive-brief/).
