---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Complex types FinancialInstitutionIdentification18 – RemittanceAmount3 in ISO 20022 pain.001.001.09, with elements, cardinality and constraints, generated from the official XSD."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complex types FinancialInstitutionIdentification18 – RemittanceAmount3 in ISO 20022 pain.001.001.09, with elements, cardinality and constraints, generated from the official XSD."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/message-spec-pain.001.001.09-types-2/"
image_alt: "Complex types FinancialInstitutionIdentification18 – RemittanceAmount3 in ISO 20022 pain.001.001.09, with elements, cardinality and constraints, generated from the official XSD."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001.001.09 types, ISO 20022 complex types, cardinality, field mapping"
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
permalink: "https://pain001.com/message-spec-pain.001.001.09-types-2/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Types FinancialInstitutionIdentification18 – RemittanceAmount3 in pain.001.001.09, defined once each — the view to use for field mapping."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.001.001.09 type reference (part 2 of 3) — FinancialInstitutionIdentification18 – RemittanceAmount3"
url: "https://pain001.com/message-spec-pain.001.001.09-types-2/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/message-spec-pain.001.001.09-types-2/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Complex types FinancialInstitutionIdentification18 – RemittanceAmount3 in ISO 20022 pain.001.001.09, with elements, cardinality and constraints, generated from the official XSD."
item_guid: "https://pain001.com/message-spec-pain.001.001.09-types-2/"
item_link: "https://pain001.com/message-spec-pain.001.001.09-types-2/"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.001.001.09 type reference (part 2 of 3) — FinancialInstitutionIdentification18 – RemittanceAmount3"
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
apple-mobile-web-app-title: "pain.001.001.09 type reference (part 2 of 3) — FinancialInstitutionIdentification18 – RemittanceAmount3"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Complex types FinancialInstitutionIdentification18 – RemittanceAmount3 in ISO 20022 pain.001.001.09, with elements, cardinality and constraints, generated from the official XSD."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.001.001.09 type reference (part 2 of 3) — FinancialInstitutionIdentification18 – RemittanceAmount3"
twitter_url: "https://pain001.com/message-spec-pain.001.001.09-types-2/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message specification"
excerpt: "Complex types FinancialInstitutionIdentification18 – RemittanceAmount3 in ISO 20022 pain.001.001.09, with elements, cardinality and constraints, generated from the official XSD."
last_reviewed: "2026-07-26"


---

Complex types in ISO 20022 `pain.001.001.09`, generated from the official XSD. **Part 2 of 3** — `FinancialInstitutionIdentification18 – RemittanceAmount3`.

[Part 1](/message-spec-pain.001.001.09-types/) · **Part 2** · [Part 3](/message-spec-pain.001.001.09-types-3/)

Each type is defined once here. The [message structure](/message-spec-pain.001.001.09/) repeats a party or address block under every party; this view does not, which is what you want when mapping source fields.

A **choice** type means the children are alternatives — supply one, not all. Cardinality in **bold** is required.

## `FinancialInstitutionIdentification18`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `BICFI` | 0..1 | `BICFIDec2014Identifier` | pattern `[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-…` |
| `ClrSysMmbId` | 0..1 | `ClearingSystemMemberIdentification2` |  |
| `LEI` | 0..1 | `LEIIdentifier` | pattern `[A-Z0-9]{18,18}[0-9]{2,2}` |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PstlAdr` | 0..1 | `PostalAddress24` |  |
| `Othr` | 0..1 | `GenericFinancialIdentification1` |  |

## `Garnishment3`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | **1..1** | `GarnishmentType1` |  |
| `Grnshee` | 0..1 | `PartyIdentification135` |  |
| `GrnshmtAdmstr` | 0..1 | `PartyIdentification135` |  |
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

## `GenericOrganisationIdentification1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `Max35Text` | length 1–35 |
| `SchmeNm` | 0..1 | `OrganisationIdentificationSchemeName1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `GenericPersonIdentification1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Id` | **1..1** | `Max35Text` | length 1–35 |
| `SchmeNm` | 0..1 | `PersonIdentificationSchemeName1Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `GroupHeader85`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `MsgId` | **1..1** | `Max35Text` | length 1–35 |
| `CreDtTm` | **1..1** | `ISODateTime` |  |
| `Authstn` | 0..2 | `Authorisation1Choice` |  |
| `NbOfTxs` | **1..1** | `Max15NumericText` | pattern `[0-9]{1,15}` |
| `CtrlSum` | 0..1 | `DecimalNumber` | 17 decimals max |
| `InitgPty` | **1..1** | `PartyIdentification135` |  |
| `FwdgAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification6` |  |

