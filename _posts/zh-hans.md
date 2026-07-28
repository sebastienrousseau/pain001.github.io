---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "开源 Python 套件,可从 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 生成经 XSD 校验的 pain.001 和 pain.008 文件——附带面向 AI 代理的 MCP 工具和 LSP 服务器。"
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "开源 Python 套件,可从 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 生成经 XSD 校验的 pain.001 和 pain.008 文件——附带面向 AI 代理的 MCP 工具和 LSP 服务器。"
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "zh-hans"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/zh-hans/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, 简体中文"
language: "zh-Hans"
layout: "page"
locale: "zh_CN"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/zh-hans/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "将您的支付数据转换为经过校验的 ISO 20022 XML 的开源套件——在到达银行之前即证明其正确性。"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — 开源 ISO 20022 支付发起"
url: "https://pain001.com/zh-hans/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/zh-hans/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "开源 Python 套件,可从 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 生成经 XSD 校验的 pain.001 和 pain.008 文件——附带面向 AI 代理的 MCP 工具和 LSP 服务器。"
item_guid: "https://pain001.com/zh-hans/rss.xml"
item_link: "https://pain001.com/zh-hans/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — 开源 ISO 20022 支付发起"
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
apple-mobile-web-app-title: "Pain001 — 开源 ISO 20022 支付发起"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "开源 Python 套件,可从 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 生成经 XSD 校验的 pain.001 和 pain.008 文件——附带面向 AI 代理的 MCP 工具和 LSP 服务器。"
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — 开源 ISO 20022 支付发起"
twitter_url: "https://pain001.com/zh-hans/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "简体中文版 Pain001"
excerpt: "开源 Python 套件,可从 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 生成经 XSD 校验的 pain.001 和 pain.008 文件——附带面向 AI 代理的 MCP 工具和 LSP 服务器。"
last_reviewed: "2026-07-26"


---

## 银行不会退回的支付文件

**Pain001** 是用于 ISO 20022 支付发起的开源 Python 套件。它将您已有的数据——CSV、Excel、SQLite、JSON、Parquet 或旧式 SWIFT MT101 报文——转换为经官方 XSD 模式校验的 `pain.001`(贷记转账)和 `pain.008`(直接借记)XML。

每个文件在写出前都要通过三层校验:逐条记录的 JSON 模式(含 IBAN 的 mod-97 校验和 BIC 结构)、清算规则(SEPA 及跨境 CBPR+)以及最终的 XSD 校验。控制合计始终重新计算,绝不复制。一切都在本地运行:任何支付数据都不会离开您的基础设施。

## 在浏览器中试用

直接在浏览器中校验示例批次——不上传任何内容——并用官方 XSD 模式证明结果:[试用 Pain001](/try/)。示例 CSV 文件可下载,作为您自己导出数据的模板。

## 2026 年 11 月 14 日截止期限

MT–MX 共存期已于 2025 年 11 月 22 日结束,下一个期限是 **2026 年 11 月 14 日**:完全非结构化的邮政地址将在 CBPR+ 支付中被拒收,银行间 MT101 中继将由 `pain.001` 第 9 版取代。Pain001 今天即可生成结构化和混合地址——并用一条命令转换 MT101。

## 快速开始

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

更多:[安装指南](/installation/)、[技术参考](/documentation/)、[至 2028 年的 ISO 20022 路线图](/iso20022-roadmap/)、[pain.002 拒绝代码](/pain002-reason-codes/)、[信任中心](/trust/)和[高管摘要](/executive-brief/)。完整文档为英文。Apache-2.0 / MIT 双重许可——任何规模均可免费商用。
