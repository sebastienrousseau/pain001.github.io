.PHONY: all build test audit lint deps verify serve clean

all: verify

build:
	./build.sh

test: build
	node --test tests/*.test.mjs tests/*.test.js
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

audit: build
	ssg audit -f ssg.toml -o site --severity warn --fail-on warn

lint:
	./scripts/verify_release_version.sh
	python3 scripts/validate_readme.py
	python3 scripts/release_notes.py --check

# Separate from lint: this one talks to the npm registry.
deps:
	python3 scripts/audit_deps.py

verify: lint test audit

serve: build
	cd site && python3 -m http.server 8099 --bind 127.0.0.1

clean:
	rm -rf output Pain001 site
