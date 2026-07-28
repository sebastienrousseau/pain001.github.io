---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Element-by-element differences between consecutive ISO 20022 pain.001 versions, computed from the official schemas."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Element-by-element differences between consecutive ISO 20022 pain.001 versions, computed from the official schemas."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/message-spec-changes/"
image_alt: "Element-by-element differences between consecutive ISO 20022 pain.001 versions, computed from the official schemas."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.001 version differences, ISO 20022 changes, schema diff, migration impact, pain.001.001.13 changes"
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
permalink: "https://pain001.com/message-spec-changes/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The delta the ISO catalogue does not publish: exactly which elements each pain.001 version added and removed."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "What changed between pain.001 versions — element-level diffs"
url: "https://pain001.com/message-spec-changes/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/message-spec-changes/"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Element-by-element differences between consecutive ISO 20022 pain.001 versions, computed from the official schemas."
item_guid: "https://pain001.com/message-spec-changes/"
item_link: "https://pain001.com/message-spec-changes/"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "What changed between pain.001 versions — element-level diffs"
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
apple-mobile-web-app-title: "What changed between pain.001 versions — element-level diffs"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Element-by-element differences between consecutive ISO 20022 pain.001 versions, computed from the official schemas."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "What changed between pain.001 versions — element-level diffs"
twitter_url: "https://pain001.com/message-spec-changes/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Message specification"
excerpt: "Element-by-element differences between consecutive ISO 20022 pain.001 versions, computed from the official schemas."
last_reviewed: "2026-07-26"


---

What changed between consecutive ISO 20022 payment-initiation versions, computed by diffing the official schemas element by element. This is the view the ISO catalogue does not provide: it publishes each version, not the delta between them.

Paths are XML element paths. An added path means the element does not exist in the earlier version, so a document using it will not validate there.

## pain.001.001.03 → pain.001.001.04

**16 added · 10 removed**

### Added

- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/BICFI`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/Id/OrgId/AnyBIC`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgt/FinInstnId/BICFI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/ChqInstr/Sgntr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1/FinInstnId/BICFI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2/FinInstnId/BICFI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3/FinInstnId/BICFI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/XchgRateInf/UnitCcy`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/BICFI`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/Id/OrgId/AnyBIC`
- `CstmrCdtTrfInitn/PmtInf/DbtrAgt/FinInstnId/BICFI`
- `CstmrCdtTrfInitn/PmtInf/InstrForDbtrAgt`
- `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/Id/OrgId/AnyBIC`
- `CstmrCdtTrfInitn/SplmtryData`
- `CstmrCdtTrfInitn/SplmtryData/Envlp`
- `CstmrCdtTrfInitn/SplmtryData/PlcAndNm`

### Removed

- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/BIC`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/Id/OrgId/BICOrBEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgt/FinInstnId/BIC`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1/FinInstnId/BIC`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2/FinInstnId/BIC`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3/FinInstnId/BIC`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/BIC`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/Id/OrgId/BICOrBEI`
- `CstmrCdtTrfInitn/PmtInf/DbtrAgt/FinInstnId/BIC`
- `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/Id/OrgId/BICOrBEI`

## pain.001.001.04 → pain.001.001.05

**3 added · 0 removed**

### Added

- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/SplmtryData`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/SplmtryData/Envlp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/SplmtryData/PlcAndNm`

## pain.001.001.05 → pain.001.001.06

**6 added · 5 removed**

### Added

- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnDtls`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnDtls/ElctrncAdr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnDtls/Mtd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnDtls/PstlAdr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RmtInf/Strd/GrnshmtRmt`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RmtInf/Strd/TaxRmt`

### Removed

- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnElctrncAdr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnMtd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnPstlAdr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnPstlAdr/Adr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RltdRmtInf/RmtLctnPstlAdr/Nm`

## pain.001.001.06 → pain.001.001.07

**0 added · 0 removed**

No element-level changes: the versions differ only in type definitions or documentation.

## pain.001.001.07 → pain.001.001.08

**2 added · 0 removed**

### Added

- `CstmrCdtTrfInitn/PmtInf/ReqdExctnDt/Dt`
- `CstmrCdtTrfInitn/PmtInf/ReqdExctnDt/DtTm`

## pain.001.001.08 → pain.001.001.09

**163 added · 1 removed**

### Added

- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/LEI`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/PstlAdr/Flr`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/PstlAdr/PstBx`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/PstlAdr/Room`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/PstlAdr/TwnLctnNm`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/LEI`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/PstlAdr/Flr`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/PstlAdr/PstBx`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/PstlAdr/Room`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/PstlAdr/TwnLctnNm`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls/Dept`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls/EmailPurp`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls/JobTitl`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls/Othr/ChanlTp`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls/Othr/Id`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls/PrefrdMtd`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls/Rspnsblty`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/Id/OrgId/LEI`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/AdrTp/Cd`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/AdrTp/Prtry`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/Flr`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/PstBx`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/Room`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/TwnLctnNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/CtctDtls/Dept`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/CtctDtls/EmailPurp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/CtctDtls/JobTitl`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/CtctDtls/PrefrdMtd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/CtctDtls/Rspnsblty`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/PstlAdr/Flr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/PstlAdr/PstBx`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/PstlAdr/Room`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/PstlAdr/TwnLctnNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAcct/Prxy`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAcct/Prxy/Id`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAcct/Prxy/Tp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgt/BrnchId/LEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgt/FinInstnId/LEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgtAcct/Prxy`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgtAcct/Prxy/Id`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/CdtrAgtAcct/Prxy/Tp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1/BrnchId/LEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1/FinInstnId/LEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1Acct/Prxy`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1Acct/Prxy/Id`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt1Acct/Prxy/Tp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2/BrnchId/LEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2/FinInstnId/LEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2Acct/Prxy`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2Acct/Prxy/Id`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt2Acct/Prxy/Tp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3/BrnchId/LEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3/FinInstnId/LEI`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3Acct/Prxy`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3Acct/Prxy/Id`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/IntrmyAgt3Acct/Prxy/Tp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/PmtId/UETR`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Tax/AdmstnZone`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/CtctDtls/Dept`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/CtctDtls/EmailPurp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/CtctDtls/JobTitl`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/CtctDtls/PrefrdMtd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/CtctDtls/Rspnsblty`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/PstlAdr/Flr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/PstlAdr/PstBx`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/PstlAdr/Room`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/PstlAdr/TwnLctnNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/CtctDtls/Dept`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/CtctDtls/EmailPurp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/CtctDtls/JobTitl`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/CtctDtls/PrefrdMtd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/CtctDtls/Rspnsblty`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/PstlAdr/Flr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/PstlAdr/PstBx`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/PstlAdr/Room`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/PstlAdr/TwnLctnNm`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Prxy`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Prxy/Id`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Prxy/Tp`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Prxy/Tp/Cd`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcct/Prxy/Tp/Prtry`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/LEI`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/PstlAdr/Flr`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/PstlAdr/PstBx`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/PstlAdr/Room`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/PstlAdr/TwnLctnNm`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/LEI`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/PstlAdr/Flr`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/PstlAdr/PstBx`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/PstlAdr/Room`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/PstlAdr/TwnLctnNm`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls/Dept`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls/EmailPurp`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls/JobTitl`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls/Othr/ChanlTp`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls/Othr/Id`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls/PrefrdMtd`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls/Rspnsblty`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/Id/OrgId/LEI`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/PstlAdr/AdrTp/Cd`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/PstlAdr/AdrTp/Prtry`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/PstlAdr/BldgNm`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/PstlAdr/DstrctNm`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/PstlAdr/Flr`
- *…and 43 more*

### Removed

- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Tax/AdmstnZn`

## pain.001.001.09 → pain.001.001.10

**32 added · 0 removed**

### Added

- `CstmrCdtTrfInitn/GrpHdr/InitnSrc`
- `CstmrCdtTrfInitn/GrpHdr/InitnSrc/Nm`
- `CstmrCdtTrfInitn/GrpHdr/InitnSrc/Prvdr`
- `CstmrCdtTrfInitn/GrpHdr/InitnSrc/Vrsn`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/InstrForDbtrAgt/Cd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/InstrForDbtrAgt/InstrInf`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/DtOfSgntr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/DtOfVrfctn`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/ElctrncSgntr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/FnlPmtDt`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Frqcy`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Frqcy/Prd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Frqcy/PtInTm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Frqcy/Tp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/FrstPmtDt`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/MndtId`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Rsn`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Rsn/Cd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Rsn/Prtry`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Tp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Tp/Clssfctn`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Tp/CtgyPurp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Tp/LclInstrm`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/MndtRltdInf/Tp/SvcLvl`
- `CstmrCdtTrfInitn/PmtInf/ReqdAdvcTp`
- `CstmrCdtTrfInitn/PmtInf/ReqdAdvcTp/CdtAdvc`
- `CstmrCdtTrfInitn/PmtInf/ReqdAdvcTp/CdtAdvc/Cd`
- `CstmrCdtTrfInitn/PmtInf/ReqdAdvcTp/CdtAdvc/Prtry`
- `CstmrCdtTrfInitn/PmtInf/ReqdAdvcTp/DbtAdvc`
- `CstmrCdtTrfInitn/PmtInf/ReqdAdvcTp/DbtAdvc/Cd`
- `CstmrCdtTrfInitn/PmtInf/ReqdAdvcTp/DbtAdvc/Prtry`

## pain.001.001.10 → pain.001.001.11

**0 added · 0 removed**

No element-level changes: the versions differ only in type definitions or documentation.

## pain.001.001.11 → pain.001.001.12

**35 added · 0 removed**

### Added

- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/BrnchId/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/GrpHdr/FwdgAgt/FinInstnId/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/CtctDtls/URLAdr`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/GrpHdr/InitgPty/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/CtctDtls/URLAdr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Cdtr/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Tax/UltmtDbtr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Tax/UltmtDbtr/Authstn`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Tax/UltmtDbtr/RegnId`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Tax/UltmtDbtr/TaxId`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/Tax/UltmtDbtr/TaxTp`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/CtctDtls/URLAdr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtCdtr/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/CtctDtls/URLAdr`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/UltmtDbtr/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/BrnchId/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/ChrgsAcctAgt/FinInstnId/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/CtctDtls/URLAdr`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/Dbtr/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/DbtrAgt/BrnchId/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/DbtrAgt/BrnchId/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/DbtrAgt/FinInstnId/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/DbtrAgt/FinInstnId/PstlAdr/UnitNb`
- `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/CtctDtls/URLAdr`
- `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/PstlAdr/CareOf`
- `CstmrCdtTrfInitn/PmtInf/UltmtDbtr/PstlAdr/UnitNb`

## pain.001.001.12 → pain.001.001.13

**2 added · 1 removed**

### Added

- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RgltryRptg/Dtls/RptgCd`
- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RmtInf/Strd/SctiesData`

### Removed

- `CstmrCdtTrfInitn/PmtInf/CdtTrfTxInf/RgltryRptg/Dtls/Cd`
