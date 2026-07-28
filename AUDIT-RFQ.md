# Request for Quote — Independent WCAG 2.2 AAA Audit of pain001.com

*Prepared 26 July 2026, revised 28 July 2026. Send to 2–3 vendors.
Indicative budget £3,000–£6,000: a static site of 360 routes, but only
~14 distinct page templates, plus one interactive tool. Vendors should
price the templates and the localisation matrix, not the raw page count.*

## Scope

- **Standard:** WCAG 2.2, Level AAA (full-site conformance claim intended).
- **Property:** https://pain001.com — static site, no authentication, no
  audio/video content (media AAA criteria expected to be recorded N/A).
- **Routes:** 360 pages in total, reducible to ~14 distinct templates.
  In scope: all English pages (~50); the interactive validator at `/try/`
  including its error scenarios, localised runtime messages and WASM
  schema gate; and a locale sample covering the writing systems —
  `/ar/` and `/ar/try/` (RTL), `/he/` (RTL), `/ja/` (CJK), `/th/`
  (complex shaping), `/de/why/` and `/fr/documentation/` (long-word and
  long-sentence reflow stress).
- **Localisation:** nine page types are generated in 34 locales
  (landing, `/try/`, `/why/`, `/solutions/`, `/executive-brief/`,
  `/documentation/`, `/faqs/`, `/installation/`, `/glossary/`), each with
  `lang`, `dir`, reciprocal `hreflang` and a language switcher. We want
  the switcher, the RTL mirroring and screen-reader language announcement
  assessed, not 34 full audits.
- **Themes:** light and dark must be assessed independently.
- **Zoom/reflow:** 200% text zoom and 400%/320 px reflow passes.

## Required methodology

1. Automated scanning is assumed but insufficient — the engagement must
   include manual assessment against every applicable AAA criterion.
2. Assistive-technology matrix, minimum: NVDA + Firefox, JAWS + Chrome,
   VoiceOver + Safari (macOS and iOS). The `/try/` demo's live regions
   (validation results, schema-gate progress phases) must be exercised.
3. Keyboard-only journey matrix including the Resources disclosure menu,
   mobile menu, theme toggle, demo end-to-end, and search overlay.
4. Forced-colors / Windows High Contrast Mode pass.

## Deliverables

- Per-criterion findings report (issue, WCAG SC, severity, location,
  remediation) suitable for direct import into GitHub issues.
- A re-test of remediated findings (one round included in quote).
- A dated conformance statement letter we may cite publicly and link from
  https://pain001.com/accessibility/ — bank vendor-assessment teams weigh
  a third-party report far above self-assessment.

## Context the vendor should know

- The site enforces its own gates in CI (ssg WCAG gate, pa11y-ci at
  WCAG2AAA, both themes, plus link-integrity and translation-parity
  gates) — the audit's value is the manual/AT layer, which tooling
  cannot reach.
- Current self-assessed position: Lighthouse accessibility 100 and pa11y
  WCAG2AAA zero errors on every page sampled, in both themes, including
  RTL and CJK locales. We are explicitly asking you to find what those
  tools miss.
- Design tokens document measured contrast ratios inline; the accessibility
  statement at /accessibility/ records current method and known limits.
- No cookies, no analytics, no third-party requests — auditors can work
  with DevTools open and will see only same-origin traffic.

## Candidate vendor types

UK/EU accessibility consultancies with financial-services references
(e.g. DAC, TetraLogical, Hassell Inclusion, AbilityNet-style practices) or
IAAP-certified independents (CPWA/WAS). Selection criteria: AT-user
testers on staff, WCAG 2.2 (not 2.1) fluency, and willingness to audit at
AAA rather than AA.
