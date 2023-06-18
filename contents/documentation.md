---

# Front Matter (YAML)

atom_link: "https://pain001.com/documentation/rss.xml"
author: "Sebastien Rousseau"
banner: "https://kura.pro/unsplash/images/banners/arto-marttinen-K2K1Ec_51SA-unsplash.jpg"
charset: "utf-8"
copyright: "© 2023 Pain001"
description: "Pain001 is a powerful Python library that enables you to create ISO 20022-compliant payment files directly from CSV or SQLite Data Files."
icon: "https://kura.pro/pain001/images/favicon.ico"
image: "https://kura.pro/pain001/images/titles/title-pain001.webp"
keywords: "pain001, iso 20022, ISO 20022 Standard, payment messages, payments, SEPA, SWIFT, automation, banks, corporation"
language: "en-GB"
layout: "category"
name: "Pain001 documentation"
permalink: "https://pain001.com/documentation/index.html"
robots: "all"
short_name: "documentation"
subtitle: "A modern, open source solution for generating ISO 20022 compliant payments"
theme_color: "#c35600"
title: "Pain001 documentation"
url: "https://www.pain001.com/documentation/index.html"

# RSS - The RSS feed front matter (YAML).

generator: "Shokunin Static Site Generator (v0.0.13)"
item_description: "Pain001 is a powerful Python library that enables you to create ISO 20022-compliant payment files directly from CSV or SQLite Data Files."
item_guid: https://pain001.com/documentation/index.html
item_link: https://pain001.com/documentation/rss.xml
item_pub_date: "Sun, 18 June 2023 10:33:10 BST"
item_title: "Payments"
last_build_date: "Sun, 18 June 2023 10:33:10 BST"
pub_date: "Sun, 18 June 2023 10:33:10 BST"

# MS Application - The MS Application front matter (YAML).

msapplication_config: "https://pain001.com/browserconfig.xml"
msapplication_tap_highlight: "no"
msapplication_tile_color: "#7ce846"
msapplication_tile_image: https://kura.pro/pain001/images/logos/pain001.svg

# Open Graph - The Open Graph front matter (YAML).

## og - The Open Graph description of the page.
og_description: "Pain001 is a powerful Python library that enables you to create ISO 20022-compliant payment files directly from CSV or SQLite Data Files."
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
og_url: https://pain001.com

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary_large_image"
twitter_creator: "wwdseb"
twitter_description: "Pain001 is a powerful Python library that enables you to create ISO 20022-compliant payment files directly from CSV or SQLite Data Files."
twitter_image: "https://kura.pro/pain001/images/banners/banner-pain001.png"
twitter_image_alt: "Simplify payment processing with Pain001, a Python library automating ISO 20022-compliant file creation"
twitter_site: "wwdseb"
twitter_title: "Pain001: Automate ISO 20022-Compliant Payment File Creation."
twitter_url: "https://pain001.com"

---

**Version:** 0.0.20

**Useful links:** [Installation](https://pain001.com/documentation/installation.html) | [Source Repository](https://github.com/sebastienrousseau/pain001) | [Issue Tracker](https://github.com/sebastienrousseau/pain001/issues) | [PyPI](https://pypi.org/project/pain001/)

## What is Pain001?

**Pain001** is an open-source Python Library that you can use to create
**ISO 20022-Compliant Payment Files** directly from your **CSV** or **SQLite**
Data Files.

The Python library focuses specifically on
**Payment Initiation and Advice Messages**, commonly known as **Pain**. In a
very simplified way, a **pain.001** is a message that initiates the customer
payment.

As of today the library is designed to be compatible with the
**pain.001.001.03** and **pain.001.001.09** message types and will support more
message types in the future.

Payments usually start with a **pain.001 payment initiation message**. The
payer sends it to the payee (or the payee’s bank) via a secure network. This
network could be **SWIFT** or **SEPA (Single Euro Payments Area) network**, or
other payment networks such as **CHAPS**, **BACS**, **Faster Payments**, etc.
The message contains the payer’s and payee’s bank account details, payment
amount, and other information required to process the payment.

The **Pain001** library can reduce payment processing complexity and costs by
generating ISO 20022-compliant payment files. These files automatically remove
the need to create and validate them manually, making the payment process more
efficient and cost-effective. It will save you time and resources and minimises
the risk of errors, making sure accurate and seamless payment processing.

Use the **Pain001** library to simplify, accelerate and automate your payment
processing.

## System requirements

The only prerequisite for installing **Pain001** is Python itself. **Pain001**
works with macOS, Linux and Windows and requires Python 3.9.0 and above.

<div class="container px-4 py-5" id="featured-3">
    <div class="row g-4 py-5 row-cols-1 row-cols-lg-3">
      <div class="feature col">
        <h2>Get started</h2>
        <p>Set up a few basic features before you start using Pain001.</p>
        <a href="/installation/index.html" class="icon-link">
          Setup basics ❯
        </a>
      </div>
    </div>
  </div>
</div>
