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

## Search engine notification (IndexNow)

After every deploy of `main`, CI's `indexnow` job runs
`scripts/indexnow.py`, which submits every URL in the live sitemap to
[IndexNow](https://www.indexnow.org/). Bing, Yandex, Seznam, Naver and the
other participating engines then recrawl within hours. No account or
secret is needed: ownership is proven by the key file
`static/06f658eb7c2b6f1a8e600692727ce56a.txt`, served at `https://pain001.com/06f658eb7c2b6f1a8e600692727ce56a.txt`. Keep that
file; renaming it means publishing a new key. The script never fails the
pipeline. Try it locally with
`python3 scripts/indexnow.py --sitemap site/sitemap.xml --dry-run`.

## Search Console scoreboard

`.github/workflows/seo-scoreboard.yml` runs `scripts/seo_scoreboard.py`
every Monday and on demand. It compares the last 28 days of Search Console
data with the 28 days before, for the whole site, the tracked queries
(`pain.001`, `pain001`, `001.001`, the version and XSD queries, `pain.002`
and others), and the top pages and countries, and writes the result to the
run's summary.

It authenticates without a stored key. Workload Identity Federation
exchanges the job's GitHub OIDC token for a one-hour token of the service
account `pain001-seo-scoreboard@teamrousseau.iam.gserviceaccount.com`, which
is a **Restricted** (read-only) user on the `pain001.com` Search Console
property and has no Google Cloud roles. There is no secret to rotate. On a
fork the authentication step is skipped and the run reports "not
configured".

The Google Cloud side, in project `teamrousseau`, for reference or rebuild:

1. Enable the **Google Search Console API** and the **IAM Service Account
   Credentials API**.
2. Create the workload identity pool `github` with the OIDC provider
   `pain001-github-io`: issuer `https://token.actions.githubusercontent.com`,
   default audience, mappings `google.subject=assertion.sub` and
   `attribute.repository_id=assertion.repository_id`, and the condition
   `assertion.repository_id == '654513234' &&
   assertion.job_workflow_ref.startsWith('sebastienrousseau/pain001.github.io/.github/workflows/seo-scoreboard.yml@')`.
3. On the service account, grant **Workload Identity User** to
   `principalSet://iam.googleapis.com/projects/116272232197/locations/global/workloadIdentityPools/github/attribute.repository_id/654513234`.
   Create no keys.

To run it locally, install `requirements/seo.txt` with `--require-hashes`
and point `GOOGLE_APPLICATION_CREDENTIALS` at Application Default
Credentials that can read the property, for example from
`gcloud auth application-default login
--impersonate-service-account=pain001-seo-scoreboard@teamrousseau.iam.gserviceaccount.com`.

## Commit policy

Create a `feat/vX.Y.Z` branch, increment only the patch component, sign the
commit cryptographically, and add a DCO trailer with `git commit -S -s`.
Pull requests must pass every required check before merge.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution flow and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the build pipeline.
