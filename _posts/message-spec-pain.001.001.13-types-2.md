---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Complex types DocumentLineType1 – PaymentInitiationSource1 in ISO 20022 pain.001.001.13, with elements, cardinality and constraints, generated from the official XSD."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complex types DocumentLineType1 – PaymentInitiationSource1 in ISO 20022 pain.001.001.13, with elements, cardinality and constraints, generated from the official XSD."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/message-spec-pain.001.001.13-types-2/"
image_alt: "Complex types DocumentLineType1 – PaymentInitiationSource1 in ISO 20022 pain.001.001.13, with elements, cardinality and constraints, generated from the official XSD."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001.001.13 types, ISO 20022 complex types, cardinality, field mapping"
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
permalink: "https://pain001.com/message-spec-pain.001.001.13-types-2/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Types DocumentLineType1 – PaymentInitiationSource1 in pain.001.001.13, defined once each — the view to use for field mapping."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.001.001.13 type reference (part 2 of 3) — DocumentLineType1 – PaymentInitiationSource1"
url: "https://pain001.com/message-spec-pain.001.001.13-types-2/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/message-spec-pain.001.001.13-types-2/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Complex types DocumentLineType1 – PaymentInitiationSource1 in ISO 20022 pain.001.001.13, with elements, cardinality and constraints, generated from the official XSD."
item_guid: "https://pain001.com/message-spec-pain.001.001.13-types-2/"
item_link: "https://pain001.com/message-spec-pain.001.001.13-types-2/"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.001.001.13 type reference (part 2 of 3) — DocumentLineType1 – PaymentInitiationSource1"
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
apple-mobile-web-app-title: "pain.001.001.13 type reference (part 2 of 3) — DocumentLineType1 – PaymentInitiationSource1"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Complex types DocumentLineType1 – PaymentInitiationSource1 in ISO 20022 pain.001.001.13, with elements, cardinality and constraints, generated from the official XSD."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.001.001.13 type reference (part 2 of 3) — DocumentLineType1 – PaymentInitiationSource1"
twitter_url: "https://pain001.com/message-spec-pain.001.001.13-types-2/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message specification"
excerpt: "Complex types DocumentLineType1 – PaymentInitiationSource1 in ISO 20022 pain.001.001.13, with elements, cardinality and constraints, generated from the official XSD."
last_reviewed: "2026-07-26"


---

Complex types in ISO 20022 `pain.001.001.13`, generated from the official XSD. **Part 2 of 3** — `DocumentLineType1 – PaymentInitiationSource1`.

[Part 1](/message-spec-pain.001.001.13-types/) · **Part 2** · [Part 3](/message-spec-pain.001.001.13-types-3/)

Each type is defined once here. The [message structure](/message-spec-pain.001.001.13/) repeats a party or address block under every party; this view does not, which is what you want when mapping source fields.

A **choice** type means the children are alternatives — supply one, not all. Cardinality in **bold** is required.

## `DocumentLineType1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CdOrPrtry` | **1..1** | `DocumentLineType1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `DocumentLineType1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalDocumentLineType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `DocumentType1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CdOrPrtry` | **1..1** | `DocumentType2Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `DocumentType2Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalDocumentType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

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

