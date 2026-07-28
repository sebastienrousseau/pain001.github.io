---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A clean terminal session installing Pain001 from PyPI and generating a first validated pain.001 file — three commands from zero to bank-ready."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Install the Pain001 suite on Python 3.10–3.12 via pip or Docker, add Excel and MT101 loaders, and produce your first bank-ready pain.001 file in three commands."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/installation/"
image_alt: "A clean terminal session installing Pain001 from PyPI and generating a first validated pain.001 file — three commands from zero to bank-ready."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "install pain001, pip install pain001, pain001 docker, ISO 20022 file generator setup, pain001 extras, PAIN001_DISABLE_PLUGINS"
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
permalink: "https://pain001.com/installation/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Python 3.10–3.12, pip or Docker, and a validated payment file in three commands."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Install Pain001: pip, Docker and First Validated File"
url: "https://pain001.com/installation/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/installation/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Install the Pain001 suite on Python 3.10–3.12 via pip or Docker, add Excel and MT101 loaders, and produce your first bank-ready pain.001 file in three commands."
item_guid: "https://pain001.com/installation/rss.xml"
item_link: "https://pain001.com/installation/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Install Pain001: pip, Docker and First Validated File"
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
apple-mobile-web-app-title: "Install Pain001: pip, Docker and First Validated File"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Install the Pain001 suite on Python 3.10–3.12 via pip or Docker, add Excel and MT101 loaders, and produce your first bank-ready pain.001 file in three commands."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Install Pain001: pip, Docker and First Validated File"
twitter_url: "https://pain001.com/installation/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Get started"
excerpt: "Install the Pain001 suite from PyPI with exactly the extras you need — REST API, Parquet, GPG, Redis, OpenTelemetry — or run the multi-architecture Docker image as a non-root user. Companion loaders for Excel and SWIFT MT101 install separately, and locked-down environments get a plugin kill switch and auditable plugin listing."
last_reviewed: "2026-07-26"

---

Pain001 runs on **Python 3.10, 3.11, and 3.12** (each version tested in CI) on macOS, Linux, and Windows. Install what you need; every optional capability is an extra, so the base install stays lean.

---

## 01. PyPI

| What you need | Command |
| :--- | :--- |
| Core CLI & Python library | `pip install pain001` |
| REST API microservice (FastAPI + Uvicorn) | `pip install "pain001[api]"` |
| Parquet ingestion (PyArrow) | `pip install "pain001[parquet]"` |
| PGP-encrypted input files (`.gpg` / `.asc`) | `pip install "pain001[gpg]"` |
| Redis-backed async job queue for the API | `pip install "pain001[redis]"` |
| OpenTelemetry tracing | `pip install "pain001[otel]"` |
| Built-in minimal MCP / LSP servers | `pip install "pain001[mcp]"` / `"pain001[lsp]"` |

Companion packages install separately and are versioned independently:

```bash
pip install pain001-loader-xlsx    # Excel ingestion (auto-discovered plugin)
pip install pain001-loader-mt101   # SWIFT MT101 parsing library
pip install pain001-mcp            # Full 17-tool MCP server for AI agents
pip install pain001-lsp            # Full six-feature editor language server
```

Verify the install and explore the message catalogue:

```bash
pain001 --version
pain001 versions          # list all 11 supported message definitions
pain001 init pain.001.001.09   # scaffold a starter CSV template
```

---

## 02. Docker

Multi-architecture images (`linux/amd64`, `linux/arm64`) are published to GitHub Container Registry. The container runs as a dedicated non-root user.

```bash
# Generate XML from a local CSV
docker run --rm -v "$PWD:/data" -w /data \
  ghcr.io/sebastienrousseau/pain001:latest \
  generate -t pain.001.001.09 -d payments.csv -o out/

# Launch the REST API
docker run --rm -p 8000:8000 \
  ghcr.io/sebastienrousseau/pain001:latest \
  serve --host 0.0.0.0 --port 8000
```

---

## 03. Locked-down environments

Bank and treasury environments often prohibit dynamic plugin loading. Two controls exist for exactly that case:

- `PAIN001_DISABLE_PLUGINS=1` disables all third-party plugin discovery; only bundled loaders run.
- `pain001 plugins list` / `pain001 plugins show <name>` make every discovered plugin auditable before first use.

Everything executes locally. No package in the suite phones home, calls a SaaS API, or moves payment data off the host.

---

## 04. First file in three commands

```bash
pip install pain001
pain001 init pain.001.001.09 -o work/
pain001 -t pain.001.001.09 -d work/template.csv -o work/ --dry-run
```

`--dry-run` validates against the JSON Schema, the XSD, and (with `--scheme`) a SEPA or cross-border rulebook without writing output — exit code `0` means your bank will not reject the file for schema reasons. Drop `--dry-run` to write the XML.

Continue to the [Technical Reference](/documentation/) for every flag and endpoint, or the [Quickstart FAQ](/faqs/) for operational questions.
