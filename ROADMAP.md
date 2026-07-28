# Implementation plan — completing the 2026 audit backlog

**Written:** 28 July 2026 · **Status:** proposal, not yet approved
**Covers:** everything from the July 2026 audit that is still open, after
the claim-architecture and defect work already merged.

This plan is written against the code as it exists, not against a generic
consulting template. Every phase names the files it touches, the data
model it introduces, and the acceptance test that proves it done.

---

## 0. Two constraints that shape everything below

Any plan that ignores these will produce estimates that are wrong by a
factor of two or more.

### 0.1 Every user-facing string now costs 34 translations

The site ships 360 pages across 34 locales, with four translation table
sets under `scripts/`:

| Table set | Covers | Strings |
|---|---|---|
| `try_i18n/` | demo UI + nav/footer chrome | ~90 |
| `pages_i18n/` | why, solutions, executive-brief | ~85 |
| `docs_i18n/` | documentation, faqs, installation, glossary | ~180 |
| `runtime_i18n/` | JS message templates with `{placeholder}` tokens | 49 |

All four are enforced in CI by `validate_*_i18n.py` for key, tag and
placeholder parity. **A new UI surface is not "build the UI" — it is
"build the UI, then translate it 34 times, then keep it in parity
forever."**

The design consequence runs through this whole plan: *rule content must
be data, not chrome*. A profile rule's message, source citation and
remediation hint should live in the profile manifest in English, be
displayed verbatim with its source link, and be explicitly out of scope
for the locale tables. Only the surrounding UI furniture ("Severity",
"Source", "Not evaluated") is translated. That keeps a registry of
thousands of rules from multiplying into a translation liability.

### 0.2 Scheme rules today are code, not data

`pain001/validation/schemes.py` is 777 lines of hand-written Python:
`_check_currency`, `_check_ibans`, `_check_bic`, `_check_mandate`,
`_check_sequence_type` and so on, each returning `SchemeViolation`
records with stable rule IDs (`SEPA-CCY`, `SEPA-AMT`, `SEPA-CHARSET`).

That design is fine for five rulebooks maintained by one person. It does
not extend to a public registry where third parties contribute bank
profiles — nobody should have to submit a Python patch, and no reviewer
should have to audit arbitrary code to accept a profile.

**So the profile registry has a hard prerequisite: a declarative rule
format and an evaluator for it (Phase C). Attempting Phase D before
Phase C is the single most likely way to make this work fail.**

The good news is that `SchemeViolation` already has close to the right
shape — `rule`, `message`, `index`, `field`, `severity`, plus a
`remediation` property. The declarative model should extend that record,
not replace it, so the CLI, REST, MCP and LSP surfaces keep working
unchanged.

---

## Phase A — pain.001.001.13 support

**Why first:** it is the smallest phase, it closes an open standards-currency
gap, and it exercises the version pipeline end to end before anything
larger depends on it. ISO published `.13` on 19 March 2026; the site now
lists it as tracked/not-supported, which is honest but temporary.

**Repository:** `sebastienrousseau/pain001` (library), then the site.

### Work

1. **Acquire the schema.** Download the official
   `pain.001.001.13.xsd` from iso20022.org. Add
   `pain001/templates/pain.001.001.13/` following the existing layout —
   every other version directory is the pattern to copy.
2. **Register the version.** Add to the supported list in
   `pain001/constants.py` (currently `.03`–`.12`).
3. **Diff `.12` → `.13`** and encode any element changes in the
   generator and in `pain001/migration/` mappings.
4. **Test vectors.** A passing and a failing document per new or changed
   constraint, in the existing fixtures layout.
5. **Site follow-through:** flip the compatibility-matrix row from
   "not yet supported" to supported; add a `_posts/pain.001.001.13.md`
   version page using the same template as the other ten; update the
   "11 message definitions" count on the homepage strip and in
   `compatibility.md`'s excerpt to 12.

### Acceptance

- `pain001 -t pain.001.001.13 -d payments.csv -o out/` produces a
  document that validates against the official XSD.
- `VersionMapper().migrate_rows(rows, "pain.001.001.09", "pain.001.001.13")`
  round-trips the test corpus.
- Site: `validate_snippets.py` passes on the new version page;
  `validate_links.py` CLEAN; the count claim is consistent everywhere
  (`grep -rn "11 message definitions"` returns nothing stale).

### Effort and risk

**5–8 person-days.** Low risk. The one unknown is how much `.13`
actually changed from `.12`; if it touches the address or structured
remittance model the migration mapping is a day or two more.

