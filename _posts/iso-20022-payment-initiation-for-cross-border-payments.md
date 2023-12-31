---

# Front Matter (YAML)
author: "Sebastien Rousseau"
banner_alt: "Lighted high-rise buildings during golden hour"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://kura.pro/stock/images/banners/jan-folwarczny-ZXBPMnNVtlE.webp"
cdn: "https://kura.pro"
changefreq: "weekly"
charset: "utf-8"
copyright: "© 2023 Pain001. All rights reserved."
date: "Nov 28, 2023"
description: "ISO 20022 Payment Initiation Messages are a set of XML-based messages enabling fast, efficient, transparent cross-border payments between financial institutions"
download: "https://pypi.org/project/pain001/"
format-detection: "telephone=no"
hreflang: "en"
icon: "https://kura.pro/pain001/images/favicon.ico"
id: "https://pain001.com/iso-20022-payment-initiation-for-cross-border-payments/index.html"
image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
image_height: "100vh"
image_width: "100vw"
image: "https://kura.pro/pain001/images/banners/banner-pain001.webp"
keywords: "pain.001.001.03, pain.001.001.04, pain.001.001.05, pain.001.001.09, ISO 20022 message format, SEPA Credit Transfers, international credit transfers, Customer Credit Transfer Initiation, Python library, payment processing automation"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
logo_height: "50vh"
logo_width: "50vw"
logo: "https://kura.pro/pain001/images/logos/pain001.webp"
menu: "active"
measurementID: "G-167B274ZWJ"
name: "ISO 20022 Payment Initiation for Cross-Border Payments"
permalink: "https://pain001.com/iso-20022-payment-initiation-for-cross-border-payments/index.html"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "pain001"
subtitle: "Pain001: Delivering Faster Payments Automation"
theme_color: "rgba(170, 70, 115, 0.618033988749894)"
tags: "ISO 20022, Pain001, cross-border payments, payment initiation, XML, messages, financial institutions, efficiency, security, automation, compliance"
title: "ISO 20022 Payment Initiation for Cross-Border Payments"
url: "https://pain001.com/iso-20022-payment-initiation-for-cross-border-payments/index.html"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://pain001.com/iso-20022-payment-initiation-for-cross-border-payments/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Shokunin (SSG) 🦀 (version 0.0.20)"
item_description: "ISO 20022 Payment Initiation Messages are a set of XML-based messages enabling fast, efficient, transparent cross-border payments between financial institutions"
item_guid: "https://pain001.com/iso-20022-payment-initiation-for-cross-border-payments/rss.xml"
item_link: "https://pain001.com/iso-20022-payment-initiation-for-cross-border-payments/rss.xml"
item_pub_date: "2023-11-28T15:51+01:00"
item_title: "ISO 20022 Payment Initiation for Cross-Border Payments"
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
apple-mobile-web-app-title: "ISO 20022 Payment Initiation for Cross-Border Payments"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).
msapplication-navbutton-color: "rgb(170, 70, 115)"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "ISO 20022 Payment Initiation Messages are a set of XML-based messages enabling fast, efficient, transparent cross-border payments between financial institutions"
twitter_image: "https://kura.pro/pain001/images/logos/pain001.svg"
twitter_image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
twitter_site: "@wwdseb"
twitter_title: "ISO 20022 Payment Initiation for Cross-Border Payments"
twitter_url: "https://pain001.com"

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

Banks, corporations, and financial institutions around the globe are adopting
ISO 20022 for high-value payments systems and cross-border payments, leveraging
its power to automate and standardise payment transactions.

The **Pain001** Python Finance Library generates fully compliant and valid
**ISO 20022 Payment messages** that can integrate seamlessly into your payment
system, reducing payments creation and processing costs and improving
efficiency.

**ISO 20022**, the brainchild of the
[International Organization for Standardization (ISO)][0], serves as the unified
platform for crafting financial messages and defines the ISO standard for
electronic data interchange between financial institutions.

## What are ISO 20022 payment initiation messages?

**ISO 20022 payment initiation messages** are a set of XML-based messages that
are used to enable payments between financial institutions. These messages are
designed to be more efficient and secure than traditional payment messages.
They also provide more detailed information about the payment.

There are two main types of ISO 20022 Payment Initiation messages:

- **CustomerCreditTransferInitiation messages** initiate credit transfers.
- **CustomerDirectDebitInitiation messages** initiate direct debits.

Both message contain information about the payer, the payee, the amount of the
payment, and the date and time of the payment. They also contain additional
information, such as the purpose of the payment and the reference number.

A wide range of financial institutions, including banks, payment service
providers, and clearing-houses, use **ISO 20022 payment initiation messages**.

## Payments Initiation list of supported messages

