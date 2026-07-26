# Request for Quote — Independent WCAG 2.2 AAA Audit of pain001.com

*Prepared 26 July 2026. Send to 2–3 vendors; typical budget for this scope
is £2,000–£5,000 (a static site of ~45 routes with one interactive tool).*

## Scope

- **Standard:** WCAG 2.2, Level AAA (full-site conformance claim intended).
- **Property:** https://pain001.com — static site, no authentication, no
  audio/video content (media AAA criteria expected to be recorded N/A).
- **Routes:** all English pages (~45), the interactive validator at `/try/`
  including its error scenarios and WASM schema gate, one RTL locale page
  (`/ar/`), and one CJK locale page (`/ja/`).
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
  WCAG2AAA, both themes) — the audit's value is the manual/AT layer.
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
