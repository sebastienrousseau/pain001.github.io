---

# Front Matter (YAML)

atom_link: "https://pain001.com/payments/rss.xml"
author: "Sebastien Rousseau"
banner: "https://kura.pro/unsplash/images/banners/willian-justen-de-vasconcellos-_MMP5j_fCqw-unsplash.jpg"
charset: "utf-8"
copyright: "© 2023 Pain001"
description: "Streamline your payments with Pain001, a Python library that automates the creation of ISO 20022 payment messages."
icon: "https://kura.pro/pain001/images/favicon.ico"
image: "https://kura.pro/pain001/images/titles/title-pain001.webp"
keywords: "pain001, iso 20022, ISO 20022 Standard, payment messages, payments, SEPA, SWIFT, automation, banks, corporation"
language: "en-GB"
layout: "page"
name: "Automate Payments Generation with Pain001"
permalink: "https://pain001.com/payments/index.html"
robots: "all"
short_name: "payments"
subtitle: "A modern, open source solution for generating ISO 20022 compliant payments"
theme_color: "#00838f"
title: "Automate Payments Generation with Pain001"
url: "https://www.pain001.com/payments/index.html"

# RSS - The RSS feed front matter (YAML).

generator: "Shokunin Static Site Generator (v0.0.13)"
item_description: "Streamline your payments with Pain001, a Python library that automates the creation of ISO 20022 payment messages."
item_guid: https://pain001.com/payments/index.html
item_link: https://pain001.com/payments/rss.xml
item_pub_date: "Sun, 18 June 2023 10:33:10 BST"
item_title: "Payments"
last_build_date: "Sun, 18 June 2023 10:33:10 BST"
pub_date: "Sun, 18 June 2023 10:33:10 BST"

# MS Application - The MS Application front matter (YAML).

## msapplication_tap_highlight - The MS Application tap highlight of the page.
msapplication_tap_highlight: no
## msapplication - The MS Application tile color of the page.
msapplication_tile_color: "#00838f"
## msapplication_tile_image - The MS Application tile image of the page.
msapplication_tile_image: https://kura.pro/pain001/images/logos/pain001.svg

# Open Graph - The Open Graph front matter (YAML).

## og - The Open Graph description of the page.
og_description: "Streamline your payments with Pain001, a Python library that automates the creation of ISO 20022 payment messages."
## og - The Open Graph image of the page.
og_image: https://kura.pro/pain001/images/logos/pain001.svg
## og:image:alt - The Open Graph image alt of the page.
og_image_alt: Logo
## og - The Open Graph locale of the page.
og_locale: en_GB
## og - The Open Graph site name of the page.
og_site_name: pain001.com
## og - The Open Graph title of the page.
og_title: Payments
## og - The Open Graph type of the page.
og_type: website
## og - The Open Graph url of the page.
og_url: https://www.pain001.com/

---

## Overview

**Pain001** automates the creation of ISO 20022 payment messages, mitigating
human errors and facilitating more efficient payment operations. The library
simplifies the generation of ISO20022 messages and integrates seamlessly into
your current systems, allowing for a simple adoption of ISO 20022.

The ISO 20022 Standard is a universally accepted, consensus-based standard for
financial information. It helps banks, financial markets, businesses, and
consumers by giving them a way to effectively and accurately exchange financial
data.

The library generates **Pain** messages for SEPA and SWIFT payments. These
messages initiate the process of transferring funds from one account to
another. They have important information like the payer, payee, and amount to
transfer.

## Payment Messages

The following **ISO 20022 Payment Initiation message types** are
currently supported:

- **[pain.001.001.03](/pain.001.001.03/index.html)** - Customer Credit Transfer Initiation

This message is used to transmit credit transfer instructions from the
originator (the party initiating the payment) to the originator's bank.
The message supports both bulk and single payment instructions, allowing
for the transmission of multiple payments in a batch or individual
payments separately. The pain.001.001.03 message format is part of the
ISO 20022 standard and is commonly used for SEPA Credit Transfers within
the Single Euro Payments Area. It includes relevant information such as
the originator's and beneficiary's details, payment amounts, payment
references, and other transaction-related information required for
processing the credit transfers.

- **[pain.001.001.09](/pain.001.001.09/index.html)** - Customer Credit Transfer Initiation

This message format is part of the ISO 20022 standard and is commonly
used for SEPA Credit Transfers within the Single Euro Payments Area. It
enables the transmission of credit transfer instructions from the
originator to the originator's bank. The message includes essential
information such as the originator's and beneficiary's details, payment
amounts, payment references, and other transaction-related information
required for processing the credit transfers.

**Pain001** is a powerful tool that can help businesses and
organizations to simplify and automate their payment processing by
providing a simple and easy way to create ISO 20022-compliant payment
files.

Whether your corporation has a centralised or decentralised structure,
**Pain001** will help you effectively manage your payments. We offer a wide
range of payments to meet your needs, no matter the size or complexity of your
payments needs.
