---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Download ISO 20022 pain.001 and pain.008 sample files built from the public scheme rulebooks per country and rail, each with a record of where it comes from and how it was checked, plus schema coverage files for every supported edition."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-09-13T08:00:00+00:00"
description: "Download ISO 20022 pain.001 and pain.008 sample files built from the public scheme rulebooks per country and rail, each with a record of where it comes from and how it was checked, plus schema coverage files for every supported edition."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/example-corpus/"
image_alt: "Download ISO 20022 pain.001 and pain.008 sample files built from the public scheme rulebooks per country and rail, each with a record of where it comes from and how it was checked, plus schema coverage files for every supported edition."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "ISO 20022 example files, pain.001 sample XML, pain.008 sample, bank usage guideline, SEPA example, CHAPS example, Faster Payments example, ACH pain.001, QR-bill pain.001, Bankgiro pain.001, test corpus"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/example-corpus/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Sample payment files for 17 countries and their payment rails, plus schema coverage files for every supported edition, each traceable to its public sources."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "ISO 20022 example files — pain.001 and pain.008 samples per country and rail"
url: "https://pain001.com/example-corpus/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/example-corpus/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Download ISO 20022 pain.001 and pain.008 sample files built from the public scheme rulebooks per country and rail, each with a record of where it comes from and how it was checked, plus schema coverage files for every supported edition."
item_guid: "https://pain001.com/example-corpus/"
item_link: "https://pain001.com/example-corpus/"
item_pub_date: "Sun, 13 Sep 2026 08:00:00 +0000"
item_title: "ISO 20022 example files — pain.001 and pain.008 samples per country and rail"
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
apple-mobile-web-app-title: "ISO 20022 example files — pain.001 and pain.008 samples per country and rail"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Download ISO 20022 pain.001 and pain.008 sample files built from the public scheme rulebooks per country and rail, each with a record of where it comes from and how it was checked, plus schema coverage files for every supported edition."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "ISO 20022 example files — pain.001 and pain.008 samples per country and rail"
twitter_url: "https://pain001.com/example-corpus/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Example corpus"
excerpt: "Download ISO 20022 pain.001 and pain.008 sample files built from the public scheme rulebooks per country and rail, each with a record of where it comes from and how it was checked, plus schema coverage files for every supported edition."
last_reviewed: "2026-07-26"


---

If you are connecting a system to a bank, writing a parser, or testing a mapping, you need sample ISO 20022 files that are correct for your country and your rail. The ones passed around are usually old, hand-edited, or from somewhere else. This page gives you files built from the public rulebooks, with a record of where each one comes from.

**What you get**

- **42 realistic payments** across 17 countries: a UK CHAPS property purchase, a Swiss QR-bill, a Swedish Bankgiro run, a US ACH payroll, a SEPA direct debit, and more, each rendered in the message editions you are likely to meet.
- **131 schema coverage files** across 13 editions: deliberately exhaustive files that exercise the elements and choices of one schema edition, for testing a parser or a mapping against the whole schema rather than the usual happy path.
- **A provenance record beside every payment file** saying where its content comes from, how far to trust it, and how the library checked it.

**How to use it**

1. Download the complete bundle below, or pick single files from the tables.
2. Open the `.xml` next to your own file and diff them; open the `.provenance.yaml` to see what the differences mean.
3. Get your bank's usage guideline (see below) and apply it on top: these files follow the public scheme rules, not any one bank's profile.

Identifiers are synthetic: IBANs, BICs, LEIs and account numbers pass their check digits but belong to nobody, and names and addresses are invented. **Do not send these files to a bank.**

## Download

| Bundle | Contents | Size |
| :--- | :--- | ---: |
| [Complete corpus](/corpus/pain001-example-corpus-0.0.70.zip) | 84 payment files with their provenance records, and 131 schema coverage files across 13 editions | 313 KB |
| Coverage files per edition | one zip each, listed on the [coverage page](/example-corpus-coverage/) | 9 to 12 KB |

Everything here is generated from pain001 0.0.70's own corpus, which also ships inside the Python package (`pain001.corpus`) and in the [repository](https://github.com/sebastienrousseau/pain001/tree/main/pain001/corpus/data).

## One scenario, end to end

Take `gb.chaps.property-purchase`: CHAPS same-day property completion with the BoE HLST purpose code.

It ships as these files:

