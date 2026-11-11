# Development

## Prerequisites

- Rust and the latest `ssg` (0.0.75; check it against crates.io before a
  release): `cargo install ssg --locked --version 0.0.75`
- Node.js 22 or later, then `npm ci`
- Python 3.12 (CI's version; 3.10 or later works locally)
- Chrome or Chromium for the browser, accessibility and performance gates
- The linters, hash-pinned: `python3 -m pip install --require-hashes -r requirements/lint.txt`

The dev container (`.devcontainer/devcontainer.json`) installs all of
these except Chrome and boots to a working `make check`.

## Build and test

```sh
make build     # build the site into site/
make test      # build, Python and JavaScript tests with coverage, validators
make lint      # every linter CI runs
make audit     # ssg's audit gates, warnings fail
make check     # lint, complexity, test and audit: the full local gate (alias of make verify)
make deps      # npm advisories against .npm-audit-exceptions.json (network)
```

`make serve` serves the generated `site/` tree at
<http://127.0.0.1:8099/>. Generated output is ignored; edit `_posts/`,
`_layouts/`, `static/`, or `scripts/` instead.

## Tests and coverage

| Suite | Location | Runner | Coverage floor |
| --- | --- | --- | --- |
| Shipped JavaScript (`static/js/`, less the vendored beacon, and `static/sw.js`) | `tests/*.test.js`, `tests/*.test.mjs`, helpers in `tests/helpers/` | `npm run coverage` (Node's test runner, jsdom, fast-check) | 100% of lines, branches and functions |
| Browser engine against the fetched runtime | `tests/engine.integration.mjs` | `node tests/engine.integration.mjs` | not measured: an integration check |
| Build, validation and release scripts (`scripts/*.py`) | `tests/python/` | `make pytest` (pytest and pytest-cov in `.venv-test/`, from the hash-pinned `requirements/test.txt`) | 100% of lines and branches, set in `.coveragerc` |
| Events Worker | `workers/events/test/` | `npm run coverage` in `workers/events` | 100% of lines, branches and functions |

Both floors fail the build below 100%. The Python floor excludes only the
`if __name__ == "__main__":` guard, which hands control to `main()`; the
tests call `main()` directly. Tests run hermetically: every file a script
reads or writes is a `tmp_path` fixture, HTTP and `subprocess` are faked,
and the third-party modules a few scripts import at run time (Pillow,
`pain001`, `google-auth`) are stubbed, so CI installs nothing beyond
`requirements/test.txt`.

The Node scripts under `scripts/` (`*.mjs`, `*.cjs`: the Lighthouse,
layout, print, measure and axe audits and the audit server) are not under
a coverage floor. They drive a real Chrome against the built site and are
themselves the gates; CI runs every one of them on every push.

A new script in `static/js/` must be loaded by a test, or
`tests/coverage-scope.test.js` fails, because Node's coverage report only
lists files a test loaded.

## CI gates and their local commands

| CI job (`.github/workflows/ci.yml`) | Local command |
| --- | --- |
| `build-and-audit`: build, ssg audit | `make build`, `make audit` |
| `build-and-audit`: unit tests and JavaScript coverage | `npm run coverage` |
| `build-and-audit`: engine integration | `node tests/engine.integration.mjs` |
| `build-and-audit`: translation, content, headings, fonts, contrast, proof, security.txt, sitemap, JSON-LD, links, versions, no-commercial, claims, locale-index validators | `make test` |
| `build-and-audit`: documentation snippets | `pip install --require-hashes -r requirements/snippets.txt` then `python3 scripts/validate_snippets.py` |
| `build-and-audit`: layout, print, measure, Lighthouse, axe, WAVE | `node scripts/serve_audit.mjs site 8899`, then the commands in the README's Gates table |
| `repository-quality`: actionlint | `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.12` |
| `repository-quality`: markdownlint, codespell, ruff, ESLint, SPDX, README template, release notes, version consistency, REUSE | `make lint` |
| `repository-quality`: pytest with the 100% floor | `make pytest` |
| `repository-quality`: complexity ceilings against `complexity-baseline.json` | `make complexity` |
| `repository-quality`: npm advisories | `make deps` |
| `node-matrix`: unit tests on Node 22 and 24, Worker coverage | `npm test`; `cd workers/events && npm run coverage` |

## Complexity

Every Python function in `scripts/` and `tests/python/` is held to
cyclomatic 10 (radon), cognitive 15 (complexipy), Halstead difficulty 30
(radon) and 60 lines, and every file to 500 lines, by
`scripts/check_complexity.py`. Code that was over a ceiling when the gate
was added is recorded in `complexity-baseline.json` with the value it had.
The gate fails on a new offender, on a baselined one that got worse, and
on a stale entry: after improving an offender, run
`.venv-test/bin/python scripts/check_complexity.py --update` and commit the
smaller baseline with the change. Never regenerate it to absorb a
regression.

## Release model

The site ships the pain001 suite version in lockstep (`VERSION`), one
`0.0.1` step per release, on a `feat/vX.Y.Z` branch. A signed annotated
tag on the merge commit triggers `release.yml`, which rebuilds the site
and publishes the archive, CycloneDX SBOM, checksums and attestations.
`main` deploys to GitHub Pages from `ci.yml`. The full procedure is in
[docs/RELEASES.md](docs/RELEASES.md).

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

Create a `feat/vX.Y.Z` branch, use the shared pain001 suite version, sign the
commit cryptographically, and add a DCO trailer with `git commit -S -s`.
Pull requests must pass every required check before merge.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution flow and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the build pipeline.