**i18n cost:** one new version page × 34 locales *if* version pages are
localised. They are currently English-only — **recommend keeping them
English-only** and leaving the localised set at the nine page types that
already exist. Say so explicitly on the page rather than letting it look
like an oversight.

---

## Phase B — layer-aware results in the demo

**Why second:** the homepage now *states* the four-layer model, but
`/try/` still returns a flat verdict. Until the demo demonstrates the
model, the claim is a paragraph rather than a product property. This is
the cheapest way to make the repositioning real.

**Files:** `static/js/try-demo.js` (pure, unit-tested),
`static/js/try-page.js` (DOM), `_layouts/try.html`,
`scripts/runtime_i18n/*.json`, `tests/try-demo.test.mjs`.

### Work

1. **Tag every finding with its layer.** `validateRecords()` findings
   gain `layer: "iso" | "scheme" | "data"`. The XSD gate's findings are
   `layer: "iso"`. This is a small change to the existing
   `{row, column, rule, value, message, template, params}` record —
   which already carries a stable `rule` ID, so the layer can be derived
   from a lookup table rather than threaded through every call site.
2. **Result summary component** replacing the single status line:

   | Layer | State |
   |---|---|
   | ISO 20022 schema | Passed / n errors / Not run |
   | Scheme rulebook | Passed / n errors / No scheme selected |
   | Your bank's profile | **Not evaluated** — Pain001 ships no bank profiles |
   | Channel and eligibility | **Not evaluated** — decided by your bank |

   The two "not evaluated" rows are permanent and deliberate. They are
   the honest part, and they are what a treasury reviewer screenshots.
3. **Scheme selection in the browser.** The CLI has `--scheme`; the
   demo currently does not expose it. Add a selector (SEPA SCT, SEPA
   Instant, SDD Core, SDD B2B, CBPR+) so layer 02 can actually run.
   This requires porting the relevant scheme checks to the browser —
   see the parity note below.
4. **Report export** gains the same four-row structure, so a
   downloaded report carries the boundary with it.

### The CLI/browser parity trap

`try-demo.js` reimplements a subset of the Python validation in
JavaScript. Adding scheme rules doubles the surface where the two can
silently diverge. **Do not hand-port the rules.** Instead:

- Generate the browser's scheme rule table from the same source the
  Python uses (after Phase C, that is the declarative manifest; before
  Phase C, a generated JSON extract from `schemes.py`).
- Add a **golden parity test**: a corpus of ~50 CSV files, each run
  through the CLI and through Node with `try-demo.js`, asserting the
  same rule IDs fire. Run it in CI.

Without that test, "browser says valid, CLI says invalid" becomes a
support burden and a credibility problem — exactly the kind of defect
that the snippet validator caught elsewhere.

### Acceptance

- Every finding carries a layer; no finding is unlabelled.
- The four-row summary appears for every run, including the failure and
  empty states.
- Golden parity test passes: browser and CLI agree on rule IDs across
  the corpus.
- `node --test tests/*.test.mjs` still green (currently 19 tests;
  expect ~35 after).
- pa11y WCAG2AAA zero errors on `/try/` and on a localised demo page;
  the summary must be readable by screen reader — the layer states go
  in the existing live region, not a colour-only indicator.

### Effort and risk

**12–18 person-days**, of which the parity harness is a third and is the
part most likely to be cut under pressure. It should not be.

**i18n cost:** ~15 new runtime strings × 34 locales, plus ~10 UI labels
in `try_i18n`. Both are established pipelines
(`extract_try_i18n.py` → translate → validate), so this is a day of
orchestration, not a rebuild.

---

## Phase C — declarative rule format and evaluator

**Why this is the hinge:** everything valuable in Phase D depends on
rules being data. This phase adds no user-visible feature, which makes
it the easiest to skip and the most expensive to skip.

**Repository:** library. **Files:** new `pain001/rules/` package,
`pain001/validation/schemes.py` (migrated, not deleted).

### The rule model

A profile is a signed, versioned document. A rule inside it is:

```yaml
id: EXAMPLEBANK-ADDR-TOWN            # stable, namespaced, never reused
applies_to:
  message: pain.001.001.09
  paths: [CdtTrfTxInf/Cdtr/PstlAdr]
condition:                            # declarative, no arbitrary code
  all:
    - exists: TwnNm
    - matches: {field: Ctry, pattern: "^[A-Z]{2}$"}
severity: error                       # error | warning | advisory
message: "Creditor town name is required for this product."
remediation: "Populate <TwnNm> from your ERP's city field."
source:
  publisher: Example Bank
  document: "Corporate Payments File Specification v4.2"
  url: https://example.com/spec-v4.2.pdf
  page: 37
  retrieved: 2026-07-28
effective_from: 2026-11-14
test_vectors:
  passing: [vectors/addr-town-ok.csv]
  failing: [vectors/addr-town-missing.csv]
```

