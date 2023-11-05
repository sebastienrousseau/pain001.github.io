<!-- markdownlint-disable MD033 MD041 -->

<img
  align="right"
  alt="Logo of Pain001"
  height="261"
  src="https://kura.pro/pain001/images/logos/pain001.webp"
  width="261"
  />

<!-- markdownlint-enable MD033 MD041 -->

# pain001.com - Official Website 🌏

A unique toolkit to support ISO 20022 Adoption and Migration for Cross-Border Payments.

## Quick Start Guide

Setting up and running the website locally is easy and quick with the
[Shokunin Static Site Generator (SSG)][00].

### Prerequisites

Ensure you have the **Rust toolchain** installed. If not, follow the guide on
the [Rust website][01] to set it up.

### Installation & Usage

1. Install Shokunin SSG:

```shell
cargo install ssg
```

2. Clone the repository

```shell
git clone https://github.com/sebastienrousseau/pain001.github.io.git
```

3. Change into the repository directory:

```shell
cd pain001.github.io
```

1. Generate the static site:

```shell
ssg -n=docs -c=_posts -t=_layouts -o=output -s=public
```

[00]: https://shokunin.one "Shokunin Static Site Generator (SSG)"
[01]: https://www.rust-lang.org/learn/get-started "Rust Getting started guide"
