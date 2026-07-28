---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Every element of ISO 20022 pain.001.001.03: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Every element of ISO 20022 pain.001.001.03: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/message-spec-pain.001.001.03/"
image_alt: "Every element of ISO 20022 pain.001.001.03: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001.001.03, ISO 20022, element reference, cardinality, code lists, XML path, message specification, pain.001"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/message-spec-pain.001.001.03/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "All 529 elements of pain.001.001.03 with cardinality, types and code lists, generated from the official ISO schema."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.001.001.03 — complete element reference"
url: "https://pain001.com/message-spec-pain.001.001.03/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/message-spec-pain.001.001.03/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Every element of ISO 20022 pain.001.001.03: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
item_guid: "https://pain001.com/message-spec-pain.001.001.03/"
item_link: "https://pain001.com/message-spec-pain.001.001.03/"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.001.001.03 — complete element reference"
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
apple-mobile-web-app-title: "pain.001.001.03 — complete element reference"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Every element of ISO 20022 pain.001.001.03: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.001.001.03 — complete element reference"
twitter_url: "https://pain001.com/message-spec-pain.001.001.03/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message specification"
excerpt: "Every element of ISO 20022 pain.001.001.03: XML path, cardinality, data type, length and pattern constraints, and code lists — generated from the official XSD."
last_reviewed: "2026-07-26"


---

This is the complete element reference for `pain.001.001.03`, generated directly from the official ISO 20022 XSD that Pain001 validates against — not transcribed by hand. Every cardinality, type and code value below can be checked against ISO's own publication.

**529 elements** · **113 required** · **66 types** · **17 code lists**

Cardinality is shown as ISO writes it: `0..1` optional, `1..1` required, `0..*` repeating. Required elements are **bold** — those are the ones whose absence makes the document invalid before any bank sees it.

## CstmrCdtTrfInitn

| Element | Path | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `CstmrCdtTrfInitn` | `CstmrCdtTrfInitn` | **1..1** | `CustomerCreditTransferInitiationV03` |  |

## GrpHdr

*Group Header — one per message*

