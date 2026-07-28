---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Complex types AccountIdentification4Choice – GenericFinancialIdentification1 in ISO 20022 pain.001.001.06, with elements, cardinality and constraints, generated from the official XSD."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complex types AccountIdentification4Choice – GenericFinancialIdentification1 in ISO 20022 pain.001.001.06, with elements, cardinality and constraints, generated from the official XSD."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/message-spec-pain.001.001.06-types/"
image_alt: "Complex types AccountIdentification4Choice – GenericFinancialIdentification1 in ISO 20022 pain.001.001.06, with elements, cardinality and constraints, generated from the official XSD."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001.001.06 types, ISO 20022 complex types, cardinality, field mapping"
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
permalink: "https://pain001.com/message-spec-pain.001.001.06-types/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Types AccountIdentification4Choice – GenericFinancialIdentification1 in pain.001.001.06, defined once each — the view to use for field mapping."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.001.001.06 type reference (part 1 of 3) — AccountIdentification4Choice – GenericFinancialIdentification1"
url: "https://pain001.com/message-spec-pain.001.001.06-types/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/message-spec-pain.001.001.06-types/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Complex types AccountIdentification4Choice – GenericFinancialIdentification1 in ISO 20022 pain.001.001.06, with elements, cardinality and constraints, generated from the official XSD."
item_guid: "https://pain001.com/message-spec-pain.001.001.06-types/"
item_link: "https://pain001.com/message-spec-pain.001.001.06-types/"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.001.001.06 type reference (part 1 of 3) — AccountIdentification4Choice – GenericFinancialIdentification1"
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
apple-mobile-web-app-title: "pain.001.001.06 type reference (part 1 of 3) — AccountIdentification4Choice – GenericFinancialIdentification1"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Complex types AccountIdentification4Choice – GenericFinancialIdentification1 in ISO 20022 pain.001.001.06, with elements, cardinality and constraints, generated from the official XSD."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.001.001.06 type reference (part 1 of 3) — AccountIdentification4Choice – GenericFinancialIdentification1"
twitter_url: "https://pain001.com/message-spec-pain.001.001.06-types/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message specification"
excerpt: "Complex types AccountIdentification4Choice – GenericFinancialIdentification1 in ISO 20022 pain.001.001.06, with elements, cardinality and constraints, generated from the official XSD."
last_reviewed: "2026-07-26"


---

Complex types in ISO 20022 `pain.001.001.06`, generated from the official XSD. **Part 1 of 3** — `AccountIdentification4Choice – GenericFinancialIdentification1`.

**Part 1** · [Part 2](/message-spec-pain.001.001.06-types-2/) · [Part 3](/message-spec-pain.001.001.06-types-3/)

Each type is defined once here. The [message structure](/message-spec-pain.001.001.06/) repeats a party or address block under every party; this view does not, which is what you want when mapping source fields.

A **choice** type means the children are alternatives — supply one, not all. Cardinality in **bold** is required.

## `AccountIdentification4Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `IBAN` | **1..1** | `IBAN2007Identifier` | pattern `[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}` |
| `Othr` | **1..1** | `GenericAccountIdentification1` |  |

## `AccountSchemeName1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalAccountIdentification1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `AmountType4Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `InstdAmt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |
| `EqvtAmt` | **1..1** | `EquivalentAmount2` |  |

## `Authorisation1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `Authorisation1Code` | 4 codes |
| `Prtry` | **1..1** | `Max128Text` | length 1–128 |

## `BranchAndFinancialInstitutionIdentification5`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `FinInstnId` | **1..1** | `FinancialInstitutionIdentification8` |  |
| `BrnchId` | 0..1 | `BranchData2` |  |

## `BranchData2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | 0..1 | `Max35Text` | length 1–35 |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PstlAdr` | 0..1 | `PostalAddress6` |  |

## `CashAccount24`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `AccountIdentification4Choice` |  |
| `Tp` | 0..1 | `CashAccountType2Choice` |  |
| `Ccy` | 0..1 | `ActiveOrHistoricCurrencyCode` | pattern `[A-Z]{3,3}` |
| `Nm` | 0..1 | `Max70Text` | length 1–70 |