## `InstructionForCreditorAgent1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | 0..1 | `Instruction3Code` | 4 codes |
| `InstrInf` | 0..1 | `Max140Text` | length 1–140 |

## `LocalInstrument2Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalLocalInstrument1Code` | length 1–35 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `NameAndAddress16`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Nm` | **1..1** | `Max140Text` | length 1–140 |
| `Adr` | **1..1** | `PostalAddress24` |  |

## `OrganisationIdentification29`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `AnyBIC` | 0..1 | `AnyBICDec2014Identifier` | pattern `[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-…` |
| `LEI` | 0..1 | `LEIIdentifier` | pattern `[A-Z0-9]{18,18}[0-9]{2,2}` |
| `Othr` | 0..* | `GenericOrganisationIdentification1` |  |

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

## `Party38Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `OrgId` | **1..1** | `OrganisationIdentification29` |  |
| `PrvtId` | **1..1** | `PersonIdentification13` |  |

## `PartyIdentification135`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `PstlAdr` | 0..1 | `PostalAddress24` |  |
| `Id` | 0..1 | `Party38Choice` |  |
| `CtryOfRes` | 0..1 | `CountryCode` | pattern `[A-Z]{2,2}` |
| `CtctDtls` | 0..1 | `Contact4` |  |

## `PaymentIdentification6`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `InstrId` | 0..1 | `Max35Text` | length 1–35 |
| `EndToEndId` | **1..1** | `Max35Text` | length 1–35 |
| `UETR` | 0..1 | `UUIDv4Identifier` | pattern `[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89…` |

## `PaymentInstruction30`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `PmtInfId` | **1..1** | `Max35Text` | length 1–35 |
| `PmtMtd` | **1..1** | `PaymentMethod3Code` | 3 codes |
| `BtchBookg` | 0..1 | `BatchBookingIndicator` |  |
| `NbOfTxs` | 0..1 | `Max15NumericText` | pattern `[0-9]{1,15}` |
| `CtrlSum` | 0..1 | `DecimalNumber` | 17 decimals max |
| `PmtTpInf` | 0..1 | `PaymentTypeInformation26` |  |
| `ReqdExctnDt` | **1..1** | `DateAndDateTime2Choice` |  |
| `PoolgAdjstmntDt` | 0..1 | `ISODate` |  |
| `Dbtr` | **1..1** | `PartyIdentification135` |  |
| `DbtrAcct` | **1..1** | `CashAccount38` |  |
| `DbtrAgt` | **1..1** | `BranchAndFinancialInstitutionIdentification6` |  |
| `DbtrAgtAcct` | 0..1 | `CashAccount38` |  |
| `InstrForDbtrAgt` | 0..1 | `Max140Text` | length 1–140 |
| `UltmtDbtr` | 0..1 | `PartyIdentification135` |  |
| `ChrgBr` | 0..1 | `ChargeBearerType1Code` | 4 codes |
| `ChrgsAcct` | 0..1 | `CashAccount38` |  |
| `ChrgsAcctAgt` | 0..1 | `BranchAndFinancialInstitutionIdentification6` |  |
| `CdtTrfTxInf` | **1..*** | `CreditTransferTransaction34` |  |

