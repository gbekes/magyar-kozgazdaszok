---
name: hu-econ-verifier
description: >
  Verify two specific facts for the Evidence for Hungary catalogue (or any
  similar research-roster project) — first, whether an economist qualifies
  as Hungarian under the project's eligibility rules, and second, whether a
  specific paper actually exists and isn't a hallucinated citation. Use this
  skill whenever the user wants to confirm an author's Hungarian eligibility,
  check whether a paper is real, validate a citation before adding it to a
  catalogue, or audit entries that look suspicious. Trigger on phrases like
  "is X Hungarian", "verify this author", "does this paper exist",
  "check this citation", "confirm this publication", "validate this entry",
  "is this a real paper", or anytime the user is adding or auditing entries
  for the Evidence for Hungary roster. Also trigger when the user shares a
  bibliographic reference and asks any form of "can you check this".
---

# hu-econ-verifier

A focused fact-checker. Two checks, nothing else. For the Evidence for Hungary catalogue or similar research-roster projects.

## Core principle

A claim is verified only when a primary or authoritative source confirms it. Absence of evidence is not evidence. If the check can't reach a confident answer, report `uncertain` and say what would resolve it. Never invent details, URLs, DOIs, or author affiliations.

For every invocation, return a short structured verdict, the evidence, and a confidence level.

---

## Check 1 — Is this author a Hungarian economist?

### Eligibility rule

An economist qualifies if **at least one** of these holds:

- Hungarian nationality (current or at time of publication)
- Born in Hungary
- Primary research affiliation at a Hungarian institution for ≥3 years — e.g. KRTK (Institute of Economics at HUN-REN Centre for Economic and Regional Studies), CEU (Central European University, especially the Budapest-era faculty and alumni), Corvinus University of Budapest, ELTE, MNB (Hungarian National Bank) Research, universities in Debrecen, Szeged, Pécs, Miskolc

Diaspora counts. Research topic is irrelevant — a Hungarian studying Indonesian trade still qualifies; a Finn studying Hungarian labor markets does not.

### Process

1. **Run a web search on the author's name** with a disambiguating term like "economist" or their known field. Try the name exactly as given first.
2. **Read the first few authoritative results.** Rank sources by quality:
   - RePEc / IDEAS author profile — if the person appears on the curated [Hungarian economists list](https://ideas.repec.org/g/hungary.html), that is near-conclusive evidence
   - University faculty page or the author's personal academic website — usually lists education, affiliations, sometimes CV
   - Wikipedia (English or Hungarian) — good for senior / well-known economists
   - CEPR, IZA, NBER affiliation pages — note the listed country
   - LinkedIn — useful for current affiliations and tenure; weak for nationality
3. **Look for a single qualifying fact:** explicit nationality, Hungarian birthplace, or a long-term (≥3 years) affiliation at a Hungarian institution. One hit is enough.

### Common traps

- **A Hungarian-sounding name is a prior, not proof.** Many non-Hungarians (especially in Slovakia, Romania, and the Jewish diaspora) have Hungarian-sounding names; many Hungarians don't. Use the name to narrow the search, not to draw a conclusion.
- **Short visiting positions don't qualify.** A one-year visiting fellowship at KRTK doesn't make someone a Hungarian economist. Look for a primary affiliation of ≥3 years.
- **"Hungarian roots" / grandparents who emigrated** doesn't qualify unless the person was also born or raised in Hungary.
- **Name clashes** are common — there are multiple economists named "István Szabó." Disambiguate with field or affiliation before committing to a verdict.

### Output format for Check 1

```
AUTHOR: [Name, exactly as provided]
QUALIFIES: yes | no | uncertain
BASIS: [nationality | birthplace | HU institutional tenure | multiple]
EVIDENCE:
  - [URL]  — [one-line summary of what this source establishes]
  - [URL]  — [one-line summary]
CONFIDENCE: high | medium | low
NOTES: [name ambiguity, multiple affiliations, other caveats]
```

If `uncertain`, state what specific piece of evidence would resolve it (e.g., "CV confirming place of birth" or "list of long-term affiliations").

---

## Check 2 — Does this paper actually exist?

Papers are sometimes hallucinated by language models: the title sounds plausible, the authors are real, but no such paper exists. Or the paper exists but the citation combines wrong authors with the right title, or lists a wrong journal. This check confirms the paper is real and the citation is accurate.

### Process

1. **If a DOI is provided, fetch it first.** A working DOI that resolves to matching metadata is the strongest possible evidence. Use `web_fetch` on `https://doi.org/[DOI]`.
2. **If no DOI, search the exact title in double quotes** plus one author's surname to disambiguate. Exact-title search in quotes is the single highest-leverage query here.
3. **Cross-check at least two independent sources:**
   - Crossref / DOI system — authoritative for published articles
   - Journal website — authoritative, especially for recent issues
   - Google Scholar — good coverage but allows duplicates
   - RePEc / IDEAS, NBER, CEPR, SSRN, arXiv — authoritative for working papers
   - Author's personal website or published CV — useful confirmation
4. **Verify all four fields match** the claimed citation: title, authors, venue (journal or WP series), year.

### Signals of a likely hallucination

- **Zero hits for the exact title in quotes.** Strong negative signal. Do not lower the bar by dropping the quotes — that's how real-sounding fakes slip through.
- **Close-but-wrong.** Title is nearly identical to a real paper but off by a few words. AI often conflates two papers. Surface the real paper and mark the claimed citation as a mismatch.
- **Right title, wrong authors.** The paper exists but was written by different people. Treat as mismatch.
- **Right paper, wrong journal.** Often a working paper version is cited as if it were the published version, or vice versa. Note both and resolve.
- **For recent working papers (last 12 months), absence from Google Scholar is not conclusive** — there's indexing lag. Check the series site directly (NBER, CEPR, SSRN, author's website).

