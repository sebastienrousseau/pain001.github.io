---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A reference table decoding ISO 20022 pain.002 payment status report reason codes, from AC01 to TM01, with causes and fixes."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Every pain.002 status code (RJCT, ACWC, PART…) and the ISO reason codes behind rejections — AC01, AM10, FF01, DU01, RR01 — with the typical cause and the practical fix for each."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/pain002-reason-codes/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain.002 reason codes, pain.002 reject codes, RJCT reason, AC01, AC04, AM04, AM10, FF01, MS03, payment rejected bank, SEPA reject codes, ExternalStatusReason, ISO 20022 status codes"
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
permalink: "https://pain001.com/pain002-reason-codes/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "The status and reason codes your bank sends back — decoded, with the typical cause and the practical fix for each."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "pain.002 Reason Codes: Why Banks Reject Payment Files"
url: "https://pain001.com/pain002-reason-codes/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain002-reason-codes/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Every pain.002 status code (RJCT, ACWC, PART…) and the ISO reason codes behind rejections — AC01, AM10, FF01, DU01, RR01 — with the typical cause and the practical fix for each."
item_guid: "https://pain001.com/pain002-reason-codes/rss.xml"
item_link: "https://pain001.com/pain002-reason-codes/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "pain.002 Reason Codes: Why Banks Reject Payment Files"
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
apple-mobile-web-app-title: "pain.002 Reason Codes: Why Banks Reject Payment Files"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Every pain.002 status code (RJCT, ACWC, PART…) and the ISO reason codes behind rejections — AC01, AM10, FF01, DU01, RR01 — with the typical cause and the practical fix for each."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "pain.002 Reason Codes: Why Banks Reject Payment Files"
twitter_url: "https://pain001.com/pain002-reason-codes/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Reference"
excerpt: "A working reference for pain.002 Customer Payment Status Reports: the nine status codes from RCVD to RJCT, and the ISO External Status Reason codes operations teams actually meet — format failures like FF01 and AM10, account failures like AC01 and AC04, mandate and regulatory codes — each with cause and fix, plus how to parse responses automatically."
last_reviewed: "2026-07-26"


---

## How to read a pain.002

When your bank answers a `pain.001` or `pain.008`, the `pain.002` Customer Payment Status Report carries a **status** at up to three levels — group (`GrpSts`), payment information block (`PmtInfSts`), and individual transaction (`TxSts`) — plus zero or more **status reason codes** explaining any non-acceptance. The codes come from the ISO 20022 External Code Sets (`ExternalStatusReason1Code`), which is the canonical registry; this page covers the codes payment-operations teams actually meet, with the usual cause and the practical fix.

## 01. Status codes: how bad is it?

| Status | Meaning | What to do |
| :--- | :--- | :--- |
| `RCVD` | Received — arrived, not yet checked | Nothing yet. |
| `ACTC` | Accepted, technical validation passed | Nothing — syntax and schema are fine. |
| `ACCP` | Accepted, customer profile checks passed | Nothing. |
| `ACSP` | Accepted, settlement in process | Nothing. |
| `ACSC` | Accepted, settlement completed | Done — reconcile against camt.053. |
| `ACWC` | Accepted **with change** — the bank altered something | Read the changes; fix your source data so the bank stops "helping". |
| `PART` | Partially accepted — some transactions rejected | Check per-transaction `TxSts`; resubmit only the rejected ones. |
| `PDNG` | Pending — further checks ongoing | Wait; investigate only if it persists past the bank's stated window. |
| `RJCT` | Rejected | Read the reason codes below; repair; resubmit. |

## 02. Format and schema failures

The rejections Pain001 exists to make impossible — every one of these is caught by the [validation gate](/try/) before submission:

| Code | Name | Typical cause | Fix |
| :--- | :--- | :--- | :--- |
| `FF01` | Invalid file format | Wrong schema version, malformed XML, wrong namespace | Validate against the exact XSD your bank profiles (`pain001 --dry-run`). |
| `AM10` | Invalid control sum | `CtrlSum` doesn't match the sum of amounts | Never hand-compute totals — Pain001 recomputes `NbOfTxs`/`CtrlSum` from the records. |
| `AM01` | Zero amount | An amount of 0 slipped through | Filter zero rows at source. |
| `AM02` | Amount not allowed | Above a scheme or account limit | Check scheme ceilings and account mandates. |
| `AM03` | Currency not allowed | Currency not supported on the account/scheme | SEPA schemes are EUR-only; use the cross-border rulebook otherwise. |
| `AM09` | Wrong amount | Amount disagrees with a referenced mandate/agreement | Reconcile against the mandate. |
| `DT01` | Invalid date | Execution date malformed, in the past, or a non-banking day | ISO 8601, forward-dated, banking-day adjusted. |
| `CH03` | Execution date too far in future | Beyond the bank's forward window (often 1 year) | Shorten the horizon. |
| `TM01` | Cut-off time | File arrived after the bank's processing cut-off | Automate submission earlier; know each bank's cut-offs. |
| `DU01`–`DU03` | Duplicate message / payment info / transaction ID | Re-used `MsgId`, `PmtInfId`, or `EndToEndId` | Generate unique IDs per submission; never resubmit a file unchanged. |

