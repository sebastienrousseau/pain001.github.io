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
description: "Exposing the Pain001 payment library as 17 first-class Model Context Protocol (MCP) agent tools for Claude Desktop, Cursor, and LLMs."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pain001-mcp/"
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
permalink: "https://pain001.com/pain001-mcp/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "ISO 20022 Payment Initiation & Transaction Orchestration Suite"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "pain001-mcp: Model Context Protocol Server for AI Payment Tools"
url: "https://pain001.com/pain001-mcp/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-mcp/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Exposing the Pain001 payment library as 17 first-class Model Context Protocol (MCP) agent tools for Claude Desktop, Cursor, and LLMs."
item_guid: "https://pain001.com/pain001-mcp/rss.xml"
item_link: "https://pain001.com/pain001-mcp/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain001-mcp: Model Context Protocol Server for AI Payment Tools"
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
apple-mobile-web-app-title: "pain001-mcp: Model Context Protocol Server for AI Payment Tools"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Exposing the Pain001 payment library as 17 first-class Model Context Protocol (MCP) agent tools for Claude Desktop, Cursor, and LLMs."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain001-mcp: Model Context Protocol Server for AI Payment Tools"
twitter_url: "https://pain001.com/pain001-mcp/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"

---

# pain001-mcp: Model Context Protocol Server

**`pain001-mcp`** is an open-source Model Context Protocol (MCP) server that exposes the `pain001` ISO 20022 payment library as **17 first-class agent tools**.

AI assistants and autonomous agents (such as Claude Desktop, Cursor, and custom FastMCP clients) can discover and invoke payment validation, charset transliteration, schema migration, and XML file generation directly within conversational workflows.

---

## Key Capabilities & Tools

| Tool Name | Description |
| :--- | :--- |
| `generate_xml_string` | Converts payment records into XSD-validated ISO 20022 `pain.001` or `pain.008` XML string. |
| `validate_identifier` | Validates IBANs (ISO 13616 / mod-97 check) and BIC codes (ISO 9362). |
| `migrate_records` | Round-trips and migrates payment records across schema versions (e.g. `pain.001.001.03` -> `pain.001.001.09` -> `.12`). |
| `sanitize_to_iso20022_charset` | Transliterates non-ISO 20022 Latin charset characters into valid SWIFT/SEPA character sets. |
| `parse_file` | Reads CSV, Excel, SQLite, or JSON files and returns structured payment dictionaries. |
| `load_schema` | Returns the official JSON Schema definition for any supported message type. |
| `get_supported_messages` | Lists all 20+ supported ISO 20022 `pain.001` and `pain.008` message versions. |

---

## Quick Start & Registration

### Installation
```bash
pip install pain001-mcp
```

### Register with Claude Desktop
Add the following snippet to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pain001": {
      "command": "python",
      "args": ["-m", "pain001_mcp"]
    }
  }
}
```