## `CashAccountType2Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalCashAccountType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `CategoryPurpose1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalCategoryPurpose1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `Cheque7`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `ChqTp` | 0..1 | `ChequeType2Code` | 5 codes |
| `ChqNb` | 0..1 | `Max35Text` | length 1–35 |
| `ChqFr` | 0..1 | `NameAndAddress10` |  |
| `DlvryMtd` | 0..1 | `ChequeDeliveryMethod1Choice` |  |
| `DlvrTo` | 0..1 | `NameAndAddress10` |  |
| `InstrPrty` | 0..1 | `Priority2Code` | 2 codes |
| `ChqMtrtyDt` | 0..1 | `ISODate` |  |
| `FrmsCd` | 0..1 | `Max35Text` | length 1–35 |
| `MemoFld` | 0..2 | `Max35Text` | length 1–35 |
| `RgnlClrZone` | 0..1 | `Max35Text` | length 1–35 |
| `PrtLctn` | 0..1 | `Max35Text` | length 1–35 |
| `Sgntr` | 0..5 | `Max70Text` | length 1–70 |

## `ChequeDeliveryMethod1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ChequeDelivery1Code` | 12 codes |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `ClearingSystemIdentification2Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalClearingSystemIdentification1Code` | length 1–5 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `ClearingSystemMemberIdentification2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `ClrSysId` | 0..1 | `ClearingSystemIdentification2Choice` |  |
| `MmbId` | **1..1** | `Max35Text` | length 1–35 |

## `ContactDetails2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `NmPrfx` | 0..1 | `NamePrefix1Code` | 4 codes |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PhneNb` | 0..1 | `PhoneNumber` | pattern `\+[0-9]{1,3}-[0-9()+\-]{1,30}` |
| `MobNb` | 0..1 | `PhoneNumber` | pattern `\+[0-9]{1,3}-[0-9()+\-]{1,30}` |
| `FaxNb` | 0..1 | `PhoneNumber` | pattern `\+[0-9]{1,3}-[0-9()+\-]{1,30}` |
| `EmailAdr` | 0..1 | `Max2048Text` | length 1–2048 |
| `Othr` | 0..1 | `Max35Text` | length 1–35 |

## `CreditTransferTransaction20`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `PmtId` | **1..1** | `PaymentIdentification1` |  |
| `PmtTpInf` | 0..1 | `PaymentTypeInformation19` |  |
| `Amt` | **1..1** | `AmountType4Choice` |  |
| `XchgRateInf` | 0..1 | `ExchangeRate1` |  |
| `ChrgBr` | 0..1 | `ChargeBearerType1Code` | 4 codes |
| `ChqInstr` | 0..1 | `Cheque7` |  |
| `UltmtDbtr` | 0..1 | `PartyIdentification43` |  |
| `IntrmyAgt1` | 0..1 | `BranchAndFinancialInstitutionIdentification5` |  |
| `IntrmyAgt1Acct` | 0..1 | `CashAccount24` |  |
| `IntrmyAgt2` | 0..1 | `BranchAndFinancialInstitutionIdentification5` |  |
| `IntrmyAgt2Acct` | 0..1 | `CashAccount24` |  |
| `IntrmyAgt3` | 0..1 | `BranchAndFinancialInstitutionIdentification5` |  |
| `IntrmyAgt3Acct` | 0..1 | `CashAccount24` |  |
| `CdtrAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification5` |  |
| `CdtrAgtAcct` | 0..1 | `CashAccount24` |  |
| `Cdtr` | 0..1 | `PartyIdentification43` |  |
| `CdtrAcct` | 0..1 | `CashAccount24` |  |
| `UltmtCdtr` | 0..1 | `PartyIdentification43` |  |
| `InstrForCdtrAgt` | 0..* | `InstructionForCreditorAgent1` |  |
| `InstrForDbtrAgt` | 0..1 | `Max140Text` | length 1–140 |
| `Purp` | 0..1 | `Purpose2Choice` |  |
| `RgltryRptg` | 0..10 | `RegulatoryReporting3` |  |
| `Tax` | 0..1 | `TaxInformation3` |  |
| `RltdRmtInf` | 0..10 | `RemittanceLocation4` |  |
| `RmtInf` | 0..1 | `RemittanceInformation10` |  |
| `SplmtryData` | 0..* | `SupplementaryData1` |  |