**Design rules, each of which exists for a reason:**

- **No arbitrary code.** Conditions come from a closed vocabulary
  (`exists`, `matches`, `in_set`, `length`, `compare`, `all`, `any`,
  `not`). A contributed profile must be reviewable by reading it. This
  is the difference between a registry that can accept community
  contributions and one that cannot.
- **Every rule cites a source with a retrieval date.** A rule without
  provenance is an opinion. This is also what makes the registry
  defensible when a bank asks where a requirement came from.
- **Every rule ships test vectors.** A rule with no failing vector has
  never been shown to fire.
- **Effective dates are first class**, so the same file can be validated
  against today's rules and against November 2026's.

### Work

1. Define the schema for the manifest (JSON Schema, versioned).
2. Write the evaluator: manifest + payment rows → `SchemeViolation`
   records. Reuse the existing record type so every downstream surface
   is unchanged.
3. **Migrate the five existing scheme rulebooks into manifests.** This
   is the proof the format is expressive enough. If SEPA SCT cannot be
   expressed declaratively, the format is wrong and better to learn it
   now than after publishing a contribution guide.
4. Keep `schemes.py` as a thin shim over the evaluator so the CLI flag,
   REST endpoint, MCP tool and LSP diagnostics keep working.
5. Property test: for the existing test corpus, the declarative SEPA
   rulebook produces byte-identical violations to the current code.

### Acceptance

- All five rulebooks expressed as manifests; the equivalence property
  test passes on the full corpus.
- 100% coverage floor holds (the repo enforces `--cov-fail-under=100`).
- No public API change: `pain001 --scheme sepa-sct` behaves identically.
- Evaluating a manifest with an unknown condition type fails closed with
  a clear error, never silently skips a rule.

### Effort and risk

**20–30 person-days.** This is the highest-risk phase because the format
must be got roughly right the first time — a published manifest schema
is hard to change once third parties depend on it. Mitigation: version
the manifest schema from day one (`manifest_version: 1`) and treat the
five migrated rulebooks as the compatibility test suite.

**i18n cost:** zero, by design. Rule messages are data in English with a
source link, per §0.1.

---

## Phase D — public profile registry

**Why it is the differentiator:** SWIFT MyStandards is the conceptual
model, but it is gated and licensed. An open, locally-executable,
source-cited profile registry is something no direct competitor has, and
it is the piece a bank or ERP vendor could plausibly contribute to.

### Legal constraint, stated first

**Do not redistribute proprietary usage guidelines.** MyStandards
content is licensed. Bank specification PDFs are usually copyrighted.
The registry must contain **rules derived from published requirements,
with a citation**, not copies of the source documents — the same
relationship a citation has to a paper. Each profile carries a
`licence_status` field: `public-source`, `permissioned` (the publisher
approved it in writing), or `community-derived`. Anything unclear does
not ship.

### Verification tiers

| Tier | Meaning |
|---|---|
| Community contributed | Submitted with source links, not yet reviewed |
| Source verified | A maintainer checked every rule against the cited public source |
| Test verified | Source verified, plus passing and failing vectors for every rule |
| Publisher verified | The bank or scheme owner has confirmed it in writing |
| Stale | Past its review SLA, or its source document has a newer version |
| Withdrawn | Superseded or no longer accepted |

**No profile may be described as "bank-certified" unless it is Publisher
verified.** That distinction is the registry's integrity.

### Initial portfolio (demand-led, not brand-led)

Start with ten, not fifty: SEPA SCT, SEPA Instant, SDD Core, SDD B2B,
CBPR+/SCORE+ public requirements, CHAPS initiation guidance, and three
to four bank corporate formats whose specifications are genuinely public
(Goldman Sachs Developer, Huntington Developer and Deutsche Bank
corporate guidance are the strongest public candidates identified in the
audit).

### Work

1. Registry repository layout, manifest signing, release versioning.
2. Contribution guide, review checklist, and a PR template that will not
   accept a rule without a source and vectors.
3. Profile explorer pages on the site — **English-only, and say so**
   (see §0.1; localising a growing registry is not sustainable).
4. Machine-readable diffs between profile versions.
5. Effective-date selector so a user can validate against a future
   profile.
6. A named owner and review cadence per profile. **This is an ongoing
   operation, not a project with an end date.** A stale profile is worse
   than no profile, because it looks authoritative.

### Acceptance

- Ten profiles at Test verified or better.
- Every rule: source, retrieval date, effective date, vectors, owner.
- Signed, versioned releases; a changed profile produces a readable diff.
- The site never presents an unverified profile as verified.

