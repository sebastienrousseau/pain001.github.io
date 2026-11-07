---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Complex types AccountIdentification4Choice – FrequencyPeriod1 in ISO 20022 pain.008.001.08, with elements, cardinality and constraints, generated from the official XSD."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complex types AccountIdentification4Choice – FrequencyPeriod1 in ISO 20022 pain.008.001.08, with elements, cardinality and constraints, generated from the official XSD."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/message-spec-pain.008.001.08-types/"
image_alt: "Complex types AccountIdentification4Choice – FrequencyPeriod1 in ISO 20022 pain.008.001.08, with elements, cardinality and constraints, generated from the official XSD."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.008.001.08 types, ISO 20022 complex types, cardinality, field mapping"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/message-spec-pain.008.001.08-types/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Types AccountIdentification4Choice – FrequencyPeriod1 in pain.008.001.08, defined once each. This is the view to use for field mapping."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.008.001.08 type reference (part 1 of 3)"
url: "https://pain001.com/message-spec-pain.008.001.08-types/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/message-spec-pain.008.001.08-types/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.75)"
item_description: "Complex types AccountIdentification4Choice – FrequencyPeriod1 in ISO 20022 pain.008.001.08, with elements, cardinality and constraints, generated from the official XSD."
item_guid: "https://pain001.com/message-spec-pain.008.001.08-types/"
item_link: "https://pain001.com/message-spec-pain.008.001.08-types/"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.008.001.08 type reference (part 1 of 3)"
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
apple-mobile-web-app-title: "pain.008.001.08 type reference (part 1 of 3)"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "Complex types AccountIdentification4Choice – FrequencyPeriod1 in ISO 20022 pain.008.001.08, with elements, cardinality and constraints, generated from the official XSD."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "pain.008.001.08 type reference (part 1 of 3)"
twitter_url: "https://pain001.com/message-spec-pain.008.001.08-types/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message specification"
excerpt: "Complex types AccountIdentification4Choice – FrequencyPeriod1 in ISO 20022 pain.008.001.08, with elements, cardinality and constraints, generated from the official XSD."
last_reviewed: "2026-07-26"


---

Complex types in ISO 20022 `pain.008.001.08`, generated from the official XSD. **Part 1 of 3**: `AccountIdentification4Choice – FrequencyPeriod1`.

**Part 1** · [Part 2](/message-spec-pain.008.001.08-types-2/) · [Part 3](/message-spec-pain.008.001.08-types-3/)

Each type is defined once here. The [message structure](/message-spec-pain.008.001.08/) repeats a party or address block under every party; this view does not, which is what you want when mapping source fields.

A **choice** type means the children are alternatives: supply one, not all. Cardinality in **bold** is required.

## `AccountIdentification4Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `IBAN` | **1..1** | `IBAN2007Identifier` | pattern `[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}` |
| `Othr` | **1..1** | `GenericAccountIdentification1` |  |

## `AccountSchemeName1Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalAccountIdentification1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `AddressType3Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `AddressType2Code` | 6 codes |
| `Prtry` | **1..1** | `GenericIdentification30` |  |

## `AmendmentInformationDetails13`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `OrgnlMndtId` | 0..1 | `Max35Text` | length 1–35 |
| `OrgnlCdtrSchmeId` | 0..1 | `PartyIdentification135` |  |
| `OrgnlCdtrAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification6` |  |
| `OrgnlCdtrAgtAcct` | 0..1 | `CashAccount38` |  |
| `OrgnlDbtr` | 0..1 | `PartyIdentification135` |  |
| `OrgnlDbtrAcct` | 0..1 | `CashAccount38` |  |
| `OrgnlDbtrAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification6` |  |
| `OrgnlDbtrAgtAcct` | 0..1 | `CashAccount38` |  |
| `OrgnlFnlColltnDt` | 0..1 | `ISODate` |  |
| `OrgnlFrqcy` | 0..1 | `Frequency36Choice` |  |
| `OrgnlRsn` | 0..1 | `MandateSetupReason1Choice` |  |
| `OrgnlTrckgDays` | 0..1 | `Exact2NumericText` | pattern `[0-9]{2}` |

