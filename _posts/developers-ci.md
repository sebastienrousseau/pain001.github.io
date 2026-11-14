---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Run pain001 check on every pull request: the GitHub Action validates pain.001 and pain.008 files against ISO 20022 rules and reports to code scanning."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-11-10T08:00:00+00:00"
description: "Run pain001 check on every pull request: the GitHub Action validates pain.001 and pain.008 files against ISO 20022 rules and reports to code scanning."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/developers/ci/"
image_alt: "Run pain001 check on every pull request: the GitHub Action validates pain.001 and pain.008 files against ISO 20022 rules and reports to code scanning."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001 github action, validate pain.001 in ci, pain.001 sarif, iso 20022 ci check"
language: en-GB
layout: "page"
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/developers/ci/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Fail the job when a payment file would fail at the bank, and see every finding in code scanning."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Check payment files in CI with the pain001 GitHub Action"
url: "https://pain001.com/developers/ci/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/developers/ci/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.75)"
item_description: "Run pain001 check on every pull request: the GitHub Action validates pain.001 and pain.008 files against ISO 20022 rules and reports to code scanning."
item_guid: "https://pain001.com/developers/ci/rss.xml"
item_link: "https://pain001.com/developers/ci/rss.xml"
item_pub_date: "Tue, 10 Nov 2026 08:00:00 +0000"
item_title: "Check payment files in CI with the pain001 GitHub Action"
last_build_date: "Tue, 10 Nov 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Tue, 10 Nov 2026 08:00:00 +0000"
ttl: 60
type: website
webmaster: contact@pain001.com
apple_mobile_web_app_orientations: portrait
apple_touch_icon_sizes: 192x192
apple-mobile-web-app-capable: yes
apple-mobile-web-app-status-bar-inset: black
apple-mobile-web-app-status-bar-style: black-translucent
apple-mobile-web-app-title: "Check payment files in CI with the pain001 GitHub Action"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "Run pain001 check on every pull request: the GitHub Action validates pain.001 and pain.008 files against ISO 20022 rules and reports to code scanning."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "Check payment files in CI with the pain001 GitHub Action"
twitter_url: "https://pain001.com/developers/ci/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Developers"
excerpt: "Run pain001 check on every pull request: the GitHub Action validates pain.001 and pain.008 files against ISO 20022 rules and reports to code scanning."
last_reviewed: "2026-11-10"

---
The core repository is a GitHub Action. It installs pain001 from the tag you pin, checks the files, uploads the findings to code scanning as SARIF, and fails the job when a file does not pass.

```yaml
permissions:
  contents: read
  security-events: write   # for the SARIF upload
steps:
  - uses: actions/checkout@<sha>
  - uses: sebastienrousseau/pain001@v0.0.87
    with:
      files: "payments/**/*.xml"
      scheme: sepa-sct
```

Pin `actions/checkout` to a full commit SHA.

## Inputs

| Input | What it does | Default |
| :--- | :--- | :--- |
| `files` | Files or globs to check, separated by spaces or newlines (`**` recurses). Required. | |
| `scheme` | Scheme profiles to apply, comma-separated, for example `sepa-sct`. | none |
| `schematron` | A Schematron rulebook: a preset (`sepa`, `fednow`, `cbpr`) or a `.sch` path. | none |
| `rules` | Path of a private YAML CEL policy file (installs `pain001[rules]`). | none |
| `skip-other-xml` | Skip XML files that are not pain.001 or pain.008. | `"true"` |
| `sarif-file` | Where to write the SARIF log. | `pain001-check.sarif` |
| `upload-sarif` | Upload the SARIF log to code scanning. | `"true"` |
| `python-version` | The Python to run pain001 on (3.11 or newer). | `"3.12"` |

The action's `exit-code` output is 0 when every file passed, 1 on an error finding, and 2 when a file could not be checked.

For your bank's own rules, see [build your own bank profile](/docs/bank-profiles/).
