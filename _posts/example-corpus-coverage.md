---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Generated pain.001 and pain.008 files that between them use every element path and choice branch of each supported schema edition, each named after what it adds, with a zip per edition."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-09-13T08:00:00+00:00"
description: "Generated pain.001 and pain.008 files that between them use every element path and choice branch of each supported schema edition, each named after what it adds, with a zip per edition."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/example-corpus-coverage/"
image_alt: "Generated pain.001 and pain.008 files that between them use every element path and choice branch of each supported schema edition, each named after what it adds, with a zip per edition."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "ISO 20022 schema coverage, pain.001 test files, pain.008 test files, XSD coverage, parser test corpus"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/example-corpus-coverage/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "One small set per edition, every file valid, every file named for the blocks it exercises."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "ISO 20022 schema coverage files — every element of every edition"
url: "https://pain001.com/example-corpus-coverage/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/example-corpus-coverage/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Generated pain.001 and pain.008 files that between them use every element path and choice branch of each supported schema edition, each named after what it adds, with a zip per edition."
item_guid: "https://pain001.com/example-corpus-coverage/"
item_link: "https://pain001.com/example-corpus-coverage/"
item_pub_date: "Sun, 13 Sep 2026 08:00:00 +0000"
item_title: "ISO 20022 schema coverage files — every element of every edition"
last_build_date: "Sun, 13 Sep 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Sun, 13 Sep 2026 08:00:00 +0000"
ttl: 60
type: website
webmaster: contact@pain001.com
apple_mobile_web_app_orientations: portrait
apple_touch_icon_sizes: 192x192
apple-mobile-web-app-capable: yes
apple-mobile-web-app-status-bar-inset: black
apple-mobile-web-app-status-bar-style: black-translucent
apple-mobile-web-app-title: "ISO 20022 schema coverage files — every element of every edition"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Generated pain.001 and pain.008 files that between them use every element path and choice branch of each supported schema edition, each named after what it adds, with a zip per edition."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "ISO 20022 schema coverage files — every element of every edition"
twitter_url: "https://pain001.com/example-corpus-coverage/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Example corpus"
excerpt: "Generated pain.001 and pain.008 files that between them use every element path and choice branch of each supported schema edition, each named after what it adds, with a zip per edition."
last_reviewed: "2026-07-26"


---

Schema coverage files are not realistic payments. Each set is generated from the schema itself so that the element paths and choice branches of one edition each appear in at least one of its files, and every file is valid against the schema and the ISO message definition report rules. Use them to smoke-test a parser, a mapping or a validator against the whole schema.

**How to pick a file.** The first file of every set is the baseline: every element once, first branch of every choice. Each later file adds elements and choice branches the earlier files did not reach, and is named after the blocks most of that new content falls under (`RmtInf` for remittance information, `UltmtDbtr` for the ultimate debtor, `ChqInstr` for cheque instructions, and so on). The recipe in the name says what kind of payment the file is: a credit transfer, a cheque delivered to the creditor agent, a cheque with no creditor agent, or a direct debit collection.

These files follow the ISO schema only. What your bank accepts is in its usage guideline; get it from your bank.

The [example corpus](/example-corpus/) page has the realistic payment files and the complete download.

## pain.001.001.03

