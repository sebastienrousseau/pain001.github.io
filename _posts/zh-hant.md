---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "開源 Python 套件,可從 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 產生經 XSD 驗證的 pain.001 與 pain.008 檔案——附有供 AI 代理使用的 MCP 工具與 LSP 伺服器。"
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "開源 Python 套件,可從 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 產生經 XSD 驗證的 pain.001 與 pain.008 檔案——附有供 AI 代理使用的 MCP 工具與 LSP 伺服器。"
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "zh-hant"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/zh-hant/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, 繁體中文"
language: "zh-Hant"
layout: "page"
locale: "zh_TW"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/zh-hant/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "將您的付款資料轉換為經驗證的 ISO 20022 XML 的開源套件——在送達銀行之前即證明其正確性。"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — 開源 ISO 20022 付款發起"
url: "https://pain001.com/zh-hant/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/zh-hant/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "開源 Python 套件,可從 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 產生經 XSD 驗證的 pain.001 與 pain.008 檔案——附有供 AI 代理使用的 MCP 工具與 LSP 伺服器。"
item_guid: "https://pain001.com/zh-hant/rss.xml"
item_link: "https://pain001.com/zh-hant/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — 開源 ISO 20022 付款發起"
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
apple-mobile-web-app-title: "Pain001 — 開源 ISO 20022 付款發起"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "開源 Python 套件,可從 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 產生經 XSD 驗證的 pain.001 與 pain.008 檔案——附有供 AI 代理使用的 MCP 工具與 LSP 伺服器。"
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — 開源 ISO 20022 付款發起"
twitter_url: "https://pain001.com/zh-hant/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "繁體中文版 Pain001"
excerpt: "開源 Python 套件,可從 CSV、Excel、SQLite、JSON、Parquet 或 SWIFT MT101 產生經 XSD 驗證的 pain.001 與 pain.008 檔案——附有供 AI 代理使用的 MCP 工具與 LSP 伺服器。"
last_reviewed: "2026-07-26"


---

## 銀行不會退回的付款檔案

**Pain001** 是用於 ISO 20022 付款發起的開源 Python 套件。它將您既有的資料——CSV、Excel、SQLite、JSON、Parquet 或舊式 SWIFT MT101 報文——轉換為經官方 XSD 結構描述驗證的 `pain.001`(信用轉帳)與 `pain.008`(直接扣款)XML。

每個檔案在寫出前都須通過三層驗證:逐筆記錄的 JSON 結構描述(含 IBAN 的 mod-97 檢查與 BIC 結構)、清算規則(SEPA 與跨境 CBPR+),以及最終的 XSD 驗證。控制總數一律重新計算,絕不複製。一切皆在本機執行:任何付款資料都不會離開您的基礎設施。

## 在瀏覽器中試用

直接在瀏覽器中驗證示範批次——不會上傳任何內容——並以官方 XSD 結構描述證明結果:[試用 Pain001](/try/)。示範 CSV 檔案可下載,作為您自己匯出資料的範本。

## 2026 年 11 月 14 日期限

MT–MX 並存期已於 2025 年 11 月 22 日結束,下一個期限是 **2026 年 11 月 14 日**:完全非結構化的郵政地址將在 CBPR+ 付款中遭拒,銀行間 MT101 中繼將由 `pain.001` 第 9 版取代。Pain001 今天即可產生結構化與混合地址——並以一道指令轉換 MT101。

## 快速開始

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

更多:[安裝指南](/installation/)、[技術參考](/documentation/)、[至 2028 年的 ISO 20022 路線圖](/iso20022-roadmap/)、[pain.002 拒絕代碼](/pain002-reason-codes/)、[信任中心](/trust/)與[高階主管摘要](/executive-brief/)。完整文件為英文。Apache-2.0 / MIT 雙授權——任何規模皆可免費商用。