## `FinancialInstitutionIdentification23`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `BICFI` | 0..1 | `BICFIDec2014Identifier` | pattern `[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-…` |
| `ClrSysMmbId` | 0..1 | `ClearingSystemMemberIdentification2` |  |
| `LEI` | 0..1 | `LEIIdentifier` | pattern `[A-Z0-9]{18,18}[0-9]{2,2}` |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PstlAdr` | 0..1 | `PostalAddress27` |  |
| `Othr` | 0..1 | `GenericFinancialIdentification1` |  |

## `Frequency36Choice` *(choice — supply one)*

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

## `Garnishment4`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | **1..1** | `GarnishmentType1` |  |
| `Grnshee` | 0..1 | `PartyIdentification272` |  |
| `GrnshmtAdmstr` | 0..1 | `PartyIdentification272` |  |
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

## `GenericIdentification30`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `Exact4AlphaNumericText` | pattern `[a-zA-Z0-9]{4}` |
| `Issr` | **1..1** | `Max35Text` | length 1–35 |
| `SchmeNm` | 0..1 | `Max35Text` | length 1–35 |

## `GenericOrganisationIdentification3`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `Max256Text` | length 1–256 |
| `SchmeNm` | 0..1 | `OrganisationIdentificationSchemeName1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `GenericPersonIdentification2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `Max256Text` | length 1–256 |
| `SchmeNm` | 0..1 | `PersonIdentificationSchemeName1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `GroupHeader114`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `MsgId` | **1..1** | `Max35Text` | length 1–35 |
| `CreDtTm` | **1..1** | `ISODateTime` |  |
| `Authstn` | 0..2 | `Authorisation1Choice` |  |
| `NbOfTxs` | **1..1** | `Max15NumericText` | pattern `[0-9]{1,15}` |
| `CtrlSum` | 0..1 | `DecimalNumber` | 17 decimals max |
| `InitgPty` | **1..1** | `PartyIdentification272` |  |
| `FwdgAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification8` |  |
| `InitnSrc` | 0..1 | `PaymentInitiationSource1` |  |

## `InstructionForCreditorAgent3`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | 0..1 | `ExternalCreditorAgentInstruction1Code` | length 1–4 |
| `InstrInf` | 0..1 | `Max140Text` | length 1–140 |

## `InstructionForDebtorAgent1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | 0..1 | `ExternalDebtorAgentInstruction1Code` | length 1–4 |
| `InstrInf` | 0..1 | `Max140Text` | length 1–140 |

## `LocalInstrument2Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalLocalInstrument1Code` | length 1–35 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `MandateClassification1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `MandateClassification1Code` | 3 codes |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `MandateSetupReason1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalMandateSetupReason1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max70Text` | length 1–70 |

## `MandateTypeInformation2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `SvcLvl` | 0..1 | `ServiceLevel8Choice` |  |
| `LclInstrm` | 0..1 | `LocalInstrument2Choice` |  |
| `CtgyPurp` | 0..1 | `CategoryPurpose1Choice` |  |
| `Clssfctn` | 0..1 | `MandateClassification1Choice` |  |

## `NameAndAddress18`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Nm` | **1..1** | `Max140Text` | length 1–140 |
| `Adr` | **1..1** | `PostalAddress27` |  |

## `OrganisationIdentification39`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `AnyBIC` | 0..1 | `AnyBICDec2014Identifier` | pattern `[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-…` |
| `LEI` | 0..1 | `LEIIdentifier` | pattern `[A-Z0-9]{18,18}[0-9]{2,2}` |
| `Othr` | 0..* | `GenericOrganisationIdentification3` |  |

## `OrganisationIdentificationSchemeName1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalOrganisationIdentification1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `OtherContact1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `ChanlTp` | **1..1** | `Max4Text` | length 1–4 |
| `Id` | 0..1 | `Max128Text` | length 1–128 |

## `Party52Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `OrgId` | **1..1** | `OrganisationIdentification39` |  |
| `PrvtId` | **1..1** | `PersonIdentification18` |  |

## `PartyIdentification272`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PstlAdr` | 0..1 | `PostalAddress27` |  |
| `Id` | 0..1 | `Party52Choice` |  |
| `CtryOfRes` | 0..1 | `CountryCode` | pattern `[A-Z]{2,2}` |
| `CtctDtls` | 0..1 | `Contact13` |  |

## `PaymentIdentification6`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `InstrId` | 0..1 | `Max35Text` | length 1–35 |
| `EndToEndId` | **1..1** | `Max35Text` | length 1–35 |
| `UETR` | 0..1 | `UUIDv4Identifier` | pattern `[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89…` |

## `PaymentInitiationSource1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Nm` | **1..1** | `Max140Text` | length 1–140 |
| `Prvdr` | 0..1 | `Max35Text` | length 1–35 |
| `Vrsn` | 0..1 | `Max35Text` | length 1–35 |
