.PHONY: all build test pytest audit lint deps verify serve clean

all: verify

build:
	./build.sh

test: build pytest
	npm test
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
	python3 scripts/validate_links.py site
	python3 scripts/validate_versions.py

# Regression tests for the build and release scripts. They run in their own
# virtualenv, built once from the hash-pinned requirements/test.txt.
.venv-test/.installed: requirements/test.txt
	python3 -m venv .venv-test
	.venv-test/bin/python -m pip install --quiet --require-hashes -r requirements/test.txt
	touch $@

pytest: .venv-test/.installed
	.venv-test/bin/python -m pytest tests/python -q -p no:cacheprovider

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

# Separate from lint: this one talks to the npm registry.
deps:
	python3 scripts/audit_deps.py

verify: lint test audit

serve: build
	cd site && python3 -m http.server 8099 --bind 127.0.0.1

clean:
	rm -rf output Pain001 site
