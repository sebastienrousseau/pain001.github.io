---
author: "contact@pain001.com (Sebastien Rousseau)"
banner_alt: "A governance and continuity statement for the Pain001 open-source project, including single-maintainer risk mitigations."
banner_height: 500
banner_width: 1200
banner: "https://pain001.com/og/pain001-card.jpg"
cdn: "https://pain001.com"
changefreq: "monthly"
charset: utf-8
cname: pain001.com
copyright: "© 2023 - 2026 Sebastien Rousseau. Dual Apache-2.0 / MIT."
date: "2026-07-26T08:00:00+00:00"
description: "Who maintains Pain001, how decisions are made, how it is funded, what mitigates single-maintainer risk, and the editorial and corrections policy, stated plainly and with limitations included."
download: "https://pypi.org/project/pain001/"
format-detection: telephone=no
hreflang: en
icon: "https://pain001.com/img/pain001.svg"
id: "https://pain001.com/governance/"
image_alt: "A question-and-answer session on ISO 20022 payment file generation, covering the questions treasury, operations, engineering, and audit teams actually ask."
image_height: 120
image_width: 120
image: "https://pain001.com/img/pain001.svg"
keywords: "pain001 governance, open source maintainer, bus factor, project continuity, funding disclosure, corrections policy, open source risk"
language: en-GB
layout: page
locale: en_GB
logo_alt: "Pain001 Logo"
logo_height: 36
logo_width: 36
logo: "https://pain001.com/img/pain001.svg"
menu: active
name: Pain001
permalink: "https://pain001.com/governance/"
rating: general
referrer: no-referrer
revisit-after: "7 days"
robots: "index, follow"
short_name: pain001
subtitle: "Who is accountable, how decisions are made, and what happens if the maintainer disappears: the honest version."
tags: "ISO 20022, pain001, payments, python, banking, CBPR+, SEPA"
theme_color: "#0b0e14"
title: "Governance & Continuity"
url: "https://pain001.com/governance/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://pain001.com/governance/rss.xml"
category: Technology
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.72)"
item_description: "Who maintains Pain001, how decisions are made, how it is funded, what mitigates single-maintainer risk, and the editorial and corrections policy, stated plainly and with limitations included."
item_guid: "https://pain001.com/governance/rss.xml"
item_link: "https://pain001.com/governance/rss.xml"
item_pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
item_title: "Governance & Continuity"
last_build_date: "Sun, 26 Jul 2026 08:00:00 +0000"
managing_editor: "contact@pain001.com (Sebastien Rousseau)"
pub_date: "Sun, 26 Jul 2026 08:00:00 +0000"
ttl: 60
type: website
webmaster: contact@pain001.com
apple_mobile_web_app_orientations: portrait
apple_touch_icon_sizes: 192x192
apple-mobile-web-app-capable: yes
apple-mobile-web-app-status-bar-inset: black
apple-mobile-web-app-status-bar-style: black-translucent
apple-mobile-web-app-title: "Governance & Continuity"
apple-touch-fullscreen: yes
msapplication-navbutton-color: "rgb(2, 132, 199)"
twitter_card: summary_large_image
twitter_creator: "@wwdseb"
twitter_description: "Who maintains Pain001, how decisions are made, how it is funded, what mitigates single-maintainer risk, and the editorial and corrections policy, stated plainly and with limitations included."
twitter_image: "https://pain001.com/og/pain001-card.jpg"
twitter_image_alt: "Pain001 Logo"
twitter_site: "@wwdseb"
twitter_title: "Governance & Continuity"
twitter_url: "https://pain001.com/governance/"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thank you for using Pain001 Suite!"
site_last_updated: 2026-07-26
site_standards: "ISO 20022, WCAG 2.2 AAA, SWIFT CBPR+, W3C HTML5, CSS3, RSS, Atom, JSON-LD"
site_components: "Pain001 Core, pain001-mcp, pain001-lsp, loader-mt101, loader-xlsx"
site_software: "Static Site Generator (SSG), Python 3.12, Rust, FastMCP, PyGLS"
eyebrow: "Governance"
excerpt: "Pain001's governance disclosure: a single-maintainer project and the specific mitigations that make that risk assessable (permissive licences, reproducible pipeline, public development, protected supply chain), plus funding and conflict-of-interest disclosure, trademark position, and the editorial and corrections policy for this site."
last_reviewed: "2026-07-26"


---

## Maintainership