### Output format for Check 2

```
PAPER: [citation exactly as provided]
EXISTS: yes | no | mismatch | uncertain
FOUND AT:
  - [URL]
  - [URL]
METADATA CHECK:
  title:   match | mismatch  — [if mismatch, state the actual title]
  authors: match | mismatch  — [if mismatch, state the actual authors]
  venue:   match | mismatch  — [if mismatch, state the actual venue]
  year:    match | mismatch  — [if mismatch, state the actual year]
DOI: [if found]
CONFIDENCE: high | medium | low
NOTES: [any discrepancy explained; replication package URL if found]
```

For `mismatch`, always provide the corrected citation.
For `no`, explain what was searched for and what (if anything) similar was found.

---

## Combined invocations

When the user asks to validate both at once (e.g., "is this paper by a Hungarian economist, and is it real?"):

1. Run Check 1 first. If the author does not qualify as Hungarian, say so and note that Check 2 is moot for Evidence for Hungary inclusion — but still run it if the user explicitly asks for both.
2. Run Check 2.
3. Return a combined verdict block with both outputs, in the formats above.

## Throughput and stopping rules

- Budget ~1–3 searches per check. Stop once you have authoritative evidence.
- Don't pad out a response with extra searches to look thorough — concise, confident verdicts are the product.
- If the first two searches return nothing useful, escalate to `uncertain` and return. Don't keep searching indefinitely.

## Examples

**Example 1 — clear positive, author**

Input: "Is Réka Juhász a Hungarian economist?"
Output:
```
AUTHOR: Réka Juhász
QUALIFIES: yes
BASIS: nationality + birthplace (Hungarian-Canadian, raised in Hungary per public bio)
EVIDENCE:
  - https://ideas.repec.org/e/pju...  — RePEc profile lists Hungarian economists list membership
  - https://www.rekajuhasz.com/  — personal site indicates Hungarian background
CONFIDENCE: high
NOTES: Currently at UBC; author of "Temporary Protection and Technology Adoption" (AER 2018).
```

**Example 2 — clear negative, author**

Input: "Should we add Xavier Jaravel? His name sounds Eastern European."
Output:
```
AUTHOR: Xavier Jaravel
QUALIFIES: no
BASIS: —
EVIDENCE:
  - https://www.xavierjaravel.com/  — bio identifies him as French; LSE professor; no Hungarian connection
CONFIDENCE: high
NOTES: French economist. Name is French, not Hungarian. Do not add.
```

**Example 3 — paper, existence confirmed**

Input: 'Verify this paper: Lindner & Harasztosi, "Who Pays for the Minimum Wage?", AER 2019'
Output:
```
PAPER: Lindner & Harasztosi, "Who Pays for the Minimum Wage?", AER 2019
EXISTS: yes
FOUND AT:
  - https://www.aeaweb.org/articles?id=10.1257/aer.20171445
  - https://doi.org/10.1257/aer.20171445
METADATA CHECK:
  title:   match
  authors: match  (Péter Harasztosi and Attila Lindner)
  venue:   match  (American Economic Review)
  year:    match  (2019, vol 109 no 8, pp 2693–2727)
DOI: 10.1257/aer.20171445
CONFIDENCE: high
NOTES: Open-access working paper version available on Lindner's website.
```

**Example 4 — paper, mismatch**

Input: 'Check: Békés & Koren 2020, "Global Value Chains and Hungarian Firms", Journal of International Economics'
Output:
```
PAPER: Békés & Koren 2020, "Global Value Chains and Hungarian Firms", Journal of International Economics
EXISTS: mismatch
FOUND AT:
  - [journal search URLs]
METADATA CHECK:
  title:   mismatch  — no paper with this exact title exists by these authors
  authors: partial   — Békés and Koren have co-authored but not on this title
  venue:   mismatch
  year:    mismatch
DOI: none
CONFIDENCE: medium
NOTES: No JIE paper found matching this citation. Closest real papers by these authors include [their actual JIE work]. Likely a hallucinated citation — return to the original source to correct before adding.
```

## What this skill does NOT do

- Writing bios, non-technical summaries, or policy-relevance text — that's a separate workflow step
- Judging paper quality or journal tier — the project's `data/journals.json` handles that
- Classifying papers into topics
- Bulk ingestion

Stay narrow. Two checks, verdict, evidence, done.
