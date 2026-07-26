---

author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Pain001 ISO 20022 Payment Initiation Suite"
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Complete installation options for Pain001 suite including PyPI, optional extras, companion loaders, Docker, and Kubernetes."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/installation/"
image_alt: "Logo of Pain001 Suite"
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, payments, SWIFT, SEPA, banking, Python, MCP, LSP"
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
permalink: "https://pain001.com/installation/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "ISO 20022 Payment Initiation & Transaction Orchestration Suite"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "Pain001 Installation Guide: PyPI, Extras, Docker & Kubernetes"
url: "https://pain001.com/installation/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/installation/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Complete installation options for Pain001 suite including PyPI, optional extras, companion loaders, Docker, and Kubernetes."
item_guid: "https://pain001.com/installation/rss.xml"
item_link: "https://pain001.com/installation/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 Installation Guide: PyPI, Extras, Docker & Kubernetes"
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
apple-mobile-web-app-title: "Pain001 Installation Guide: PyPI, Extras, Docker & Kubernetes"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Complete installation options for Pain001 suite including PyPI, optional extras, companion loaders, Docker, and Kubernetes."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 Installation Guide: PyPI, Extras, Docker & Kubernetes"
twitter_url: "https://pain001.com/installation/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"

---

# Pain001 Installation & Deployment Guide

Pain001 requires **Python 3.10 or later** and runs natively on macOS, Linux, and Windows.

---

## 1. PyPI Installation Channels

| Channel | Command | Use Case |
| :--- | :--- | :--- |
| **Core CLI & Library** | `pip install pain001` | Standard command-line and Python API |
| **REST API Server** | `pip install "pain001[api]"` | Includes FastAPI + Uvicorn microservice |
| **Parquet Support** | `pip install "pain001[parquet]"` | Ingest PyArrow Parquet analytical datasets |
| **Redis Job Queue** | `pip install "pain001[redis]"` | Distributed background job processing |
| **MCP AI Server** | `pip install "pain001[mcp]"` | In-tree Model Context Protocol server |
| **LSP Language Server** | `pip install "pain001[lsp]"` | In-tree Language Server Protocol backend |

---

## 2. Installing Companion Loaders

To enable Excel and legacy SWIFT MT101 file support, install the official companion loaders:

```bash
# Direct Excel (.xlsx / .xlsm) loader with IBAN safety protection
pip install pain001-loader-xlsx

# Legacy SWIFT MT101 to pain.001 converter loader
pip install pain001-loader-mt101
```

---

## 3. Docker Deployment (GHCR)

Pre-built multi-architecture Docker images (`linux/amd64`, `linux/arm64`) are published to GitHub Container Registry.

### Execute CLI via Docker
```bash
docker run --rm -v "$PWD:/data" -w /data   ghcr.io/sebastienrousseau/pain001:latest   generate -t pain.001.001.09 -d payments.csv -o output.xml
```

### Launch REST API via Docker
```bash
docker run --rm -p 8000:8000   ghcr.io/sebastienrousseau/pain001:latest   serve --host 0.0.0.0 --port 8000
```

> **Security Posture**: The Docker container executes under a dedicated non-root `pain001` user account (UID 10001).