Pain001 is created and maintained by [Sebastien Rousseau](https://sebastienrousseau.com), a London-based fintech engineering leader. Development is public: [issues, pull requests, and releases](https://github.com/sebastienrousseau/pain001) are all on GitHub. Community contributions are reviewed and merged by the maintainer.

**This is a single-maintainer project.** That is a real concentration risk, and pretending otherwise would undermine everything else on this page. What makes the risk *assessable* rather than disqualifying:

- **Permissive licences with no CLA barrier**: the core is Apache-2.0 or MIT; any organisation can fork, patch, and redistribute indefinitely without permission.
- **Reproducible pipeline**: pinned dependencies, deterministic builds, 100% branch-covered tests, and a fully documented build mean a competent team can take over maintenance from the repository alone.
- **No hidden infrastructure**: there is no server, database, or service whose loss would strand users; everything runs from the published packages.
- **Protected supply chain**: signed commits, SHA-pinned CI, least-privilege tokens, and release provenance limit what a compromised account could silently ship.

## Decision-making

Decisions are made in public. Day-to-day changes go through a pull request and merge by lazy consensus once CI is green; significant changes (new public APIs, breaking changes, new dependencies, new message types or scheme profiles) start as an issue or discussion and need a maintainer's explicit approval. A decision that will be questioned later is recorded as an architecture decision record in the core's [docs/adr](https://github.com/sebastienrousseau/pain001/tree/main/docs/adr). Every commit carries a Developer Certificate of Origin sign-off, checked in CI. The full rules are in the core's [GOVERNANCE.md](https://github.com/sebastienrousseau/pain001/blob/main/GOVERNANCE.md).

## Release process

Releases follow the core's [RELEASING.md](https://github.com/sebastienrousseau/pain001/blob/main/RELEASING.md): an automated preflight, a signed annotated tag, PyPI publication through a trusted publisher, and build provenance and an SBOM attached to the release. The nine repositories of the suite release together at one version. Release authority (the PyPI trusted publisher and the tag-signing key) rests with the lead maintainer today.

## Becoming a maintainer

More maintainers is the single biggest thing that would de-risk the project. Contribute a few reviewed pull requests in one area (a scheme profile, an input loader, the documentation), help triage issues and review others' pull requests, then say you are interested in a [GitHub issue](https://github.com/sebastienrousseau/pain001/issues). A maintainer proposes you, and with no objection from the existing maintainers within a week you are added to [MAINTAINERS.md](https://github.com/sebastienrousseau/pain001/blob/main/MAINTAINERS.md).

## Funding and conflicts of interest

Development is **self-funded**. The core has no commercial edition and no revenue relationship with any bank, vendor, or standards body mentioned on this site; the [comparison page](/competitors-comparison/) names commercial competitors' genuine advantages precisely because no commercial interest prevents it. There is no paid tier and nothing for sale: no support contracts, services, sponsorships, donations or referral fees under any name. The [maintenance policy](/for-banks/#maintenance-policy), the [evidence pack](/for-banks/) and the [bank-profile guide](/docs/bank-profiles/) are free. The licence lets any firm support Pain001 commercially; the project has no commercial partners and takes no fees or referrals.

## Traction, stated plainly

<!-- traction:start -->
Figures refreshed at each site build from public sources (PyPI download statistics and the GitHub API); the date is the build date.

| Measure | Value | Source |
| :--- | ---: | :--- |
| pain001 downloads, last 30 days | 3,517 | PyPI |
| pain001 downloads, last 7 days | 3,432 | PyPI |
| GitHub stars | 49 | GitHub |
| GitHub forks | 17 | GitHub |

Refreshed 2026-11-10. Page views are counted by Cloudflare Web Analytics, cookieless and without identifiers, and a few anonymous events by the site's own Worker ([privacy](/privacy/)).
<!-- traction:end -->

## Trademark

"Pain001" is used as a project name; no trademark registration is claimed. `pain.001` itself is an ISO 20022 message identifier that belongs to the standard, not to this project.

## Corrections and editorial policy

Every research page carries a "last reviewed" date, and regulatory claims cite primary sources (SWIFT, central banks, EU institutions) rather than press coverage. Errors are corrected in place: [open an issue](https://github.com/sebastienrousseau/pain001.github.io/issues) describing the inaccuracy, and material corrections are noted in the page's git history, which is [public](https://github.com/sebastienrousseau/pain001.github.io/commits/main). Dated deadlines are re-verified against sources at each review; anything scheduled beyond the current year is explicitly marked revisable.

## Continuity commitments

- Releases remain on [PyPI](https://pypi.org/project/pain001/) and GitHub independent of any infrastructure this project operates.
- The website's full source, build pipeline, and content are [public](https://github.com/sebastienrousseau/pain001.github.io) and rebuildable with two open-source tools.
- If the project is ever discontinued, the repositories will be archived in place (readable, forkable, and installable) rather than deleted.

## Bus-factor plan

The goal is a second maintainer with release rights by mid-2027. Until then, what happens if the maintainer is unavailable is written down here, one item at a time:

- **Release keys.** Not yet arranged: release authority (the tag-signing key and the PyPI trusted publisher) rests with the lead maintainer, and no hand-over to a second maintainer is set up.
- **Domain.** Not yet arranged: the pain001.com registration and DNS are held by the lead maintainer, with no transfer procedure written down.
- **PyPI and GitHub ownership.** Not yet arranged: there is no second PyPI owner or GitHub administrator yet.

Everything else a successor needs is already public: the source, the release process, the build pipeline and this site.
