---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "The structure of an ISO 20022 pain.001 message: group header, payment information and credit transfer transactions."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-09-26T08:00:00+00:00"
description: "pain.001 is the ISO 20022 XML message a company sends its bank to order credit transfers: its structure, versions .03 to .13, a validated example and pain.002."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "en"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/pain-001/"
image_alt: "The pain.001 message explained: what it is, how it is structured and which version to use."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001, pain001, what is pain.001, pain.001 format, pain.001 XML, pain.001 example, pain.001 structure, pain.001.001.09, pain.001.001.03, pain.001 vs pain.002, pain.001 vs pacs.008, ISO 20022 customer credit transfer initiation"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/pain-001/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The ISO 20022 message a company sends its bank to order credit transfers: what it is, how it is built, which version to use, and a complete example that validates against the official schema."
tags: "ISO 20022, pain.001, pain001, payments, credit transfer, SEPA, CBPR+"
theme_color: "#0b0e14"
title: "What Is pain.001? ISO 20022 Credit Transfer Initiation"
url: "https://pain001.com/pain-001/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain-001/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.63)"
item_description: "pain.001 is the ISO 20022 XML message a company sends its bank to order credit transfers: its structure, versions .03 to .13, a validated example and pain.002."
item_guid: "https://pain001.com/pain-001/rss.xml"
item_link: "https://pain001.com/pain-001/rss.xml"
item_pub_date: "Sat, 26 Sep 2026 08:00:00 +0000"
item_title: "What Is pain.001? ISO 20022 Credit Transfer Initiation"
last_build_date: "Sat, 26 Sep 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Sat, 26 Sep 2026 08:00:00 +0000"
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
twitter_creator: "@wwdseb"
twitter_description: "What a rejected payment file costs, why structured payment data still matters now that Swift has deferred its deadline, what Pain001 does about it, what it costs (nothing), and whether it is safe, with each answer linked to its proof."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "Why Pain001: the Business Case in Five Questions"
twitter_url: "https://pain001.com/why/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "ISO 20022 explained"
excerpt: "pain.001, Customer Credit Transfer Initiation, is the ISO 20022 XML message a company sends its bank to order one or more credit transfers. This guide covers its three-level structure, the eleven versions from pain.001.001.03 to .13, a complete example that validates against the official XSD, how it relates to pain.002, pain.008, pacs.008 and MT101, and why banks reject files."
last_reviewed: "2026-09-26"
---

**pain.001** is the ISO 20022 message a company sends its bank to order one or more credit transfers. Its full name is *Customer Credit Transfer Initiation*: "pain" is the payment initiation message family, `.001` is the message number, and the suffix, such as `pain.001.001.09`, is the version. It is XML, it is validated against an official schema (XSD), and it replaces bank-specific CSV formats and the SWIFT MT101 text message.

## pain.001 in one minute

- **Who sends it:** a company (the debtor, or an agent acting for it) sends it to its own bank (the debtor agent).
- **What it carries:** one or more batches of credit transfers, each with a debtor account, a requested execution date and any number of payments to creditors.
- **What comes back:** the bank answers with **pain.002**, the Customer Payment Status Report, accepting or rejecting the file or individual transactions with ISO reason codes.
- **What happens next:** once accepted, the bank turns each instruction into interbank messages such as **pacs.008**, which the company never sees.
- **Where it is used:** SEPA credit transfers under the EPC rulebooks, cross-border payments on Swift under CBPR+ (`pain.001.001.09`), and many domestic schemes. Pain001's [example corpus](/example-corpus/) covers 42 scenarios across 17 markets.

## How a pain.001 message is structured

Every version shares the same three-level skeleton inside a `<CstmrCdtTrfInitn>` element.