- [gb.chaps.property-purchase.pain.001.001.03.xml](/corpus/market/gb/priority-payment/gb.chaps.property-purchase.pain.001.001.03.xml): the payment in pain.001.001.03, and beside it [gb.chaps.property-purchase.pain.001.001.03.provenance.yaml](/corpus/market/gb/priority-payment/gb.chaps.property-purchase.pain.001.001.03.provenance.yaml), its provenance record.
- [gb.chaps.property-purchase.pain.001.001.09.xml](/corpus/market/gb/priority-payment/gb.chaps.property-purchase.pain.001.001.09.xml): the payment in pain.001.001.09, and beside it [gb.chaps.property-purchase.pain.001.001.09.provenance.yaml](/corpus/market/gb/priority-payment/gb.chaps.property-purchase.pain.001.001.09.provenance.yaml), its provenance record.

The provenance record answers the questions you would otherwise have to ask us:

- **Where does the content come from?** Bank of England: ISO 20022 purpose codes for CHAPS property transactions.
- **How much can I trust it?** Confidence `derived`: built from the public rulebook or implementation guide; no published sample was available to compare.
- **How was it checked?** By the library, against the schema, the ISO rules and the `uk-chaps`, `purpose-mandate-gb` profiles; the record lists every finding, including warnings.
- **Is it exactly this file?** Its SHA-256 is in the record.

What the record does not tell you is what *your* bank requires. That is the subject of the next section.

## Your bank's guideline

Every bank and clearing house publishes its own **message usage guideline**: which ISO 20022 elements it requires, which it ignores, and the values it accepts. Two banks on the same scheme can differ. Those guidelines are the bank's documentation, so they are not reproduced here: **download them from your bank or financial organisation**, typically from its client portal or from its collection on Swift MyStandards, and treat them as the final word.

The library is built for that step. Its overlay grammar expresses a guideline as a short list of rules (an element that must be present, one that must be absent, a value that must be one of a set), `scripts/derive_overlay.py` reads a guideline's schema and drafts those rules for you, and the corpus builder can then render any scenario on this page the way your bank wants it, privately, in your own environment. The [corpus guide](https://github.com/sebastienrousseau/pain001/blob/main/docs/corpus.md) walks through it.

## How the library checked these files

| Step | What it checks |
| :--- | :--- |
| Schema | well-formed and valid against the edition's official ISO 20022 XSD |
| ISO rules | the cross-element rules of the ISO message definition report, such as a cheque never carrying a creditor account |
| Scheme profile | the public rulebook of the rail: service levels, national identifiers, reference formats, amount limits |
| Public overlay | what a scheme body or regulator requires on top, where one has published it |

These checks are the library's own; they are not a certification, and passing them does not mean a bank will accept the file. Channel rules, onboarding profiles, cut-off times and the bank's guideline sit on top.

**Reading the evidence column.** `verified` means checked against a sample the scheme itself published. `derived` means built from the public rulebook or implementation guide; no published sample was available to compare. `assumed` means one detail rests on an assumption the record names; treat that detail with care.

## Payment files by country

### AE (AE)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`ae.uaefts.single`](/corpus-ae-uaefts-single/) | UAE domestic AED transfer through UAEFTS with the CBUAE regulatory reporting code. | `ae-uaefts`, `purpose-mandate-ae` | [pain.001.001.03](/corpus/market/ae/priority-payment/ae.uaefts.single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/ae/priority-payment/ae.uaefts.single.pain.001.001.09.xml) | assumed |

### Belgium (BE)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`be.sepa.sct-supplier`](/corpus-be-sepa-sct-supplier/) | SEPA credit transfer with a Belgian structured communication (BBA). | `sepa-sct` | [pain.001.001.03](/corpus/market/be/sepa-credit-transfer/be.sepa.sct-supplier.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/be/sepa-credit-transfer/be.sepa.sct-supplier.pain.001.001.09.xml) | derived |
| [`be.sepa.sdd-core`](/corpus-be-sepa-sdd-core/) | SEPA Core direct debit, recurring, Belgian creditor identifier. | `sepa-sdd` | [pain.008.001.02](/corpus/market/be/sepa-direct-debit/be.sepa.sdd-core.pain.008.001.02.xml), [pain.008.001.08](/corpus/market/be/sepa-direct-debit/be.sepa.sdd-core.pain.008.001.08.xml) | derived |

