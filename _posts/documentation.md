---

# Front Matter (YAML)
author: "Sebastien Rousseau"
banner_alt: "Photo of mountains and sky"
banner_height: "398"
banner_width: "1440"
banner: "https://kura.pro/stock/images/banners/arto-marttinen-K2K1Ec_51SA.webp"
cdn: "https://kura.pro"
changefreq: "weekly"
charset: "utf-8"
copyright: "© 2023 Pain001. All rights reserved."
date: "Nov 05, 2023"
description: "Access information about the Pain001 library, including release notes, installation and configuration instructions, and more."
download: ""
format-detection: "telephone=no"
hreflang: "en"
icon: "https://kura.pro/pain001/images/favicon.ico"
id: "https://pain001.com/documentation/index.html"
image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
image_height: "100vh"
image_width: "100vw"
image: "https://kura.pro/pain001/images/banners/banner-pain001.webp"
keywords: "documentation, pain001, python, library, payments, ISO 20022, release notes, installation, configuration, CSV, SQLite"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
logo_height: "25"
logo_width: "100"
logo: "https://kura.pro/pain001/images/titles/title-pain001.webp"
menu: "active"
name: "pain001"
permalink: "https://pain001.com/documentation/index.html"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "pain001"
subtitle: "A modern, open source solution for generating ISO 20022 compliant payments"
theme-color: "rgba(84,41,22, 0.618033988749894)"
tags: "documentation, pain001, python, library, payments, ISO 20022, release notes, installation, configuration, CSV, SQLite"
title: "Product Documentation for Pain001"
type_: "website"
url: "https://pain001.com/documentation/index.html"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://pain001.com/documentation/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Shokunin (SSG) 🦀 (version 0.0.20)"
item_description: "Access information about the Pain001 library, including release notes, installation and configuration instructions, and more."
item_guid: "https://pain001.com/documentation/rss.xml"
item_link: "https://pain001.com/documentation/rss.xml"
item_pub_date: "Nov 05, 2023"
item_title: "Product Documentation for Pain001"
last_build_date: "Wednesday, 27 Sep 2023 27:27:27 GMT"
managing_editor: "contact@pain001.com"
pub_date: "Nov 05, 2023"
ttl: "60"
type: "website"
webmaster: "contact@pain001.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Product Documentation for Pain001"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).
msapplication-navbutton-color: "rgb(84,41,22)"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "Access information about the Pain001 library, including release notes, installation and configuration instructions, and more."
twitter_image: "https://kura.pro/pain001/images/logos/pain001.svg"
twitter_image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
twitter_site: "@wwdseb"
twitter_title: "Product Documentation for Pain001"
twitter_url: "https://pain001.com"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.co.uk"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2023-09-20"
site_standards: "HTML5, CSS3, RSS, Atom, CSV, JSON, XML, YAML, Markdown, TOML, SQLite"
site_components: "Kaishi, Kaishi Templates, Kaishi Themes"
site_software: "Shokunin, SSG, Rust, Cargo, Git, GitHub, Bootstrap, SQLite, VS Code"

---

**Version:** 0.0.23

**Useful links:** [Installation](/installation/index.html) | [Source Repository](https://github.com/sebastienrousseau/pain001) | [Issue Tracker](https://github.com/sebastienrousseau/pain001/issues) | [PyPI](https://pypi.org/project/pain001/)

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

<div class="container px-4 py-5 bg-dark" id="featured-3">
    <div class="row g-4 row-cols-1 row-cols-lg-3">
      <div class="feature col text-white">
        <h2 class="text-white">Get started</h2>
        <p>Set up a few basic features before you start using Pain001.</p>
        <a href="/installation/index.html" class="icon-link text-white">
          Setup basics ❯
        </a>
      </div>
    </div>
  </div>
</div>