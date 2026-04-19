# WORKFLOW — Content ingestion

How content gets from "a name of an economist" to "a paper page on the live site."

The site is the easy part. Content is the work. This document specifies how that work happens.

---

## Overview

Five stages:

1. **Roster** — build and maintain the list of eligible economists
2. **Paper discovery** — for each economist, find their eligible papers
3. **Metadata fetch** — title, authors, journal, abstract, links
4. **AI drafting** — generate summary, data description, policy relevance, tags
5. **Review** — human reads, edits, approves → commit → site rebuilds

Each stage is tracked in a simple state column on the `papers/*.json` file: `review_status` ∈ `{discovered, metadata-fetched, ai-drafted, human-reviewed, author-approved}`.

---

## Stage 1 — Roster

**Input:** the seed list in `docs/SEED_ECONOMISTS.md`.

**Process:**
1. For each candidate name, check eligibility per `SPEC.md` § 1
2. Verify at least one publication in a Tier A or Tier B journal (see `data/journals.json`)
3. Create `data/authors/[slug].json` from the template

**Sources for discovering more economists:**
- [RePEc Hungary author list](https://ideas.repec.org/g/hungary.html) — the curated list of Hungarian economists with RePEc profiles
- [RePEc Hungary ranking](https://ideas.repec.org/top/top.hungary.html) — ranked by aggregated score
- CEPR member directory (filter: Hungary)
- KRTK Institute of Economics faculty page
- CEU Department of Economics and Business — current + alumni
- Corvinus University of Budapest faculty pages
- Diaspora discovery: check co-author networks of anyone already in. Hungarian economists co-author disproportionately with other Hungarians — the snowball works.

**Goal for MVP:** 30 authors on the site. Full roster target: ~80–100.

---

## Stage 2 — Paper discovery

For each admitted author:

1. Pull publication list from:
   - Their **RePEc/IDEAS profile** (most structured, has journal, year, DOI)
   - Their **personal website** (usually most current on working papers)
   - **Google Scholar** profile (catches missed items, but noisy — has duplicates and non-papers)
   - **CEPR discussion papers** by author
   - **NBER working papers** by author (for Hungarian-diaspora folks)
2. Deduplicate (same paper on multiple platforms — use title + year match)
3. Filter: keep published articles and working papers posted in the last 10 years. Older WPs only if they're canonical and unpublished.
4. Create one `data/papers/[slug].json` per paper, populating minimum fields (title, authors, year, journal or WP series, URL)

**Paper ID / slug convention:**
`[lead-author-surname]-[second-author-surname-or-et-al]-[year]-[short-outlet]`, e.g.
- `bekes-halpern-2023-jie`
- `koren-szeidl-2012-qje`
- `koszegi-rabin-et-al-2006-qje`

Keep slugs short and memorable — they appear in URLs.

**Automating stage 2:** RePEc has an API (no auth, XML). A small Python script can pull structured publication lists from author IDs. Write it once, run per author. Claude Code can write this script in the afternoon session as a nice-to-have.

---

## Stage 3 — Metadata fetch

For each paper now in the system with minimum fields:

1. If DOI known, fetch Crossref metadata — fills in volume, issue, pages, authors with IDs
2. Fetch abstract from:
   - Crossref (sometimes has it)
   - Journal page (requires scraping or manual copy)
   - SSRN / RePEc abstract page
   - Author's website (often has PDF + abstract)
3. Get the PDF URL (open-access version preferred: author's website, RePEc, SSRN, NBER)
4. Check for replication package (GitHub, Dataverse, journal supplement) — add URL if found

Set `review_status = "metadata-fetched"`.

---

## Stage 4 — AI drafting

This is the one stage where Claude is load-bearing. Prompt template:

```text
You are drafting a policy-facing entry for a Hungarian economics research catalogue.

Input:
TITLE: {title}
AUTHORS: {authors}
JOURNAL/OUTLET: {journal_or_working_paper_series}
YEAR: {year}
ABSTRACT: {abstract}
{optional: PDF_TEXT: first 5000 words of the paper}

Produce four outputs, in JSON:

1. summary_en — 80–150 words, 2–3 sentences. What question did the paper ask, what did they find, why is it interesting. No jargon; define any term that must appear. Name the country or setting studied explicitly. Do NOT paraphrase the abstract closely — rewrite entirely for a non-economist reader.

2. data_used — 40–80 words. What data did they use? Source, years, scale (number of firms / people / observations), country. Be concrete: "Hungarian firm-level tax data 2005–2020, ~12,000 firms, annual panel" is good; "administrative data" is not.

3. policy_relevance — 60–120 words. What should a Hungarian policymaker take from this? Name specific policy levers where possible (ministry, program, regulation). Include at least one caveat about generalizability — if the evidence is from another country, flag that. If the paper is theoretical, discuss which empirical regularities would need to hold for the theory to apply to Hungary.

4. tags — a JSON object with:
   - topics: array of 1–3 IDs from: labor-markets, education-skills, health, demographics-migration, trade-fdi, firms-productivity, innovation-digital, banking-finance, fiscal-tax, regional-urban, energy-environment, inequality-welfare, political-economy, transition-postcommunist, methods
   - methods: array of 1–2 from: rct, diff-in-diff, iv, rd, panel-data, synthetic-control, structural, theory, time-series, ml-text, descriptive-survey
   - data_types: array of 1–3 from: admin-firm, admin-tax, admin-individual, survey, firm-level-dataset, field-experiment, macro-aggregate, digital-trace, historical
   - countries: array of ISO codes from the countries studied

If you cannot determine a field confidently from the abstract alone, flag it in a 5th field:
   uncertain: array of field names you are unsure about, with a one-sentence note each.

Output valid JSON only. No prose outside the JSON.
```

**Model:** Claude Opus for drafting; Claude Sonnet can do bulk at lower cost but produces weaker policy framing. Budget: with Opus at current API pricing, ~300 papers × ~6k tokens each ≈ manageable. See `docs/SPEC.md` for integration options.

**Post-process:**
- Validate JSON parses
- Validate all tag IDs are in the controlled vocabularies
- Write to `papers/[slug].json`
- Set `review_status = "ai-drafted"`

---

## Stage 5 — Review

A human (initially Gábor; later other editors) opens each `ai-drafted` paper and:

1. Reads the three summary fields against the abstract / paper
2. Edits for accuracy, tone, and Hungarian policy relevance specifically
3. Checks tags — adds/removes as appropriate
4. Writes the Hungarian versions (`summary_hu`, `data_used_hu`, `policy_relevance_hu`) — or flags for later if doing English-first
5. Sets `review_status = "human-reviewed"`
6. Git commit triggers CI, site rebuilds with new paper

**Optional author-approval step:** email the author a preview link; if they reply OK, set `review_status = "author-approved"` and show a green checkmark on the paper page. Nice-to-have, not blocking.

**Throughput target:** 10 papers/hour review pace once the pipeline is running. So ~30 hours of review time to review the first 300 papers. Front-load the most senior / most-cited authors.

---

## Tooling

**Minimum viable toolkit:**
- Python script(s) for RePEc/Crossref fetching → `scripts/fetch.py`
- Claude Code session for AI drafting → use the prompt template above in batch
- Git + VS Code for review (edit JSON directly)
- GitHub Actions for build+deploy on push

**Nice-to-haves (post-MVP):**
- A lightweight review UI reading/writing JSON files (a local Astro page behind basic auth that shows the draft vs. the abstract side-by-side with edit fields)
- A Slack/email notification when new papers land in the `ai-drafted` queue
- Quarterly Google Scholar citation-count refresh

---

## Governance

- **Editor-in-chief:** Gábor initially. Names who can merge to main.
- **Editors:** can take papers from `ai-drafted` to `human-reviewed`. Add as roster grows.
- **Authors:** can submit corrections via GitHub issue or email. Open PR welcome.
- **Quality bar:** if a paper's summary makes a non-economist reader confused, it fails. Better to be plain and brief than technically rich.

---

## Tracking progress

Keep a `docs/PROGRESS.md` auto-generated from the JSON files:
- Authors admitted / target
- Papers by `review_status`
- Papers by topic (heatmap)
- Most-recent additions
- Papers with missing Hungarian translations

Regenerate weekly. Review at monthly content meeting once it's a team.
