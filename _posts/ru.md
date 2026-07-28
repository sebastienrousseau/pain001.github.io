---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Python-пакет с открытым кодом: файлы pain.001 и pain.008 с XSD-валидацией из CSV, Excel, SQLite, JSON, Parquet или SWIFT MT101 — с инструментами MCP для ИИ-агентов и LSP-сервером."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Python-пакет с открытым кодом: файлы pain.001 и pain.008 с XSD-валидацией из CSV, Excel, SQLite, JSON, Parquet или SWIFT MT101 — с инструментами MCP для ИИ-агентов и LSP-сервером."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "ru"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/ru/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, Русский"
language: "ru"
layout: "page"
locale: "ru_RU"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/ru/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Пакет с открытым кодом, превращающий платёжные данные в валидированный XML ISO 20022 — проверенный до того, как его увидит банк."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — инициирование платежей ISO 20022 с открытым кодом"
url: "https://pain001.com/ru/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/ru/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Python-пакет с открытым кодом: файлы pain.001 и pain.008 с XSD-валидацией из CSV, Excel, SQLite, JSON, Parquet или SWIFT MT101 — с инструментами MCP для ИИ-агентов и LSP-сервером."
item_guid: "https://pain001.com/ru/rss.xml"
item_link: "https://pain001.com/ru/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — инициирование платежей ISO 20022 с открытым кодом"
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
apple-mobile-web-app-title: "Pain001 — инициирование платежей ISO 20022 с открытым кодом"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Python-пакет с открытым кодом: файлы pain.001 и pain.008 с XSD-валидацией из CSV, Excel, SQLite, JSON, Parquet или SWIFT MT101 — с инструментами MCP для ИИ-агентов и LSP-сервером."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — инициирование платежей ISO 20022 с открытым кодом"
twitter_url: "https://pain001.com/ru/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 по-русски"
excerpt: "Python-пакет с открытым кодом: файлы pain.001 и pain.008 с XSD-валидацией из CSV, Excel, SQLite, JSON, Parquet или SWIFT MT101 — с инструментами MCP для ИИ-агентов и LSP-сервером."
last_reviewed: "2026-07-26"


---

## Платёжные файлы, которые банк не отклонит

**Pain001** — Python-пакет с открытым исходным кодом для инициирования платежей ISO 20022. Он преобразует данные, которые у вас уже есть — CSV, Excel, SQLite, JSON, Parquet или устаревшие сообщения SWIFT MT101 — в XML `pain.001` (переводы) и `pain.008` (прямые дебеты), валидированный официальными XSD-схемами.

Каждый файл проходит три уровня проверки: JSON-схема для каждой записи (включая контроль mod-97 для IBAN и структуру BIC), правила scheme (SEPA и трансграничный CBPR+) и итоговую XSD-валидацию. Контрольные суммы пересчитываются, а не копируются. Всё работает локально: платёжные данные не покидают вашу инфраструктуру.

## Попробуйте в браузере

Проверьте пример пакета прямо в браузере — ничего не загружается на сервер — и подтвердите результат официальной XSD-схемой: [попробовать Pain001](/try/). Примеры CSV-файлов можно скачать как шаблоны для собственных выгрузок.

## Срок — 14 ноября 2026 года

После завершения сосуществования MT–MX 22 ноября 2025 года следующий срок — **14 ноября 2026 года**: полностью неструктурированные почтовые адреса будут отклоняться в платежах CBPR+, а межбанковская трансляция MT101 будет заменена `pain.001` версии 9. Pain001 уже генерирует структурированные и гибридные адреса — и конвертирует MT101 одной командой.

## Начало работы

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

Далее: [руководство по установке](/installation/), [технический справочник](/documentation/), [дорожная карта ISO 20022 до 2028 года](/iso20022-roadmap/), [коды отклонения pain.002](/pain002-reason-codes/), [центр доверия](/trust/) и [резюме для руководства](/executive-brief/). Полная документация на английском. Двойная лицензия Apache-2.0 / MIT — свободное коммерческое использование в любом масштабе.
