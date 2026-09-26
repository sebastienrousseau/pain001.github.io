---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Pain001 ISO 20022 compliance toolkit, validation workflow, and implementation resources."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-09-21T08:00:00+00:00"
description: "A practical ISO 20022 compliance hub: current pain.001 guidance, regional rulebooks, schemas, validated examples, audit evidence, migration paths, integrations, and community support."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/compliance-toolkit/"
image_alt: "Pain001 ISO 20022 compliance toolkit, validation workflow, and implementation resources."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "ISO 20022 compliance, pain.001 validation, SEPA rulebook, CBPR+, payment audit trail, payment migration guide"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/compliance-toolkit/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "One evidence-led route from current market practice to a locally validated file, an implementation checklist, and a reviewable audit trail."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#07172b"
title: "ISO 20022 Compliance and Implementation Toolkit"
url: "https://pain001.com/compliance-toolkit/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/compliance-toolkit/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.63)"
item_description: "A practical ISO 20022 compliance hub with current standards sources, regional guidance, validation examples, checklists, migration paths, and audit evidence."
item_guid: "https://pain001.com/compliance-toolkit/rss.xml"
item_link: "https://pain001.com/compliance-toolkit/rss.xml"
item_pub_date: "Mon, 21 Sep 2026 08:00:00 +0000"
item_title: "ISO 20022 Compliance and Implementation Toolkit"
last_build_date: "Mon, 21 Sep 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Mon, 21 Sep 2026 08:00:00 +0000"
ttl: 60
type: website
webmaster: contact@pain001.com
apple_mobile_web_app_orientations: portrait
apple_touch_icon_sizes: 192x192
apple-mobile-web-app-capable: yes
apple-mobile-web-app-status-bar-inset: black
apple-mobile-web-app-status-bar-style: black-translucent
apple-mobile-web-app-title: "ISO 20022 Compliance Toolkit"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(7, 23, 43)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "Current ISO 20022 and regional guidance, validation examples, implementation checklists, migration paths, and audit evidence."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 ISO 20022 compliance toolkit"
twitter_site: "@wwdseb"
twitter_title: "ISO 20022 Compliance and Implementation Toolkit"
twitter_url: "https://pain001.com/compliance-toolkit/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-09-21
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Compliance hub"
excerpt: "A single route through authoritative ISO 20022 sources, regional market-practice constraints, validation, audit evidence, migration, integration, and community support."
last_reviewed: "2026-09-21"
---

## Start with the governing source

ISO 20022 message definitions and market-practice rules are separate layers.
Choose the message your bank or clearing channel requires; do not assume the
highest numbered schema is accepted by that channel.

| Layer | Current source | What to record |
| --- | --- | --- |
| Base message | [ISO 20022 message catalogue](https://www.iso20022.org/iso-20022-message-definitions) and [archive](https://www.iso20022.org/catalogue-messages/iso-20022-messages-archive) | Message identifier, XSD checksum, retrieval date |
| Cross-border | [Swift Standards Releases](https://www.swift.com/standards/standards-releases) and your MyStandards profile | CBPR+ release, usage guideline, channel profile |
| SEPA | [EPC SCT rulebook and implementation guidelines](https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-credit-transfer-sct/sepa-credit-transfer-rulebook-and) | Rulebook version, effective date, SCT/SCT Inst/SDD scheme |
| Bank-specific | Your bank's implementation guide and onboarding response | Product, channel, cut-off, account entitlement, accepted variants |

The [living roadmap](/iso20022-roadmap/) tracks dated changes. The
[2026 briefing](/2026-iso20022-migration-trends/) explains the structured or
hybrid address transition, while the [compatibility matrix](/compatibility/)
states exactly which checks Pain001 performs.

## Validate a representative file

Use the [browser validator and message builder](/try/) for a same-origin,
local demonstration, or install the CLI for repeatable pipeline gates:

```sh
pip install pain001==0.0.71
pain001 -t pain.001.001.09 -d payments.csv --scheme sepa-sct --dry-run
```

The [example corpus](/example-corpus/) supplies positive and negative cases.
Every scenario links to its input, expected outcome, message edition, scheme,
and generated artefacts. [Message specifications](/message-specs/) provide
field-level XML schema documentation. The
[technical reference](/documentation/) covers Python, CLI, REST, validation
errors, and operational exit codes.

## Implementation checklist

- [ ] Name the target scheme, channel, bank product, message identifier, and
      implementation-guide version.
- [ ] Preserve source-data provenance and use masked test data outside
      production.
- [ ] Validate required fields, identifiers, exact decimal amounts, control
      totals, character sets, scheme rules, and the official XSD.
- [ ] Test positive, boundary, and intentionally invalid examples against the
      bank's certification environment.
- [ ] Record the tool version, command, configuration, XSD checksum, input
      checksum, output checksum, timestamp, and validation result.
- [ ] Keep the bank acknowledgement and map any rejection through the
      [pain.002 reason-code reference](/pain002-reason-codes/).
- [ ] Obtain business, operations, security, and compliance sign-off before
      production enablement.
- [ ] Re-run the suite when an ISO, scheme, bank profile, or software version
      changes.

This checklist is a reusable control template, not legal advice and not proof
that a receiving bank will accept a file. Pain001 can prove schema and shipped
rulebook checks; only the bank can prove its profile, channel, and entitlement.

## Migration and integration paths

| Starting point | Guide | Validation target |
| --- | --- | --- |
| SWIFT MT101 | [MT101 migration](/mt101-migration/) and [loader reference](/pain001-loader-mt101/) | pain.001.001.09 plus chosen market practice |
| Excel | [Excel migration](/excel-to-pain001/) and [loader reference](/pain001-loader-xlsx/) | typed records before XML generation |
| CSV, JSON, SQLite, Parquet | [Payment pipelines](/payments/) | the same shared validation pipeline |
| Application API | [REST and Python reference](/documentation/) | synchronous validation or asynchronous job result |
| AI workflow | [MCP tools](/pain001-mcp/) | local, read-only generation and validation tools |
| Editor workflow | [LSP integration](/pain001-lsp/) | diagnostics and completion before runtime |

Run load and latency tests with production-shaped, non-sensitive batches. The
website does not publish a universal throughput claim: hardware, schema,
format, plugin, and validation profile all affect results. Treat non-zero CLI
exit codes, structured REST errors, and `pain.002` responses as operational
events with owners and retry rules.

## Audit evidence package

For each controlled run, retain a manifest similar to this:

```json
{
  "tool": "pain001",
  "tool_version": "0.0.71",
  "message": "pain.001.001.09",
  "scheme": "sepa-sct",
  "input_sha256": "<sha256>",
  "output_sha256": "<sha256>",
  "xsd_sha256": "<sha256>",
  "validation": "passed",
  "bank_profile": "not-evaluated",
  "executed_at": "<RFC3339 timestamp>"
}
```

Store that manifest with change approval, test evidence, bank certification,
and the eventual acknowledgement. The [Trust Centre](/trust/) links the site
SBOM, security policy, accessibility statement, and architecture evidence.

## Find help and contribute evidence

Use [GitHub Discussions](https://github.com/sebastienrousseau/pain001.github.io/discussions)
for implementation questions, [the issue tracker](https://github.com/sebastienrousseau/pain001.github.io/issues)
for website defects, and [contact](/contact/) for direct feedback. Case-study
and adopter-story submissions are welcome through a new issue; remove all real
payment data first. Watch GitHub releases or the [RSS feed](/rss.xml) for
updates. Each documentation page can be saved locally with its **Save page**
control; bookmarks remain on the device.
