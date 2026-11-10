<!-- SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Site lift: audit claims checked

The "pain001.com 10/10: Final Audit & Implementation Plan" (9 November
2026) was written from the live pages. Before acting on it, each
factual claim in its Phases 1, 5, 6 and 8 was checked against this
repository and a local build of `feat/v0.0.84` (`./build.sh`, 711
pages). Verdicts: **true**, **false**, or **partly**. "Fixed" names the
commit on `work/site-lift` that addresses it.

## Phase 1: conversion quick wins

| Claim | Verdict | Evidence |
| --- | --- | --- |
| "Five focused packages" heads six cards, a miscount | False | Five tiles are packages (pain001, -mcp, -lsp, -loader-mt101, -loader-xlsx); the sixth is the example corpus. The count is now derived from the tiles (6511b5fc) |
| Informative homepage images have empty alt text | False | All six homepage images are atmosphere photos (city, facade, data centre, columns, Bank of England, city at dusk) carrying no information, so `alt=""` is correct. Two `make audit` gates (WCAG-1.1.1, IMG-ALT) already fail any `<img>` without `alt` |
| Homepage `og:type` is `article` | True | ssg writes `article` on every page whatever the front matter says. Fixed for the 35 home pages (cd046ace) |
| The sandbox sits behind a text link; the main CTA is a sales briefing | True | Fixed: the hero leads with the sandbox (41401f0c) |
| `/try/?sample=sepa` opens a loaded, validated sample | False | No such link existed; only `#sample=corpus:<id>` worked. `#sample=sepa-sct` now loads and validates the built-in SEPA sample (11699687) |

## Phase 5: technical SEO

| Claim | Verdict | Evidence |
| --- | --- | --- |
| `hreflang` and `x-default` need adding | False | Every built page carries a reciprocal cluster; ssg's hreflang and lang_consistency gates pass |
| Self-referencing absolute canonical needed on every page | Partly | Every indexable page has one. The 210 translated corpus pages and the utility pages (404, offline, thanks) have none on purpose: they are `noindex` |
| Exactly one H1 per page | True already | 710 of 710 pages |
| Titles of 60 characters or fewer | Partly | 258 pages run longer, mostly corpus and locale pages whose H1 is the SEO title; `validate_headings.py` already ratchets that count |
| Meta descriptions of 160 or fewer | Partly | 486 pages run longer; not yet gated |
| OG image on every page, with `og:image:alt` | Partly | Every page has an image; 4 lack `og:image:alt` (`executive-brief-de/-es/-fr`, `made-with-shokunin`) |
| `sitemap.xml` lists only indexable canonical URLs | True already | `validate_sitemap.py` gates it |
| Sitemap `lastmod` is the build date on every URL | True | Fixed: commit dates of each page's sources (ac61ba1a) |
| (Not in the plan) the homepage is missing from the sitemap | True | The dot-directory filter matched the homepage's path `.`. Fixed (91298aec) |
| `robots.txt` has no AI-crawler policy | True | Fixed (7a8e2eeb) |
| IndexNow on deploy needs adding | False | CI's `indexnow` job has submitted the sitemap after every deploy of `main` since before this audit |
| 404 page with search and main CTAs | Partly | `/404.html` is published and `noindex`, and links home, documentation, FAQs, glossary and installation; no search box or `/try/` link |
| Breadcrumbs on non-home pages | Partly | 428 of 710 pages |
| `/developers/` and `/about/` exist | False | Both return 404; the "Developers" nav item points at `/documentation/` |

## Phase 6: structured data and AI search

| Claim | Verdict | Evidence |
| --- | --- | --- |
| The site has no structured data | False | 985 JSON-LD blocks on 711 pages: WebSite and WebPage (697 pages), TechArticle (35), Dataset (252 corpus pages) |
| No SoftwareApplication or Organization entity | True | Fixed: merged into the homepage graph with the version from the release (f6111a88) |
| The Person entity on sebastienrousseau.com can be linked | True | `https://sebastienrousseau.com/#person` is published there |
| No `llms.txt` confirmed | False | `/llms.txt` and `/llms-full.txt` are built by `postbuild_fix.write_llms` |
| (Not in the plan) `llms.txt` facts are current | False | It said the MCP server has 21 tools; 0.0.83 ships 30. Fixed (3122c50d) |
| Markdown twins of docs pages | True (absent) | No page links a `text/markdown` alternate |
| `FAQPage` markup where an FAQ is shown | True (absent) | No page carries it |
| A `/search/` SearchAction target | False | The site has no `/search/` page, so no SearchAction was added |

## Phase 8: performance, mobile and accessibility

| Claim | Verdict | Evidence |
| --- | --- | --- |
| The hero font is not preloaded | False | `inter-var-latin.woff2` is preloaded; `font-display` is set in `prism.css` |
| Images lack `width`/`height` | False | 669 of 669 images carry both |
| The sandbox engine is 13 MB, loaded on request | Partly | It loads only once data arrives, but the vendored runtime is 18 MB, and the size is not shown on any control |
| `navigator.connection.saveData` is honoured | True (absent) | Not referenced anywhere |
| Copy buttons on code and a skip link exist | True already | Homepage commands and the new hero install line share one copy script with a polite live region; the homepage has a skip link |
| AAA contrast is checked | True already | `validate_contrast.py` runs in `make test` and CI |
| Lighthouse and axe gates | True already | CI runs Lighthouse over five profiles and a site-wide axe scan; not run locally |

## Phase 0: analytics

The plan proposes Plausible or Umami with custom events. The deployed
site loads Cloudflare Web Analytics (`static/js/pain001-analytics.js`,
a vendored beacon on deployed hosts only), which records page views but
no custom events. The event list in Phase 0 needs a maintainer decision
on the analytics tool before it can be built.
