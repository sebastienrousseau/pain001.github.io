# Release signing keys

Every release tag is an annotated, cryptographically signed Git tag. Verify a
tag with:

```sh
git fetch --tags --force
git tag -v v0.0.3
```

The authoritative signer is the verified GitHub identity of repository owner
Sebastien Rousseau. GitHub displays the verification result beside each tag
and release commit. Key rotation is announced in a signed commit and recorded
in this file; no retired key is silently removed.
