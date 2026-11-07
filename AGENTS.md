# Agent instructions

- Read `README.md`, `DEVELOPMENT.md`, and `/Users/seb/Code/REPO-STANDARD.md`
  before changing this repository.
- Build with the latest `ssg` release (0.0.74), locally and in CI; never
  pin an older one. Move `SSG_VERSION` in every workflow when ssg releases.
- Never edit generated `docs/` or generated corpus/locale pages directly.
- Preserve WCAG 2.2 AAA, zero accessibility findings, and 100 Lighthouse
  scores on mobile and desktop.
- Run `make verify` before proposing a commit.
- Use a `feat/vX.Y.Z` branch with patch-only increments.
- Sign and DCO-sign off every commit (`git commit -S -s`).
- Do not publish, tag, release, or merge unless all required checks are green.