## 03. Account and identifier failures

| Code | Name | Typical cause | Fix |
| :--- | :--- | :--- | :--- |
| `AC01` | Incorrect account number | IBAN fails validation or doesn't exist | Mod-97 check before submission — the [demo](/try/) shows this live. |
| `AC03` | Invalid creditor account | Creditor IBAN wrong or closed | Verify against the invoice/master data. |
| `AC04` | Closed account | Account has been closed | Contact the counterparty for current details. |
| `AC06` | Blocked account | Account blocked for this transaction type | Counterparty must resolve with their bank. |
| `RC01` | Bank identifier incorrect | Malformed or unknown BIC | ISO 9362 structure check + directory lookup. |
| `AG01` | Transaction forbidden | Payment type not allowed on this account | Wrong account or missing product agreement. |
| `AG02` | Invalid bank operation code | Wrong local instrument / service level combination | Match your bank's implementation guide. |

## 04. Party, mandate, and regulatory failures

| Code | Name | Typical cause | Fix |
| :--- | :--- | :--- | :--- |
| `BE01` | Inconsistent with end customer | Name doesn't match the account | Fix creditor master data; this is what Verification of Payee checks pre-submission. |
| `BE04` | Missing creditor address | Address absent where required | From 14 Nov 2026, CBPR+ requires structured or hybrid addresses — see the [roadmap](/iso20022-roadmap/). |
| `BE05` | Unrecognised initiating party | Initiating party not authorised on the account | Check the bank mandate for the submitting entity. |
| `MD01` | No mandate | Direct debit without a valid mandate | Collect/register the mandate before collecting funds. |
| `MD02` | Missing mandate information | Mandate data incomplete in the pain.008 | Populate all mandate-related fields. |
| `MD07` | End customer deceased | — | Close the mandate. |
| `RR01`–`RR04` | Regulatory reasons | Missing debtor/creditor identification, name, address, or other regulatory data | Populate the party data your corridor requires; structured addresses solve most of these. |
| `AM04` | Insufficient funds | Not a format problem | Treasury, not toolchain. |
| `MS02` / `MS03` | Reason not specified (customer / bank generated) | The bank chose not to say | Call the bank; often accompanies sanctions or internal-policy holds. |
| `NARR` | Narrative | Free-text explanation in `AddtlInf` | Read the narrative field. |

## 05. Close the loop automatically

Pain001 parses pain.002 responses into structured data, so your pipeline can route rejections without a human reading XML:

```bash
pip install pain001
```

```python
from pain001.pain002 import parse_pain002_report

report = parse_pain002_report("bank-response.xml")
for tx in report["payment_statuses"]:
    if tx["transaction_status"] == "RJCT":
        print(tx["original_end_to_end_id"], tx["status_reason"])
```

### Validating the response before you trust it

The parser reads whichever pain.002 version your bank sends — it detects the namespace rather than assuming one. If you want the response checked against the official ISO schema first, pass `validate=True`:

```python
from pain001.pain002 import bundled_schema_versions, parse_pain002_report

report = parse_pain002_report("bank-response.xml", validate=True)
```

Pain001 bundles the ISO schemas for `pain.002.001.03` (what SEPA banks commonly reply with), `pain.002.001.12`, `pain.002.001.14` and `pain.002.001.15`; `bundled_schema_versions()` returns the current list. **If your bank replies in a version that is not bundled, `validate=True` raises rather than parsing unvalidated.** That is deliberate: silently skipping the check would report a validation that never happened. Either supply the schema yourself with `xsd_file_path=`, or omit `validate` and parse without schema validation.

The [MCP server](/pain001-mcp/) exposes the same parser to AI agents as `parse_pain002`, and the [payment-lifecycle guide](/payments/) shows where status handling sits in the full pipeline.

> **Canonical source.** Code definitions live in the ISO 20022 External Code Sets, maintained at [iso20022.org/catalogue-messages/additional-content-messages/external-code-sets](https://www.iso20022.org/catalogue-messages/additional-content-messages/external-code-sets "ISO 20022 External Code Sets registry") and revised quarterly. Bank implementation guides may narrow — but not contradict — these meanings. Spot an inaccuracy? [Report it](https://github.com/sebastienrousseau/pain001.github.io/issues).
