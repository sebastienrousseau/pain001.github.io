---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A timeline of global ISO 20022 payment-system milestones, with the deferred Swift structured-address requirement and the 2027 to 2028 schedule."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "The ISO 20022 landscape in September 2026, with primary sources: Swift's deferral of the structured-address deadline, the June 2027 release, Fedwire, FedNow, IPR and VoP, LEIs and AI agents."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/2026-iso20022-migration-trends/"
image_alt: "A timeline of global ISO 20022 payment-system milestones, with the deferred Swift structured-address requirement and the 2027 to 2028 schedule."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "ISO 20022 2026, structured address deferral, Standards Release 2026, CBPR+, hybrid postal address, MT101, Fedwire ISO 20022, FedNow, verification of payee, instant payments regulation"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/2026-iso20022-migration-trends/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The migration is done. Swift has deferred the structured-address deadline, and the data work still decides who gets paid first. Every date, with primary sources."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "ISO 20022 in 2026: Deadlines, Data and What Comes Next"
url: "https://pain001.com/2026-iso20022-migration-trends/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/2026-iso20022-migration-trends/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.63)"
item_description: "The ISO 20022 landscape in September 2026, with primary sources: Swift's deferral of the structured-address deadline, the June 2027 release, Fedwire, FedNow, IPR and VoP, LEIs and AI agents."
item_guid: "https://pain001.com/2026-iso20022-migration-trends/rss.xml"
item_link: "https://pain001.com/2026-iso20022-migration-trends/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "ISO 20022 in 2026: Deadlines, Data and What Comes Next"
last_build_date: "Wed, 23 Sep 2026 08:00:00 +0000"
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
apple-mobile-web-app-title: "ISO 20022 in 2026: Deadlines, Data and What Comes Next"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "The ISO 20022 landscape in September 2026, with primary sources: Swift's deferral of the structured-address deadline, the June 2027 release, Fedwire, FedNow, IPR and VoP, LEIs and AI agents."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "ISO 20022 in 2026: Deadlines, Data and What Comes Next"
twitter_url: "https://pain001.com/2026-iso20022-migration-trends/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-09-23
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Research briefing"
excerpt: "A primary-sourced briefing on ISO 20022 in September 2026: the end of MT–MX coexistence, Swift's August 2026 deferral of the structured-address and other payments changes, the June 2027 release, Fedwire moving its next release to November 2027, FedNow, the Instant Payments Regulation, LEIs, and what AI agents need from payment data."
last_reviewed: "2026-09-23"

---
> **Executive summary.** The format migration is done: Swift ended MT–MX coexistence for cross-border payment instructions on 22 November 2025, Fedwire has run on ISO 20022 since 14 July 2025, and more than 98% of payment instructions on Swift now use the standard. The data work is not done. On 27 August 2026 Swift deferred all payments changes planned for Standards Release 2026, including the rule that would have rejected fully unstructured postal addresses from November 2026, because large parts of the industry were not ready. Swift will announce the new timing by December 2026 at the latest. The date moved; the requirement did not. Every claim below links to a primary or corroborating source, checked on 23 September 2026.


## 01. Coexistence is over

SWIFT's MT/ISO 20022 coexistence period for cross-border payment instructions (CBPR+) ended on **22 November 2025**. MT103 traffic moved to `pacs.008`, and MT202 and MT202COV to `pacs.009`. Swift confirmed completion on 25 November 2025 ([press release](https://www.swift.com/news-events/press-releases/global-financial-community-completes-switch-iso-20022-paving-way-new-levels-cross-border-payment-speed-and-innovation-around-world "Swift: global financial community completes switch to ISO 20022")).

