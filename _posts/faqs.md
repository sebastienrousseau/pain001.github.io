---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Why banks reject payment files, pain.001 vs pain.008, the November 2026 deadlines, streaming large batches, security posture, and audit reproducibility — answered plainly."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/faqs/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain.001 FAQ, pain.001 vs pain.008, why bank rejects payment file, SEPA validation questions, ISO 20022 FAQ, payment file audit"
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
permalink: "https://pain001.com/faqs/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Straight answers for treasurers, payment operations, engineers, and auditors — phrased the way people actually ask."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "Pain001 FAQs for Treasury, Ops, Engineering and Audit"
url: "https://pain001.com/faqs/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/faqs/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Why banks reject payment files, pain.001 vs pain.008, the November 2026 deadlines, streaming large batches, security posture, and audit reproducibility — answered plainly."
item_guid: "https://pain001.com/faqs/rss.xml"
item_link: "https://pain001.com/faqs/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 FAQs for Treasury, Ops, Engineering and Audit"
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
apple-mobile-web-app-title: "Pain001 FAQs for Treasury, Ops, Engineering and Audit"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Why banks reject payment files, pain.001 vs pain.008, the November 2026 deadlines, streaming large batches, security posture, and audit reproducibility — answered plainly."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 FAQs for Treasury, Ops, Engineering and Audit"
twitter_url: "https://pain001.com/faqs/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Questions"
excerpt: "Why banks reject payment files and how Pain001 prevents it; the difference between pain.001 and pain.008; what the November 2026 deadlines really require; streaming half-million-row batches; the security posture; audit reproducibility; and what any of it costs. Sixteen questions, answered plainly, grouped by the person asking."
last_reviewed: "2026-07-26"

---

Straight answers for treasurers, payment operations, engineers, and auditors. Questions are phrased the way people actually ask them. For deeper technical detail, see the [Technical Reference](/documentation/).

---

## For treasury and finance leaders

**What is pain.001, in one paragraph?**

`pain.001` is the ISO 20022 message a customer sends to its bank to initiate credit transfers — the XML successor to formats like SWIFT MT101 and domestic flat files. Your bank validates it against a schema and a scheme rulebook before accepting it. Pain001 (the software) produces those files from the data you already have and proves they are valid before you submit them.

**What is the difference between pain.001 and pain.008?**

Direction of the pull. `pain.001` initiates credit transfers — you push money out. `pain.008` initiates direct debits — you collect money owed to you under a mandate. Pain001 generates both: ten versions of `pain.001` (`.001.03` through `.001.12`) and `pain.008.001.02`.

**We still send MT101 files. How urgent is migration?**

Urgent. SWIFT retired MT category 1, 2 and 9 messages for cross-border interbank payment instructions in November 2025; corporate channels that still accept MT do so at each bank's discretion and on borrowed time. The [MT101 loader](/pain001-loader-mt101/) converts existing MT101 flows to validated `pain.001` without re-keying anything.

**What does the November 2026 structured address deadline mean for us?**

From the end of November 2026, fully unstructured postal addresses are no longer accepted in CBPR+ cross-border payments; addresses must be structured or hybrid — discrete elements such as town (`<TwnNm>`) and country (`<Ctry>`) instead of free-text lines. If your master data holds addresses as blobs, the work is in your data, not your bank connection. Start there. The [2026 briefing](/2026-iso20022-migration-trends/) covers the timeline in detail.

**What does Pain001 cost?**

Nothing. The core is dual-licensed Apache-2.0 / MIT; companion packages are Apache-2.0. Commercial use, modification, and redistribution are all permitted. For scale reference, SWIFT's translation SDK alone lists at €10,000–30,000 per year.

---

## For payment operations

**Why do banks reject payment files?**

