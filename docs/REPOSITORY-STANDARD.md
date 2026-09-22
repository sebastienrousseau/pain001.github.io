# Repository standard conformance

This matrix records the applicability of `/Users/seb/Code/REPO-STANDARD.md` to
this static website at v0.0.3.

| Area | Status | Evidence |
| --- | --- | --- |
| Identity and README | Conformant | README purpose, badges, version, install, quick start, layout, security and licence |
| Documentation | Conformant | `DEVELOPMENT.md`, architecture, ADR, migration guide, support and contribution policy |
| Build interface | Conformant | `Makefile`, pinned local SSG build, reproducible Pages artefact |
| Release engineering | Conformant | SemVer `VERSION`, signed sequential tags, changelog, tag release workflow, SBOM and checksums |
| CI quality | Conformant | unit, integration, content, link, i18n, layout, print, AAA and Lighthouse gates |
| Security | Conformant | CSP, CodeQL, Dependabot, Scorecard, SBOM, security policy, pinned actions |
| Community | Conformant | code of conduct, contributing, governance, support, agents, citation, editor and devcontainer files |
| Binary packaging | Not applicable | static website; no executable, native library, ABI, man page, shell completion, package-manager formula, or FFI |
| API compatibility | Not applicable | website publishes documentation and a browser demo; the separate `pain001` repository owns the library API |
| Fuzzing and benchmarks | Not applicable | no parser implementation is maintained here; vendored runtime behaviour is integration-tested against the library |

“Not applicable” removes only requirements that cannot describe this
repository type. Accessibility, release integrity, security, documentation,
and deterministic build requirements remain mandatory.
