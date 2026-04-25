---
name: audit-author
description: >
  Audit one author's full record in the Magyar Közgazdászok catalogue and
  produce a prioritised gap list. Looks at the author JSON, all of their
  papers, all of their press, all of their policy items, and the journal
  whitelist. Reports: missing or stale author fields (photo, bio, repec_id,
  qualifying_publication, scholar_id, orcid), draft-completeness gaps
  (papers / policy with no `summary_en` or no `summary_hu`), broken DOIs,
  TBD co-authors, missing `linked_paper_id` opportunities, and any RePEc-vs-
  catalogue diff. Use when the user asks to "audit X", "check what's missing
  for Y", "what's the state of Z's page", "what needs work on W",
  "review X's catalogue", "qa X", or names an author and asks "what's left
  to do here". Returns a numbered task list ranked by editor-stated
  priority (drafts > photos > bios > linked_paper > qualifying > repec_id).
---

# audit-author

A read-only QA pass on one author. Reports gaps; doesn't fix them.
Each gap is a pointer to the right follow-up skill (`research-author`,
`draft-summary`, `media-scan`).

## Core principle

The audit is the cheap step. Fixing each gap is a separate, more
expensive step that the editor approves one by one. So this skill
makes the gap list as concrete and ranked as possible — every line
should be actionable on its own.

## Inputs

- An author slug or name. Resolve name → slug via `data/authors/`.
- That's it. No flags. The audit is comprehensive by default; the
  output's ranking handles prioritisation.

## What to check

### A. Author-level fields — `data/authors/<slug>.json`

- `name_en`, `name_hu` — both present and non-empty
- `affiliations` — at least one entry; current primary affiliation
  has no `end` date
- `bio_en`, `bio_hu` — both present, ≥2 sentences, not the seed
  one-liner from `authors-seed.json`
- `photo_url` — non-null and resolves (200 OK, image content type).
  Skip URL fetch if URL is on a known-stable host
  (kti.krtk.hu, economics.ceu.edu, *.uni-corvinus.hu, bruegel.org,
  ideas.repec.org, en.wikipedia.org, commons.wikimedia.org); fetch
  to verify otherwise.
- `repec_id` — present (only 14/87 have it as of 2026-04-25)
- `scholar_id` — present
- `orcid` — present
- `qualifying_publication` — non-null (only 7/87 have it)
- `primary_fields` — at least one entry, all valid against the
  topic taxonomy in `TAXONOMY.md`
- `review_status` — flag if `stub`
- `deceased` / `died` — internally consistent (if deceased=true,
  died should be a year)

### B. Catalogue contents — diff against `data/papers/`, `data/policy/`, `data/press/`

For every paper / policy / press JSON whose `authors` array
contains `<slug>`:

- **Research papers (`data/papers/<slug>-*.json`):**
  - `review_status` (count by: `metadata-fetched`, `ai-drafted`,
    `human-reviewed`, `author-approved`)
  - `summary_en` present and ≥80 words (per SPEC §5)
  - `summary_hu` present
  - `data_used` present, ≥40 words
  - `policy_relevance` present, ≥60 words
  - `topics` non-empty
  - `doi` present (for articles); resolves if fetched
  - `url_published` present
  - co-author list — flag any `TBD`, `unknown`, or single-name
    string entries
- **Policy items (`data/policy/`):**
  - `summary_en` present (currently only 11/46 have it)
  - `policy_relevance` present (required by SPEC §2.6)
  - `summary_hu`, `policy_relevance_hu`
  - `linked_paper_id` — opportunity check: search
    `data/papers/<slug>-*.json` for a likely match by topic + year
  - `outlet_kind` valid: `{report, chapter, working_paper}`