Only payment instructions switched. Cash-management reporting still runs in parallel: MT940, MT942 and MT950 statements continue alongside `camt` messages until November 2028 ([Swift implementation FAQ](https://www.swift.com/standards/iso-20022/iso-20022-faqs/implementation "Swift ISO 20022 implementation FAQ")). Corporate-to-bank traffic can keep using MT101, and Swift has set no deadline for corporates to move to SCORE+ ([Swift call to action](https://www.swift.com/standards/iso-20022/iso-20022-bytes/call-action-november-2026 "Swift: call to action November 2026")).

## 02. The structured-address deadline, deferred

The community decided in 2023 that CBPR+ payment messages would stop accepting **fully unstructured postal addresses** with Standards Release 2026 in November 2026. On **27 August 2026** Swift deferred that requirement, together with every other payments change in the release, after several communities asked for more time. Swift is consulting banks, central banks, market infrastructures and corporates, and will publish the new timing **by December 2026 at the latest** ([Swift, 27 August 2026](https://www.swift.com/news-events/news/swift-accepts-community-request-extend-structured-address-migration-iso-20022-payment-messages "Swift extends the structured address migration")).

The target has not changed. Accepted addresses will be **structured** or **hybrid**: a hybrid address carries town name and country in structured elements (`<TwnNm>`, `<Ctry>`), with up to two 70-character address lines for the rest. Hybrid has been allowed since November 2025, and the Payments Market Practice Group's guideline is at version 1.12 of 5 March 2026 ([PMPG v1.12](https://www.swift.com/about-us/community/swift-advisory-groups/payments-market-practice-group "PMPG Hybrid Postal Address v1.12")). Swift's own April 2026 data showed 61.2% of payments with unstructured debtor addresses and 62.9% with unstructured creditor addresses ([Swift call to action](https://www.swift.com/standards/iso-20022/iso-20022-bytes/call-action-november-2026 "Swift: call to action November 2026")), which is why the deadline moved.

Swift is explicit that the extension is not a pause: structured addresses already flow across the network, and it asks institutions to keep going. The bottleneck is customer master data, not message formatting. Pain001 generates structured and hybrid address elements today; the remediation work lives in your vendor files, and it is the same work whatever date Swift announces.

## 03. MT101 between banks: also deferred

Standards Release 2026 would also have retired the interbank MT101 relay, the request-for-transfer flow between banks, in favour of CBPR+ **`pain.001` version 9**, with multi-transaction MT101s rejected and single transactions converted during a contingency period ([Swift call to action](https://www.swift.com/standards/iso-20022/iso-20022-bytes/call-action-november-2026 "Swift: call to action November 2026")). That change is one of the deferred payments changes, so MT101 continues to work between banks after November 2026 until Swift sets a new date.

The direction is unchanged, which is where the [Pain001 MT101 loader](/pain001-loader-mt101/) fits: parse the MT101, regenerate it as `pain.001.001.09`, and validate it against the official XSD on your own infrastructure, with no dependency on in-network conversion you do not control.

## 04. What is still dated

- **12 June 2027.** The non-payments part of Standards Release 2026 goes live: all MT messages except Category 1, ISO 20022 securities and funds messages, tracker messages, and exceptions and investigations ([Swift update, 21 September 2026](https://www.swift.com/news-events/news/swift-accepts-community-request-extend-structured-address-migration-iso-20022-payment-messages "Swift: deferred SR 2026 release date")). The requirement to receive `camt.110` investigations moves with it.
- **November 2027.** Investigations move to `camt.110` and `camt.111` through Swift Case Management, replacing the MT n92, n95 and n96 formats ([Swift E&I FAQ](https://www.swift.com/standards/iso-20022/iso-20022-faqs/iso-20022-exceptions-and-investigations "Swift exceptions and investigations FAQ")). Fedwire's next ISO 20022 release, first planned for November 2026, is also now November 2027 ([Federal Reserve, 27 August 2026](https://www.frbservices.org/news/communications/082726-fedwire-november-release-rescheduled "Fedwire November release rescheduled")). In the UK, purpose codes become mandatory on all CHAPS payments ([Bank of England policy statement](https://www.bankofengland.co.uk/paper/2025/ps/expanding-mandatory-iso-20022-enhanced-data-in-chaps-from-2027 "BoE: expanding mandatory ISO 20022 enhanced data")).
- **November 2028.** MT statements (MT940, MT942, MT950) end alongside `camt` reporting ([Swift implementation FAQ](https://www.swift.com/standards/iso-20022/iso-20022-faqs/implementation "Swift ISO 20022 implementation FAQ")).

## 05. The rails, region by region

- **United States.** Fedwire moved to ISO 20022 in a single day on **14 July 2025** ([Federal Reserve, On the Wire, August 2025](https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center/on-the-wire-iso-20022-newsletter/august-2025-iso-20022-newsletter "Fedwire ISO 20022 newsletter")). CHIPS migrated on 8 April 2024 ([The Clearing House](https://www.theclearinghouse.org/payment-systems/Articles/2024/04/CHIPS_Network_Migrates_ISO_20022_04-10-2024 "CHIPS migrates to ISO 20022")). FedNow raised its transaction limit to **$10 million** in November 2025 and settled almost 5.0 million payments worth $274.7 billion in the second quarter of 2026 ([Federal Reserve](https://www.frbservices.org/resources/financial-services/fednow/volume-value-stats "FedNow volume and value statistics")); the Richmond Fed counted 1,725 participating institutions in the first quarter ([Richmond Fed](https://www.richmondfed.org/publications/research/economic_brief/2026/eb_26-28 "Richmond Fed economic brief")).
- **Euro area.** T2 has run on ISO 20022 since March 2023. The Instant Payments Regulation is fully in force for euro-area payment service providers: receiving since 9 January 2025, and sending plus **Verification of Payee since 9 October 2025**, for standard and instant credit transfers alike ([ECB](https://www.ecb.europa.eu/paym/retail/instant_payments/html/instant_payments_regulation.en.html "ECB on the Instant Payments Regulation")). The ECB announced **cross-currency settlement in TIPS** between euro, Swedish krona and Danish krone on 10 June 2026 ([ECB](https://www.ecb.europa.eu/press/intro/news/html/ecb.mipnews260610.en.html "TIPS cross-currency settlement")).
- **United Kingdom.** CHAPS has run on ISO 20022 since June 2023. Since May 2025, purpose codes are required on interbank and property payments and LEIs on interbank payments; from November 2027 purpose codes extend to all CHAPS payments ([Bank of England](https://www.bankofengland.co.uk/paper/2025/ps/expanding-mandatory-iso-20022-enhanced-data-in-chaps-from-2027 "BoE policy statement")). The retail New Payments Architecture, as procured, was cancelled; renewal now runs through the Payments Vision Delivery Committee ([Bank of England](https://www.bankofengland.co.uk/news/2025/july/a-new-approach-to-retail-payments-infrastructure "A new approach to retail payments infrastructure")).
- **Asia-Pacific and the Gulf.** Singapore's MEPS+ (2022), Australia's RITS (March 2023, [RBA](https://www.rba.gov.au/rits/info/HVCSISO.htm "RBA: HVCS and ISO 20022")) and Hong Kong's CHATS (2024) are on ISO 20022. Japan's BOJ-NET, on the standard since 2015, moved to the 2019 message versions in November 2025 ([Bank of Japan](https://www.boj.or.jp/en/paym/bojnet/index.htm "BOJ-NET message version upgrade")). The UAE's ISO-native Aani instant scheme reported 74 participants and more than 12.5 million users in April 2026 ([Al Etihad Payments](https://www.aep.ae/en/news-media/press-releasesarticles/aani-delivers-a-transformational-leap-in-the-uae-s-digital-payments-landscape-125-million-users-and-instant-transfers-in-3-seconds/ "Aani: 12.5 million users")), and has chosen Montran for its cross-border gateway ([Montran](https://www.montran.com/resources/al-etihad-payments-selects-montran-to-power-cross-border-instant-payments-integration/ "AEP selects Montran")).

## 06. Beyond compliance: what the data is for

- **Identity.** The active LEI population passed **3 million in the first quarter of 2026** ([GLEIF](https://www.gleif.org/en/newsroom/blog/the-lei-in-numbers-active-lei-population-surpasses-3-million-in-q1-2026 "GLEIF LEI statistics")), and the FSB recommends LEI use in cross-border payments.
- **Speed.** ACI Worldwide forecasts 575.1 billion real-time transactions a year by 2028, 27.1% of all electronic payments ([ACI Worldwide, 2024](https://www.aciworldwide.com/real-time-payments-report "ACI Prime Time for Real-Time 2024")).
- **Progress.** The FSB's October 2025 review found that satisfactory global improvement is **unlikely by the 2027 deadline** for the G20 cross-border targets ([FSB](https://www.fsb.org/2025/10/g20-roadmap-for-cross-border-payments-consolidated-progress-report-for-2025/ "FSB consolidated progress report 2025")). Structured data is a prerequisite for closing that gap, which is why the CPMI updated its harmonised ISO 20022 data requirements in February 2026 ([BIS CPMI](https://www.bis.org/cpmi/publ/d230.htm "CPMI harmonised ISO 20022 data requirements")).
- **Fraud.** In a Swift experiment with 13 institutions, a federated-learning model trained on synthetic data from 10 million transactions found known fraud about **twice as effectively** as a model trained on one institution's data ([Swift](https://www.swift.com/news-events/press-releases/swift-ai-innovation-creates-blueprint-banks-stop-fraud-faster-through-cross-border-collaboration "Swift federated learning results")). Rich, structured payment data is what makes that kind of model possible.
- **Agents.** Mastercard Agent Pay, Visa's Trusted Agent Protocol and Google's AP2 are building the authorisation layer for AI-agent commerce, and the Linux Foundation's x402 Foundation launched in July 2026 with Visa, Mastercard and Stripe among its members ([Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications "x402 Foundation launch")). At the file layer, where corporate credit transfers are initiated, [`pain001-mcp`](/pain001-mcp/) lets an agent generate and validate `pain.001` files locally, against the official schema.

## 07. What to do this quarter

1. **Audit address data now.** Count beneficiaries with free-text-only addresses. The deferral buys time to fix them, not a reason to stop.
2. **Plan for the dates that stand.** June 2027 for investigations and the non-payments release, November 2027 for CHAPS purpose codes and case management, November 2028 for statements.
3. **Regenerate, do not translate.** Move remaining MT101 flows to validated `pain.001.001.09` on your own timetable, before Swift sets one.
4. **Validate before the bank does.** A `--dry-run` gate in CI catches schema and rulebook failures at commit time, at no cost.

Swift will publish the new structured-address timing by December 2026, and this page will be updated when it does.


## References

- Swift (2025). *Global financial community completes switch to ISO 20022*. [swift.com](https://www.swift.com/news-events/press-releases/global-financial-community-completes-switch-iso-20022-paving-way-new-levels-cross-border-payment-speed-and-innovation-around-world "Swift press release, 25 November 2025")
- Swift (2026). *Swift accepts community request to extend structured address migration for ISO 20022 payment messages* (27 August 2026, updated 21 September 2026). [swift.com](https://www.swift.com/news-events/news/swift-accepts-community-request-extend-structured-address-migration-iso-20022-payment-messages "Swift, 27 August 2026")
- Swift (2026). *ISO 20022 in bytes: call to action for November 2026*. [swift.com](https://www.swift.com/standards/iso-20022/iso-20022-bytes/call-action-november-2026 "Swift call to action")
- PMPG (2026). *Hybrid Postal Address, v1.12* (5 March 2026), published by the Payments Market Practice Group. [swift.com](https://www.swift.com/about-us/community/swift-advisory-groups/payments-market-practice-group "PMPG v1.12")
- Federal Reserve Financial Services (2026). *Fedwire Funds Service November 2026 release rescheduled*. [frbservices.org](https://www.frbservices.org/news/communications/082726-fedwire-november-release-rescheduled "Fedwire release rescheduled")
- European Central Bank (2025 to 2026). *Instant Payments Regulation*; *TIPS cross-currency settlement*. [ecb.europa.eu](https://www.ecb.europa.eu/paym/retail/instant_payments/html/instant_payments_regulation.en.html "ECB IPR overview")
- Bank of England (2025). *Expanding mandatory ISO 20022 enhanced data in CHAPS from 2027*. [bankofengland.co.uk](https://www.bankofengland.co.uk/paper/2025/ps/expanding-mandatory-iso-20022-enhanced-data-in-chaps-from-2027 "BoE policy statement")
- CPMI (2026). *Harmonised ISO 20022 data requirements for enhancing cross-border payments: updated report*. [bis.org](https://www.bis.org/cpmi/publ/d230.htm "CPMI d230")
- FSB (2025). *G20 Roadmap for Cross-border Payments: consolidated progress report*. [fsb.org](https://www.fsb.org/2025/10/g20-roadmap-for-cross-border-payments-consolidated-progress-report-for-2025/ "FSB progress report")
- GLEIF (2026). *The LEI in numbers: active LEI population surpasses 3 million in Q1 2026*. [gleif.org](https://www.gleif.org/en/newsroom/blog/the-lei-in-numbers-active-lei-population-surpasses-3-million-in-q1-2026 "GLEIF statistics")
- ACI Worldwide (2024). *Prime Time for Real-Time*. [aciworldwide.com](https://www.aciworldwide.com/real-time-payments-report "ACI real-time payments report 2024")
