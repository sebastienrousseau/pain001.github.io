---

# Front Matter (YAML)
author: "Sebastien Rousseau"
banner_alt: "Antelope Canyon"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://kura.pro/stock/images/banners/joe-gardner-4xv3lqnanYc.webp"
cdn: "https://kura.pro"
changefreq: "weekly"
charset: "utf-8"
copyright: "© 2023 Pain001. All rights reserved."
date: "Nov 28, 2023"
description: "Pain001 is a powerful Python library that enables you to create ISO 20022-compliant payment files directly from CSV or SQLite Data Files."
download: ""
format-detection: "telephone=no"
hreflang: "en"
icon: "https://kura.pro/pain001/images/favicon.ico"
id: "https://pain001.com/installation/index.html"
image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
image_height: "100vh"
image_width: "100vw"
image: "https://kura.pro/pain001/images/banners/banner-pain001.webp"
keywords: "pain001, iso 20022, ISO 20022 Standard, payment messages, payments, SEPA, SWIFT, automation, banks, corporation"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
logo_height: "33"
logo_width: "33"
logo: "https://kura.pro/pain001/images/logos/pain001.webp"
menu: "active"
measurementID: "G-167B274ZWJ"
name: "pain001"
permalink: "https://pain001.com/installation/index.html"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "pain001"
subtitle: "Whether you’re just getting started or want to make sure you have the basics set up, you’re in the right place."
theme_color: "rgba(213,63,0, 0.618033988749894)"
tags: "installation, Python, ISO 20022, pain001, payments, CSV, SQLite, XML, XSD, template, command-line"
title: "Pain001 installation"
url: "https://pain001.com/installation/index.html"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://pain001.com/installation/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Shokunin (SSG) 🦀 (version 0.0.20)"
item_description: "Pain001 is a powerful Python library that enables you to create ISO 20022-compliant payment files directly from CSV or SQLite Data Files."
item_guid: "https://pain001.com/installation/rss.xml"
item_link: "https://pain001.com/installation/rss.xml"
item_pub_date: "2023-11-28T15:51+01:00"
item_title: "Pain001 installation"
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
apple-mobile-web-app-title: "Pain001 installation"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).
msapplication-navbutton-color: "rgb(213,63,0)"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "Pain001 is a powerful Python library that enables you to create ISO 20022-compliant payment files directly from CSV or SQLite Data Files."
twitter_image: "https://kura.pro/pain001/images/logos/pain001.svg"
twitter_image_alt: "Logo of Pain001: Automate ISO 20022-Compliant Payment File Creation"
twitter_site: "@wwdseb"
twitter_title: "Pain001 installation"
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

## Get started

It takes just a few seconds to get up and running with **Pain001**. If you use
pip, open your terminal and run the following command:

```sh
pip install pain001
```

Add the -U switch to update to the current version, if `pain001` is already
installed. For example:

```sh
pip install -U pain001
```

If you do not have pip installed, you can download and install it from this
page: <https://pypi.org/project/pip/>. Alternatively, you can use
[Anaconda](https://www.anaconda.com/products/individual) to install pip.

## How do I use Pain001?

It’s easy to use **Pain001** to generate a payment initiation message from a
CSV or SQLite Data file. After installation, you can run **Pain001** directly
from the command line.

Simply call the main module pain001 with the paths of your:

- **XML template file** containing the various parameters you want to pass from
  your Data file,
- **XSD schema file** to validate the generated XML file, and
- **Data file (CSV or SQLite)** containing the payment instructions that you
  want to submit.

Here’s how you would do that:

```sh
python3 -m pain001 \
    <xml_message_type> \
    <xml_template_file_path> \
    <xsd_schema_file_path> \
    <data_file_path>
```

### Arguments

When running **Pain001**, you will need to specify four arguments:

- An `xml_message_type`: This is the type of XML message you want to generate.

  The currently supported types are:
  - pain.001.001.03
  - pain.001.001.04
  - pain.001.001.09
- An `xml_template_file_path`: This is the path to the XML template file you
  are using that contains variables that will be replaced by the values in your
  Data file.
- An `xsd_schema_file_path`: This is the path to the XSD schema file you are
  using to validate the generated XML file.
- A `data_file_path`: This is the path to the CSV or SQLite Data file you want
  to convert to XML format.

## Examples

The following examples demonstrate how to use **Pain001** to generate a payment
initiation message from a CSV file and a SQLite Data file.

### Using a CSV Data File as the source

```sh
python3 -m pain001 \
    pain.001.001.03 \
    /path/to/your/template.xml \
    /path/to/your/pain.001.001.03.xsd \
    /path/to/your/template.csv
```

### Using a SQLite Data File as the source

```sh
python3 -m pain001 \
    pain.001.001.03 \
    /path/to/your/template.xml \
    /path/to/your/pain.001.001.03.xsd \
    /path/to/your/template.db
```

### Using the Source code

You can clone the source code and run the example code in your
terminal/command-line. To check out the source code, clone the repository from
GitHub:

```sh
git clone https://github.com/sebastienrousseau/pain001.git
```

  Then, navigate to the `pain001` directory and run the following command:

  ```sh
  python3 -m pain001 \
      pain.001.001.03 \
      templates/pain.001.001.03/template.xml \
      templates/pain.001.001.03/pain.001.001.03.xsd \
      templates/pain.001.001.03/template.csv
  ```

This will generate a payment initiation message from the sample CSV Data file.

You can do the same with the sample SQLite Data file:

```sh
python3 -m pain001 \
    pain.001.001.03 \
    templates/pain.001.001.03/template.xml \
    templates/pain.001.001.03/pain.001.001.03.xsd \
    templates/pain.001.001.03/template.db
```

> **Note:** The XML file that **Pain001** generates will automatically be
validated against the XSD template file before the new XML file is saved. If
the validation fails, **Pain001** will stop running and display an error
message in your terminal.

### Embedded in an Application

To embed **Pain001** in a new or existing application, import the main function
and use it in your code.

Here's an example:

```python
from pain001 import main

if __name__ == '__main__':
  xml_message_type = 'pain.001.001.03'
  xml_template_file_path = 'template.xml'
  xsd_schema_file_path = 'schema.xsd'
  data_file_path = 'data.csv'
  main(
    xml_message_type,
    xml_template_file_path,
    xsd_schema_file_path,
    data_file_path
  )
```

### Validation

To validate the generated XML file against a given xsd schema, use the
following method:

```python
from pain001.core import validate_xml_against_xsd

xml_message_type = 'pain.001.001.03'
xml_file = 'generated.xml'
xsd_file = 'schema.xsd'

is_valid = validate_xml_against_xsd(
  xml_message_type,
  xml_file,
  xsd_file
)
print(f"XML validation result: {is_valid}")
```