| Level | Element | What it holds |
| --- | --- | --- |
| 1 | `<GrpHdr>` Group Header | Message ID, creation timestamp, number of transactions (`NbOfTxs`), control sum (`CtrlSum`), initiating party |
| 2 | `<PmtInf>` Payment Information | One batch: payment method, requested execution date, debtor, debtor account and agent, charge bearer |
| 3 | `<CdtTrfTxInf>` Credit Transfer Transaction | One payment: end-to-end reference, amount and currency, creditor, creditor account and agent, remittance information |

A file can hold several `<PmtInf>` batches, and each batch many `<CdtTrfTxInf>` payments. `NbOfTxs` and `CtrlSum` appear at both the file and the batch level and must match the payments they count, which is one of the most common reasons a bank rejects a file.

## A complete pain.001 example

This is a single SEPA credit transfer in `pain.001.001.09`, taken unchanged from Pain001's [example corpus](/corpus-it-sepa-sct-single/). It validates against the official ISO 20022 XSD. The parties, IBANs and BICs are fictitious.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09">
  <CstmrCdtTrfInitn>
    <GrpHdr>
      <MsgId>OML-SCT-20260921</MsgId>
      <CreDtTm>2026-09-21T12:00:00</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <CtrlSum>2200.00</CtrlSum>
      <InitgPty>
        <Nm>Officine Meccaniche Lombarde SpA</Nm>
        <PstlAdr>
          <PstCd>20123</PstCd>
          <TwnNm>Milano</TwnNm>
          <Ctry>IT</Ctry>
          <AdrLine>Via Torino 15</AdrLine>
        </PstlAdr>
      </InitgPty>
    </GrpHdr>
    <PmtInf>
      <PmtInfId>SCT-20260921-IT-01</PmtInfId>
      <PmtMtd>TRF</PmtMtd>
      <BtchBookg>false</BtchBookg>
      <NbOfTxs>1</NbOfTxs>
      <CtrlSum>2200.00</CtrlSum>
      <PmtTpInf>
        <SvcLvl>
          <Cd>SEPA</Cd>
        </SvcLvl>
      </PmtTpInf>
      <ReqdExctnDt>
        <Dt>2026-09-22</Dt>
      </ReqdExctnDt>
      <Dbtr>
        <Nm>Officine Meccaniche Lombarde SpA</Nm>
        <PstlAdr>
          <PstCd>20123</PstCd>
          <TwnNm>Milano</TwnNm>
          <Ctry>IT</Ctry>
          <AdrLine>Via Torino 15</AdrLine>
        </PstlAdr>
      </Dbtr>
      <DbtrAcct>
        <Id>
          <IBAN>IT48T78971134594OGDKY5VXE41</IBAN>
        </Id>
      </DbtrAcct>
      <DbtrAgt>
        <FinInstnId>
          <BICFI>TLAOIT60</BICFI>
        </FinInstnId>
      </DbtrAgt>
      <ChrgBr>SLEV</ChrgBr>
      <CdtTrfTxInf>
        <PmtId>
          <EndToEndId>OML-2026-0921-01</EndToEndId>
        </PmtId>
        <Amt>
          <InstdAmt Ccy="EUR">2200.00</InstdAmt>
        </Amt>
        <CdtrAgt>
          <FinInstnId>
            <BICFI>MHXHITI0</BICFI>
          </FinInstnId>
        </CdtrAgt>
        <Cdtr>
          <Nm>Fonderia Bresciana Srl</Nm>
          <PstlAdr>
            <PstCd>25121</PstCd>
            <TwnNm>Brescia</TwnNm>
            <Ctry>IT</Ctry>
          </PstlAdr>
        </Cdtr>
        <CdtrAcct>
          <Id>
            <IBAN>IT23J14887404856NF3794IGWXN</IBAN>
          </Id>
        </CdtrAcct>
        <RmtInf>
          <Ustrd>Fattura 117/2026</Ustrd>
        </RmtInf>
      </CdtTrfTxInf>
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>
```

Try your own data in the [browser demo](/try/): it builds a pain.001 file from a CSV and validates it against the official schema without the data leaving your machine.

## pain.001 versions

ISO publishes a new version when the message model changes. Banks and schemes each accept particular versions, so the version you send is the one your bank's channel documentation names.

| Version | Notes |
| --- | --- |
| [pain.001.001.03](/pain.001.001.03/) | The long-standing SEPA and CGI workhorse; identifies banks with `<BIC>` |
| [.04](/pain.001.001.04/), [.05](/pain.001.001.05/), [.06](/pain.001.001.06/), [.07](/pain.001.001.07/), [.08](/pain.001.001.08/) | Maintenance versions used by particular channels |
| [pain.001.001.09](/pain.001.001.09/) | The 2019 version CBPR+ selected for Swift; identifies banks with `<BICFI>`, adds LEI and UETR carriage |
| [.10](/pain.001.001.10/), [.11](/pain.001.001.11/), [.12](/pain.001.001.12/) | Post-2019 refinements |
| [pain.001.001.13](/pain.001.001.13/) | Published by ISO on 19 March 2026; adds an optional unique transaction identifier (`UnqTxIdr`) |

The [compatibility matrix](/compatibility/) shows which versions Pain001 generates, validates and migrates between.

## pain.001 compared with related messages

| Message | Direction | Purpose |
| --- | --- | --- |
| **pain.001** | Company to its bank | Orders credit transfers (pushes money out) |
| **pain.002** | Bank to company | Reports the status of a pain.001 or pain.008: accepted, partially accepted or rejected, with [reason codes](/pain002-reason-codes/) |
| **pain.008** | Company to its bank | Orders direct debits (collects money under a mandate) |
| **pacs.008** | Bank to bank | The interbank credit transfer a pain.001 instruction becomes |
| **MT101** | Company or bank, over Swift | The legacy text "Request for Transfer" that pain.001 replaces. Swift deferred the retirement of the interbank MT101 relay in August 2026 ([Swift](https://www.swift.com/news-events/news/swift-accepts-community-request-extend-structured-address-migration-iso-20022-payment-messages)); see [MT101 to pain.001](/pain001-loader-mt101/) |

The [glossary](/glossary/) defines the rest of the ISO 20022 vocabulary in plain English.

## Why banks reject pain.001 files

A file can be well-formed XML and still be rejected. The checks stack up in layers:

1. **Schema:** the file must validate against the official XSD for its version.
2. **Data quality:** IBANs pass their check digits, BICs are well formed, dates and amounts are valid, and `NbOfTxs` and `CtrlSum` match the payments.
3. **Scheme rules:** SEPA, CBPR+ and domestic schemes add their own constraints, such as the allowed character set or a structured postal address.
4. **Your bank's profile and channel:** each bank publishes its own usage guidelines on top of the scheme.

Pain001 checks the first three layers before the file reaches the bank and states plainly that the fourth is the bank's to confirm.

## How to create a pain.001 file

- **From a spreadsheet:** [Excel to pain.001](/excel-to-pain001/) turns an Excel or CSV payment list into a validated file.
- **In the browser:** the [demo](/try/) generates and validates a file locally, with no upload.
- **From code or the command line:** install the open-source [pain001 library](/installation/) and run:

```bash
pain001 -t pain.001.001.09 -d payments.csv -o out/
```

The [technical reference](/documentation/) covers every option, and the [FAQs](/faqs/) answer the questions treasury, operations and engineering teams ask most.

## Sources

- ISO 20022 message definitions and archive: [iso20022.org](https://www.iso20022.org/iso-20022-message-definitions)
- SEPA Credit Transfer rulebook: [European Payments Council](https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-credit-transfer-sct/sepa-credit-transfer-rulebook-and)
- CBPR+ and the MT101 relay: [Swift](https://www.swift.com/news-events/news/swift-accepts-community-request-extend-structured-address-migration-iso-20022-payment-messages)
