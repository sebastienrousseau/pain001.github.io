---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A timeline of global ISO 20022 payment-system milestones converging on the 14 November 2026 CBPR+ deadlines for structured addresses and the MT101 relay."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "The post-migration landscape with primary sources: the 14 Nov 2026 structured address and MT101-relay deadlines, Fedwire and FedNow status, IPR and VoP, LEIs, and agentic AI."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/2026-iso20022-migration-trends/"
image_alt: "A timeline of global ISO 20022 payment-system milestones converging on the 14 November 2026 CBPR+ deadlines for structured addresses and the MT101 relay."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "ISO 20022 2026, structured address November 2026, MT101 decommission, CBPR+ deadline, hybrid postal address, Fedwire ISO 20022, FedNow, verification of payee, instant payments regulation"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/2026-iso20022-migration-trends/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The migration is over; the data era has begun. Every 2026 deadline, with primary sources."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "ISO 20022 in 2026: Deadlines, Data and What Comes Next"
url: "https://pain001.com/2026-iso20022-migration-trends/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/2026-iso20022-migration-trends/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "The post-migration landscape with primary sources: the 14 Nov 2026 structured address and MT101-relay deadlines, Fedwire and FedNow status, IPR and VoP, LEIs, and agentic AI."
item_guid: "https://pain001.com/2026-iso20022-migration-trends/rss.xml"
item_link: "https://pain001.com/2026-iso20022-migration-trends/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "ISO 20022 in 2026: Deadlines, Data and What Comes Next"
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
apple-mobile-web-app-title: "ISO 20022 in 2026: Deadlines, Data and What Comes Next"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "The post-migration landscape with primary sources: the 14 Nov 2026 structured address and MT101-relay deadlines, Fedwire and FedNow status, IPR and VoP, LEIs, and agentic AI."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "ISO 20022 in 2026: Deadlines, Data and What Comes Next"
twitter_url: "https://pain001.com/2026-iso20022-migration-trends/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Research briefing"
excerpt: "A primary-sourced briefing on ISO 20022 in mid-2026: the end of MT–MX coexistence, the 14 November 2026 structured-address and MT101-relay deadlines, Fedwire and FedNow after go-live, the Instant Payments Regulation and Verification of Payee in force, CHAPS purpose codes from 2027, LEI growth, fraud models, and the agentic-payments race."
last_reviewed: "2026-07-26"

---

> **Executive summary.** The great migration is over; the data era has begun. SWIFT ended MT–MX coexistence for cross-border payment instructions on 22 November 2025, Fedwire went ISO-native on 14 July 2025, and roughly 97% of cross-border payment instructions now travel as ISO 20022. Two hard deadlines dominate the next four months: on **14 November 2026**, fully unstructured postal addresses stop being accepted in CBPR+ payments, and the interbank MT101 relay is decommissioned in favour of `pain.001` version 9. Beyond that, the roadmap runs through 2028 — investigations, statements, and direct debits — while instant rails, LEIs, and agentic AI reshape what the standard is for. Every claim below carries a primary or corroborated source, verified 26 July 2026.

---

## 01. Coexistence is over

SWIFT's MT/ISO 20022 coexistence period for cross-border payments (CBPR+) ended on **22 November 2025**. Payments-scope MT categories 1, 2 and 9 no longer meet CBPR+ requirements between financial institutions: MT103 traffic moved to `pacs.008`, MT202/202COV to `pacs.009`. SWIFT confirmed completion on 25 November 2025 ([press release](https://www.swift.com/news-events/press-releases/global-financial-community-completes-switch-iso-20022-paving-way-new-levels-cross-border-payment-speed-and-innovation-around-world "Swift: global financial community completes switch to ISO 20022")).