### Switzerland (CH)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`ch.international.usd`](/corpus-ch-international-usd/) | Cross-border USD payment from Switzerland (SPS payment type X). | `cbpr-cross-border` | [pain.001.001.03](/corpus/market/ch/cross-border/ch.international.usd.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/ch/cross-border/ch.international.usd.pain.001.001.09.xml) | derived |
| [`ch.sps.qr-bill`](/corpus-ch-sps-qr-bill/) | Swiss domestic credit transfer settling a QR-bill (QRR reference). | `ch-domestic` | [pain.001.001.03](/corpus/market/ch/domestic-credit-transfer/ch.sps.qr-bill.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/ch/domestic-credit-transfer/ch.sps.qr-bill.pain.001.001.09.xml) | derived |
| [`ch.sps.scor`](/corpus-ch-sps-scor/) | Swiss domestic credit transfer with an ISO 11649 creditor reference (SCOR). | `ch-domestic` | [pain.001.001.03](/corpus/market/ch/domestic-credit-transfer/ch.sps.scor.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/ch/domestic-credit-transfer/ch.sps.scor.pain.001.001.09.xml) | derived |
| [`ch.sepa.sct`](/corpus-ch-sepa-sct/) | SEPA credit transfer from Switzerland (SPS payment type S). | `ch-sepa` | [pain.001.001.03](/corpus/market/ch/sepa-credit-transfer/ch.sepa.sct.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/ch/sepa-credit-transfer/ch.sepa.sct.pain.001.001.09.xml) | derived |

### CZ (CZ)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`cz.certis.domestic`](/corpus-cz-certis-domestic/) | Czech domestic CZK transfer through CERTIS with VS/KS/SS payment symbols. | base rules only | [pain.001.001.03](/corpus/market/cz/domestic-credit-transfer/cz.certis.domestic.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/cz/domestic-credit-transfer/cz.certis.domestic.pain.001.001.09.xml) | derived |
| [`cz.sepa.sct`](/corpus-cz-sepa-sct/) | SEPA credit transfer from a Czech EUR account to a German supplier. | `sepa-sct` | [pain.001.001.03](/corpus/market/cz/sepa-credit-transfer/cz.sepa.sct.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/cz/sepa-credit-transfer/cz.sepa.sct.pain.001.001.09.xml) | derived |

### Germany (DE)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`de.axz.foreign`](/corpus-de-axz-foreign/) | Foreign payment in USD from a German account, DK order type AXZ. | `de-axz` | [pain.001.001.03](/corpus/market/de/cross-border/de.axz.foreign.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/de/cross-border/de.axz.foreign.pain.001.001.09.xml) | assumed |
| [`de.sepa.sct-salary`](/corpus-de-sepa-sct-salary/) | SEPA SCT salary batch with structured and unstructured remittance. | `sepa-sct` | [pain.001.001.03](/corpus/market/de/sepa-credit-transfer/de.sepa.sct-salary.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/de/sepa-credit-transfer/de.sepa.sct-salary.pain.001.001.09.xml), [pain.001.001.13](/corpus/market/de/sepa-credit-transfer/de.sepa.sct-salary.pain.001.001.13.xml) | derived |
| [`de.sepa.sdd-b2b`](/corpus-de-sepa-sdd-b2b/) | SEPA B2B direct debit, first collection. | `sepa-b2b` | [pain.008.001.02](/corpus/market/de/sepa-direct-debit/de.sepa.sdd-b2b.pain.008.001.02.xml), [pain.008.001.08](/corpus/market/de/sepa-direct-debit/de.sepa.sdd-b2b.pain.008.001.08.xml) | derived |
| [`de.sepa.sct-inst`](/corpus-de-sepa-sct-inst/) | SEPA Instant credit transfer, single, INST at PmtInf. | `sepa-inst` | [pain.001.001.09](/corpus/market/de/sepa-instant/de.sepa.sct-inst.pain.001.001.09.xml) | derived |
| [`de.ccu.urgent`](/corpus-de-ccu-urgent/) | Urgent euro payment (TARGET) from a German account, DK order type CCU. | `de-ccu` | [pain.001.001.03](/corpus/market/de/urgent-euro/de.ccu.urgent.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/de/urgent-euro/de.ccu.urgent.pain.001.001.09.xml) | derived |