10 files. [Download the set](/corpus/pain001-coverage-pain.001.001.03-0.0.70.zip) (10 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.03/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.03/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 152 element paths and 60 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.03/03-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 23 element paths and 18 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [04-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.03/04-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 10 element paths and 10 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-Id.xml](/corpus/coverage/pain.001.001.03/05-transfer-UltmtDbtr-PstlAdr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 30 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, Id. |
| [06-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.03/06-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 11 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, Id. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.03/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.03/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.03/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 37 element paths and 1 choice branch no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.03/10-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.04

10 files. [Download the set](/corpus/pain001-coverage-pain.001.001.04-0.0.70.zip) (10 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.04/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.04/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 154 element paths and 62 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.04/03-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 23 element paths and 18 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [04-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.04/04-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 10 element paths and 10 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-Id.xml](/corpus/coverage/pain.001.001.04/05-transfer-UltmtDbtr-PstlAdr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 30 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, Id. |
| [06-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.04/06-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 11 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, Id. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.04/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.04/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.04/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 38 element paths and 1 choice branch no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.04/10-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.05

10 files. [Download the set](/corpus/pain001-coverage-pain.001.001.05-0.0.70.zip) (10 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.05/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.05/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 154 element paths and 62 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.05/03-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 23 element paths and 18 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [04-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.05/04-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 10 element paths and 10 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-Id.xml](/corpus/coverage/pain.001.001.05/05-transfer-UltmtDbtr-PstlAdr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 30 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, Id. |
| [06-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.05/06-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 11 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, Id. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.05/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.05/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.05/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 38 element paths and 1 choice branch no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.05/10-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.06

10 files. [Download the set](/corpus/pain001-coverage-pain.001.001.06-0.0.70.zip) (11 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.06/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.06/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 177 element paths and 67 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.06/03-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 25 element paths and 20 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [04-transfer-RmtInf-PmtTpInf-InitgPty.xml](/corpus/coverage/pain.001.001.06/04-transfer-RmtInf-PmtTpInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 12 element paths and 12 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-Id.xml](/corpus/coverage/pain.001.001.06/05-transfer-UltmtDbtr-PstlAdr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 30 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, Id. |
| [06-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.06/06-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 11 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, Id. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.06/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.06/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.06/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 38 element paths and 1 choice branch no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.06/10-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.07

10 files. [Download the set](/corpus/pain001-coverage-pain.001.001.07-0.0.70.zip) (11 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.07/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.07/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 180 element paths and 70 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.07/03-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 25 element paths and 20 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [04-transfer-RmtInf-PmtTpInf-InitgPty.xml](/corpus/coverage/pain.001.001.07/04-transfer-RmtInf-PmtTpInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 12 element paths and 12 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-Id.xml](/corpus/coverage/pain.001.001.07/05-transfer-UltmtDbtr-PstlAdr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 30 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, Id. |
| [06-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.07/06-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 11 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, Id. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.07/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.07/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.07/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 38 element paths and 1 choice branch no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.07/10-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.08

10 files. [Download the set](/corpus/pain001-coverage-pain.001.001.08-0.0.70.zip) (11 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.08/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.08/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 181 element paths and 71 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.08/03-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 25 element paths and 20 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [04-transfer-RmtInf-PmtTpInf-InitgPty.xml](/corpus/coverage/pain.001.001.08/04-transfer-RmtInf-PmtTpInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 12 element paths and 12 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-Id.xml](/corpus/coverage/pain.001.001.08/05-transfer-UltmtDbtr-PstlAdr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 30 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, Id. |
| [06-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.08/06-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 11 element paths and 2 choice branches no earlier file covers, mostly under UltmtDbtr, Id. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.08/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.08/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.08/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 38 element paths and 1 choice branch no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.08/10-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.09

11 files. [Download the set](/corpus/pain001-coverage-pain.001.001.09-0.0.70.zip) (13 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.09/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.09/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 285 element paths and 103 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-InitgPty.xml](/corpus/coverage/pain.001.001.09/03-transfer-PmtTpInf-RmtInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 25 element paths and 20 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, InitgPty. |
| [04-transfer-RmtInf-PmtTpInf-InitgPty.xml](/corpus/coverage/pain.001.001.09/04-transfer-RmtInf-PmtTpInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 12 element paths and 12 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml](/corpus/coverage/pain.001.001.09/05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml) | A credit transfer (PmtMtd TRF) that adds 45 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, CtctDtls. |
| [06-transfer-UltmtDbtr-Id-PstlAdr.xml](/corpus/coverage/pain.001.001.09/06-transfer-UltmtDbtr-Id-PstlAdr.xml) | A credit transfer (PmtMtd TRF) that adds 15 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, Id, PstlAdr. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.09/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.09/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.09/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 52 element paths and 3 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.09/10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 8 element paths and 2 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [11-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.09/11-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.10

11 files. [Download the set](/corpus/pain001-coverage-pain.001.001.10-0.0.70.zip) (13 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.10/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.10/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 297 element paths and 111 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-MndtRltdInf.xml](/corpus/coverage/pain.001.001.10/03-transfer-PmtTpInf-RmtInf-MndtRltdInf.xml) | A credit transfer (PmtMtd TRF) that adds 28 element paths and 21 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, MndtRltdInf. |
| [04-transfer-RmtInf-PmtTpInf-InitgPty.xml](/corpus/coverage/pain.001.001.10/04-transfer-RmtInf-PmtTpInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 12 element paths and 12 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml](/corpus/coverage/pain.001.001.10/05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml) | A credit transfer (PmtMtd TRF) that adds 45 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, CtctDtls. |
| [06-transfer-UltmtDbtr-Id-PstlAdr.xml](/corpus/coverage/pain.001.001.10/06-transfer-UltmtDbtr-Id-PstlAdr.xml) | A credit transfer (PmtMtd TRF) that adds 15 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, Id, PstlAdr. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.10/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.10/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.10/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 52 element paths and 3 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.10/10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 8 element paths and 2 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [11-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.10/11-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.11

11 files. [Download the set](/corpus/pain001-coverage-pain.001.001.11-0.0.70.zip) (13 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.11/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.11/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 297 element paths and 111 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-MndtRltdInf.xml](/corpus/coverage/pain.001.001.11/03-transfer-PmtTpInf-RmtInf-MndtRltdInf.xml) | A credit transfer (PmtMtd TRF) that adds 28 element paths and 21 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, MndtRltdInf. |
| [04-transfer-RmtInf-PmtTpInf-InitgPty.xml](/corpus/coverage/pain.001.001.11/04-transfer-RmtInf-PmtTpInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 12 element paths and 12 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml](/corpus/coverage/pain.001.001.11/05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml) | A credit transfer (PmtMtd TRF) that adds 45 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, CtctDtls. |
| [06-transfer-UltmtDbtr-Id-PstlAdr.xml](/corpus/coverage/pain.001.001.11/06-transfer-UltmtDbtr-Id-PstlAdr.xml) | A credit transfer (PmtMtd TRF) that adds 15 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, Id, PstlAdr. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.11/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.11/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.11/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 52 element paths and 3 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.11/10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 8 element paths and 2 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [11-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.11/11-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.12

11 files. [Download the set](/corpus/pain001-coverage-pain.001.001.12-0.0.70.zip) (13 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.12/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.12/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 296 element paths and 110 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-MndtRltdInf.xml](/corpus/coverage/pain.001.001.12/03-transfer-PmtTpInf-RmtInf-MndtRltdInf.xml) | A credit transfer (PmtMtd TRF) that adds 28 element paths and 21 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, MndtRltdInf. |
| [04-transfer-RmtInf-PmtTpInf-InitgPty.xml](/corpus/coverage/pain.001.001.12/04-transfer-RmtInf-PmtTpInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 12 element paths and 12 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml](/corpus/coverage/pain.001.001.12/05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml) | A credit transfer (PmtMtd TRF) that adds 48 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, CtctDtls. |
| [06-transfer-UltmtDbtr-Id-PstlAdr.xml](/corpus/coverage/pain.001.001.12/06-transfer-UltmtDbtr-Id-PstlAdr.xml) | A credit transfer (PmtMtd TRF) that adds 15 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, Id, PstlAdr. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.12/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.12/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.12/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 56 element paths and 3 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.12/10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 8 element paths and 2 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [11-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.12/11-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.001.001.13

11 files. [Download the set](/corpus/pain001-coverage-pain.001.001.13-0.0.70.zip) (14 KB).

| File | What it is for |
| :--- | :--- |
| [01-transfer-every-element.xml](/corpus/coverage/pain.001.001.13/01-transfer-every-element.xml) | The baseline: every element of the schema once as a credit transfer (PmtMtd TRF), taking the first branch of every choice. |
| [02-transfer-RmtInf-InitgPty-Cdtr.xml](/corpus/coverage/pain.001.001.13/02-transfer-RmtInf-InitgPty-Cdtr.xml) | A credit transfer (PmtMtd TRF) that adds 297 element paths and 111 choice branches no earlier file covers, mostly under RmtInf, InitgPty, Cdtr. |
| [03-transfer-PmtTpInf-RmtInf-MndtRltdInf.xml](/corpus/coverage/pain.001.001.13/03-transfer-PmtTpInf-RmtInf-MndtRltdInf.xml) | A credit transfer (PmtMtd TRF) that adds 28 element paths and 21 choice branches no earlier file covers, mostly under PmtTpInf, RmtInf, MndtRltdInf. |
| [04-transfer-RmtInf-PmtTpInf-InitgPty.xml](/corpus/coverage/pain.001.001.13/04-transfer-RmtInf-PmtTpInf-InitgPty.xml) | A credit transfer (PmtMtd TRF) that adds 12 element paths and 12 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, InitgPty. |
| [05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml](/corpus/coverage/pain.001.001.13/05-transfer-UltmtDbtr-PstlAdr-CtctDtls.xml) | A credit transfer (PmtMtd TRF) that adds 48 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, PstlAdr, CtctDtls. |
| [06-transfer-UltmtDbtr-Id-PstlAdr.xml](/corpus/coverage/pain.001.001.13/06-transfer-UltmtDbtr-Id-PstlAdr.xml) | A credit transfer (PmtMtd TRF) that adds 15 element paths and 3 choice branches no earlier file covers, mostly under UltmtDbtr, Id, PstlAdr. |
| [07-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.13/07-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [08-transfer-UltmtDbtr-Id.xml](/corpus/coverage/pain.001.001.13/08-transfer-UltmtDbtr-Id.xml) | A credit transfer (PmtMtd TRF) that adds 1 element path and 1 choice branch no earlier file covers, mostly under UltmtDbtr, Id. |
| [09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.13/09-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 56 element paths and 3 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml](/corpus/coverage/pain.001.001.13/10-cheque-to-agent-ChqInstr-ChqFr-DlvrTo.xml) | A cheque delivered to the creditor agent (PmtMtd CHK) that adds 8 element paths and 2 choice branches no earlier file covers, mostly under ChqInstr, ChqFr, DlvrTo. |
| [11-cheque-no-agent-ChqInstr-DlvryMtd.xml](/corpus/coverage/pain.001.001.13/11-cheque-no-agent-ChqInstr-DlvryMtd.xml) | A cheque with no creditor agent (PmtMtd CHK) that adds 1 element path and 1 choice branch no earlier file covers, mostly under ChqInstr, DlvryMtd. |

## pain.008.001.02

8 files. [Download the set](/corpus/pain001-coverage-pain.008.001.02-0.0.70.zip) (10 KB).

| File | What it is for |
| :--- | :--- |
| [01-collection-every-element.xml](/corpus/coverage/pain.008.001.02/01-collection-every-element.xml) | The baseline: every element of the schema once as a direct debit collection (PmtMtd DD), taking the first branch of every choice. |
| [02-collection-DrctDbtTx-RmtInf-InitgPty.xml](/corpus/coverage/pain.008.001.02/02-collection-DrctDbtTx-RmtInf-InitgPty.xml) | A direct debit collection (PmtMtd DD) that adds 178 element paths and 63 choice branches no earlier file covers, mostly under DrctDbtTx, RmtInf, InitgPty. |
| [03-collection-PmtTpInf-DrctDbtTx-RmtInf.xml](/corpus/coverage/pain.008.001.02/03-collection-PmtTpInf-DrctDbtTx-RmtInf.xml) | A direct debit collection (PmtMtd DD) that adds 27 element paths and 21 choice branches no earlier file covers, mostly under PmtTpInf, DrctDbtTx, RmtInf. |
| [04-collection-PmtTpInf-DrctDbtTx-RmtInf.xml](/corpus/coverage/pain.008.001.02/04-collection-PmtTpInf-DrctDbtTx-RmtInf.xml) | A direct debit collection (PmtMtd DD) that adds 13 element paths and 13 choice branches no earlier file covers, mostly under PmtTpInf, DrctDbtTx, RmtInf. |
| [05-collection-DrctDbtTx-UltmtCdtr.xml](/corpus/coverage/pain.008.001.02/05-collection-DrctDbtTx-UltmtCdtr.xml) | A direct debit collection (PmtMtd DD) that adds 60 element paths and 4 choice branches no earlier file covers, mostly under DrctDbtTx, UltmtCdtr. |
| [06-collection-DrctDbtTx-UltmtCdtr.xml](/corpus/coverage/pain.008.001.02/06-collection-DrctDbtTx-UltmtCdtr.xml) | A direct debit collection (PmtMtd DD) that adds 22 element paths and 4 choice branches no earlier file covers, mostly under DrctDbtTx, UltmtCdtr. |
| [07-collection-DrctDbtTx-UltmtCdtr.xml](/corpus/coverage/pain.008.001.02/07-collection-DrctDbtTx-UltmtCdtr.xml) | A direct debit collection (PmtMtd DD) that adds 2 element paths and 2 choice branches no earlier file covers, mostly under DrctDbtTx, UltmtCdtr. |
| [08-collection-DrctDbtTx-UltmtCdtr.xml](/corpus/coverage/pain.008.001.02/08-collection-DrctDbtTx-UltmtCdtr.xml) | A direct debit collection (PmtMtd DD) that adds 2 element paths and 2 choice branches no earlier file covers, mostly under DrctDbtTx, UltmtCdtr. |

## pain.008.001.08

8 files. [Download the set](/corpus/pain001-coverage-pain.008.001.08-0.0.70.zip) (12 KB).

| File | What it is for |
| :--- | :--- |
| [01-collection-every-element.xml](/corpus/coverage/pain.008.001.08/01-collection-every-element.xml) | The baseline: every element of the schema once as a direct debit collection (PmtMtd DD), taking the first branch of every choice. |
| [02-collection-DrctDbtTx-RmtInf-InitgPty.xml](/corpus/coverage/pain.008.001.08/02-collection-DrctDbtTx-RmtInf-InitgPty.xml) | A direct debit collection (PmtMtd DD) that adds 322 element paths and 110 choice branches no earlier file covers, mostly under DrctDbtTx, RmtInf, InitgPty. |
| [03-collection-DrctDbtTx-PmtTpInf-RmtInf.xml](/corpus/coverage/pain.008.001.08/03-collection-DrctDbtTx-PmtTpInf-RmtInf.xml) | A direct debit collection (PmtMtd DD) that adds 35 element paths and 25 choice branches no earlier file covers, mostly under DrctDbtTx, PmtTpInf, RmtInf. |
| [04-collection-RmtInf-PmtTpInf-DrctDbtTx.xml](/corpus/coverage/pain.008.001.08/04-collection-RmtInf-PmtTpInf-DrctDbtTx.xml) | A direct debit collection (PmtMtd DD) that adds 15 element paths and 15 choice branches no earlier file covers, mostly under RmtInf, PmtTpInf, DrctDbtTx. |
| [05-collection-DrctDbtTx-UltmtCdtr.xml](/corpus/coverage/pain.008.001.08/05-collection-DrctDbtTx-UltmtCdtr.xml) | A direct debit collection (PmtMtd DD) that adds 90 element paths and 6 choice branches no earlier file covers, mostly under DrctDbtTx, UltmtCdtr. |
| [06-collection-DrctDbtTx-UltmtCdtr.xml](/corpus/coverage/pain.008.001.08/06-collection-DrctDbtTx-UltmtCdtr.xml) | A direct debit collection (PmtMtd DD) that adds 30 element paths and 6 choice branches no earlier file covers, mostly under DrctDbtTx, UltmtCdtr. |
| [07-collection-DrctDbtTx-UltmtCdtr.xml](/corpus/coverage/pain.008.001.08/07-collection-DrctDbtTx-UltmtCdtr.xml) | A direct debit collection (PmtMtd DD) that adds 2 element paths and 2 choice branches no earlier file covers, mostly under DrctDbtTx, UltmtCdtr. |
| [08-collection-DrctDbtTx-UltmtCdtr.xml](/corpus/coverage/pain.008.001.08/08-collection-DrctDbtTx-UltmtCdtr.xml) | A direct debit collection (PmtMtd DD) that adds 2 element paths and 2 choice branches no earlier file covers, mostly under DrctDbtTx, UltmtCdtr. |
