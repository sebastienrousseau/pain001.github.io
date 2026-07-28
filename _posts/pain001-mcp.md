---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "An AI assistant conversation generating a validated ISO 20022 payment file through the pain001-mcp Model Context Protocol server, entirely on the user's own machine."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "17 Model Context Protocol tools for AI agents — validate IBANs, migrate pain.001 versions, convert MT101, and generate XSD-validated payment XML locally over stdio."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/pain001-mcp/"
image_alt: "An AI assistant conversation generating a validated ISO 20022 payment file through the pain001-mcp Model Context Protocol server, entirely on the user's own machine."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001-mcp, MCP server payments, ISO 20022 AI agent, Model Context Protocol finance, Claude payment tools, agentic payments, pain.001 generation AI"
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
permalink: "https://pain001.com/pain001-mcp/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Seventeen read-only tools that let AI agents validate, migrate, convert, and generate ISO 20022 payment files — locally, over stdio."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain001-mcp: The MCP Server for ISO 20022 Payments"
url: "https://pain001.com/pain001-mcp/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-mcp/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "17 Model Context Protocol tools for AI agents — validate IBANs, migrate pain.001 versions, convert MT101, and generate XSD-validated payment XML locally over stdio."
item_guid: "https://pain001.com/pain001-mcp/rss.xml"
item_link: "https://pain001.com/pain001-mcp/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain001-mcp: The MCP Server for ISO 20022 Payments"
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
apple-mobile-web-app-title: "pain001-mcp: The MCP Server for ISO 20022 Payments"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "17 Model Context Protocol tools for AI agents — validate IBANs, migrate pain.001 versions, convert MT101, and generate XSD-validated payment XML locally over stdio."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain001-mcp: The MCP Server for ISO 20022 Payments"
twitter_url: "https://pain001.com/pain001-mcp/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "AI agents"
excerpt: "pain001-mcp is the Model Context Protocol server for ISO 20022 payment initiation. Claude, Cursor, and any MCP client can check IBANs, inspect schemas, migrate message versions, convert SWIFT MT101, parse camt.053 and pain.002, and generate XSD-validated XML. Every tool is annotated read-only and idempotent; no tool can submit a payment."
last_reviewed: "2026-07-26"

---

**`pain001-mcp` v0.0.57** exposes the Pain001 suite to AI agents as **17 Model Context Protocol tools**. Claude Desktop, Claude Code, Cursor, and any MCP-compatible orchestrator can validate IBANs, migrate message versions, convert SWIFT MT101, and generate schema-validated `pain.001` XML — inside a conversation, on your own machine.

Card networks and PSPs have built agentic *checkout* rails. The corporate payment-file layer — where credit transfers are actually initiated — had no agent interface. This server fills that gap. Payment data never leaves your machine: the transport is stdio, and every tool is annotated read-only and idempotent, so an agent can explore safely without side effects.

---

## 01. The 17 tools

| Tool | What it does |
| :--- | :--- |
| `list_message_types` | List the 11 supported message definitions with human-readable names. |
| `get_required_fields` | Return the required input fields for a message type. |
| `get_input_schema` | Return the full JSON Schema for a message type. |
| `validate_records` | Validate flat payment records against the input schema. |
| `validate_identifier` | Check a single IBAN (ISO 13616 mod-97) or BIC (ISO 9362). |
| `generate_message` | Generate XSD-validated pain XML from in-memory records. |
| `generate_message_async` | Off-event-loop generation for large batches. |
| `generate_message_from_file` | Generate XML from a CSV file on disk. |
| `list_supported_formats` | List loadable on-disk formats (CSV, SQLite, JSON, JSONL, Parquet). |
| `parse_camt053` | Parse a camt.053 bank statement XML file. |
| `parse_pain002` | Parse a pain.002 payment status report. |
| `inspect_template` | Show the CSV column headers of a bundled template. |
| `validate_payment_scheme` | Enforce a scheme rulebook: SEPA SCT, Instant, SDD Core, B2B, or cross-border. |
| `migrate_records` | Migrate records between pain.001 versions (e.g. `.03` → `.09`). |
| `validate_xml_against_schema` | Validate raw XML against the bundled official XSD. |
| `sanitize_to_iso20022_charset` | Transliterate text to the ISO 20022 Latin character set. |
| `convert_mt101` | Convert a legacy SWIFT MT101 message into pain.001 records. |

The server also publishes a `pain001://schema/{message_type}` resource and a `build_payment_batch` prompt. Shorthand aliases resolve sensibly: `pain.001` → `pain.001.001.09`, `pain.008` → `pain.008.001.02`.

---

## 02. Registration

```bash
pip install pain001-mcp
```

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "pain001": {
      "command": "pain001-mcp"
    }
  }
}
```

**Claude Code:**

```bash
claude mcp add pain001 -- pain001-mcp
```

A Docker image is published as `ghcr.io/sebastienrousseau/pain001-mcp` with build provenance attestation, and the server is listed in the MCP registry as `io.github.sebastienrousseau/pain001-mcp`.

---

## 03. Design decisions that matter in a payments context

- **Read-only by contract.** All 17 tools carry MCP `ToolAnnotations` with `readOnlyHint=true`, `destructiveHint=false`, and `idempotentHint=true`. The server never writes to your filesystem.
- **Errors are data, not crashes.** Tools return structured `{"error": ...}` payloads instead of raising, so agent loops degrade gracefully.
- **Local-only transport.** stdio only — no network listener, no credentials, no payment data leaving the host.
- **Validated output or nothing.** `generate_message` runs the same JSON Schema → scheme rulebook → XSD pipeline as the CLI; an agent cannot produce a malformed file.

Note the distinction: `pain001 mcp` (the core library's built-in server) exposes a minimal 5-tool surface. The full 17-tool surface documented here is the standalone `pain001-mcp` package.

---

## FAQ

**Can an AI agent actually submit payments with this?**

No. The server generates and validates payment *files*; it has no bank connectivity and no tool with side effects beyond returning XML as text. Submission to your bank channel remains a human-controlled step — by design.

**Does it work with agentic-payment protocols like AP2?**

It complements them. AP2 and similar protocols handle mandates and authorisation for agent-initiated commerce; `pain001-mcp` handles the ISO 20022 file layer that corporate banking channels actually consume. The related [ap2-iso20022](https://github.com/sebastienrousseau/ap2-iso20022) project bridges the two.

**Which clients are tested?**

Any MCP client speaking stdio works. Claude Desktop, Claude Code, and Cursor configurations are documented in the [repository](https://github.com/sebastienrousseau/pain001-mcp), and CI runs the official MCP Inspector against every release.