| Element | Path | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| &nbsp;&nbsp;`GrpHdr` | `CstmrCdtTrfInitn/GrpHdr` | **1..1** | `GroupHeader32` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`MsgId` | `CstmrCdtTrfInitn/GrpHdr/MsgId` | **1..1** | `Max35Text` | length 1–35 |
| &nbsp;&nbsp;&nbsp;&nbsp;`CreDtTm` | `CstmrCdtTrfInitn/GrpHdr/CreDtTm` | **1..1** | `ISODateTime` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`Authstn` | `CstmrCdtTrfInitn/GrpHdr/Authstn` | 0..2 | `Authorisation1Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Cd` | `CstmrCdtTrfInitn/GrpHdr/Authstn/Cd` | **1..1** | `Authorisation1Code` | 4 codes |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Prtry` | `CstmrCdtTrfInitn/GrpHdr/Authstn/Prtry` | **1..1** | `Max128Text` | length 1–128 |
| &nbsp;&nbsp;&nbsp;&nbsp;`NbOfTxs` | `CstmrCdtTrfInitn/GrpHdr/NbOfTxs` | **1..1** | `Max15NumericText` | pattern `[0-9]{1,15}` |
| &nbsp;&nbsp;&nbsp;&nbsp;`CtrlSum` | `CstmrCdtTrfInitn/GrpHdr/CtrlSum` | 0..1 | `DecimalNumber` | 17 decimals max |
| &nbsp;&nbsp;&nbsp;&nbsp;`InitgPty` | `CstmrCdtTrfInitn/GrpHdr/InitgPty` | **1..1** | `PartyIdentification32` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Nm` | `CstmrCdtTrfInitn/GrpHdr/InitgPty/Nm` | 0..1 | `Max140Text` | length 1–140 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PstlAdr` | `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr` | 0..1 | `PostalAddress6` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Id` | `CstmrCdtTrfInitn/GrpHdr/InitgPty/Id` | 0..1 | `Party6Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CtryOfRes` | `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtryOfRes` | 0..1 | `CountryCode` | pattern `[A-Z]{2,2}` |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CtctDtls` | `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls` | 0..1 | `ContactDetails2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`FwdgAgt` | `CstmrCdtTrfInitn/GrpHdr/FwdgAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification4` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FinInstnId` | `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId` | **1..1** | `FinancialInstitutionIdentification7` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`BrnchId` | `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId` | 0..1 | `BranchData2` |  |

*56 further nested elements sit below this depth — every one of them is defined in the type reference below, which lists each type once instead of repeating it under every party.*

## PmtInf

*Payment Information — one per debtor account and execution date*

| Element | Path | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| &nbsp;&nbsp;`PmtInf` | `CstmrCdtTrfInitn/PmtInf` | **1..*** | `PaymentInstructionInformation3` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`PmtInfId` | `CstmrCdtTrfInitn/PmtInf/PmtInfId` | **1..1** | `Max35Text` | length 1–35 |
| &nbsp;&nbsp;&nbsp;&nbsp;`PmtMtd` | `CstmrCdtTrfInitn/PmtInf/PmtMtd` | **1..1** | `PaymentMethod3Code` | 3 codes |
| &nbsp;&nbsp;&nbsp;&nbsp;`BtchBookg` | `CstmrCdtTrfInitn/PmtInf/BtchBookg` | 0..1 | `BatchBookingIndicator` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`NbOfTxs` | `CstmrCdtTrfInitn/PmtInf/NbOfTxs` | 0..1 | `Max15NumericText` | pattern `[0-9]{1,15}` |
| &nbsp;&nbsp;&nbsp;&nbsp;`CtrlSum` | `CstmrCdtTrfInitn/PmtInf/CtrlSum` | 0..1 | `DecimalNumber` | 17 decimals max |
| &nbsp;&nbsp;&nbsp;&nbsp;`PmtTpInf` | `CstmrCdtTrfInitn/PmtInf/PmtTpInf` | 0..1 | `PaymentTypeInformation19` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`InstrPrty` | `CstmrCdtTrfInitn/PmtInf/PmtTpInf/InstrPrty` | 0..1 | `Priority2Code` | 2 codes |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`SvcLvl` | `CstmrCdtTrfInitn/PmtInf/PmtTpInf/SvcLvl` | 0..1 | `ServiceLevel8Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`LclInstrm` | `CstmrCdtTrfInitn/PmtInf/PmtTpInf/LclInstrm` | 0..1 | `LocalInstrument2Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CtgyPurp` | `CstmrCdtTrfInitn/PmtInf/PmtTpInf/CtgyPurp` | 0..1 | `CategoryPurpose1Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`ReqdExctnDt` | `CstmrCdtTrfInitn/PmtInf/ReqdExctnDt` | **1..1** | `ISODate` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`PoolgAdjstmntDt` | `CstmrCdtTrfInitn/PmtInf/PoolgAdjstmntDt` | 0..1 | `ISODate` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`Dbtr` | `CstmrCdtTrfInitn/PmtInf/Dbtr` | **1..1** | `PartyIdentification32` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Nm` | `CstmrCdtTrfInitn/PmtInf/Dbtr/Nm` | 0..1 | `Max140Text` | length 1–140 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PstlAdr` | `CstmrCdtTrfInitn/PmtInf/Dbtr/PstlAdr` | 0..1 | `PostalAddress6` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Id` | `CstmrCdtTrfInitn/PmtInf/Dbtr/Id` | 0..1 | `Party6Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CtryOfRes` | `CstmrCdtTrfInitn/PmtInf/Dbtr/CtryOfRes` | 0..1 | `CountryCode` | pattern `[A-Z]{2,2}` |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CtctDtls` | `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls` | 0..1 | `ContactDetails2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`DbtrAcct` | `CstmrCdtTrfInitn/PmtInf/DbtrAcct` | **1..1** | `CashAccount16` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Id` | `CstmrCdtTrfInitn/PmtInf/DbtrAcct/Id` | **1..1** | `AccountIdentification4Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Tp` | `CstmrCdtTrfInitn/PmtInf/DbtrAcct/Tp` | 0..1 | `CashAccountType2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Ccy` | `CstmrCdtTrfInitn/PmtInf/DbtrAcct/Ccy` | 0..1 | `ActiveOrHistoricCurrencyCode` | pattern `[A-Z]{3,3}` |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Nm` | `CstmrCdtTrfInitn/PmtInf/DbtrAcct/Nm` | 0..1 | `Max70Text` | length 1–70 |
| &nbsp;&nbsp;&nbsp;&nbsp;`DbtrAgt` | `CstmrCdtTrfInitn/PmtInf/DbtrAgt` | **1..1** | `BranchAndFinancialInstitutionIdentification4` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FinInstnId` | `CstmrCdtTrfInitn/PmtInf/DbtrAgt/FinInstnId` | **1..1** | `FinancialInstitutionIdentification7` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`BrnchId` | `CstmrCdtTrfInitn/PmtInf/DbtrAgt/BrnchId` | 0..1 | `BranchData2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`DbtrAgtAcct` | `CstmrCdtTrfInitn/PmtInf/DbtrAgtAcct` | 0..1 | `CashAccount16` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Id` | `CstmrCdtTrfInitn/PmtInf/DbtrAgtAcct/Id` | **1..1** | `AccountIdentification4Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Tp` | `CstmrCdtTrfInitn/PmtInf/DbtrAgtAcct/Tp` | 0..1 | `CashAccountType2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Ccy` | `CstmrCdtTrfInitn/PmtInf/DbtrAgtAcct/Ccy` | 0..1 | `ActiveOrHistoricCurrencyCode` | pattern `[A-Z]{3,3}` |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Nm` | `CstmrCdtTrfInitn/PmtInf/DbtrAgtAcct/Nm` | 0..1 | `Max70Text` | length 1–70 |
| &nbsp;&nbsp;&nbsp;&nbsp;`UltmtDbtr` | `CstmrCdtTrfInitn/PmtInf/UltmtDbtr` | 0..1 | `PartyIdentification32` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Nm` | `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/Nm` | 0..1 | `Max140Text` | length 1–140 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PstlAdr` | `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/PstlAdr` | 0..1 | `PostalAddress6` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Id` | `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/Id` | 0..1 | `Party6Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CtryOfRes` | `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/CtryOfRes` | 0..1 | `CountryCode` | pattern `[A-Z]{2,2}` |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CtctDtls` | `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/CtctDtls` | 0..1 | `ContactDetails2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`ChrgBr` | `CstmrCdtTrfInitn/PmtInf/ChrgBr` | 0..1 | `ChargeBearerType1Code` | 4 codes |
| &nbsp;&nbsp;&nbsp;&nbsp;`ChrgsAcct` | `CstmrCdtTrfInitn/PmtInf/ChrgsAcct` | 0..1 | `CashAccount16` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Id` | `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Id` | **1..1** | `AccountIdentification4Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Tp` | `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Tp` | 0..1 | `CashAccountType2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Ccy` | `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Ccy` | 0..1 | `ActiveOrHistoricCurrencyCode` | pattern `[A-Z]{3,3}` |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Nm` | `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Nm` | 0..1 | `Max70Text` | length 1–70 |
| &nbsp;&nbsp;&nbsp;&nbsp;`ChrgsAcctAgt` | `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification4` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FinInstnId` | `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId` | **1..1** | `FinancialInstitutionIdentification7` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`BrnchId` | `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId` | 0..1 | `BranchData2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`CdtTrfTxInf` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf` | **1..*** | `CreditTransferTransactionInformation10` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PmtId` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/PmtId` | **1..1** | `PaymentIdentification1` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PmtTpInf` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/PmtTpInf` | 0..1 | `PaymentTypeInformation19` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Amt` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Amt` | **1..1** | `AmountType3Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`XchgRateInf` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/XchgRateInf` | 0..1 | `ExchangeRateInformation1` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ChrgBr` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/ChrgBr` | 0..1 | `ChargeBearerType1Code` | 4 codes |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ChqInstr` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/ChqInstr` | 0..1 | `Cheque6` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`UltmtDbtr` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr` | 0..1 | `PartyIdentification32` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`IntrmyAgt1` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1` | 0..1 | `BranchAndFinancialInstitutionIdentification4` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`IntrmyAgt1Acct` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1Acct` | 0..1 | `CashAccount16` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`IntrmyAgt2` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2` | 0..1 | `BranchAndFinancialInstitutionIdentification4` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`IntrmyAgt2Acct` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2Acct` | 0..1 | `CashAccount16` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`IntrmyAgt3` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3` | 0..1 | `BranchAndFinancialInstitutionIdentification4` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`IntrmyAgt3Acct` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3Acct` | 0..1 | `CashAccount16` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CdtrAgt` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification4` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CdtrAgtAcct` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgtAcct` | 0..1 | `CashAccount16` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Cdtr` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr` | 0..1 | `PartyIdentification32` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CdtrAcct` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAcct` | 0..1 | `CashAccount16` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`UltmtCdtr` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr` | 0..1 | `PartyIdentification32` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`InstrForCdtrAgt` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/InstrForCdtrAgt` | 0..* | `InstructionForCreditorAgent1` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`InstrForDbtrAgt` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/InstrForDbtrAgt` | 0..1 | `Max140Text` | length 1–140 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Purp` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Purp` | 0..1 | `Purpose2Choice` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`RgltryRptg` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RgltryRptg` | 0..10 | `RegulatoryReporting3` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Tax` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Tax` | 0..1 | `TaxInformation3` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`RltdRmtInf` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf` | 0..10 | `RemittanceLocation2` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`RmtInf` | `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RmtInf` | 0..1 | `RemittanceInformation5` |  |

