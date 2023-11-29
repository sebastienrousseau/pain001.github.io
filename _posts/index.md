---

# Front Matter (YAML)

author: "Sebastien Rousseau"
banner_alt: "Assorted-color hot air balloons during daytime"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://kura.pro/stock/images/banners/ian-dooley-DuBNA1QMpPA.webp"
cdn: "https://kura.pro"
changefreq: "weekly"
charset: "utf-8"
cname: "pain001.com"
copyright: "© 2023 Pain001. All rights reserved."
date: "Nov 28, 2023"
description: "Pain001 Is a Powerful Python Library for ISO 20022 Compliant Payment File Creation from CSV or SQLite Data Files, simplifying Payment Automation and Processing"
download: "https://pypi.org/project/pain001/"
format-detection: "telephone=no"
hreflang: "en"
icon: "https://kura.pro/pain001/images/favicon.ico"
id: "https://pain001.com/"
image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
image_height: "100vh"
image_width: "100vw"
image: "https://kura.pro/pain001/images/banners/banner-pain001.webp"
keywords: "Pain001, Python library, ISO 20022, payment files, payment processing, automate payments, ISO 20022-compliant, SWIFT, SEPA, payment initiation messages"
language: "en-GB"
layout: "index"
locale: "en_GB"
logo_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
logo_height: "33"
logo_width: "33"
logo: "https://kura.pro/pain001/images/logos/pain001.webp"
menu: "active"
measurementID: "G-167B274ZWJ"
name: "Pain001"
permalink: "https://pain001.com"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "pain001"
subtitle: "A unique toolkit to support ISO 20022 Adoption and Migration for Cross-Border Payments"
theme_color: "rgba(0, 153, 172, 0.618033988749894)"
tags: "ISO 20022, pain001, payments, automation, python, library, cross-border, compliance, efficiency, accuracy, cost reduction"
title: "Pain001: Automate ISO 20022-Compliant Payment File Creation"
url: "https://pain001.com/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://pain001.com/rss.xml"
category: "Technology"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "Shokunin (SSG) 🦀 (version 0.0.20)"
item_description: "Pain001 Is a Powerful Python Library for ISO 20022 Compliant Payment File Creation from CSV or SQLite Data Files, simplifying Payment Automation and Processing"
item_guid: https://pain001.com/rss.xml
item_link: https://pain001.com/rss.xml
item_pub_date: "2023-11-28T15:51+01:00"
item_title: "RSS"
last_build_date: "2023-11-28T15:51+01:00"
managing_editor: contact@pain001.com
pub_date: "2023-11-28T15:51+01:00"
ttl: "60"
type: "website"
webmaster: contact@pain001.com

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Pain001: Automate ISO 20022-Compliant Payment File Creation"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).
msapplication-navbutton-color: "rgb(0, 153, 172)"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "Pain001 Is a Powerful Python Library for ISO 20022 Compliant Payment File Creation from CSV or SQLite Data Files, simplifying Payment Automation and Processing"
twitter_image: "https://kura.pro/kaishi/images/logos/kaishi.svg"
twitter_image_alt: "Logo of Kaishi, a starter template for static sites"
twitter_site: "@wwdseb"
twitter_title: "Pain001: Automate ISO 20022-Compliant Payment File Creation"
twitter_url: "https://pain001.com/"

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

Today, the payment industry is experiencing a rapid evolution and transformation
as it moves towards adopting **[ISO 20022][01]** as the new norm. **ISO 20022**
is a global standard for sharing financial information across organisations.
It provides a harmonised protocol used by banks, corporations, and financial
institutions to automate and standardise payment transactions.

Here are some of the benefits of using ISO 20022:

- **Improved data quality**: ISO 20022 messages are more structured and
  detailed than traditional payment messages, reducing errors and improving
  efficiency.
- **Increased transparency**: ISO 20022 messages provide more information about
  the payment transaction, which can help to improve the visibility and
  traceability of payments.
- **Enhanced compliance**: ISO 20022 messages can help organisations follow
  AML/CFT and PSD2 regulations.

Overall, ISO 20022 is a significant improvement over traditional payment
messaging standards. It provides a more efficient, transparent, and compliant
way to process payments.

## What is Pain001

**Pain001** is a unique toolkit to support ISO 20022 Adoption and Migration for
Cross-Border Payments. The Python library takes full advantage of the ISO 20022
standard to automate the creation of on payment initiation files, commonly known
as **PAIN (PAyment INitiation)**.

Cross-Border Payments usually start with a
**pain.001 payment initiation message**. The payer sends it to the payee
(or the payee's bank) via a secure network. This network could be **SWIFT** or
**SEPA (Single Euro Payments Area)** network, or other payment networks such as
**CHAPS**, **BACS**, **Faster Payments**, etc. The message contains the payer's
and payee's bank account details, payment amount, and other information
required to process the payment.

**Pain001** can reduce payment processing complexity and costs by generating
ISO 20022-compliant payment files. These files automatically remove the need to
create and validate them manually, making the payment process more efficient
and cost-effective. It will save you time and resources and minimises the risk
of errors, making sure accurate and seamless payment processing.

If you are seeking to simplify and automate your payment processing, consider
leveraging the capabilities of **Pain001**.

## Features

- **Easy to use:** Both developers and non-developers can easily use the
  library, as it requires minimal coding knowledge.
- **Open-source**: The library is open-source and free to use, making it
  accessible to everyone.
- **Secure**: The library is secure and does not store any sensitive data,
  making sure that all information remains confidential.
- **Customizable**: The library allows developers to customise the output,
  making it adaptable to specific business requirements and preferences.
- **Scalable solution**: The **Pain001** library can handle varying volumes of
  payment files, making it suitable for businesses of different sizes and
  transaction volumes.
- **Time-saving**: The automated file creation process reduces the time spent
  on manual data entry and file generation, increasing overall productivity.
- **Seamless integration**: As a Python package, the Pain001 library is
  compatible with various Python-based applications and easily integrates into
  any existing projects or workflows.
- **Cross-border compatibility**: The library supports both Single Euro
  Payments Area (SEPA) and non-SEPA credit transfers, making it versatile for
  use in different countries and regions.
- **Improve accuracy** by providing precise data; the library reduces errors in
  payment file creation and processing.
- **Enhance efficiency** by automating the creation of Payment Initiation
  message files
- **Accelerate payment file creation** by automating the process and reducing
  the time required to create payment files.
- **Guarantee the highest quality and compliance** by validating all payment
  files to meet the ISO 20022 standards.
- **Simplify ISO 20022-compliant payment initiation message creation** by
  providing a standardised payment file format.
- **Reduce costs** by removing manual data entry and file generation, reducing
  payment processing time, and reducing errors.

Explore the impact of [ISO 20022 on the payments industry][02] and learn about
Pain001's solutions for generating **ISO 20022 payments**.

[01]: https://www.iso20022.org/ "ISO 20022, Universal financial industry message scheme"
[02]: /payments/index.html "ISO 20022 for Payments: The New Global Messaging Standard"
