# SEO outreach pack

Ready-to-send submissions that earn relevant links to
<https://pain001.com/pain-001/> and the rest of the site. Each one is
published under the maintainer's own account, so each is a draft to
review and send, not something automation posts.

Search Console, 90 days to 27 September 2026, shows pain001.com at
average position 2.1 for "pain001" and 9.4 for the generic "pain.001"
queries, where older, more-linked domains rank above it. Relevant links
from established resources are the largest remaining lever.

## 1. Curated GitHub lists

None of these lists mentions pain001 yet. Open one pull request per list,
following that list's contribution guide.

### moov-io/awesome-fintech (376 stars), section "Payments & Integrations"

It already lists iso20022.js and jPOS there. Proposed entry:

```markdown
- [pain001](https://github.com/sebastienrousseau/pain001) – Open-source Python library, CLI, REST API and MCP server that generates and validates ISO 20022 pain.001 and pain.008 payment files (versions .03 to .13) against the official XSDs and scheme rulebooks. ([What is pain.001?](https://pain001.com/pain-001/))
```

### 7kfpun/awesome-fintech (356 stars), section "Libraries › Python"

```markdown
- [pain001](https://github.com/sebastienrousseau/pain001) - Generate and validate ISO 20022 pain.001 and pain.008 payment files from CSV, Excel, SQLite, JSON or SWIFT MT101.
```

### brandonhimpfen/awesome-payments, section "Bank Transfers & ACH" or "Payment APIs & Developer Tools"

```markdown
- [pain001](https://pain001.com/) – Open-source generator and validator for ISO 20022 pain.001 credit-transfer files, with a browser demo that validates against the official XSD.
```

## 2. Stack Overflow

Answer only where pain001 genuinely solves the question, and say that
you maintain it (Stack Overflow requires disclosing affiliation).

- **[Creating a SEPA XML file](https://stackoverflow.com/questions/58142328)**
  (1,100 views, no accepted answer). Draft:

  > A SEPA credit transfer file is an ISO 20022 `pain.001` message (SEPA
  > still commonly uses `pain.001.001.03` or `.09`). It has three levels:
  > a group header with the message ID, transaction count and control sum,
  > one `PmtInf` block per debtor account and execution date, and one
  > `CdtTrfTxInf` per payment. The counts and sums must match the payments
  > or the bank rejects the file. [What is pain.001?](https://pain001.com/pain-001/)
  > walks through the structure with a complete example that validates
  > against the official XSD.
  >
  > Disclosure: I maintain pain001, an open-source Python tool that
  > generates these files from CSV or Excel and validates them:
  > `pip install pain001`, then
  > `pain001 -t pain.001.001.09 -d payments.csv -o out/`.

- **[understanding XML pain.001.001.03 tags](https://stackoverflow.com/questions/66874598)**.
  Add an answer only if the existing one leaves the asker's question open.
  The element reference at
  <https://pain001.com/message-spec-pain.001.001.03/> answers "what does
  this tag mean" for every path.

## 3. Search engines other than Google

- **Bing Webmaster Tools** (also feeds DuckDuckGo, Yahoo and several AI
  assistants): sign in at <https://www.bing.com/webmasters>, choose
  "Import from Google Search Console" to verify pain001.com in one step,
  then submit <https://pain001.com/sitemap.xml>.
- **IndexNow** needs no account: the site pings it after every deploy.

## 4. Adopters and case studies

A named adopter outweighs any on-page change for buyers and for search
engines. See [case-study-template.md](case-study-template.md) for the
structure and a permission request to send to users.
