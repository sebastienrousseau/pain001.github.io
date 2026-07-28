---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Complex types PostalAddress24 – TaxRecordDetails2 in ISO 20022 pain.001.001.10, with elements, cardinality and constraints, generated from the official XSD."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complex types PostalAddress24 – TaxRecordDetails2 in ISO 20022 pain.001.001.10, with elements, cardinality and constraints, generated from the official XSD."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/message-spec-pain.001.001.10-types-3/"
image_alt: "Complex types PostalAddress24 – TaxRecordDetails2 in ISO 20022 pain.001.001.10, with elements, cardinality and constraints, generated from the official XSD."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001.001.10 types, ISO 20022 complex types, cardinality, field mapping"
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
permalink: "https://pain001.com/message-spec-pain.001.001.10-types-3/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Types PostalAddress24 – TaxRecordDetails2 in pain.001.001.10, defined once each — the view to use for field mapping."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.001.001.10 type reference (part 3 of 3) — PostalAddress24 – TaxRecordDetails2"
url: "https://pain001.com/message-spec-pain.001.001.10-types-3/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/message-spec-pain.001.001.10-types-3/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Complex types PostalAddress24 – TaxRecordDetails2 in ISO 20022 pain.001.001.10, with elements, cardinality and constraints, generated from the official XSD."
item_guid: "https://pain001.com/message-spec-pain.001.001.10-types-3/"
item_link: "https://pain001.com/message-spec-pain.001.001.10-types-3/"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.001.001.10 type reference (part 3 of 3) — PostalAddress24 – TaxRecordDetails2"
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
apple-mobile-web-app-title: "pain.001.001.10 type reference (part 3 of 3) — PostalAddress24 – TaxRecordDetails2"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Complex types PostalAddress24 – TaxRecordDetails2 in ISO 20022 pain.001.001.10, with elements, cardinality and constraints, generated from the official XSD."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.001.001.10 type reference (part 3 of 3) — PostalAddress24 – TaxRecordDetails2"
twitter_url: "https://pain001.com/message-spec-pain.001.001.10-types-3/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message specification"
excerpt: "Complex types PostalAddress24 – TaxRecordDetails2 in ISO 20022 pain.001.001.10, with elements, cardinality and constraints, generated from the official XSD."
last_reviewed: "2026-07-26"


---

Complex types in ISO 20022 `pain.001.001.10`, generated from the official XSD. **Part 3 of 3** — `PostalAddress24 – TaxRecordDetails2`.

[Part 1](/message-spec-pain.001.001.10-types/) · [Part 2](/message-spec-pain.001.001.10-types-2/) · **Part 3**

Each type is defined once here. The [message structure](/message-spec-pain.001.001.10/) repeats a party or address block under every party; this view does not, which is what you want when mapping source fields.

A **choice** type means the children are alternatives — supply one, not all. Cardinality in **bold** is required.

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

## `RemittanceInformation16`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Ustrd` | 0..* | `Max140Text` | length 1–140 |
| `Strd` | 0..* | `StructuredRemittanceInformation16` |  |

## `RemittanceLocation7`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `RmtId` | 0..1 | `Max35Text` | length 1–35 |
| `RmtLctnDtls` | 0..* | `RemittanceLocationData1` |  |

## `RemittanceLocationData1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Mtd` | **1..1** | `RemittanceLocationMethod2Code` | 6 codes |
| `ElctrncAdr` | 0..1 | `Max2048Text` | length 1–2048 |
| `PstlAdr` | 0..1 | `NameAndAddress16` |  |

## `ServiceLevel8Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalServiceLevel1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `StructuredRegulatoryReporting3`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `Max35Text` | length 1–35 |
| `Dt` | 0..1 | `ISODate` |  |
| `Ctry` | 0..1 | `CountryCode` | pattern `[A-Z]{2,2}` |
| `Cd` | 0..1 | `Max10Text` | length 1–10 |
| `Amt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `Inf` | 0..* | `Max35Text` | length 1–35 |

## `StructuredRemittanceInformation16`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `RfrdDocInf` | 0..* | `ReferredDocumentInformation7` |  |
| `RfrdDocAmt` | 0..1 | `RemittanceAmount2` |  |
| `CdtrRefInf` | 0..1 | `CreditorReferenceInformation2` |  |
| `Invcr` | 0..1 | `PartyIdentification135` |  |
| `Invcee` | 0..1 | `PartyIdentification135` |  |
| `TaxRmt` | 0..1 | `TaxInformation7` |  |
| `GrnshmtRmt` | 0..1 | `Garnishment3` |  |
| `AddtlRmtInf` | 0..3 | `Max140Text` | length 1–140 |

## `SupplementaryData1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `PlcAndNm` | 0..1 | `Max350Text` | length 1–350 |
| `Envlp` | **1..1** | `SupplementaryDataEnvelope1` |  |

