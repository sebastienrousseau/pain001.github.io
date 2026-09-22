# Development

## Prerequisites

- Rust and `ssg` 0.0.63: `cargo install ssg --locked --version 0.0.63`
- Node.js 22 or later
- Python 3.10 or later
- Chrome or Chromium for browser, accessibility, and performance gates

## Build and test

```sh
make build
make test
make audit
```

`make serve` serves the generated `site/` tree at
<http://127.0.0.1:8099/>. Generated output is ignored; edit `_posts/`,
`_layouts/`, `static/`, or `scripts/` instead.

## Commit policy

Create a `feat/vX.Y.Z` branch, increment only the patch component, sign the
commit cryptographically, and add a DCO trailer with `git commit -S -s`.
Pull requests must pass every required check before merge.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution flow and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the build pipeline.
