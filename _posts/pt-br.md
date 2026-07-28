---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "Suíte Python de código aberto para gerar arquivos pain.001 e pain.008 validados por XSD a partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — com ferramentas MCP para agentes de IA e servidor LSP."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Suíte Python de código aberto para gerar arquivos pain.001 e pain.008 validados por XSD a partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — com ferramentas MCP para agentes de IA e servidor LSP."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: "pt-br"
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/pt-br/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation — the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001, ISO 20022, pain.001, SEPA, SWIFT, Python, Português (Brasil)"
language: "pt-BR"
layout: "page"
locale: "pt_BR"
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
measurementID: G-167B274ZWJ
name: Pain001
permalink: "https://pain001.com/pt-br/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "A suíte de código aberto que transforma seus dados de pagamento em XML ISO 20022 validado — comprovado antes de chegar ao banco."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Pain001 — Iniciação de pagamentos ISO 20022 em código aberto"
url: "https://pain001.com/pt-br/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/pt-br/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.47)"
item_description: "Suíte Python de código aberto para gerar arquivos pain.001 e pain.008 validados por XSD a partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — com ferramentas MCP para agentes de IA e servidor LSP."
item_guid: "https://pain001.com/pt-br/rss.xml"
item_link: "https://pain001.com/pt-br/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Pain001 — Iniciação de pagamentos ISO 20022 em código aberto"
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
apple-mobile-web-app-title: "Pain001 — Iniciação de pagamentos ISO 20022 em código aberto"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: @wwdseb
twitter_description: "Suíte Python de código aberto para gerar arquivos pain.001 e pain.008 validados por XSD a partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — com ferramentas MCP para agentes de IA e servidor LSP."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: @wwdseb
twitter_title: "Pain001 — Iniciação de pagamentos ISO 20022 em código aberto"
twitter_url: "https://pain001.com/pt-br/"
author_website: "https://sebastienrousseau.com"
author_twitter: @wwdseb
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Pain001 em português"
excerpt: "Suíte Python de código aberto para gerar arquivos pain.001 e pain.008 validados por XSD a partir de CSV, Excel, SQLite, JSON, Parquet ou SWIFT MT101 — com ferramentas MCP para agentes de IA e servidor LSP."
last_reviewed: "2026-07-26"


---

## Arquivos de pagamento que seu banco não vai rejeitar

**Pain001** é uma suíte Python de código aberto para iniciação de pagamentos ISO 20022. Ela converte os dados que você já tem — CSV, Excel, SQLite, JSON, Parquet ou mensagens SWIFT MT101 legadas — em XML `pain.001` (transferências) e `pain.008` (débitos diretos), validados contra os esquemas XSD oficiais.

Cada arquivo passa por três camadas de validação antes de ser gravado: esquema JSON por registro (com verificação mod-97 do IBAN e estrutura do BIC), regras de scheme (SEPA e CBPR+ internacional) e validação XSD final. Os totais de controle são recalculados, nunca copiados. Tudo roda localmente: nenhum dado de pagamento sai da sua infraestrutura.

## Teste no navegador

Valide um lote de exemplo diretamente no navegador — nada é enviado — e prove o resultado contra o esquema XSD oficial: [testar o Pain001](/try/). Arquivos CSV de exemplo podem ser baixados como modelos para suas exportações.

## O prazo de 14 de novembro de 2026

Com o fim da coexistência MT–MX em 22 de novembro de 2025, o próximo prazo é **14 de novembro de 2026**: endereços postais totalmente não estruturados serão rejeitados nos pagamentos CBPR+ e o relay interbancário MT101 será substituído pelo `pain.001` versão 9. O Pain001 já gera endereços estruturados e híbridos — e converte MT101 com um único comando.

## Como começar

```bash
pip install pain001
pain001 -t pain.001.001.09 -d payments.csv -o out/ --dry-run
```

Para aprofundar: [guia de instalação](/installation/), [referência técnica](/documentation/), [roteiro ISO 20022 até 2028](/iso20022-roadmap/), [códigos de rejeição pain.002](/pain002-reason-codes/), [central de confiança](/trust/) e [resumo executivo](/executive-brief/). A documentação completa está em inglês. Licença dupla Apache-2.0 / MIT — uso comercial livre em qualquer escala.