## `TaxAmount2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Rate` | 0..1 | `PercentageRate` | 10 decimals max |
| `TaxblBaseAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `TtlAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `Dtls` | 0..* | `TaxRecordDetails2` |  |

## `TaxAmountAndType1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `TaxAmountType1Choice` |  |
| `Amt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |

## `TaxAmountType1Choice` *(choice — supply one)*

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cd` | **1..1** | `ExternalTaxAmountType1Code` | length 1–4 |
| `Prtry` | **1..1** | `Max35Text` | length 1–35 |

## `TaxAuthorisation1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Titl` | 0..1 | `Max35Text` | length 1–35 |
| `Nm` | 0..1 | `Max140Text` | length 1–140 |

## `TaxInformation7`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cdtr` | 0..1 | `TaxParty1` |  |
| `Dbtr` | 0..1 | `TaxParty2` |  |
| `UltmtDbtr` | 0..1 | `TaxParty2` |  |
| `AdmstnZone` | 0..1 | `Max35Text` | length 1–35 |
| `RefNb` | 0..1 | `Max140Text` | length 1–140 |
| `Mtd` | 0..1 | `Max35Text` | length 1–35 |
| `TtlTaxblBaseAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `TtlTaxAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `Dt` | 0..1 | `ISODate` |  |
| `SeqNb` | 0..1 | `Number` | 0 decimals max |
| `Rcrd` | 0..* | `TaxRecord2` |  |

## `TaxInformation8`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Cdtr` | 0..1 | `TaxParty1` |  |
| `Dbtr` | 0..1 | `TaxParty2` |  |
| `AdmstnZone` | 0..1 | `Max35Text` | length 1–35 |
| `RefNb` | 0..1 | `Max140Text` | length 1–140 |
| `Mtd` | 0..1 | `Max35Text` | length 1–35 |
| `TtlTaxblBaseAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `TtlTaxAmt` | 0..1 | `ActiveOrHistoricCurrencyAndAmount` |  |
| `Dt` | 0..1 | `ISODate` |  |
| `SeqNb` | 0..1 | `Number` | 0 decimals max |
| `Rcrd` | 0..* | `TaxRecord2` |  |

## `TaxParty1`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `TaxId` | 0..1 | `Max35Text` | length 1–35 |
| `RegnId` | 0..1 | `Max35Text` | length 1–35 |
| `TaxTp` | 0..1 | `Max35Text` | length 1–35 |

## `TaxParty2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `TaxId` | 0..1 | `Max35Text` | length 1–35 |
| `RegnId` | 0..1 | `Max35Text` | length 1–35 |
| `TaxTp` | 0..1 | `Max35Text` | length 1–35 |
| `Authstn` | 0..1 | `TaxAuthorisation1` |  |

## `TaxPeriod2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Yr` | 0..1 | `ISODate` |  |
| `Tp` | 0..1 | `TaxRecordPeriod1Code` | 18 codes |
| `FrToDt` | 0..1 | `DatePeriod2` |  |

## `TaxRecord2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Tp` | 0..1 | `Max35Text` | length 1–35 |
| `Ctgy` | 0..1 | `Max35Text` | length 1–35 |
| `CtgyDtls` | 0..1 | `Max35Text` | length 1–35 |
| `DbtrSts` | 0..1 | `Max35Text` | length 1–35 |
| `CertId` | 0..1 | `Max35Text` | length 1–35 |
| `FrmsCd` | 0..1 | `Max35Text` | length 1–35 |
| `Prd` | 0..1 | `TaxPeriod2` |  |
| `TaxAmt` | 0..1 | `TaxAmount2` |  |
| `AddtlInf` | 0..1 | `Max140Text` | length 1–140 |

## `TaxRecordDetails2`

| Element | Card. | Type | Constraints |
| :--- | :--- | :--- | :--- |
| `Prd` | 0..1 | `TaxPeriod2` |  |
| `Amt` | **1..1** | `ActiveOrHistoricCurrencyAndAmount` |  |