### Spain (ES)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`es.sepa.sct-single`](/corpus-es-sepa-sct-single/) | SEPA credit transfer, single, initiating party identified by NIF. | `sepa-sct` | [pain.001.001.03](/corpus/market/es/sepa-credit-transfer/es.sepa.sct-single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/es/sepa-credit-transfer/es.sepa.sct-single.pain.001.001.09.xml) | derived |
| [`es.sepa.sdd-core`](/corpus-es-sepa-sdd-core/) | SEPA Core direct debit, recurring, Spanish creditor identifier. | `sepa-sdd` | [pain.008.001.02](/corpus/market/es/sepa-direct-debit/es.sepa.sdd-core.pain.008.001.02.xml), [pain.008.001.08](/corpus/market/es/sepa-direct-debit/es.sepa.sdd-core.pain.008.001.08.xml) | derived |

### France (FR)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`fr.sepa.sct-supplier`](/corpus-fr-sepa-sct-supplier/) | SEPA credit transfer, supplier invoice with an RF creditor reference. | `sepa-sct` | [pain.001.001.03](/corpus/market/fr/sepa-credit-transfer/fr.sepa.sct-supplier.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/fr/sepa-credit-transfer/fr.sepa.sct-supplier.pain.001.001.09.xml) | derived |
| [`fr.sepa.sdd-core`](/corpus-fr-sepa-sdd-core/) | SEPA Core direct debit, recurring collection on an amended mandate. | `sepa-sdd` | [pain.008.001.02](/corpus/market/fr/sepa-direct-debit/fr.sepa.sdd-core.pain.008.001.02.xml), [pain.008.001.08](/corpus/market/fr/sepa-direct-debit/fr.sepa.sdd-core.pain.008.001.08.xml) | derived |

### United Kingdom (GB)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`gb.bacs.supplier-run`](/corpus-gb-bacs-supplier-run/) | Bacs Direct Credit supplier run, two payments, SUN in the debtor id. | `uk-bacs` | [pain.001.001.03](/corpus/market/gb/bacs-direct-credit/gb.bacs.supplier-run.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/gb/bacs-direct-credit/gb.bacs.supplier-run.pain.001.001.09.xml) | derived |
| [`gb.bacs-dd.collection`](/corpus-gb-bacs-dd-collection/) | Bacs Direct Debit collection, first and recurring, SUN as creditor id. | `uk-bacs-dd` | [pain.008.001.02](/corpus/market/gb/bacs-direct-debit/gb.bacs-dd.collection.pain.008.001.02.xml), [pain.008.001.08](/corpus/market/gb/bacs-direct-debit/gb.bacs-dd.collection.pain.008.001.08.xml) | derived |
| [`gb.fps.single`](/corpus-gb-fps-single/) | Faster Payments single supplier payment, sort code and account. | `uk-fps` | [pain.001.001.03](/corpus/market/gb/faster-payment/gb.fps.single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/gb/faster-payment/gb.fps.single.pain.001.001.09.xml) | derived |
| [`gb.chaps.property-purchase`](/corpus-gb-chaps-property-purchase/) | CHAPS same-day property completion with the BoE HLST purpose code. | `uk-chaps`, `purpose-mandate-gb` | [pain.001.001.03](/corpus/market/gb/priority-payment/gb.chaps.property-purchase.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/gb/priority-payment/gb.chaps.property-purchase.pain.001.001.09.xml) | derived |
| [`gb.international.usd`](/corpus-gb-international-usd/) | USD cross-border payment from a UK account to a US supplier. | `cbpr-cross-border` | [pain.001.001.03](/corpus/market/gb/priority-payment/gb.international.usd.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/gb/priority-payment/gb.international.usd.pain.001.001.09.xml) | derived |

### HK (HK)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`hk.fps.single`](/corpus-hk-fps-single/) | Hong Kong FPS credit in HKD, clearing codes and account numbers. | `hk-fps`, `purpose-mandate-hk` | [pain.001.001.03](/corpus/market/hk/instant-payment/hk.fps.single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/hk/instant-payment/hk.fps.single.pain.001.001.09.xml) | assumed |

### Italy (IT)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`it.sepa.sct-single`](/corpus-it-sepa-sct-single/) | SEPA credit transfer, single supplier payment. | `sepa-sct` | [pain.001.001.03](/corpus/market/it/sepa-credit-transfer/it.sepa.sct-single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/it/sepa-credit-transfer/it.sepa.sct-single.pain.001.001.09.xml) | derived |

