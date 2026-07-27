---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "CSV・Excel・SQLite・JSON・Parquet・SWIFT MT101 から XSD 検証済みの pain.001 / pain.008 ファイルを生成するオープンソース Python スイート。AI エージェント向け MCP ツールと LSP サーバーを同梱。"
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://cloudcdn.pro"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "CSV・Excel・SQLite・JSON・Parquet・SWIFT MT101 から XSD 検証済みの pain.001 / pain.008 ファイルを生成するオープンソース Python スイート。AI エージェント向け MCP ツールと LSP サーバーを同梱。"
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "ja"
icon: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
id: "https://pain001.com/ja/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, 日本語"
language: "ja"
layout: "page"
locale: "ja_JP"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://cloudcdn.pro/pain001/v1/logos/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/ja/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "支払いデータを検証済み ISO 20022 XML に変換するオープンソーススイート — 銀行に届く前に正しさを証明します。"
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — オープンソースの ISO 20022 送金指図"
url: "https://pain001.com/ja/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/ja/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "CSV・Excel・SQLite・JSON・Parquet・SWIFT MT101 から XSD 検証済みの pain.001 / pain.008 ファイルを生成するオープンソース Python スイート。AI エージェント向け MCP ツールと LSP サーバーを同梱。"
item_guid: "https://pain001.com/ja/rss.xml"
item_link: "https://pain001.com/ja/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — オープンソースの ISO 20022 送金指図"
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
apple-mobile-web-app-title: "Pain001 — オープンソースの ISO 20022 送金指図"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "CSV・Excel・SQLite・JSON・Parquet・SWIFT MT101 から XSD 検証済みの pain.001 / pain.008 ファイルを生成するオープンソース Python スイート。AI エージェント向け MCP ツールと LSP サーバーを同梱。"
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — オープンソースの ISO 20022 送金指図"
twitter_url: "https://pain001.com/ja/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "日本語版 Pain001"
excerpt: "CSV・Excel・SQLite・JSON・Parquet・SWIFT MT101 から XSD 検証済みの pain.001 / pain.008 ファイルを生成するオープンソース Python スイート。AI エージェント向け MCP ツールと LSP サーバーを同梱。"
last_reviewed: "2026-07-26"


---

## 銀行に差し戻されない支払いファイル

**Pain001** は ISO 20022 送金指図のためのオープンソース Python スイートです。手元にあるデータ — CSV、Excel、SQLite、JSON、Parquet、旧来の SWIFT MT101 メッセージ — を、公式 XSD スキーマで検証済みの `pain.001`(振込)および `pain.008`(口座振替)XML に変換します。

各ファイルは書き出される前に 3 段階の検証を通過します。レコードごとの JSON スキーマ(IBAN の mod-97 チェックと BIC 構造を含む)、スキームルール(SEPA および国際送金 CBPR+)、最終 XSD 検証です。コントロール合計は必ず再計算され、コピーされることはありません。すべてローカルで動作し、支払いデータがインフラの外に出ることはありません。

## ブラウザで試す

サンプルバッチをブラウザ内で直接検証できます — 何もアップロードされません — 結果は公式 XSD スキーマで証明されます:[Pain001 を試す](/try/)。サンプル CSV は自社エクスポートのテンプレートとしてダウンロード可能です。

## 2026 年 11 月 14 日の期限

2025 年 11 月 22 日に MT–MX 共存期間が終了し、次の期限は **2026 年 11 月 14 日**です。完全に非構造化の住所は CBPR+ 送金で拒否され、銀行間 MT101 リレーは `pain.001` バージョン 9 に置き換えられます。Pain001 は構造化住所・ハイブリッド住所を今日から生成でき、MT101 も 1 コマンドで変換します。

## はじめに

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

さらに:[インストールガイド](/installation/)、[技術リファレンス](/documentation/)、[2028 年までの ISO 20022 ロードマップ](/iso20022-roadmap/)、[pain.002 拒否コード](/pain002-reason-codes/)、[トラストセンター](/trust/)、[経営層向けサマリー](/executive-brief/)。完全なドキュメントは英語です。Apache-2.0 / MIT のデュアルライセンスで、どの規模でも商用利用は無償です。