## `PaymentTypeInformation26`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `InstrPrty` | 0..1 | `Priority2Code` | 2 codes |
| `SvcLvl` | 0..* | `ServiceLevel8Choice` |  |
| `LclInstrm` | 0..1 | `LocalInstrument2Choice` |  |
| `CtgyPurp` | 0..1 | `CategoryPurpose1Choice` |  |

## `PersonIdentification13`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `DtAndPlcOfBirth` | 0..1 | `DateAndPlaceOfBirth1` |  |
| `Othr` | 0..* | `GenericPersonIdentification1` |  |

## `PersonIdentificationSchemeName1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalPersonIdentification1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `PostalAddress24`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `AdrTp` | 0..1 | `AddressType3Choice` |  |
| `Dept` | 0..1 | `Max70Text` | length 1–70 |
| `SubDept` | 0..1 | `Max70Text` | length 1–70 |
| `StrtNm` | 0..1 | `Max70Text` | length 1–70 |
| `BldgNb` | 0..1 | `Max16Text` | length 1–16 |
| `BldgNm` | 0..1 | `Max35Text` | length 1–35 |
| `Flr` | 0..1 | `Max70Text` | length 1–70 |
| `PstBx` | 0..1 | `Max16Text` | length 1–16 |
| `Room` | 0..1 | `Max70Text` | length 1–70 |
| `PstCd` | 0..1 | `Max16Text` | length 1–16 |
| `TwnNm` | 0..1 | `Max35Text` | length 1–35 |
| `TwnLctnNm` | 0..1 | `Max35Text` | length 1–35 |
| `DstrctNm` | 0..1 | `Max35Text` | length 1–35 |
| `CtrySubDvsn` | 0..1 | `Max35Text` | length 1–35 |
| `Ctry` | 0..1 | `CountryCode` | pattern `[A-Z]{2,2}` |
| `AdrLine` | 0..7 | `Max70Text` | length 1–70 |

## `ProxyAccountIdentification1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `ProxyAccountType1Choice` |  |
| `Id` | **1..1** | `Max2048Text` | length 1–2048 |

## `ProxyAccountType1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalProxyAccountType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `Purpose2Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalPurpose1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `ReferredDocumentInformation7`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `ReferredDocumentType4` |  |
| `Nb` | 0..1 | `Max35Text` | length 1–35 |
| `RltdDt` | 0..1 | `ISODate` |  |
| `LineDtls` | 0..* | `DocumentLineInformation1` |  |

## `ReferredDocumentType3Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `DocumentType6Code` | 16 codes |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `ReferredDocumentType4`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `CdOrPrtry` | **1..1** | `ReferredDocumentType3Choice` |  |
| `Issr` | 0..1 | `Max35Text` | length 1–35 |

## `RegulatoryAuthority2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |
| `Ctry` | 0..1 | `CountryCode` | pattern `[A-Z]{2,2}` |

## `RegulatoryReporting3`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `DbtCdtRptgInd` | 0..1 | `RegulatoryReportingType1Code` | 3 codes |
| `Authrty` | 0..1 | `RegulatoryAuthority2` |  |
| `Dtls` | 0..* | `StructuredRegulatoryReporting3` |  |

## `RemittanceAmount2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `DuePyblAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `DscntApldAmt` | 0..* | `DiscountAmountAndType1` |  |
| `CdtNoteAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `TaxAmt` | 0..* | `TaxAmountAndType1` |  |
| `AdjstmntAmtAndRsn` | 0..* | `DocumentAdjustment1` |  |
| `RmtdAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |

## `RemittanceAmount3`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `DuePyblAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `DscntApldAmt` | 0..* | `DiscountAmountAndType1` |  |
| `CdtNoteAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `TaxAmt` | 0..* | `TaxAmountAndType1` |  |
| `AdjstmntAmtAndRsn` | 0..* | `DocumentAdjustment1` |  |
| `RmtdAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
