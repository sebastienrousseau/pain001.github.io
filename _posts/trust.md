---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A trust-centre index assembling Pain001's security, supply-chain, privacy, accessibility, and governance evidence for reviewers."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Everything a vendor-risk, security, or audit reviewer needs in one place: security posture, supply-chain evidence, data flows, accessibility conformance, governance, and release policy — each claim linked to its artefact."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/trust/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001 trust centre, vendor risk assessment open source, SBOM, OpenSSF scorecard, SLSA provenance, security review ISO 20022, third-party risk"
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
permalink: "https://pain001.com/trust/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The due-diligence page: security, supply chain, data flows, accessibility, governance, and support — every claim linked to the artefact that proves it."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Trust Centre"
url: "https://pain001.com/trust/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/trust/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Everything a vendor-risk, security, or audit reviewer needs in one place: security posture, supply-chain evidence, data flows, accessibility conformance, governance, and release policy — each claim linked to its artefact."
item_guid: "https://pain001.com/trust/rss.xml"
item_link: "https://pain001.com/trust/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Trust Centre"
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
apple-mobile-web-app-title: "Trust Centre"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Everything a vendor-risk, security, or audit reviewer needs in one place: security posture, supply-chain evidence, data flows, accessibility conformance, governance, and release policy — each claim linked to its artefact."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Trust Centre"
twitter_url: "https://pain001.com/trust/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Trust Centre"
excerpt: "Pain001's Trust Centre assembles the evidence a bank vendor-risk or security reviewer needs without emailing the maintainer: threat posture and XML hardening, published SBOM and independently scored supply chain, complete data-flow statements, gate-enforced accessibility, governance and continuity disclosure, and the release and support policy."
last_reviewed: "2026-07-26"


---

This page exists so that a security, vendor-risk, or audit reviewer can answer standard due-diligence questions **without emailing anyone**. Every claim links to the artefact that proves it. Where no formal certification exists, the wording is "supports assessment against" — never "compliant with".

## 01. Security

- **Zero-trust XML processing** — all parsing routes through `defusedxml` (XXE and entity-expansion defence); no `lxml` in the dependency tree; path-traversal validation on file inputs; non-root containers. Full detail with code-level references: [Architecture & security](/architecture-and-patents/).
- **Responsible disclosure** — private vulnerability reporting via [GitHub Security](https://github.com/sebastienrousseau/pain001/security); machine-readable policy at [/security.txt](/security.txt). Reports are acknowledged and credited.
- **Static analysis in CI** — CodeQL, Bandit, and pip-audit run on every change to the core.

## 02. Software supply chain

- **Independently scored** — [OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/sebastienrousseau/pain001) runs weekly and on every push; the score is published by the OpenSSF, not self-asserted.
- **SBOM** — a CycloneDX software bill of materials is generated for core release builds ([this site's own SBOM](/sbom.cdx.json) is also published).
- **Provenance** — a SLSA Build L3 attestation workflow is armed on the release pipeline; signed `*.intoto.jsonl` attestations attach to releases published from v0.0.57 onward, verifiable with `slsa-verifier`.
- **Pinned CI** — every GitHub Action in the build pipeline is pinned to a full commit SHA; workflow tokens follow least privilege.
- **Kill switch** — third-party plugin discovery can be disabled outright (`PAIN001_DISABLE_PLUGINS=1`), and every discovered plugin is auditable before first use (`pain001 plugins list`).

## 03. Data and privacy

- **Product data flows** — every component (CLI, library, REST service, MCP server, LSP server) executes on your infrastructure. There is no telemetry, no SaaS callback, no network dependency for generation or validation. [Privacy position](/privacy/).
- **Website** — no cookies, no analytics scripts, no third-party requests beyond one logo CDN. The [browser demo](/try/) reads files locally via the FileReader API; the "Verify it yourself" panel on that page shows how to falsify this with DevTools open.
- **Demo boundary** — the demo's WASM validation engine is served from this origin and cached by a service worker; after first load the demo works offline, which is the strongest proof no data leaves the machine.

## 04. Accessibility

WCAG 2.2 AAA as a build gate: the generator's WCAG audit plus independent pa11y scans at the AAA standard, both themes, enforced in CI — with a manual keyboard pass per release and honest limitations stated. Full method and known limits: [Accessibility statement](/accessibility/). Independent assistive-technology testing is the named next step; the procurement scope for that audit is [published in the repository](https://github.com/sebastienrousseau/pain001.github.io/blob/main/AUDIT-RFQ.md).

## 05. Governance and continuity

Who maintains Pain001, how decisions are made, how the project is funded, and what mitigates single-maintainer risk — stated plainly, including the parts that are genuinely limitations: [Governance & continuity](/governance/).

## 06. Releases and support

Versioning scheme, what "supported" means pre-1.0, security-fix policy, signing and provenance, and rollback guidance: [Release & support policy](/release-policy/).

## 07. Compliance mappings

No certification is claimed. The controls above **support assessment against**:

| Framework | Relevant Pain001 controls |
| :--- | :--- |
| NIST SSDF (SP 800-218) | Protected build pipeline, SHA-pinned dependencies, static analysis, vulnerability response process, SBOM |
| SLSA | Build L3 provenance workflow on releases; source on GitHub with signed commits |
| OWASP (XML security) | defusedxml everywhere, no DTD/entity resolution, input path validation |
| WCAG 2.2 | AAA-targeted, gate-enforced, statement published per page scope |
| Bank third-party-risk questionnaires | This page, plus the linked artefacts, answers the standard data-locality, supply-chain, and continuity sections |

## 08. Contact

Security: [private disclosure](https://github.com/sebastienrousseau/pain001/security) · General: [contact page](/contact/) · Corrections to anything on this site: [open an issue](https://github.com/sebastienrousseau/pain001.github.io/issues) — see the [corrections policy](/governance/#corrections-and-editorial-policy).
