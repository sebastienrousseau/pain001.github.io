---

# Front Matter (YAML)
author: "Sebastien Rousseau"
banner_alt: "Aerial photography of mountain under clear blue sky"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://kura.pro/stock/images/banners/brady-bellini-WEQbe2jBg40.webp"
cdn: "https://kura.pro"
changefreq: "weekly"
charset: "utf-8"
copyright: "© 2023 Pain001. All rights reserved."
date: "Nov 28, 2023"
description: "pain.001.001.04, is an XML-based message format under the ISO 20022 standard designed to streamline cross-border and domestic payment processes."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://kura.pro/pain001/images/favicon.ico"
id: "https://pain001.com/pain.001.001.04/index.html"
image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
image_height: "100vh"
image_width: "100vw"
image: "https://kura.pro/pain001/images/titles/title-pain001.webp"
keywords: "pain.001.001.04, customer credit transfer initiation, XML, ISO 20022, cross-border payments, domestic payments, efficiency, speed, cost, compliance, market opportunity"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
logo_height: "44"
logo_width: "44"
logo: "https://kura.pro/pain001/images/logos/pain001.webp"
menu: "active"
measurementID: "G-167B274ZWJ"
name: "Customer Credit Transfer Initiation V4 (pain.001.001.04)"
permalink: "https://pain001.com/pain.001.001.04/index.html"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "pain001"
subtitle: "pain.001 version 4: A standardized XML message format for initiating credit transfers."
theme_color: "rgba(2, 66, 145, 0.618033988749894)"
tags: "pain.001.001.04, ISO 20022, pain001, version 4, credit transfer, XML, message format, standardization, automation, cross-border, domestic, payments"
title: "Customer Credit Transfer Initiation V4 (pain.001.001.04)"
url: "https://pain001.com/pain.001.001.04/index.html"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://pain001.com/pain.001.001.04/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Shokunin (SSG) 🦀 (version 0.0.20)"
item_description: "pain.001.001.04, is an XML-based message format under the ISO 20022 standard designed to streamline cross-border and domestic payment processes."
item_guid: "https://pain001.com/pain.001.001.04/rss.xml"
item_link: "https://pain001.com/pain.001.001.04/rss.xml"
item_pub_date: "2023-11-28T15:51+01:00"
item_title: "Customer Credit Transfer Initiation V4 (pain.001.001.04)"
last_build_date: "2023-11-28T15:51+01:00"
managing_editor: "contact@pain001.com"
pub_date: "2023-11-28T15:51+01:00"
ttl: "60"
type: "website"
webmaster: "contact@pain001.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Customer Credit Transfer Initiation V4 (pain.001.001.04)"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).
msapplication-navbutton-color: "rgb(2, 66, 145)"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "pain.001.001.04, is an XML-based message format under the ISO 20022 standard designed to streamline cross-border and domestic payment processes."
twitter_image: "https://kura.pro/pain001/images/logos/pain001.svg"
twitter_image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
twitter_site: "@wwdseb"
twitter_title: "Customer Credit Transfer Initiation V4 (pain.001.001.04)"
twitter_url: "https://pain001.com/pain.001.001.04/index.html"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2023-11-28"
site_standards: "HTML5, CSS3, RSS, Atom, CSV, JSON, XML, YAML, Markdown, TOML, SQLite"
site_components: "Kaishi, Kaishi Templates, Kaishi Themes"
site_software: "Shokunin, SSG, Rust, Cargo, Git, GitHub, Bootstrap, SQLite, VS Code"

---

## Overview

The [Customer Credit Transfer Initiation V4 (`pain.001.001.04` ⧉)][00] is an XML-based message format under the ISO 20022 standard, primarily used for initiating a movement of funds from a debtor's account to a creditor's account. This message format is a crucial component of financial transaction processing, enabling efficient fund transfers in both domestic and cross-border contexts.

## Features

The `pain.001.001.04` message format provides a number of features and benefits
that can help financial institutions and their customers, including:

- **Fund Transfer Request**: The primary function of the pain.001.001.04 message is to facilitate the transfer of funds from a debtor to a creditor.
- **Multiple Transfer Instructions**: It can contain one or more customer credit transfer instructions, making it versatile for different transaction requirements.
- **Scope of Transactions**: The message covers a range of transactions, including book transfers at the debtor agent, payments to other financial institutions, electronic cash transfers to creditor accounts, and cheque issuances.
- **Direct and Relay Scenarios**: It supports both direct scenarios (message sent directly to the debtor agent) and relay scenarios (message sent to a forwarding agent who then forwards it to the debtor agent).
- **Usage by Initiating Party**: An initiating party with the authority can use this message to send on behalf of the debtor. This is particularly useful in scenarios like a payments factory managing transactions for a large corporate.
- **Domestic and Cross-Border Applicability**: Suitable for both local and international fund transfers.
- **Restriction on Debtor Agents**: The message is not intended for debtor agents to execute credit transfer instructions; for this purpose, the FIToFICustomerCreditTransfer message is used instead.
- **Structured Format**: Composed of two key building blocks:
  - **Group Header**: A mandatory section that includes elements like MessageIdentification, CreationDateAndTime, and a Grouping indicator.
  - **Payment Information**: Another mandatory and repetitive section containing elements related to both debit (e.g., Debtor, PaymentTypeInformation) and credit (e.g., Creditor, RemittanceInformation) aspects of the transaction​​.

## Market Opportunity

The adoption of `pain.001.001.04` presents a significant market opportunity for
financial institutions. By implementing this message format, organisations can:

- **Enhance customer experience** by offering faster and more transparent
  transactions
- **Improve operational efficiency** and reduce costs associated with manual
  processing
- Position themselves as **industry leaders** in adopting global standards for
  payment processing
- Leverage the ISO 20022 standard to
  **explore new business opportunities and partnerships**
- **Ensure compliance** with evolving regulatory requirements and stay ahead of
  the competition

Find out about the
[Customer Credit Transfer Initiation V5 (pain.001.001.05)][01], and learn about
this version of the ISO 20022 Customer Credit Transfer Initiation message.

[00]: https://www.iso20022.org/catalogue-messages/iso-20022-messages-archive?search=pain.001.001.04 "ISO 20022 Customer Credit Transfer Initiation V4 (pain.001.001.04)"
[01]: /pain.001.001.05/index.html "Customer Credit Transfer Initiation V5 (pain.001.001.05)"