The table shows the supported Payments Initiation messages in **Pain001**, and
their original release dates of the messages. The **Pain001** library supports
the following versions of the ISO 20022 Customer Credit Transfer Initiation
messages:

| Version | Release Date | Description |
|---------|--------------|-------------|
| [pain.001.001.03][3] | 2009 | Customer Credit Transfer Initiation V3, the most popular version |
| [pain.001.001.04][4] | 2012 | Customer Credit Transfer Initiation V4 |
| [pain.001.001.05][5] | 2013 | Customer Credit Transfer Initiation V5 |
| [pain.001.001.06][6] | 2015 | Customer Credit Transfer Initiation V6 |
| [pain.001.001.07][7] | 2016 | Customer Credit Transfer Initiation V7 |
| [pain.001.001.08][8] | 2018 | Customer Credit Transfer Initiation V8 |
| [pain.001.001.09][9] | 2019 | Customer Credit Transfer Initiation V9 |

All of these are part of the ISO 20022 standard. V3 is common for SEPA Credit
Transfers, and V4 for international credit transfers outside the Single Euro
Payments Area (SEPA).

All versions carry the originator’s and beneficiary’s details, references, and
other relevant information for credit transfer processing. V9, as a newer
iteration, adds extras such as the currency and the SWIFT codes of the involved
banks, and allows for more payments in a single message.

These messages transmit credit transfer instructions from the originator to
their bank, supporting both bulk and single payment instructions. This
capability enables transmission of multiple payments in a batch or individual
payments separately.

## Benefits

**Pain001** offers many benefits, including:

- **Accuracy**: Pain001 helps to mitigate human errors by automating the creation of ISO 20022 payment messages.
- **Compliance**: Pain001 helps you comply with the latest regulatory requirements for payment processing.
- **Efficiency**: Pain001 can reduce payment processing time and costs by creating ISO 20022 payment messages quickly.
- **Flexibility**: Pain001 can be used to create ISO 20022 payment messages for a wide range of payment types, including SEPA Credit Transfers and international credit transfers.
- **Security**: Pain001 helps you protect your customers' data by creating ISO 20022 payment messages that are compliant with the latest security standards.
- **Simplicity**: Pain001 is a simple and easy-to-use library that can be quickly and easily integrated into your existing payment processing systems.

## Resources

- **Documentation**

  The [Pain001 Documentation](/documentation/index.html) contains all necessary
  information for developers and other stakeholders to prepare and use the
  **Pain001** library. It is intended to help organisations prepare for the
  transition to ISO 20022, by delivering **faster payments automation** and
  **simplifying payment processing**.

- **Source Code**

  Browse through the source code of the **Pain001** library directly from our
  [GitHub repository][1]. The source code is available under the dual licenses
  [Apache License 2.0](https://opensource.org/licenses/Apache-2.0) and the
  [MIT License](https://opensource.org/licenses/MIT).

- **Intellectual Property Rights**

  **Pain001** provides message definitions and XML schemas for demonstration
  purposes only. The message definitions and XML schemas are copyrighted by the
  ISO 20022 organisation and under its ISO 2002 Intellectual Property Rights
  Policy available at
  [https://www.iso20022.org/intellectual-property-rights][2].

## Conclusion

**Pain001** is a powerful tool that can help businesses and organisations to
simplify and automate their payment processing. It makes paying easier by
creating ISO 20022-compliant payment files from Excel, CSV, and SQLite files.
If you are looking for a way to improve the efficiency and accuracy of your
payment processing operations, **Pain001** is a great option.

Find out about the
[Customer Credit Transfer Initiation V3 (pain.001.001.03)][3], and learn about
this version of the ISO 20022 Customer Credit Transfer Initiation message.


[0]: https://www.iso20022.org/ "ISO 20022"
[1]: https://github.com/sebastienrousseau/pain001
[2]: https://www.iso20022.org/intellectual-property-rights
[3]: /pain.001.001.03/index.html "Find out about the Customer Credit Transfer Initiation V3 (pain.001.001.03)"
[4]: /pain.001.001.04/index.html "Find out about the Customer Credit Transfer Initiation V4 (pain.001.001.04)"
[5]: /pain.001.001.05/index.html "Find out about the Customer Credit Transfer Initiation V5 (pain.001.001.05)"
[6]: /pain.001.001.06/index.html "Find out about the Customer Credit Transfer Initiation V6 (pain.001.001.06)"
[7]: /pain.001.001.07/index.html "Find out about the Customer Credit Transfer Initiation V7 (pain.001.001.07)"
[8]: /pain.001.001.08/index.html "Find out about the Customer Credit Transfer Initiation V8 (pain.001.001.08)"
[9]: /pain.001.001.09/index.html "Find out about the Customer Credit Transfer Initiation V9 (pain.001.001.09)"