## `Authorisation1Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `Authorisation1Code` | 4 codes |
| `Prtry` | **1..1** | `Max128Text` | length 1–128 |

## `BranchAndFinancialInstitutionIdentification6`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `FinInstnId` | **1..1** | `FinancialInstitutionIdentification18` |  |
| `BrnchId` | 0..1 | `BranchData3` |  |

## `BranchData3`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | 0..1 | `Max35Text` | length 1–35 |
| `LEI` | 0..1 | `LEIIdentifier` | pattern `[A-Z0-9]{18,18}[0-9]{2,2}` |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PstlAdr` | 0..1 | `PostalAddress24` |  |

## `CashAccount38`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `AccountIdentification4Choice` |  |
| `Tp` | 0..1 | `CashAccountType2Choice` |  |
| `Ccy` | 0..1 | `ActiveOrHistoricCurrencyCode` | pattern `[A-Z]{3,3}` |
| `Nm` | 0..1 | `Max70Text` | length 1–70 |
| `Prxy` | 0..1 | `ProxyAccountIdentification1` |  |

## `CashAccountType2Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalCashAccountType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `CategoryPurpose1Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalCategoryPurpose1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `ClearingSystemIdentification2Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalClearingSystemIdentification1Code` | length 1–5 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `ClearingSystemMemberIdentification2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `ClrSysId` | 0..1 | `ClearingSystemIdentification2Choice` |  |
| `MmbId` | **1..1** | `Max35Text` | length 1–35 |

## `Contact4`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `NmPrfx` | 0..1 | `NamePrefix2Code` | 5 codes |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PhneNb` | 0..1 | `PhoneNumber` | pattern `\+[0-9]{1,3}-[0-9()+\-]{1,30}` |
| `MobNb` | 0..1 | `PhoneNumber` | pattern `\+[0-9]{1,3}-[0-9()+\-]{1,30}` |
| `FaxNb` | 0..1 | `PhoneNumber` | pattern `\+[0-9]{1,3}-[0-9()+\-]{1,30}` |
| `EmailAdr` | 0..1 | `Max2048Text` | length 1–2048 |
| `EmailPurp` | 0..1 | `Max35Text` | length 1–35 |
| `JobTitl` | 0..1 | `Max35Text` | length 1–35 |
| `Rspnsblty` | 0..1 | `Max35Text` | length 1–35 |
| `Dept` | 0..1 | `Max70Text` | length 1–70 |
| `Othr` | 0..* | `OtherContact1` |  |
| `PrefrdMtd` | 0..1 | `PreferredContactMethod1Code` | 5 codes |

## `CreditorReferenceInformation2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `CreditorReferenceType2` |  |
| `Ref` | 0..1 | `Max35Text` | length 1–35 |

## `CreditorReferenceType1Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `DocumentType3Code` | 6 codes |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `CreditorReferenceType2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CdOrPrtry` | **1..1** | `CreditorReferenceType1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `CustomerDirectDebitInitiationV08`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `GrpHdr` | **1..1** | `GroupHeader83` |  |
| `PmtInf` | **1..*** | `PaymentInstruction29` |  |
| `SplmtryData` | 0..* | `SupplementaryData1` |  |

## `DateAndPlaceOfBirth1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `BirthDt` | **1..1** | `ISODate` |  |
| `PrvcOfBirth` | 0..1 | `Max35Text` | length 1–35 |
| `CityOfBirth` | **1..1** | `Max35Text` | length 1–35 |
| `CtryOfBirth` | **1..1** | `CountryCode` | pattern `[A-Z]{2,2}` |

## `DatePeriod2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `FrDt` | **1..1** | `ISODate` |  |
| `ToDt` | **1..1** | `ISODate` |  |

## `DirectDebitTransaction10`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `MndtRltdInf` | 0..1 | `MandateRelatedInformation14` |  |
| `CdtrSchmeId` | 0..1 | `PartyIdentification135` |  |
| `PreNtfctnId` | 0..1 | `Max35Text` | length 1–35 |
| `PreNtfctnDt` | 0..1 | `ISODate` |  |