What did *not* end in November 2025 matters just as much. Corporate-to-bank traffic (SCORE) may still carry MT101 with no announced decommission date, closed user groups continue, and the FX, securities, and trade categories (3, 5, 7) were never in scope. Statements and direct debits follow later: investigations move to camt-based case management by November 2027, and MT9xx statements plus MT104/107 phase out by November 2028 ([Swift CBPR+ roadmap, June 2026 edition](https://www.swift.com/swift-resource/252463/download "CBPR+ roadmap beyond November 2025")).

Coexistence was a courtesy. It is over.

## 02. 14 November 2026: structured addresses

From 14 November 2026, CBPR+ payment messages carrying **fully unstructured addresses are rejected** on the SWIFT network. The accepted forms are structured — or **hybrid**: town name and country in structured elements (`<TwnNm>`, `<Ctry>`), with up to two 70-character address lines for the remainder. Hybrid has been available since November 2025 and is codified in the Payments Market Practice Group's Hybrid Postal Address guideline v1.12 of 5 March 2026 ([SWIFT: removal of unstructured address](https://www.swift.com/standards/iso-20022/removal-unstructured-address "Swift structured address milestone"); [PMPG v1.12](https://www.swift.com/sites/default/files/files/pmpg-hybrid-postal-address-v1.12-05mar2026.pdf "PMPG Hybrid Postal Address v1.12")).

Industry analysis in early 2026 still put the share of messages carrying unstructured addresses at roughly two-thirds ([NTT DATA](https://be.nttdata.com/insights/blog/swift-cbpr-address-data-compliance-risk-november-2026-deadline "NTT DATA on the November 2026 address deadline")). The bottleneck is not message formatting — it is customer master data. Pain001 generates structured and hybrid address elements today; the remediation work lives in your vendor files.

Fix the data, and the format follows.

## 03. 14 November 2026: MT101 relay becomes pain.001

The same date retires the interbank MT101 relay — the request-for-transfer flow between banks — replaced by CBPR+ **`pain.001` version 9**. Multi-transaction MT101s will be rejected outright; single-transaction messages get temporary contingency conversion with additional validation ([Swift call to action for November 2026](https://www.swift.com/standards/iso-20022/iso-20022-bytes/call-action-november-2026 "Swift: call to action November 2026")).

This is precisely the seam the [Pain001 MT101 loader](/pain001-loader-mt101/) closes: parse the MT101, regenerate as `pain.001.001.09`, validate against the official XSD, submit with confidence — no dependency on in-network contingency translation you do not control.

## 04. The rails, region by region

- **United States.** Fedwire completed its single-day ISO 20022 cutover on **14 July 2025** with more than 4,700 participants ([Federal Reserve](https://www.frbservices.org/news/communications/061825-fedwire-iso-go "Fedwire ISO 20022 go-live confirmation")). CHIPS migrated in April 2024. FedNow passed **1,600 participating institutions**, raised its transaction limit to **$10 million**, and settled 2.73 million payments worth $271 billion in Q1 2026 ([Digital Transactions](https://www.digitaltransactions.net/fednow-tallies-more-than-1600-fis-in-its-real-time-payments-service/ "FedNow participation")).
- **Euro area.** T2 has been ISO-native since 2023. The Instant Payments Regulation is fully in force for euro-area PSPs — receive since 9 January 2025, send plus **Verification of Payee since 9 October 2025**, applying to *all* SEPA credit transfers, not just instant ones ([ECB](https://www.ecb.europa.eu/paym/retail/instant_payments/html/instant_payments_regulation.en.html "ECB on the Instant Payments Regulation")). TIPS opened **cross-currency settlement** (EUR/SEK/DKK) on 8 June 2026 ([ECB MIP news](https://www.ecb.europa.eu/press/intro/news/html/ecb.mipnews260610.en.html "TIPS cross-currency go-live")).
- **United Kingdom.** CHAPS has run on ISO 20022 since June 2023; purpose codes and LEIs became mandatory for property and interbank payments in May 2025, and the Bank of England will extend **mandatory purpose codes to all CHAPS payments from November 2027** ([Bank of England policy statement](https://www.bankofengland.co.uk/paper/2025/ps/expanding-mandatory-iso-20022-enhanced-data-in-chaps-from-2027 "BoE: expanding mandatory ISO 20022 enhanced data")). The retail NPA programme as procured was cancelled; upgrades now run through the refocused infrastructure-renewal effort under the Payments Vision Delivery Committee.
- **Asia-Pacific and Gulf.** Japan's BOJ-NET completed migration in November 2025, joining MEPS+ (2022), RITS (2023), and CHATS (2024). The UAE's ISO-native Aani instant scheme counts 74 participants and 1.5 million users, with cross-border interlinking procurement under way in 2026.

## 05. Beyond compliance: what the data is for

- **Identity.** The active LEI population passed **3 million in Q1 2026**, and the FSB endorses LEI use in cross-border payments ([GLEIF](https://www.gleif.org/en/newsroom/blog/the-lei-in-numbers-active-lei-population-surpasses-3-million-in-q1-2026 "GLEIF LEI statistics")).
- **Speed.** ACI forecasts **427.7 billion real-time transactions in 2026**, rising to 27.1% of all electronic payments by 2028 ([ACI Worldwide](https://www.aciworldwide.com/real-time-payments-report "ACI Prime Time for Real-Time")).
- **Honesty about progress.** The FSB's October 2025 review concludes the G20 cross-border targets are **unlikely to be met by 2027** — cost, speed, and access KPIs have barely moved ([FSB](https://www.fsb.org/2025/10/g20-roadmap-for-cross-border-payments-consolidated-progress-report-for-2025/ "FSB consolidated progress report 2025")). Structured ISO 20022 data is the prerequisite for fixing that, which is why the CPMI refreshed its harmonised data requirements in February 2026 ([BIS CPMI](https://www.bis.org/cpmi/publ/d230.htm "CPMI harmonised ISO 20022 data requirements, updated 2026")).
- **Fraud.** SWIFT and 13 global banks demonstrated that federated-learning models detect cross-border fraud roughly **twice as well** as siloed models in 2025 trials ([SWIFT](https://www.swift.com/news-events/press-releases/swift-ai-innovation-creates-blueprint-banks-stop-fraud-faster-through-cross-border-collaboration "Swift federated learning results")). Rich, structured payment data is what makes such models possible.
- **Agents.** Mastercard's Agent Pay, Visa's Trusted Agent Protocol, Google's AP2, and the Linux Foundation's x402 effort (backed by Visa, Mastercard, and Stripe as of July 2026) are building the authorisation layer for AI-agent commerce. The file layer — where corporate credit transfers are actually initiated — is served by exactly one open MCP implementation: [`pain001-mcp`](/pain001-mcp/).

## 06. What to do this quarter

1. **Audit address data now.** Count beneficiaries with free-text-only addresses; that number is your November exposure.
2. **Regenerate, do not translate.** Convert remaining MT101 flows to validated `pain.001.001.09` while the contingency window is open — not after it closes.
3. **Validate before the bank does.** A `--dry-run` gate in CI catches schema and rulebook failures at commit time, for nothing.
4. **Watch 2027–2028.** Investigations (camt.110/111), statements (camt.05x), and direct debit migration are already scheduled. Teams that treat ISO 20022 as a living standard, not a completed project, will absorb each wave quietly.

There is no soft landing left to wait for. The teams that fixed their data are already collecting the dividend.

---

## References

- SWIFT (2025). *Global financial community completes switch to ISO 20022*. [swift.com](https://www.swift.com/news-events/press-releases/global-financial-community-completes-switch-iso-20022-paving-way-new-levels-cross-border-payment-speed-and-innovation-around-world "Swift press release, 25 November 2025")
- SWIFT (2026). *Removal of unstructured address — November 2026 milestone*. [swift.com](https://www.swift.com/standards/iso-20022/removal-unstructured-address "Swift structured address requirements")
- PMPG (2026). *Hybrid Postal Address, v1.12*. [swift.com](https://www.swift.com/sites/default/files/files/pmpg-hybrid-postal-address-v1.12-05mar2026.pdf "PMPG guideline")
- Federal Reserve Financial Services (2025). *Fedwire Funds Service ISO 20022 implementation*. [frbservices.org](https://www.frbservices.org/news/communications/061825-fedwire-iso-go "Fedwire go-live")
- European Central Bank (2025–2026). *Instant Payments Regulation*; *TIPS cross-currency settlement*. [ecb.europa.eu](https://www.ecb.europa.eu/paym/retail/instant_payments/html/instant_payments_regulation.en.html "ECB IPR overview")
- Bank of England (2025). *Expanding mandatory ISO 20022 enhanced data in CHAPS from 2027*. [bankofengland.co.uk](https://www.bankofengland.co.uk/paper/2025/ps/expanding-mandatory-iso-20022-enhanced-data-in-chaps-from-2027 "BoE policy statement")
- CPMI (2026). *Harmonised ISO 20022 data requirements for enhancing cross-border payments — updated report*. [bis.org](https://www.bis.org/cpmi/publ/d230.htm "CPMI d230")
- FSB (2025). *G20 Roadmap for Cross-border Payments: consolidated progress report*. [fsb.org](https://www.fsb.org/2025/10/g20-roadmap-for-cross-border-payments-consolidated-progress-report-for-2025/ "FSB progress report")
- GLEIF (2026). *The LEI in numbers, Q1 2026*. [gleif.org](https://www.gleif.org/en/newsroom/blog/the-lei-in-numbers-active-lei-population-surpasses-3-million-in-q1-2026 "GLEIF statistics")
- ACI Worldwide (2025). *Prime Time for Real-Time*. [aciworldwide.com](https://www.aciworldwide.com/real-time-payments-report "ACI real-time payments report")
