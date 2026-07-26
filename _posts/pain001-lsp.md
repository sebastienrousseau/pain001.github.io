---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A code editor showing red diagnostics under an invalid IBAN in a payment JSON file — pain001-lsp validating ISO 20022 data as it is typed."
banner_height: 500
banner_width: 1200
banner: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
cdn: "https://cloudcdn.pro"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Language Server Protocol support for payment JSON: live schema validation, IBAN/BIC diagnostics, completion, hover docs, and quick fixes in VS Code, Neovim, Helix, Emacs."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/pain001-lsp/"
image_alt: "A code editor showing red diagnostics under an invalid IBAN in a payment JSON file — pain001-lsp validating ISO 20022 data as it is typed."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001-lsp, payment file validation editor, LSP language server, pain.001 JSON validation, IBAN checksum editor, pygls"
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
permalink: "https://pain001.com/pain001-lsp/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Payment-file mistakes caught at the keystroke: live ISO 20022 diagnostics in VS Code, Neovim, Helix, and Emacs."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "0, 132, 199"
title: "pain001-lsp: ISO 20022 Diagnostics in Your Editor"
url: "https://pain001.com/pain001-lsp/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-lsp/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Language Server Protocol support for payment JSON: live schema validation, IBAN/BIC diagnostics, completion, hover docs, and quick fixes in VS Code, Neovim, Helix, Emacs."
item_guid: "https://pain001.com/pain001-lsp/rss.xml"
item_link: "https://pain001.com/pain001-lsp/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain001-lsp: ISO 20022 Diagnostics in Your Editor"
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
apple-mobile-web-app-title: "pain001-lsp: ISO 20022 Diagnostics in Your Editor"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Language Server Protocol support for payment JSON: live schema validation, IBAN/BIC diagnostics, completion, hover docs, and quick fixes in VS Code, Neovim, Helix, Emacs."
twitter_image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain001-lsp: ISO 20022 Diagnostics in Your Editor"
twitter_url: "https://pain001.com/pain001-lsp/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Editor tooling"
excerpt: "pain001-lsp brings the Language Server Protocol to payment data authoring: as-you-type schema validation, IBAN checksum and BIC diagnostics, field completion, hover documentation, a quick-fix that inserts missing required fields, formatting, and document symbols for large batches — built on pygls and tested to 100% branch coverage."
last_reviewed: "2026-07-26"

---

**`pain001-lsp` v0.0.54** is a Language Server Protocol implementation for payment-data authoring. It validates payment JSON against ISO 20022 message schemas as you type — in VS Code, Neovim, Helix, Emacs, or any LSP-compliant editor.

A malformed batch discovered at the bank gateway costs a repair cycle, a cut-off time, and sometimes a settlement day. The same error discovered as a red squiggle while typing costs nothing. That is the entire premise.

---

## 01. Six editor features

- **Live diagnostics.** Each record in a payment JSON file is validated against the selected message type's JSON Schema on open and on every change. Dedicated checks cover IBAN checksums (ISO 13616 mod-97) and BIC structure (ISO 9362) across debtor, creditor, charge, and forwarding-agent fields.
- **Completion.** Field-name and message-type suggestions with inline documentation.
- **Hover.** Schema descriptions for the field under the cursor — lengths, formats, requirements.
- **Quick-fix code action.** "Add missing required fields" inserts type-correct placeholders, multi-record aware.
- **Formatting.** Re-serialises payment JSON with 2-space indentation and a trailing newline; malformed JSON is left untouched rather than mangled.
- **Document symbols.** One symbol per payment record, so editor outlines and breadcrumbs navigate large batches.

CSV files are supported for diagnostics: `.csv` URIs are routed through a dedicated CSV validation path.

The default message type is `pain.001.001.09`; all 11 supported definitions (`pain.001.001.03`–`.12`, `pain.008.001.02`) can be selected per workspace via `initializationOptions` or live via `workspace/didChangeConfiguration`.

---

## 02. Setup

```bash
pip install pain001-lsp
```

**Neovim (0.11+):**

```lua
vim.lsp.config("pain001", {
  cmd = { "pain001-lsp" },
  filetypes = { "json" },
  init_options = { messageType = "pain.001.001.09" },
})
vim.lsp.enable("pain001")
```

**VS Code:** a launchable extension scaffold ships in the repository's `editors/vscode/` directory. **Helix, Emacs (eglot), and generic clients:** point the language server command at `pain001-lsp` (stdio).

---

## 03. Built on pygls, verified to 100%

The server is a single auditable module built on [pygls](https://github.com/openlawlibrary/pygls), the same foundation used by major Python language servers. Diagnostics carry `source: "pain001-lsp"` so they compose cleanly with other servers, and the test suite is enforced at 100% line and branch coverage in CI.

---

## FAQ

**Why validate payment files in an editor at all?**

Because most corporate payment batches still begin life as a file a human assembles or reviews. Editor-time validation moves rejection-class errors — a transposed IBAN digit, a missing `requested_execution_date` — from the bank's gateway to the keystroke where they happen.

**Does it validate the final XML?**

The LSP validates the *input records*. XSD validation of the rendered XML happens in the [core library](/documentation/) at generation time — the same dual gate the CLI and REST API apply.

**Which file types does it understand?**

JSON arrays of flat payment records (the primary target, with all six features) and CSV files (diagnostics). See the [repository](https://github.com/sebastienrousseau/pain001-lsp) for editor-specific guides.
