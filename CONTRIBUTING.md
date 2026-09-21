# Contributing

Thank you for improving Pain001's documentation website.

1. Open an issue for substantial behavioural or information-architecture
   changes.
2. Branch from `main` using `feat/vX.Y.Z`, where the version is exactly one
   patch after the latest release.
3. Follow [DEVELOPMENT.md](DEVELOPMENT.md), run `make verify`, and update the
   changelog for user-visible work.
4. Commit with both a cryptographic signature and the DCO trailer:
   `git commit -S -s`.
5. Open a pull request. Do not merge until all required checks are green.

Generated corpus and locale pages identify their source generator in the
README. Edit that generator, not the derived file. Report vulnerabilities
privately as described in [SECURITY.md](SECURITY.md).