## `CreditorReferenceInformation2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `CreditorReferenceType2` |  |
| `Ref` | 0..1 | `Max35Text` | length 1–35 |

## `CreditorReferenceType1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `DocumentType3Code` | 6 codes |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `CreditorReferenceType2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CdOrPrtry` | **1..1** | `CreditorReferenceType1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `CustomerCreditTransferInitiationV06`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `GrpHdr` | **1..1** | `GroupHeader48` |  |
| `PmtInf` | **1..*** | `PaymentInstruction16` |  |
| `SplmtryData` | 0..* | `SupplementaryData1` |  |

## `DateAndPlaceOfBirth`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `BirthDt` | **1..1** | `ISODate` |  |
| `PrvcOfBirth` | 0..1 | `Max35Text` | length 1–35 |
| `CityOfBirth` | **1..1** | `Max35Text` | length 1–35 |
| `CtryOfBirth` | **1..1** | `CountryCode` | pattern `[A-Z]{2,2}` |

## `DatePeriodDetails`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `FrDt` | **1..1** | `ISODate` |  |
| `ToDt` | **1..1** | `ISODate` |  |

## `DiscountAmountAndType1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `DiscountAmountType1Choice` |  |
| `Amt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |

## `DiscountAmountType1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalDiscountAmountType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `Document`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CstmrCdtTrfInitn` | **1..1** | `CustomerCreditTransferInitiationV06` |  |

## `DocumentAdjustment1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Amt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |
| `CdtDbtInd` | 0..1 | `CreditDebitCode` | 2 codes |
| `Rsn` | 0..1 | `Max4Text` | length 1–4 |
| `AddtlInf` | 0..1 | `Max140Text` | length 1–140 |

## `EquivalentAmount2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Amt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |
| `CcyOfTrf` | **1..1** | `ActiveOrHistoricCurrencyCode` | pattern `[A-Z]{3,3}` |

## `ExchangeRate1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `UnitCcy` | 0..1 | `ActiveOrHistoricCurrencyCode` | pattern `[A-Z]{3,3}` |
| `XchgRate` | 0..1 | `BaseOneRate` | 10 decimals max |
| `RateTp` | 0..1 | `ExchangeRateType1Code` | 3 codes |
| `CtrctId` | 0..1 | `Max35Text` | length 1–35 |

## `FinancialIdentificationSchemeName1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalFinancialInstitutionIdentification1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `FinancialInstitutionIdentification8`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `BICFI` | 0..1 | `BICFIIdentifier` | pattern `[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3…` |
| `ClrSysMmbId` | 0..1 | `ClearingSystemMemberIdentification2` |  |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PstlAdr` | 0..1 | `PostalAddress6` |  |
| `Othr` | 0..1 | `GenericFinancialIdentification1` |  |

## `Garnishment1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | **1..1** | `GarnishmentType1` |  |
| `Grnshee` | 0..1 | `PartyIdentification43` |  |
| `GrnshmtAdmstr` | 0..1 | `PartyIdentification43` |  |
| `RefNb` | 0..1 | `Max140Text` | length 1–140 |
| `Dt` | 0..1 | `ISODate` |  |
| `RmtdAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `FmlyMdclInsrncInd` | 0..1 | `TrueFalseIndicator` |  |
| `MplyeeTermntnInd` | 0..1 | `TrueFalseIndicator` |  |

## `GarnishmentType1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CdOrPrtry` | **1..1** | `GarnishmentType1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `GarnishmentType1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalGarnishmentType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `GenericAccountIdentification1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `Max34Text` | length 1–34 |
| `SchmeNm` | 0..1 | `AccountSchemeName1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `GenericFinancialIdentification1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `Max35Text` | length 1–35 |
| `SchmeNm` | 0..1 | `FinancialIdentificationSchemeName1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |
