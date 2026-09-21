# Release process

1. Start `feat/vX.Y.Z`, incrementing the latest release by exactly `0.0.1`.
2. Update `VERSION`, `CITATION.cff`, `CHANGELOG.md`, and migration notes.
3. Run `make verify`, the desktop and mobile Lighthouse gates, and WCAG 2.2
   AAA browser scans locally.
4. Commit with `git commit -S -s`, push, open a pull request, and wait for all
   required checks.
5. Merge through GitHub. Create an annotated signed tag on the merge commit:
   `git tag -s vX.Y.Z -m "pain001.com vX.Y.Z"`.
6. Push the tag. The release workflow rebuilds, verifies the tag/version,
   produces the site archive, CycloneDX SBOM, and SHA-256 checksums, then
   publishes the GitHub release.

Historical tags are never moved or overwritten.
