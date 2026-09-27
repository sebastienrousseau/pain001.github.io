# Development

## Prerequisites

- Rust and `ssg` 0.0.63: `cargo install ssg --locked --version 0.0.63`
- Node.js 22 or later
- Python 3.10 or later
- Chrome or Chromium for browser, accessibility, and performance gates
- The linters, hash-pinned: `python3 -m pip install --require-hashes -r requirements/lint.txt`

## Build and test

```sh
make build
make test
make audit
npm run coverage
```

`npm run coverage` runs the unit, property and jsdom tests with the
coverage gate CI applies to the shipped JavaScript in `static/js/` and
the demo's service worker, `static/sw.js`: 90% of lines and 80% of
branches.

`make test` also runs the Python regression tests (`make pytest`) in a
local `.venv-test/` virtualenv, built on first use from the hash-pinned
`requirements/test.txt`.

`make serve` serves the generated `site/` tree at
<http://127.0.0.1:8099/>. Generated output is ignored; edit `_posts/`,
`_layouts/`, `static/`, or `scripts/` instead.

## Coding standards

Each language has a named standard, and CI enforces every one of them on
each push and pull request.

| Language | Standard | Enforced by |
| --- | --- | --- |
| Python | PEP 8 as checked by ruff's pycodestyle, Pyflakes and bugbear rules; line length is not enforced (see `ruff.toml`) | `ruff check scripts tests` |
| JavaScript | ESLint's recommended rules for browser and Node code (see `eslint.config.mjs`) | `npm run lint` |
| Markdown | markdownlint's default rules as configured in `.markdownlint-cli2.jsonc` | `markdownlint-cli2` |
| GitHub Actions | actionlint | `rhysd/actionlint` |
| Spelling | codespell | `codespell` |
| Licensing | REUSE 3.3, with an SPDX header in every source file | `reuse lint` and `scripts/validate_spdx_headers.py` |

Run them locally with `make lint`.

## Commit policy

Create a `feat/vX.Y.Z` branch, increment only the patch component, sign the
commit cryptographically, and add a DCO trailer with `git commit -S -s`.
Pull requests must pass every required check before merge.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution flow and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the build pipeline.
