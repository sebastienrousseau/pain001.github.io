---

# Front Matter (YAML)

atom_link: "https://pain001.com/payments/rss.xml"
author: "Sebastien Rousseau"
banner: "https://kura.pro/unsplash/images/banners/marek-piwnicki-DgdJ_0us5SE-unsplash.jpg"
charset: "utf-8"
copyright: "© 2023 Pain001"
description: "Pain001 is a Python library that automates the creation of ISO 20022 payment messages. It simplifies payment processing by creating ISO 20022-compliant payment files, thus delivering faster payments automation."
icon: "https://kura.pro/pain001/images/favicon.ico"
image: "https://kura.pro/pain001/images/titles/title-pain001.webp"
keywords: "pain.001.001.03, pain.001.001.04, pain.001.001.09, ISO 20022 message format, SEPA Credit Transfers, international credit transfers, Customer Credit Transfer Initiation, Python library, payment processing automation"
language: "en-GB"
layout: "page"
name: "ISO 20022 Payments"
permalink: "https://pain001.com/payments/index.html"
robots: "all"
short_name: "payments"
subtitle: "Delivering faster payments automation"
theme_color: "142, 65, 74"
title: "ISO 20022 Payments"
url: "https://www.pain001.com/payments/index.html"

# RSS - The RSS feed front matter (YAML).

atom_link: "https://pain001.com/payments/rss.xml"
generator: "Shokunin Static Site Generator (v0.0.13)"
item_description: "Pain001 is a Python library that automates the creation of ISO 20022 payment messages. It simplifies payment processing by creating ISO 20022-compliant payment files, thus delivering faster payments automation."
item_guid: "https://pain001.com/payments/index.html"
item_link: "https://pain001.com/payments/rss.xml"
item_pub_date: "Thu, 22 June 2023 09:09:09 BST"
item_title: "ISO 20022 Payments"
last_build_date: "Thu, 22 June 2023 09:09:09 BST"
pub_date: "Thu, 22 June 2023 09:09:09 BST"

# MS Application - The MS Application front matter (YAML).

msapplication_config: "https://pain001.com/browserconfig.xml"
msapplication_tap_highlight: "no"
msapplication_tile_color: "142, 65, 74"
msapplication_tile_image: "https://kura.pro/pain001/images/logos/pain001.svg"

# Open Graph - The Open Graph front matter (YAML).

og_description: "Pain001 is a Python library that automates the creation of ISO 20022 payment messages. It simplifies payment processing by creating ISO 20022-compliant payment files, thus delivering faster payments automation."
og_image_alt: "ISO 20022 Payments"
og_image: "https://kura.pro/pain001/images/logos/pain001.svg"
og_locale: "en_GB"
og_site_name: "Pain001"
og_title: "ISO 20022 Payments"
og_type: "website"
og_url: "https://www.pain001.com/payments/index.html"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary_large_image"
twitter_creator: "wwdseb"
twitter_description: "Pain001 is a Python library that automates the creation of ISO 20022 payment messages. It simplifies payment processing by creating ISO 20022-compliant payment files, thus delivering faster payments automation."
twitter_image: "https://kura.pro/pain001/images/banners/banner-pain001.png"
twitter_image_alt: "Simplify payment processing with Pain001, a Python library automating ISO 20022-compliant file creation"
twitter_site: "wwdseb"
twitter_title: "ISO 20022 Payments"
twitter_url: "https://www.pain001.com/payments/index.html"
---

## Overview

This Python Finance Library generates **ISO 20022-compliant payments messages**
and can integrate seamlessly into your systems, reducing payments creation and
processing costs.

## What is ISO 20022?

The **ISO 20022 Standard** is a universally accepted, consensus-based standard
for financial information. It helps banks, financial markets, businesses, and
consumers by giving them a way to effectively and accurately exchange financial
data.

<!-- markdownlint-disable MD033 MD041 -->

<div class="row g-0">
  <div class="col-lg-6 order-lg-1 text-white" style="
  background: url(
  'https://kura.pro/unsplash/images/banners/ash-YfgE8WCcZsQ-unsplash.jpg')
  no-repeat;
  background-size: cover;
  background-position: center;
  "></div>
  <div class="col-lg-6 order-lg-1 text-left">
    <div class="container-fluid px-5 py-5">

<!-- markdownlint-enable MD033 MD041 -->

## Payment Messages

The **ISO 20022 Payment Initiation messages** are a set of XML-based messages
that are used to enable payments between financial institutions. These messages
are designed to be more efficient and secure than traditional payment messages.
They also provide more detailed information about the payment.

There are two main types of ISO 20022 Payment Initiation messages:

- **CustomerCreditTransferInitiation messages** initiate credit transfers.
- **CustomerDirectDebitInitiation messages** initiate direct debits.

Both message contain information about the payer, the payee, the amount of the
payment, and the date and time of the payment. They also contain additional
information, such as the purpose of the payment and the reference number.

A wide range of financial institutions, including banks, payment service
providers, and clearinghouses, use **ISO 20022 payment initiation messages**.

**Pain001** supports the following ISO 20022 Payment Initiation message types:

- **[Customer Credit Transfer Initiation V3 (pain.001.001.03) ❯][3]**
- **[Customer Credit Transfer Initiation V4 (pain.001.001.04) ❯][4]**
- **[Customer Credit Transfer Initiation V9 (pain.001.001.09) ❯][9]**

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

**Pain001** offers many benefits, such as:

- **Simplicity**: Pain001 is a simple and easy-to-use library that can be
  quickly and easily integrated into your existing payment processing systems.
- **Accuracy**: Pain001 helps to mitigate human errors by automating the
  creation of ISO 20022 payment messages.
- **Efficiency**: Pain001 can reduce payment processing time and costs by
  creating ISO 20022 payment messages quickly.
- **Compliance**: Pain001 helps you comply with the latest regulatory
  requirements for payment processing.

**Pain001** automates the creation of **ISO 20022 payment messages**,
mitigating human errors and facilitating more efficient payment operations.

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

<!-- markdownlint-disable MD033 MD041 -->

  </div>
  </div>
</div>

<!-- markdownlint-enable MD033 MD041 -->

[1]: https://github.com/sebastienrousseau/pain001
[2]: https://www.iso20022.org/intellectual-property-rights
[3]: /pain.001.001.03/index.html "Find out about the Customer Credit Transfer Initiation V3 (pain.001.001.03)"
[4]: /pain.001.001.04/index.html "Find out about the Customer Credit Transfer Initiation V4 (pain.001.001.04)"
[9]: /pain.001.001.09/index.html "Find out about the Customer Credit Transfer Initiation V9 (pain.001.001.09)"
