# Notes for distribution maintainers

Pain001.com is a static website, not a system package or executable. Debian,
RPM, Homebrew, AUR, Nix, manpage, completion, ABI, and FFI packaging therefore
do not apply.

To reproduce the deployable artefact, install Shokunin SSG 0.0.63, Node.js 22,
and Python 3.10 or later, then run `make build`. The resulting `docs/` tree is
the artefact. The build can run offline except for optional traction refresh;
if those sources are unavailable, the script retains the checked figures.

Project-authored material is dual licensed Apache-2.0 OR MIT. Vendored assets
are documented in `THIRD_PARTY_NOTICES.md` and `REUSE.toml`. Verify the source
tag against `KEYS.asc`, and compare the release archive with `SHA256SUMS`.
