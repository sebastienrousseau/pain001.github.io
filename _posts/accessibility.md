---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "An accessibility statement documenting WCAG 2.2 AAA conformance testing for pain001.com."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "pain001.com targets WCAG 2.2 AAA, enforced as a build gate: measured 7:1 contrast in both themes, pa11y-verified pages, keyboard-first interaction, and an open channel for reports."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/accessibility/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "accessibility statement, WCAG 2.2 AAA, pa11y, contrast ratio, keyboard navigation, inclusive design, a11y"
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
permalink: "https://pain001.com/accessibility/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "WCAG 2.2 AAA as a build gate, not a review item — the target, the evidence, and the honest limits."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Accessibility Statement"
url: "https://pain001.com/accessibility/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/accessibility/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "pain001.com targets WCAG 2.2 AAA, enforced as a build gate: measured 7:1 contrast in both themes, pa11y-verified pages, keyboard-first interaction, and an open channel for reports."
item_guid: "https://pain001.com/accessibility/rss.xml"
item_link: "https://pain001.com/accessibility/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Accessibility Statement"
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
apple-mobile-web-app-title: "Accessibility Statement"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "pain001.com targets WCAG 2.2 AAA, enforced as a build gate: measured 7:1 contrast in both themes, pa11y-verified pages, keyboard-first interaction, and an open channel for reports."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Accessibility Statement"
twitter_url: "https://pain001.com/accessibility/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Accessibility"
excerpt: "The accessibility statement for pain001.com: WCAG 2.2 AAA conformance enforced in continuous integration through the generator's WCAG gates, independent pa11y scans at the AAA standard in both themes, and manual keyboard passes — with known limitations stated plainly and a public channel for reports."
last_reviewed: "2026-07-26"


---

This website targets **WCAG 2.2 Level AAA** — beyond the AA level most financial institutions publish against — and treats accessibility as a build gate, not a review item. This page states the target, the evidence, and the honest limits.

---

## 01. Conformance status

All pages of pain001.com are built to conform to WCAG 2.2 AAA. Concretely:

- **Contrast**: every colour token is documented in the stylesheet with its measured contrast ratio; body text meets or exceeds **7:1** in both light and dark themes, verified computationally and by automated scan.
- **Keyboard**: every interactive element is reachable and operable by keyboard, with a visible focus indicator (3px ring) on all controls, a skip-to-content link as the first focusable element, and a CSS-only navigation menu that requires no JavaScript.
- **Motion and preferences**: `prefers-reduced-motion` disables animation and smooth scrolling; `prefers-contrast: more` promotes all muted text to full-contrast ink; the theme honours `prefers-color-scheme` before first paint.
- **Structure**: one `h1` per page, landmark regions, visible breadcrumbs mirrored in structured data, tables with proper header scope that collapse to labelled cards on small screens, and touch targets of at least 44px.
- **Zero-JS interactivity**: FAQs are native `details`/`summary` elements; the mobile menu is a checkbox toggle. JavaScript is an enhancement, never a requirement, everywhere except the [interactive demo](/try/) — which is progressively disclosed and fully keyboard-operable.

## 02. How this is tested

Three layers, run on every build via [continuous integration](https://github.com/sebastienrousseau/pain001.github.io/blob/main/.github/workflows/ci.yml):

1. **Build gates** — the site generator's WCAG audit runs across all pages on every build and fails the build on any finding.
2. **Independent automated scan** — [pa11y](https://pa11y.org/) 4.1.1 at the **WCAG2AAA** standard across twelve representative pages (home, documentation, installation, demo, MCP, briefing, FAQs, glossary, comparison, contact, French, 404), in **both light and dark themes**. Current result: zero errors.
3. **Manual keyboard pass** — tab-order walk, skip-link operation, focus-visibility check, and keyboard operation of the demo and FAQ widgets, performed on the current release (last performed: 26 July 2026).

Fixes found by this process are applied at the source or in the build pipeline — including repairs to third-party components (the search widget's injected styles and the markdown renderer's presentational attributes were both corrected at build time to meet AAA).

## 03. Known limitations

- **Assistive-technology coverage**: testing to date uses automated tooling, computed contrast, and manual keyboard passes. Structured testing with screen readers (VoiceOver, NVDA, JAWS) has not yet been performed by users of those technologies; if you rely on one and hit friction anywhere, that is a bug — please report it.
- **Code samples** scroll horizontally on narrow screens rather than wrapping, preserving meaning at the cost of a scroll gesture.
- **Third-party destinations** (GitHub, PyPI) linked from this site have their own accessibility policies.

## 04. Feedback and enforcement

Accessibility issues are treated with the same severity as functional bugs. Report anything — however small — via [GitHub issues](https://github.com/sebastienrousseau/pain001.github.io/issues) or [contact@pain001.com](mailto:contact@pain001.com). Reports are typically acknowledged within a few days.

This statement was prepared on 26 July 2026 and is reviewed with each site release.