Four recurring causes: schema violations (wrong element, wrong version, wrong namespace), bad identifiers (IBAN checksum failures, malformed BICs), broken control totals (`NbOfTxs` / `CtrlSum` not matching the transactions), and characters outside the ISO 20022 Latin set. Pain001 checks all four before a file exists: JSON Schema validation per record, mod-97 IBAN and ISO 9362 BIC checks, recomputed control totals, charset transliteration, and final XSD validation of the rendered XML.

**Can we validate a file without generating anything?**

Yes — `pain001 --dry-run` (or the `validate` subcommand, or `POST /api/v1/validate`). Exit code `0` means valid; `1` means validation failed with field-level errors. Wire it into CI or a pre-submission checklist.

**Which SEPA rulebooks are covered?**

Five scheme rulebooks ship built-in: SEPA Credit Transfer (`sepa-sct`), SEPA Instant (`sepa-inst`), SEPA Direct Debit Core (`sepa-sdd`), SEPA B2B (`sepa-b2b`), and cross-border credit transfer (`xborder-ct`). Use `--scheme <name> --explain` to see every rule that passed or failed.

**Our data lives in Excel. What is the catch?**

Excel silently coerces IBAN-like strings into numbers. The [Excel loader](/pain001-loader-xlsx/) reads `.xlsx`/`.xlsm` directly and hard-stops if IBAN columns contain numeric cells — the corruption is caught at load, not at the bank.

**How does it handle a 500,000-row batch?**

`--streaming` processes input in memory-bounded chunks (default 1,000 transactions), each emitted as its own XML file with correct recomputed control totals. The REST API offers `POST /api/v1/generate/async` with job polling for the same reason.

---

## For engineers and architects

**How do we integrate it — library, CLI, or API?**

All three exist as first-class surfaces: a typed Python API, a CLI with CI-friendly exit codes, and a FastAPI microservice (`pain001 serve`) with sync, async-job, health, and Prometheus metrics endpoints. Same validation pipeline underneath, so results never diverge between surfaces.

**Is the XML generation actually safe against float rounding?**

Amounts are `decimal.Decimal` end-to-end in generation and scheme validation — parsed as exact decimals, summed as exact decimals, rendered without float representation. Control totals are recomputed from validated records, never trusted from input.

**What is the security posture?**

All XML parsing routes through `defusedxml` (blocking XXE and entity-expansion attacks); there is no `lxml` in the dependency tree. Inputs pass a path-traversal validator. The Docker image runs non-root. A CycloneDX SBOM is generated for core releases, and third-party plugin discovery can be disabled outright with `PAIN001_DISABLE_PLUGINS=1`.

**How is quality enforced?**

100% line and branch coverage as a hard CI gate on the core (verifiably: 3,828 lines, 926 branches at 100%), strict mypy, 100% docstring coverage, Bandit and pip-audit security linting, and CodeQL scanning. The companion packages carry the same 100% coverage discipline.

**Can we extend it for a proprietary format?**

Yes — four plugin entry-point groups (`pain001.loaders`, `pain001.validators`, `pain001.schemes`, `pain001.writers`). The Excel loader is itself a plugin using the public protocol, so it doubles as a reference implementation.

---

## For auditors and compliance

**Can we reproduce a file that was generated last quarter?**

Yes. Pin the package version, replay the same input, and the output is deterministic. Because the toolchain is open source, the audit trail extends into the code path itself — not just a vendor attestation.

**Does payment data leave our environment?**

No. Every component — CLI, library, REST API, MCP server, LSP — executes locally. There is no telemetry, no SaaS callback, no external validation service. The MCP server speaks stdio only and all 17 of its tools are annotated read-only and idempotent.

**Who maintains Pain001?**

[Sebastien Rousseau](https://sebastienrousseau.com), a London-based fintech engineering leader, with community contributors. Development is public on [GitHub](https://github.com/sebastienrousseau/pain001), releases are published to [PyPI](https://pypi.org/project/pain001/), and the changelog is versioned with every release.
