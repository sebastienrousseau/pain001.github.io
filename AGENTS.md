# Agent instructions

- Read `README.md`, `DEVELOPMENT.md`, and `/Users/seb/Code/REPO-STANDARD.md`
  before changing this repository.
- Build with the latest `ssg` release, locally and in CI; never pin an
  older one. The pin is `SSG_VERSION` in `.github/workflows/ci.yml`; move
  it, and the same key in every other workflow, when ssg releases.
- Never edit generated `docs/` or generated corpus/locale pages directly.
- Preserve WCAG 2.2 AAA, zero accessibility findings, and 100 Lighthouse
  scores on mobile and desktop.
- Run `make verify` before proposing a commit.
- The website ships the pain001 suite version in lockstep. The maintainer
  authorized joining at 0.0.82; subsequent releases advance one patch together.
- Use the suite release branch `feat/vX.Y.Z`. Preserve published tags.
- Sign and DCO-sign off every commit (`git commit -S -s`).
- Do not publish, tag, release, or merge unless all required checks are green.
