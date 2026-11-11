# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
.PHONY: all build test pytest complexity audit lint deps verify check serve clean

all: verify

build:
	./build.sh

test: build pytest
	npm run coverage
	python3 scripts/css_minify.py
	python3 scripts/validate_try_i18n.py
	python3 scripts/validate_pages_i18n.py pages_i18n
	python3 scripts/validate_pages_i18n.py docs_i18n
	python3 scripts/validate_runtime_i18n.py
	python3 scripts/validate_i18n_keys_live.py
	python3 scripts/validate_content_integrity.py
	python3 scripts/validate_headings.py
	python3 scripts/validate_fonts.py
	python3 scripts/validate_css_content.py
	python3 scripts/validate_contrast.py
	python3 scripts/validate_proof.py
	python3 scripts/validate_security_txt.py
	python3 scripts/validate_sitemap.py
	python3 scripts/validate_jsonld.py
	python3 scripts/validate_links.py site
	python3 scripts/validate_versions.py
	python3 scripts/validate_no_commercial.py
	python3 scripts/validate_claims.py
	python3 scripts/validate_locale_index.py

# Regression tests for the build and release scripts. They run in their own
# virtualenv, built once from the hash-pinned requirements/test.txt.
.venv-test/.installed: requirements/test.txt
	python3 -m venv .venv-test
	.venv-test/bin/python -m pip install --quiet --require-hashes -r requirements/test.txt
	touch $@

# Fails below 100% line and branch coverage of scripts/ (see .coveragerc).
pytest: .venv-test/.installed
	.venv-test/bin/python -m pytest tests/python -q -p no:cacheprovider --cov=scripts --cov-report=term

audit: build
	ssg audit -f ssg.toml -o site --severity warn --fail-on warn

lint:
	./scripts/verify_release_version.sh
	python3 scripts/validate_readme.py
	python3 scripts/release_notes.py --check
	ruff check scripts tests
	npm run lint
	npx --no-install markdownlint-cli2
	codespell
	reuse lint
	python3 scripts/validate_spdx_headers.py

# Separate from lint: this one talks to the npm registry.
deps:
	python3 scripts/audit_deps.py

# Per-function ceilings (cyclomatic 10, cognitive 15, Halstead 30, 60
# lines; 500 lines per file) against complexity-baseline.json, which may
# only shrink. See scripts/check_complexity.py.
complexity: .venv-test/.installed
	.venv-test/bin/python scripts/check_complexity.py

verify: lint complexity test audit

# The workspace name for the full local gate.
check: verify

serve: build
	cd site && python3 -m http.server 8099 --bind 127.0.0.1

clean:
	rm -rf output Pain001 site
