---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "The release and support policy for the Pain001 suite, covering versioning, security fixes, verification, and rollback."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "How Pain001 versions, what 'supported' means before 1.0, how security fixes ship, how releases are signed and attested, and how to roll back safely."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/release-policy/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001 release policy, supported versions, semantic versioning, security fixes, SLSA provenance, rollback, version pinning"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/release-policy/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "What 'supported' means before 1.0, how fixes ship, and how to verify and pin what you deploy."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Release & Support Policy"
url: "https://pain001.com/release-policy/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/release-policy/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "How Pain001 versions, what 'supported' means before 1.0, how security fixes ship, how releases are signed and attested, and how to roll back safely."
item_guid: "https://pain001.com/release-policy/rss.xml"
item_link: "https://pain001.com/release-policy/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Release & Support Policy"
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
apple-mobile-web-app-title: "Release & Support Policy"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "How Pain001 versions, what 'supported' means before 1.0, how security fixes ship, how releases are signed and attested, and how to roll back safely."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Release & Support Policy"
twitter_url: "https://pain001.com/release-policy/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Releases"
excerpt: "Pain001's release and support policy stated without gloss: 0.0.x semantic pre-1.0 versioning, latest-release support with security fixes shipping as new releases, per-release SBOM and provenance, verification commands, pinning and rollback guidance, and what the 1.0 commitment will mean when it is made."
last_reviewed: "2026-07-26"


---

## Versioning

Pain001 is **pre-1.0** (`0.0.x`). Within that range, releases are frequent and may include breaking changes; every breaking change is documented in the [release notes](https://github.com/sebastienrousseau/pain001/releases). Companion packages (`pain001-mcp`, `pain001-lsp`, the loaders) version independently and declare their compatible core range in their dependency metadata — the resolver, not the version number, is the compatibility contract.

## What "supported" means

The honest pre-1.0 statement: **the latest release is the supported release.** Bug and security fixes ship as new releases rather than backports. If you need a frozen version, pin it (`pain001==0.0.56`) — pinned installs keep working because releases are never deleted or mutated on PyPI.

Security reports against older versions are still triaged: if the flaw exists in the latest release, it is fixed there with an advisory noting affected versions.

## Verifying a release

- **Integrity** — install from PyPI with hash-checking (`pip install --require-hashes` against your lockfile).
- **Provenance** — from v0.0.57 onward, releases carry a SLSA Build L3 attestation (`multiple.intoto.jsonl` on the GitHub release), verifiable with [`slsa-verifier`](https://github.com/slsa-framework/slsa-verifier) against `github.com/sebastienrousseau/pain001`.
- **Inventory** — each core release build generates a CycloneDX SBOM for dependency review.

## Pinning and rollback

Deployments should pin exact versions in a lockfile and treat upgrades as changes: run your own regression (a `--dry-run` over a representative batch is the natural smoke test) before promoting. Rollback is `pip install pain001==<previous>` — no migrations, no state, no server-side coupling; generated files from any version remain valid against the schemas they targeted.

## Cadence and deprecation

There is no fixed calendar cadence; releases ship when tested work is ready — historically multiple times per month ([release history](https://github.com/sebastienrousseau/pain001/releases)). Deprecations appear in release notes at least one release before removal. **The 1.0 commitment**, when made, will bring semantic-versioning guarantees: no breaking changes within a major version and a documented support window per major — that promise is deliberately not being made before it can be kept.
