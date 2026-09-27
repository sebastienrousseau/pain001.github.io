---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "High-throughput native Rust validation engine for ISO 20022 payments with pain001-fast."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: weekly
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-09-27T08:00:00+00:00"
description: "High-throughput native Rust acceleration core for ISO 20022 payments: zero-allocation IBAN mod-97, BIC routing checks, and 50,000+ tx/s batch validation."
download: "https://pypi.org/project/pain001-fast/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/pain001-fast/"
image_alt: "High-throughput native Rust validation engine for ISO 20022 payments with pain001-fast."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001-fast, rust iso20022, high-throughput financial validation, pyo3 payment engine, iban mod 97 rust, rayon payment batching"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/pain001-fast/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Sub-25ns zero-allocation validation and 50,000+ tx/s multi-core batch processing for high-frequency financial gateways."
tags: "ISO 20022, pain001, payments, python, banking"
theme_color: "#0b0e14"
title: "pain001-fast: Native Rust High-Throughput Core"
url: "https://pain001.com/pain001-fast/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pain001-fast/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.63)"
item_description: "High-throughput native Rust acceleration core for ISO 20022 payments: zero-allocation IBAN mod-97, BIC routing checks, and 50,000+ tx/s batch validation."
item_guid: "https://pain001.com/pain001-fast/rss.xml"
item_link: "https://pain001.com/pain001-fast/rss.xml"
item_pub_date: "Sun, 27 Sep 2026 08:00:00 +0000"
item_title: "pain001-fast: Native Rust High-Throughput Core"
last_build_date: "Sun, 27 Sep 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Sun, 27 Sep 2026 08:00:00 +0000"
ttl: 60
type: website
webmaster: contact@pain001.com
apple_mobile_web_app_orientations: portrait
---

## High-Throughput Native Acceleration for ISO 20022

`pain001-fast` is an optional, high-throughput native acceleration core written in Rust with PyO3 bindings. Designed for corporate treasury backbones, high-frequency clearing hubs, and payment service providers, it offloads CPU-intensive validation loops from the Python Global Interpreter Lock (GIL) to parallel multi-core hardware.

```bash
pip install pain001-fast
```

When installed, `pain001` core automatically promotes IBAN, BIC, and character set validations to native machine speed without requiring any configuration or API changes.

---

## Performance Characteristics

Micro-benchmarked on modern 64-bit multi-core hardware:

| Benchmark Scenario | Standard Pure Python | pain001-fast (Rust) | Speedup Factor |
| :--- | :--- | :--- | :--- |
| **IBAN Checksum (Mod-97)** | 1,850 ns / op | **22 ns / op** | **~84× faster** |
| **BIC Structural Check** | 1,200 ns / op | **14 ns / op** | **~85× faster** |
| **SWIFT-X Diacritic Sanitization** | 2,100 ns / op | **115 ns / op** | **~18× faster** |
| **Batch Analysis (10,000 orders)** | 3,450 ms | **165 ms** | **> 60,000 tx/sec** |
| **Heap Memory Overhead** | ~12 objects / tx | **0 heap allocations** | **Zero Allocation** |

---

## Core Capabilities

### 1. Zero-Allocation Mod-97 Engine
Implements ISO 7064 mod-97-10 check digit verification directly in CPU registers. By streaming ASCII character byte arithmetic through an inlined modular accumulator, `pain001-fast` completely eliminates the big integer string heap allocations that constrain standard interpreter runtimes.

### 2. Regex-Free Structural BIC Parsing
Validates 8 and 11 character ISO 9362 Business Identifier Codes using inlined byte checks and branchless lookup tables against the official ISO 3166-1 alpha-2 country registry.

### 3. NFKD Character Set Sanitizer
Fast Unicode normalization decomposes accented characters (such as `é` to `e`, `ü` to `u`) and replaces unpermitted characters with compliant ASCII delimiters in sub-microsecond time.

### 4. Parallel Multi-Core Batch Analyzer
Leverages Rayon work-stealing thread pools to validate thousands of transaction records across all available CPU cores simultaneously:
- Calculates per-currency control sums and counts.
- Builds SHA-256 / composite collision fingerprints to detect duplicate payments in memory.
- Returns comprehensive structured diagnostic reports with sub-50ms p99 latency.

---

## Python API Quick Start

```python
from pain001_fast import validate_iban, validate_bic, validate_payment_batch

# Sub-25ns IBAN validation
assert validate_iban("DE89370400440532013000") is True

# Structural BIC verification
assert validate_bic("DEUTDEFF500") is True

# High-throughput batch validation across CPU cores
orders = [
    {
        "creditor_iban": "DE89370400440532013000",
        "creditor_bic": "DEUTDEFF",
        "amount": "1250.00",
        "currency": "EUR",
        "execution_date": "2026-10-01",
    }
]

report = validate_payment_batch(orders)
assert report["valid"] is True
assert report["transaction_count"] == 1
assert report["control_sums"]["EUR"] == 1250.00
```

---

## Architectural Guarantee & Fallback

`pain001-fast` maintains complete behavioral and cryptographic parity with standard `pain001`. In constrained execution environments such as Pyodide, WebAssembly, or minimalist containers where native compiled extensions are unavailable, `pain001` falls back cleanly to its pure-Python routines with zero disruption.