### Effort and risk

**40–70 person-days for the first ten profiles**, then **ongoing
maintenance that does not stop**. Budget review time per profile per
quarter, forever. The main risk is not technical — it is committing to
freshness that a solo maintainer cannot sustain. If the cadence cannot
be staffed, publish fewer profiles with an honest review SLA rather than
more with a stale one.

---

## Phase E — Payment Readiness Lab

The audit's flagship recommendation. With Phases B–D done, this is
mostly assembly: XML upload and paste, MT101 input, context selection
(country, rail, bank, channel, message version, effective date), the
layered result model, migration compatibility reporting, address
readiness scoring for the November 2026 deadline, and report export.

**Effort: 30–50 person-days** on top of B–D. Deliberately last: every
one of its parts is cheaper once the layer model, the rule engine and
the registry exist. Building it first would mean building each part
twice.

Two specifics worth pulling forward if the deadline pressure is real:

- **Address readiness checker.** Upload an ERP customer extract, get a
  structured/hybrid/unstructured classification and a remediation list.
  This is master-data remediation *before* XML generation, it maps
  directly to the 14 November 2026 deadline the site already leads on,
  and it can ship standalone before the rest of the Lab.
- **MT101 migration decision tree.** The audit correctly notes that
  MT101 migration is segmented — SWIFT treats MT101 multiple and single
  differently — and the site should stop implying one rule fits every
  corporate flow.

---

## Phase F — enterprise packaging

Supported release channel, LTS policy, signed containers, air-gapped
install pack, procurement questionnaire responses, architecture and
data-flow diagrams, ERP/TMS integration recipes.

**Effort: 30–60 person-days.** Sequence last, and only if there is
demand evidence — this phase is worthless without Phase G, and doing it
speculatively is how open-source projects acquire process without users.

Keep the boundary statements that already serve the project well:
Pain001 holds no funds, submits no payments, replaces no bank testing,
and is not a sanctions or AML system.

---

## Phase G — the track only you can run

No amount of engineering substitutes for these, and they gate any claim
of market leadership.

| Item | Status | Next action |
|---|---|---|
| Independent accessibility audit | RFQ and vendor shortlist ready in `AUDIT-RFQ.md` / `AUDIT-OUTREACH.md` | Send one of the three drafted emails |
| Independent security review | Not started | Scope after the accessibility audit lands |
| Named adopters | None | Ask the first three real users for permission to name them |
| Quantified case studies | None | One is worth more than ten feature bullets |
| Scorecard Signed-Releases | 2/10, rises automatically | Ship releases; it averages the last five |
| OpenSSF badge silver/gold | Passing earned | Silver needs governance docs already partly written |

**The honest read:** the project's ceiling right now is not technical.
Phases A–F would take it from an excellent tool to a category-defining
one, but *nothing in them produces a named reference customer*, and that
is the single thing an institutional buyer looks for first.

---

## Sequencing and totals

| Phase | Effort (person-days) | Depends on | Ship value |
|---|---:|---|---|
| A — pain.001.001.13 | 5–8 | — | Standards currency |
| B — layer-aware demo | 12–18 | — | Makes the new claim real |
| C — rule engine | 20–30 | — | Prerequisite for D |
| D — profile registry | 40–70 + ongoing | C | The differentiator |
| E — Readiness Lab | 30–50 | B, C, D | Flagship product |
| F — enterprise packaging | 30–60 | demand | Regulated adoption |
| **Total** | **137–236** | | |

That is meaningfully below the audit's 365–625 estimate, for two
reasons: it excludes the team-building and marketing workstreams that
estimate included, and it reuses far more of the existing architecture
(the violation record, the i18n pipelines, the CI gates) than a
from-scratch plan would assume.

**A and B are independent and can run in parallel.** If only two weeks
are available, do A and B: they close the standards gap and make the
repositioning tangible, and neither creates a maintenance commitment.

**C is the decision point.** Committing to C implies committing to D,
and D implies an indefinite freshness obligation. That is a genuine
strategic commitment, not a sprint — worth taking only if profile
maintenance can be staffed beyond one person.

---

## What I would not do

- **Do not localise the profile registry or the version pages.** The
  34-locale multiplier makes growing content sets unsustainable. State
  the language boundary rather than letting it look accidental.
- **Do not build the Lab before the rule engine.** Every component would
  be written twice.
- **Do not publish profiles faster than they can be reviewed.** A stale
  profile presented as authoritative is worse than an absent one.
- **Do not chase Scorecard Code-Review or Contributors.** Both require a
  second person; they are structurally unreachable and not worth
  distorting the workflow for.
