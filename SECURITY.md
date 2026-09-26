# Security policy

## Supported versions

Only the current production deployment and latest source on `main` receive
security fixes. Historical website tags are immutable records and are not
maintained deployments.

## Reporting

Use GitHub's private vulnerability reporting for this repository, or email
`contact@pain001.com` if the private form is unavailable. Include impact,
reproduction steps, affected URLs, and a safe proof of concept. Do not submit
real payment or account data.

You should receive acknowledgement within seven days. Please allow reasonable
time for investigation and coordinated remediation before disclosure.

## How a report is handled

1. **Acknowledge** the report within seven days, privately.
2. **Assess** it: reproduce the issue, decide whether it is a vulnerability,
   and rate its severity with CVSS. The reporter hears the outcome.
3. **Fix** it on a private branch or a GitHub security advisory draft. A fix
   comes with a regression test or gate that fails without it.
4. **Release** the fix: deploy the site from `main`, and cut a patch release
   whose notes identify the vulnerability.
5. **Disclose** it through a GitHub security advisory once the fix is live,
   with a CVE when one applies.

## Credit

Reporters are credited by name in the advisory and the release notes, unless
they ask to remain anonymous.

## What to expect from the site

The site's security design, its trust boundaries and the weaknesses it
counters are set out in [docs/assurance-case.md](docs/assurance-case.md).
The latest security review is
[docs/security-review-2026-09.md](docs/security-review-2026-09.md).