*382 further nested elements sit below this depth — every one of them is defined in the type reference below, which lists each type once instead of repeating it under every party.*

## Type reference

Every complex type in this version is defined once on the [**pain.001.001.03 type reference**](/message-spec-pain.001.001.03-types/) — 65 types. The tree above repeats a party or address structure under each party; the type reference does not, which makes it the better page for mapping work.

## Code lists used by this version

| Code list | Values |
| :--- | :--- |
| `AddressType2Code` | `ADDR`, `PBOX`, `HOME`, `BIZZ`, `MLTO`, `DLVY` |
| `Authorisation1Code` | `AUTH`, `FDET`, `FSUM`, `ILEV` |
| `CashAccountType4Code` | `CASH`, `CHAR`, `COMM`, `TAXE`, `CISH`, `TRAS`, `SACC`, `CACC`, `SVGS`, `ONDP`, `MGLD`, `NREX`, `MOMA`, `LOAN` *(+2 more)* |
| `ChargeBearerType1Code` | `DEBT`, `CRED`, `SHAR`, `SLEV` |
| `ChequeDelivery1Code` | `MLDB`, `MLCD`, `MLFA`, `CRDB`, `CRCD`, `CRFA`, `PUDB`, `PUCD`, `PUFA`, `RGDB`, `RGCD`, `RGFA` |
| `ChequeType2Code` | `CCHQ`, `CCCH`, `BCHQ`, `DRFT`, `ELDR` |
| `CreditDebitCode` | `CRDT`, `DBIT` |
| `DocumentType3Code` | `RADM`, `RPIN`, `FXDR`, `DISP`, `PUOR`, `SCOR` |
| `DocumentType5Code` | `MSIN`, `CNFA`, `DNFA`, `CINV`, `CREN`, `DEBN`, `HIRI`, `SBIN`, `CMCN`, `SOAC`, `DISP`, `BOLD`, `VCHR`, `AROI` *(+1 more)* |
| `ExchangeRateType1Code` | `SPOT`, `SALE`, `AGRD` |
| `Instruction3Code` | `CHQB`, `HOLD`, `PHOB`, `TELB` |
| `NamePrefix1Code` | `DOCT`, `MIST`, `MISS`, `MADM` |
| `PaymentMethod3Code` | `CHK`, `TRF`, `TRA` |
| `Priority2Code` | `HIGH`, `NORM` |
| `RegulatoryReportingType1Code` | `CRED`, `DEBT`, `BOTH` |
| `RemittanceLocationMethod2Code` | `FAXI`, `EDIC`, `URID`, `EMAL`, `POST`, `SMSM` |
| `TaxRecordPeriod1Code` | `MM01`, `MM02`, `MM03`, `MM04`, `MM05`, `MM06`, `MM07`, `MM08`, `MM09`, `MM10`, `MM11`, `MM12`, `QTR1`, `QTR2` *(+4 more)* |

The full value set for every list is on the [code lists page](/message-spec-code-lists/).

## Generate and validate this version

```bash
pain001 -t pain.001.001.03 -d payments.csv -o out/ --dry-run
```

See the [narrative page for pain.001.001.03](/pain.001.001.03/) for what distinguishes this version and when to choose it, the [full compatibility matrix](/compatibility/), or [what changed between versions](/message-spec-changes/).
