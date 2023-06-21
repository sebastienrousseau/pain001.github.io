---

# Front Matter (YAML)

atom_link: "https://pain001.com/installation/rss.xml"
author: "Sebastien Rousseau"
banner: "https://kura.pro/unsplash/images/banners/joe-gardner-4xv3lqnanYc-unsplash.jpg"
charset: "utf-8"
copyright: "© 2023 Pain001"
description: "Pain001 has an easy setup process to help you get started quickly. This
guide will walk you through the steps to install Pain001 on your system."
icon: "https://kura.pro/pain001/images/favicon.ico"
image: "https://kura.pro/pain001/images/titles/title-pain001.webp"
keywords: "pain001, iso 20022, ISO 20022 Standard, payment messages, payments, SEPA, SWIFT, automation, banks, corporation"
language: "en-GB"
layout: "category"
name: "Pain001 installation"
permalink: "https://pain001.com/installation/index.html"
robots: "all"
short_name: "installation"
subtitle: "Whether you’re just getting started or want to make sure you have the basics set up, you’re in the right place."
theme_color: "#d53f00"
title: "Pain001 installation"
url: "https://www.pain001.com/installation/index.html"

# RSS - The RSS feed front matter (YAML).

generator: "Shokunin Static Site Generator (v0.0.13)"
item_description: "Pain001 has an easy setup process to help you get started quickly. This
guide will walk you through the steps to install Pain001 on your system."
item_guid: https://pain001.com/installation/index.html
item_link: https://pain001.com/installation/rss.xml
item_pub_date: "Wed, 21 June 2023 21:21:21 BST"
item_title: "Payments"
last_build_date: "Wed, 21 June 2023 21:21:21 BST"
pub_date: "Wed, 21 June 2023 21:21:21 BST"

# MS Application - The MS Application front matter (YAML).

msapplication_config: "https://pain001.com/browserconfig.xml"
msapplication_tap_highlight: "no"
msapplication_tile_color: "#d53f00"
msapplication_tile_image: https://kura.pro/pain001/images/logos/pain001.svg

# Open Graph - The Open Graph front matter (YAML).

## og - The Open Graph description of the page.
og_description: "Pain001 has an easy setup process to help you get started quickly. This
guide will walk you through the steps to install Pain001 on your system."
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

## Installation

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

## Quick Start

After installation, you can run **Pain001** directly from the command line.
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
