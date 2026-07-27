---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "The build toolchain of pain001.com — Markdown sources compiled to hardened static HTML by the Shokunin static site generator."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "A Rust static site generator with security-first defaults, Markdown content, no JavaScript framework, and machine-readable surfaces from llms.txt to a CycloneDX SBOM."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/made-with-shokunin/"
image_alt: "The build toolchain of pain001.com — Markdown sources compiled to hardened static HTML by the Shokunin static site generator."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "shokunin, static site generator rust, ssg, llms.txt, static site security"
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
permalink: "https://pain001.com/made-with-shokunin/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Markdown in, hardened static HTML out — the toolchain behind this site."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Made with Shokunin: How This Site Is Built"
url: "https://pain001.com/made-with-shokunin/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/made-with-shokunin/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "A Rust static site generator with security-first defaults, Markdown content, no JavaScript framework, and machine-readable surfaces from llms.txt to a CycloneDX SBOM."
item_guid: "https://pain001.com/made-with-shokunin/rss.xml"
item_link: "https://pain001.com/made-with-shokunin/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Made with Shokunin: How This Site Is Built"
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
apple-mobile-web-app-title: "Made with Shokunin: How This Site Is Built"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "A Rust static site generator with security-first defaults, Markdown content, no JavaScript framework, and machine-readable surfaces from llms.txt to a CycloneDX SBOM."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Made with Shokunin: How This Site Is Built"
twitter_url: "https://pain001.com/made-with-shokunin/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Colophon"
excerpt: "How pain001.com is built: the Shokunin static site generator compiles Markdown and layouts into static HTML with security-first defaults, a small build script repairs and publishes the output, and the result ships machine-readable surfaces from llms.txt to a CycloneDX SBOM with no runtime, framework, or database."
last_reviewed: "2026-07-26"

---

This site is compiled by [Shokunin (ssg)](https://github.com/sebastienrousseau/shokunin), a static site generator written in Rust with a security-first default posture: WCAG validation, CSP metadata, SBOM generation, and AI-discovery files (`llms.txt`) built into the toolchain.

The full stack, for the curious:

- **Content** — Markdown with structured frontmatter, versioned in [Git](https://github.com/sebastienrousseau/pain001.github.io).
- **Build** — `ssg` compiles content and layouts into static HTML; a small build script publishes to GitHub Pages.
- **No runtime** — no JavaScript framework, no server, no database. The only client-side script is a few lines for theme switching and navigation.
- **Machine-readable surfaces** — [llms.txt](/llms.txt), [sitemap.xml](/sitemap.xml), [RSS](/rss.xml), [Atom](/atom.xml), [JSON Feed](/feed.json), [security.txt](/security.txt), [humans.txt](/humans.txt), and a [CycloneDX SBOM](/sbom.cdx.json).

The same philosophy as the Pain001 software: standards first, validation as a gate, nothing hidden.