### Luxembourg (LU)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`lu.sepa.sct-single`](/corpus-lu-sepa-sct-single/) | SEPA credit transfer, single supplier payment. | `sepa-sct` | [pain.001.001.03](/corpus/market/lu/sepa-credit-transfer/lu.sepa.sct-single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/lu/sepa-credit-transfer/lu.sepa.sct-single.pain.001.001.09.xml) | derived |

### MY (MY)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`my.duitnow.single`](/corpus-my-duitnow-single/) | Malaysia DuitNow credit in MYR with a BNM purpose code. | `my-duitnow`, `purpose-mandate-my` | [pain.001.001.03](/corpus/market/my/instant-payment/my.duitnow.single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/my/instant-payment/my.duitnow.single.pain.001.001.09.xml) | assumed |

### Netherlands (NL)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`nl.sepa.sct-supplier`](/corpus-nl-sepa-sct-supplier/) | SEPA credit transfer with a Dutch payment reference (CUR). | `sepa-sct` | [pain.001.001.03](/corpus/market/nl/sepa-credit-transfer/nl.sepa.sct-supplier.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/nl/sepa-credit-transfer/nl.sepa.sct-supplier.pain.001.001.09.xml) | derived |
| [`nl.sepa.sdd-core`](/corpus-nl-sepa-sdd-core/) | SEPA Core direct debit, recurring collections under mandates. | `sepa-sdd` | [pain.008.001.02](/corpus/market/nl/sepa-direct-debit/nl.sepa.sdd-core.pain.008.001.02.xml), [pain.008.001.08](/corpus/market/nl/sepa-direct-debit/nl.sepa.sdd-core.pain.008.001.08.xml) | derived |

### QA (QA)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`qa.qatch.single`](/corpus-qa-qatch-single/) | Qatar QATCH credit in QAR with the QCB purpose of payment. | `qa-qatch`, `purpose-mandate-qa` | [pain.001.001.03](/corpus/market/qa/domestic-credit-transfer/qa.qatch.single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/qa/domestic-credit-transfer/qa.qatch.single.pain.001.001.09.xml) | assumed |

### Sweden (SE)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`se.bankgiro.supplier`](/corpus-se-bankgiro-supplier/) | Swedish Bankgiro supplier payment with an OCR reference. | `se-bankgiro` | [pain.001.001.03](/corpus/market/se/bankgiro-credit/se.bankgiro.supplier.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/se/bankgiro-credit/se.bankgiro.supplier.pain.001.001.09.xml) | derived |
| [`se.plusgiro.supplier`](/corpus-se-plusgiro-supplier/) | Swedish Plusgiro supplier payment with an invoice message. | `se-bankgiro` | [pain.001.001.03](/corpus/market/se/plusgiro-credit/se.plusgiro.supplier.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/se/plusgiro-credit/se.plusgiro.supplier.pain.001.001.09.xml) | derived |
| [`se.rix.urgent`](/corpus-se-rix-urgent/) | Swedish domestic high-value SEK payment through RIX, urgent, intra-group. | base rules only | [pain.001.001.03](/corpus/market/se/priority-payment/se.rix.urgent.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/se/priority-payment/se.rix.urgent.pain.001.001.09.xml) | derived |
| [`se.bankgiro.salary`](/corpus-se-bankgiro-salary/) | Swedish salary batch (Bankgirot Löner), SALA, one debit. | `se-bankgiro` | [pain.001.001.03](/corpus/market/se/salary/se.bankgiro.salary.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/se/salary/se.bankgiro.salary.pain.001.001.09.xml) | derived |

### SG (SG)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`sg.fast.single`](/corpus-sg-fast-single/) | Singapore FAST credit in SGD, bank and branch codes, addresses on both parties. | `sg-fast` | [pain.001.001.03](/corpus/market/sg/instant-payment/sg.fast.single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/sg/instant-payment/sg.fast.single.pain.001.001.09.xml) | assumed |

### United States (US)

