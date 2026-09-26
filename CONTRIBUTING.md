# Contributing

Thank you for improving Pain001's documentation website.

New here? Issues labelled
[good first issue](https://github.com/sebastienrousseau/pain001.github.io/labels/good%20first%20issue)
are small, self-contained tasks, each with the files to look at and what
done looks like.

1. Open an issue for substantial behavioural or information-architecture
   changes.
2. Branch from `main` using `feat/vX.Y.Z`, where the version is exactly one
   patch after the latest release.
3. Follow [DEVELOPMENT.md](DEVELOPMENT.md), run `make verify`, and update the
   changelog for user-visible work.
4. Add tests with every new or changed behaviour: unit or property tests
   under `tests/` for the demo's code, or a validator under `scripts/` wired
   into `make test` and CI for a site-wide rule. A fix comes with a test that
   fails without it. Pull requests that add functionality without tests are
   not merged.
5. Commit with both a cryptographic signature and the DCO trailer:
   `git commit -S -s`.
6. Open a pull request. Do not merge until all required checks are green.

## Reviewing changes

Every pull request is reviewed against the checklist below before it is
merged, and CI must be green. Today the project has one maintainer, so the
maintainer reviews their own changes against this list and CI is the second
check; once there is a second maintainer, every change needs an approving
review from someone other than its author.

A reviewer confirms that the change:

1. **Does what it says.** The description matches the diff, and nothing
   unrelated rides along.
2. **Is tested.** New or changed behaviour has tests, and a fix has a test
   that fails without it (step 4 above).
3. **Keeps every gate green.** `make verify`, the accessibility and
   Lighthouse audits, and the coverage gate pass; no threshold or rule was
   lowered to make them pass.
4. **Edits sources, not output.** Generated corpus, locale and `site/`
   files change only through their generator.
5. **Is accurate.** Every claim on a page (a version, a count, a deadline,
   a feature) matches its source, and a library feature is documented only
   once it is in a released version.
6. **Is safe.** Changes to the Content-Security-Policy, workflow
   permissions, dependencies or anything that handles demo input get a
   security read: no new third-party origin, no widened token scope, every
   dependency pinned by hash or lockfile, visitor data rendered only as
   text.
7. **Is recorded.** User-visible changes are in `CHANGELOG.md`, and every
   commit is signed with a DCO sign-off.

Generated corpus and locale pages identify their source generator in the
README. Edit that generator, not the derived file. Report vulnerabilities
privately as described in [SECURITY.md](SECURITY.md).
