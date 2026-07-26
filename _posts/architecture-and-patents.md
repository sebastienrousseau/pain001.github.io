---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "An architecture diagram of the Pain001 validation pipeline, from loaders through JSON Schema, scheme rulebooks, and XSD validation to ISO 20022 XML."
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Zero-trust XML parsing, decimal-exact arithmetic, validation as a hard gate, 100% branch coverage — and where Pain001 sits amid patented MT–MX transformation services."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/architecture-and-patents/"
image_alt: "An architecture diagram of the Pain001 validation pipeline, from loaders through JSON Schema, scheme rulebooks, and XSD validation to ISO 20022 XML."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001 architecture, defusedxml XXE, payment file security, ISO 20022 patents, MT MX transformation patent, decimal precision payments, CycloneDX SBOM"
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
permalink: "https://pain001.com/architecture-and-patents/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Zero-trust XML, exact decimal arithmetic, validation as a hard gate — and where an open implementation sits in a patented market."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Architecture, Security and the Patent Landscape"
url: "https://pain001.com/architecture-and-patents/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/architecture-and-patents/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Zero-trust XML parsing, decimal-exact arithmetic, validation as a hard gate, 100% branch coverage — and where Pain001 sits amid patented MT–MX transformation services."
item_guid: "https://pain001.com/architecture-and-patents/rss.xml"
item_link: "https://pain001.com/architecture-and-patents/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Architecture, Security and the Patent Landscape"
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
apple-mobile-web-app-title: "Architecture, Security and the Patent Landscape"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Zero-trust XML parsing, decimal-exact arithmetic, validation as a hard gate, 100% branch coverage — and where Pain001 sits amid patented MT–MX transformation services."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Architecture, Security and the Patent Landscape"
twitter_url: "https://pain001.com/architecture-and-patents/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Engineering"
excerpt: "How Pain001 is engineered for hostile input and audited environments: defusedxml everywhere, path-traversal guards, recomputed control totals, decimal.Decimal end to end in generation, 100% line-and-branch coverage as a CI gate, SBOM per release — and the Bottomline transformation patents that make an open, standards-based alternative worth having."
last_reviewed: "2026-07-26"

---

How Pain001 is engineered, why its guarantees hold, and where it sits in a message-transformation market that commercial vendors have patented around. Every architectural claim below maps to shipped, auditable code.

---

## 01. Zero-trust XML processing

Payment files are an attack surface. Pain001 treats every input as hostile:

- **XXE and entity-expansion defence.** All XML parsing — pain.002 status reports, camt.053 statements, XSD validation input — routes through `defusedxml`, blocking external entity injection and "billion laughs" expansion attacks. There is no `lxml` anywhere in the dependency tree.
- **Path-traversal validation.** File paths pass a dedicated security validator before any read or write.
- **Charset containment.** Text is transliterated to the ISO 20022 Latin character set accepted by SWIFT and SEPA before serialisation, so injection-adjacent characters never reach the wire format.
- **Plugin kill switch.** `PAIN001_DISABLE_PLUGINS=1` disables third-party plugin discovery for locked-down deployments, and `pain001 plugins list` makes every active extension auditable.

## 02. Exact arithmetic, recomputed totals

IEEE 754 floats cannot represent most decimal amounts exactly; payment files built on floats eventually produce a control-sum mismatch. Pain001's generation and scheme-validation pipeline handles every amount as `decimal.Decimal`, and the group-header totals (`NbOfTxs`, `CtrlSum`) are **recomputed from validated records** — never copied from input. A file whose totals disagree with its transactions cannot be produced.

## 03. Validation as a gate, not an option

Every generation path — CLI, Python API, REST, MCP — runs the same three-layer pipeline: JSON Schema per record, optional scheme rulebook (SEPA SCT / Instant / SDD Core / B2B, cross-border), then XSD validation of the rendered document against the official ISO 20022 schema **before writing**. Surfaces cannot diverge because there is one pipeline.

Quality is enforced the same way: 100% line **and** branch coverage as a hard CI gate on the core (3,828 lines, 926 branches), strict mypy, Bandit and pip-audit, CodeQL, and a CycloneDX SBOM per release build. The Docker image runs as a dedicated non-root user.

## 04. The patent landscape — and the open alternative

Message transformation between SWIFT MT and ISO 20022 is patented commercial territory. Representative grants:

- **US 11,704,671 B2** — "Financial messaging transformation-as-a-service" (Bottomline Technologies, granted 2023): converting financial messages between formats, including MT ↔ ISO 20022, delivered as a controlled-access service ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11704671 "US 11,704,671 B2")).
- **US 9,412,091 B2** — "Dynamic adaption of electronic routing slips for financial messaging" ([Google Patents](https://patents.google.com/patent/US9412091 "US 9,412,091 B2")).

Academic work is converging on the same problem from the open side — including structural mapping frameworks for MT101 → `pain.001` transformation ([ResearchGate](https://www.researchgate.net/publication/403546971_Bridging_Legacy_SWIFT_MT_and_ISO_20022_MX_Standards_A_Structural_Mapping_Framework_for_MT101_to_pain001_Transformation "MT101 to pain.001 structural mapping framework")).

Pain001's position is deliberate: implement the **published, open ISO 20022 standard** — schemas, market-practice rulebooks, documented MT field mappings — as liberally licensed open source. Pain001 claims no patents and depends on none. The standard is public; tooling for it should be too.

## 05. Architectural shape

```text
   CSV / JSON / JSONL / SQLite / Parquet / GPG      Excel (.xlsx/.xlsm)      SWIFT MT101
                    │                                      │                     │
                    ▼                                      ▼                     ▼
              bundled loaders                    pain001-loader-xlsx    pain001-loader-mt101
                    └──────────────────┬───────────────────┘                     │
                                       ▼                                        │
                        normalisation & field aliases  ◄────────────────────────┘
                                       ▼
                 JSON Schema validation → scheme rulebook → Jinja2 render
                                       ▼
                        XSD validation (official ISO 20022 schema)
                                       ▼
              pain.001.001.03 – .12  /  pain.008.001.02 XML
```

One pipeline, four entry surfaces (CLI, library, REST, MCP), four plugin extension points (`loaders`, `validators`, `schemes`, `writers`). The [Technical Reference](/documentation/) documents every stage.

---

## FAQ

**Is "100% coverage" a real gate or a badge?**

A hard gate: CI fails below 100% line and branch coverage on the core, and the repository's coverage report is verifiable (3,828 of 3,828 lines, 926 of 926 branches). Coverage does not prove correctness — the XSD validation against official schemas is what does that — but it proves every branch is exercised.

**Does using Pain001 infringe the transformation patents above?**

Pain001 implements the public ISO 20022 standard and publishes its MT101 field mapping openly; it is not a transformation-as-a-service platform. Nothing here is legal advice — the citations exist so your counsel can assess the landscape from primary sources.

**Where do I report a security issue?**

Via the repository's security policy on [GitHub](https://github.com/sebastienrousseau/pain001/security "Pain001 security policy") — coordinated disclosure is welcomed and credited.