- **Press items (`data/press/`):**
  - `title_hu` present for items with `language=hu`
  - `title` present (English canonical)
  - `linked_paper_id` opportunity check
  - `kind` valid: `{op-ed, column, interview, podcast, blog,
    newspaper, radio-tv, event-talk}`
  - `url` resolves (light check — domain-level, don't hammer)

### C. RePEc diff (only if `repec_id` is present)

If the author has a RePEc ID:

1. Fetch `https://ideas.repec.org/e/<repec_id>.html` (or the `/f/`
   form). The script `scripts/verify_repec.py` has the parser logic;
   read it for reference.
2. Extract their published-articles list.
3. For each RePEc article whose journal is on `data/journals.json`
   tier A or B, check whether `data/papers/` has a corresponding
   slug. If not, list it as "missing from catalogue".
4. Same for 2023+ NBER / CEPR / IZA / CESifo working papers.

If `repec_id` is missing, skip this section but flag it as a
high-priority gap (RePEc diff is the catch-all for missed papers).

### D. Press / policy coverage diff

Check whether known media outlets cover this author but the catalogue
hasn't picked it up. Quick passes:

1. `site:portfolio.hu <name>` — surfaces Portfolio columns
2. `site:voxeu.org <name>` — surfaces VoxEU columns
3. `site:bruegel.org <name>` — for Bruegel-affiliated authors
4. `site:telex.hu <name>` — Telex Analysis pieces
5. `site:index.hu defacto <name>` — older Index defacto items

Cap at 5 searches. The `media-scan` skill goes deeper across the
full source list; here we're only catching the obvious. Items found
that aren't in `data/press/` or `data/policy/` go into the gap list.

## Output format

```
AUTHOR: <slug>  (<name_en>)
SUMMARY:
  papers:   <ai-drafted> / <total>   (HU: <hu> / <total>)
  policy:   <drafted> / <total>      (HU: <hu> / <total>)
  press:    <total>                  (HU title: <n> / <total>)
  fields filled: <count>/13
  review_status: <value>

HIGH PRIORITY (drafts + translations):
  [P1] Draft summary_en for <N> metadata-fetched papers:
       - <slug-1>
       - <slug-2>
       ...
  [P2] HU translation for <N> already-drafted papers:
       - <slug-1>
       - ...
  [P3] Draft summary_en + policy_relevance for <N> Policy items:
       - <slug-1>
       - ...

MEDIUM PRIORITY (visibility):
  [P4] Photo missing — try <suggested faculty page URL>
  [P5] Bio is at review_status: stub — refresh
  [P6] qualifying_publication is null — propose:
       <highest-tier paper from catalogue>

LOW PRIORITY (completeness):
  [P7] repec_id missing — search ideas.repec.org/e/<surname>
  [P8] scholar_id missing
  [P9] orcid missing
  [P10] linked_paper_id opportunities:
       - press <slug> may link to paper <slug>
       - ...

CATALOGUE GAPS (RePEc diff — only if repec_id was present):
  Missing from data/papers/:
   - <Title>, <Journal> <Year>  [tier A]
   - ...

EXTERNAL COVERAGE GAPS (media diff):
  Likely missing from data/press/:
   - Portfolio column, <date>, <title>  — <URL>
   - VoxEU column, <date>, <title>      — <URL>

DATA HEALTH:
  - DOI broken on <slug>: <doi>
  - Co-author "TBD" on <slug>
  - <other anomalies>

NEXT STEPS:
  Run: research-author <slug>            (for fields gaps)
       draft-summary --research <slug>   (for P1 / P2)
       draft-summary --policy <slug>     (for P3)
       media-scan --author <slug>        (for external coverage)
```

If a section has no entries, omit it rather than printing "none".
A short report is the success case.

## Priority ordering (editor's stated preference)

From the 2026-04-25 handover, in order:

1. Hungarian translations of already-drafted papers
2. First drafts of metadata-fetched policy items
3. First drafts of metadata-fetched research papers (esp. for
   authors with 0 drafts)
4. Author photos
5. Author bio review (stubs)
6. `qualifying_publication`
7. HU translations of EN-origin Press *(deferred — option b)*
8. `linked_paper_id` cross-links
9. `repec_id` coverage

Use this exact ordering for ranking gaps. The audit's value is
ranking, not just enumeration.

## Stopping rules

- One author per invocation. If the user names two, ask which first.
- 5 web fetches max for the external-coverage diff. Anything more
  belongs in `media-scan`.
- If `data/authors/<slug>.json` does not exist, halt and suggest
  `research-author <slug>` to build the entry first.

## What this skill does NOT do

- Fix anything. Output only.
- Bulk audits across all 87 authors. Use the script
  `scripts/verify_authors.py` if you need a global view; this skill
  is per-author.
- Verify Hungarian eligibility — that's `hu-econ-verifier`.
- Compute global statistics (catalogue snapshots) — that lives in
  `build.py`.