| Scenario | What it shows | Checked against | Editions | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| [`us.ach.ccd-supplier`](/corpus-us-ach-ccd-supplier/) | ACH CCD credit to a supplier with an addenda remittance line. | `us-ach` | [pain.001.001.03](/corpus/market/us/ach-credit/us.ach.ccd-supplier.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/us/ach-credit/us.ach.ccd-supplier.pain.001.001.09.xml) | derived |
| [`us.ach.ppd-payroll`](/corpus-us-ach-ppd-payroll/) | ACH PPD payroll run, two employees. | `us-ach` | [pain.001.001.03](/corpus/market/us/ach-credit/us.ach.ppd-payroll.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/us/ach-credit/us.ach.ppd-payroll.pain.001.001.09.xml) | derived |
| [`us.eftps.tax`](/corpus-us-eftps-tax/) | IRS EFTPS federal tax deposit, CCD with the TXP addenda string. | `us-ach` | [pain.001.001.03](/corpus/market/us/ach-credit/us.eftps.tax.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/us/ach-credit/us.eftps.tax.pain.001.001.09.xml) | derived |
| [`us.ach.debit`](/corpus-us-ach-debit/) | ACH debit collection (CCD) with routing numbers. | `us-ach` | [pain.008.001.02](/corpus/market/us/ach-debit/us.ach.debit.pain.008.001.02.xml), [pain.008.001.08](/corpus/market/us/ach-debit/us.ach.debit.pain.008.001.08.xml) | derived |
| [`us.check.vendor`](/corpus-us-check-vendor/) | Bank-issued cheque to a vendor, mailed to the creditor. | base rules only | [pain.001.001.03](/corpus/market/us/cheque/us.check.vendor.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/us/cheque/us.check.vendor.pain.001.001.09.xml) | assumed |
| [`us.rtp.single`](/corpus-us-rtp-single/) | RTP real-time payment, single. | `us-rtp` | [pain.001.001.03](/corpus/market/us/instant-payment/us.rtp.single.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/us/instant-payment/us.rtp.single.pain.001.001.09.xml) | derived |
| [`us.wire.domestic`](/corpus-us-wire-domestic/) | Fedwire domestic funds transfer, urgent. | `us-wire` | [pain.001.001.03](/corpus/market/us/priority-payment/us.wire.domestic.pain.001.001.03.xml), [pain.001.001.09](/corpus/market/us/priority-payment/us.wire.domestic.pain.001.001.09.xml) | derived |

## Schema coverage files

Each edition has a small set of files built so that the elements and choice branches its schema declares each appear in at least one file. The first file is the baseline that carries every element once; each later file is named after the blocks it adds, so you can pick the one that exercises what you are testing. The [coverage page](/example-corpus-coverage/) lists every file with what it adds and a zip per edition.

| Edition | Files |
| :--- | ---: |
| [`pain.001.001.03`](/example-corpus-coverage/#pain-001-001-03) | 10 |
| [`pain.001.001.04`](/example-corpus-coverage/#pain-001-001-04) | 10 |
| [`pain.001.001.05`](/example-corpus-coverage/#pain-001-001-05) | 10 |
| [`pain.001.001.06`](/example-corpus-coverage/#pain-001-001-06) | 10 |
| [`pain.001.001.07`](/example-corpus-coverage/#pain-001-001-07) | 10 |
| [`pain.001.001.08`](/example-corpus-coverage/#pain-001-001-08) | 10 |
| [`pain.001.001.09`](/example-corpus-coverage/#pain-001-001-09) | 11 |
| [`pain.001.001.10`](/example-corpus-coverage/#pain-001-001-10) | 11 |
| [`pain.001.001.11`](/example-corpus-coverage/#pain-001-001-11) | 11 |
| [`pain.001.001.12`](/example-corpus-coverage/#pain-001-001-12) | 11 |
| [`pain.001.001.13`](/example-corpus-coverage/#pain-001-001-13) | 11 |
| [`pain.008.001.02`](/example-corpus-coverage/#pain-008-001-02) | 8 |
| [`pain.008.001.08`](/example-corpus-coverage/#pain-008-001-08) | 8 |

## Notes

- The site publishes the generic files and their public sources. Bank-specific material stays with the banks.
- The corpus is English only and grows with every release; it is generated data, not a translated page.
- The [corpus guide](https://github.com/sebastienrousseau/pain001/blob/main/docs/corpus.md) explains the scenario format, the overlay grammar and how to add a country or a rail. Corrections and new scenarios are welcome there.
- Regenerate this page and its downloads with `poetry run python3 scripts/generate_corpus_page.py` from the pain001 checkout after a corpus change.