## `DirectDebitTransactionInformation23`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `PmtId` | **1..1** | `PaymentIdentification6` |  |
| `PmtTpInf` | 0..1 | `PaymentTypeInformation29` |  |
| `InstdAmt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |
| `ChrgBr` | 0..1 | `ChargeBearerType1Code` | 4 codes |
| `DrctDbtTx` | 0..1 | `DirectDebitTransaction10` |  |
| `UltmtCdtr` | 0..1 | `PartyIdentification135` |  |
| `DbtrAgt` | **1..1** | `BranchAndFinancialInstitutionIdentification6` |  |
| `DbtrAgtAcct` | 0..1 | `CashAccount38` |  |
| `Dbtr` | **1..1** | `PartyIdentification135` |  |
| `DbtrAcct` | **1..1** | `CashAccount38` |  |
| `UltmtDbtr` | 0..1 | `PartyIdentification135` |  |
| `InstrForCdtrAgt` | 0..1 | `Max140Text` | length 1–140 |
| `Purp` | 0..1 | `Purpose2Choice` |  |
| `RgltryRptg` | 0..10 | `RegulatoryReporting3` |  |
| `Tax` | 0..1 | `TaxInformation8` |  |
| `RltdRmtInf` | 0..10 | `RemittanceLocation7` |  |
| `RmtInf` | 0..1 | `RemittanceInformation16` |  |
| `SplmtryData` | 0..* | `SupplementaryData1` |  |

## `DiscountAmountAndType1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `DiscountAmountType1Choice` |  |
| `Amt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |

## `DiscountAmountType1Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalDiscountAmountType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `Document`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CstmrDrctDbtInitn` | **1..1** | `CustomerDirectDebitInitiationV08` |  |

## `DocumentAdjustment1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Amt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |
| `CdtDbtInd` | 0..1 | `CreditDebitCode` | 2 codes |
| `Rsn` | 0..1 | `Max4Text` | length 1–4 |
| `AddtlInf` | 0..1 | `Max140Text` | length 1–140 |

## `DocumentLineIdentification1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `DocumentLineType1` |  |
| `Nb` | 0..1 | `Max35Text` | length 1–35 |
| `RltdDt` | 0..1 | `ISODate` |  |

## `DocumentLineInformation1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..*** | `DocumentLineIdentification1` |  |
| `Desc` | 0..1 | `Max2048Text` | length 1–2048 |
| `Amt` | 0..1 | `RemittanceAmount3` |  |

## `DocumentLineType1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CdOrPrtry` | **1..1** | `DocumentLineType1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `DocumentLineType1Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalDocumentLineType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `FinancialIdentificationSchemeName1Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalFinancialInstitutionIdentification1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `FinancialInstitutionIdentification18`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `BICFI` | 0..1 | `BICFIDec2014Identifier` | pattern `[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-…` |
| `ClrSysMmbId` | 0..1 | `ClearingSystemMemberIdentification2` |  |
| `LEI` | 0..1 | `LEIIdentifier` | pattern `[A-Z0-9]{18,18}[0-9]{2,2}` |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PstlAdr` | 0..1 | `PostalAddress24` |  |
| `Othr` | 0..1 | `GenericFinancialIdentification1` |  |

## `Frequency36Choice` *(choice: supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | **1..1** | `Frequency6Code` | 9 codes |
| `Prd` | **1..1** | `FrequencyPeriod1` |  |
| `PtInTm` | **1..1** | `FrequencyAndMoment1` |  |

## `FrequencyAndMoment1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | **1..1** | `Frequency6Code` | 9 codes |
| `PtInTm` | **1..1** | `Exact2NumericText` | pattern `[0-9]{2}` |

## `FrequencyPeriod1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | **1..1** | `Frequency6Code` | 9 codes |
| `CntPerPrd` | **1..1** | `DecimalNumber` | 17 decimals max |
