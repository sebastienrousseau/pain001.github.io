# Independent AAA audit — vendor shortlist and ready-to-send enquiries

Companion to `AUDIT-RFQ.md`. I cannot send these for you: commissioning an
audit is a financial commitment and the mail has to come from your address.
Everything below is ready to copy, paste and send — attach or link
`AUDIT-RFQ.md` in each.

Vendor details were checked on 2026-07-28 from each vendor's own site.
Prices are indicative only; none is a quote.

## Shortlist

### 1. Digital Accessibility Centre (DAC) — Swansea, UK
- Sales: `team@daca11y.org` · General: `info@digitalaccessibilitycentre.org`
- Phone: +44 (0)1792 815267
- Site: <https://digitalaccessibilitycentre.org/>
- **Why them:** their differentiator is a staff team of disabled testers
  using real assistive technology (screen readers, braille displays, voice
  recognition, high-visibility keyboards), and they invite clients to
  observe sessions. That is exactly the layer your CI cannot reach.
- **Watch for:** confirm in writing they will assess at **AAA**, not AA —
  their public material says "latest recognised standards" without naming
  the level.

### 2. TetraLogical — London, UK
- Email: `hello@tetralogical.com`
- Phone: +44 (0)20 8895 6768
- Site: <https://tetralogical.com/services/>
- **Why them:** deep W3C/standards involvement, so WCAG 2.2 fluency is a
  given, and they run usability testing with disabled people. Strongest
  choice if you want the conformance statement to carry weight with a bank
  vendor-assessment team.
- **Watch for:** their standard packages are framed as "assessments"
  rather than level-specific audits — ask them to price the AAA scope
  explicitly.

### 3. AbilityNet — UK charity
- Site: <https://abilitynet.org.uk/accessibility-services/products-and-services/accessibility-audit>
- **Why them:** published price point (a Digital Accessibility Review is
  advertised around £4,950 + VAT), charity status, and consultants who
  will help draft the accessibility statement itself.
- **Watch for:** the advertised review targets WCAG 2.2 failures and risk
  areas generally; confirm AAA coverage and how many templates the fee
  covers.

Optional fourth if you want a non-UK comparison: Hassell Inclusion
(<https://www.hassellinclusion.com/>) or an IAAP-certified independent
holding CPWA/WAS.

---

## Email 1 — to DAC (`team@daca11y.org`)

> **Subject:** WCAG 2.2 AAA audit + AT user testing — pain001.com (RFQ attached)
>
> Hello,
>
> I maintain pain001.com, an open-source ISO 20022 payment-initiation
> toolkit. The site is a static, no-tracking property of 360 pages built
> from about 14 templates, localised into 34 languages, with one
> interactive in-browser validation tool.
>
> I would like a quote for an independent audit at **WCAG 2.2 Level AAA**,
> with testing by your disabled testers on real assistive technology. The
> site already passes automated gates in CI (Lighthouse accessibility 100,
> pa11y at WCAG2AAA with zero errors, both light and dark themes,
> including RTL and CJK locales), so I am specifically buying the manual
> and AT layer that tooling cannot reach.
>
> The full scope, required methodology, AT matrix and deliverables are in
> the attached RFQ. Two things I would like confirmed in your reply:
>
> 1. That you will assess against **AAA**, not AA, and record N/A criteria
>    explicitly.
> 2. Whether observing a testing session is possible for this engagement.
>
> Could you let me know your availability, indicative fee, and whether one
> round of re-testing after remediation is included?
>
> Many thanks,
> Sebastien Rousseau
> https://pain001.com

## Email 2 — to TetraLogical (`hello@tetralogical.com`)

> **Subject:** Quote request — WCAG 2.2 AAA assessment of pain001.com
>
> Hello,
>
> I am looking for an independent accessibility assessment of pain001.com,
> an open-source ISO 20022 payment-initiation toolkit aimed at treasury and
> banking teams. It is a static site — no cookies, no analytics, no
> third-party requests — of 360 pages generated from roughly 14 templates
> and localised into 34 languages, plus an interactive validator that runs
> entirely in the browser (WebAssembly, with live-region status updates).
>
> I would like this assessed at **WCAG 2.2 Level AAA**. The site currently
> passes its own CI gates (pa11y at WCAG2AAA, zero errors across both
> themes and across RTL and CJK locales), so the value I am buying is your
> manual expertise and testing with disabled people — particularly around
> the validator's live regions, the language switcher, and RTL mirroring.
>
> The attached RFQ sets out scope, the assistive-technology matrix I would
> like covered, and deliverables. I am especially interested in a dated
> conformance statement I can cite publicly, since bank vendor-assessment
> teams weigh a third-party report far above self-assessment.
>
> Could you confirm whether you price AAA engagements, and give an
> indicative fee and lead time?
>
> Best regards,
> Sebastien Rousseau
> https://pain001.com

## Email 3 — to AbilityNet (via their contact form or enquiry address)

> **Subject:** Accessibility audit enquiry — WCAG 2.2 AAA, pain001.com
>
> Hello,
>
> I would like to enquire about an accessibility audit for pain001.com, an
> open-source ISO 20022 payment-initiation toolkit. It is a static site of
> 360 pages built from about 14 templates and localised into 34 languages,
> with one interactive in-browser validation tool. No authentication, no
> cookies, no analytics, no video or audio content.
>
> Your published Digital Accessibility Review looks close to what I need,
> but I would like to confirm two points before proceeding:
>
> 1. Can the review be conducted against **WCAG 2.2 Level AAA** rather
>    than AA?
> 2. How many distinct templates does the standard fee cover, and what
>    would the incremental cost be for the locale sample listed in the
>    attached RFQ (Arabic and Hebrew for RTL, Japanese and Thai for
>    script shaping)?
>
> I would also value your consultants' help reviewing the existing
> accessibility statement at https://pain001.com/accessibility/.
>
> Kind regards,
> Sebastien Rousseau
> https://pain001.com

---

## After the quotes come back

- Compare on: AAA (not AA) commitment, AT testers on staff, whether a
  re-test round is included, and whether the conformance statement may be
  cited publicly.
- Budget sanity: £3,000–£6,000 is the realistic band for this scope in the
  UK. A quote far below that usually means automated scanning with a
  report wrapper — which you already have for free in CI.
- Once a report lands, its findings become GitHub issues; the accessibility
  statement at `/accessibility/` should then cite the audit date, vendor
  and standard, replacing the current self-assessment wording.
