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
Each gap points at the right follow-up skill (`research-author`,
`draft-summary`, `media-scan`).

## Entry requirement (admission rule)

Before auditing, confirm the author meets the catalogue's admission
rule (SPEC §1.2). An author qualifies if **either**:

- (i) at least one publication in a journal on `data/journals.json`
  Tier A or B, **or**
- (ii) ≥ 3 peer-reviewed published articles in English in any
  economics, finance, or management journal.

If neither holds, halt and flag for the editor — don't audit
someone who shouldn't be in the catalogue. Run `hu-econ-verifier`
(Check 1) for eligibility doubts.

## Inputs

An author slug or name. Resolve name → slug via `data/authors/`.

## What to check

### A. Author-level fields — `data/authors/<slug>.json`

- `name_en`, `name_hu` — non-empty
- `affiliations` — at least one entry; primary affiliation has no `end` date
- `bio_en`, `bio_hu` — non-empty, ≥2 sentences, not the seed one-liner
- `photo_url` — non-null and resolves (200 OK, image content type).
  Skip URL fetch if the host is known-stable (kti.krtk.hu,
  economics.ceu.edu, *.uni-corvinus.hu, bruegel.org, ideas.repec.org,
  en.wikipedia.org, commons.wikimedia.org); fetch otherwise.
- `repec_id`, `scholar_id`, `orcid` — present
- `qualifying_publication` — non-null
- `primary_fields` — at least one entry, all valid against `TAXONOMY.md`
- `review_status` — flag if `stub`
- `deceased` / `died` — internally consistent

### B. Catalogue contents — diff against `data/papers/`, `data/policy/`, `data/press/`

For every paper / policy / press JSON whose `authors` array contains `<slug>`:

**Research papers (`data/papers/`):**
- `review_status` count by `metadata-fetched`, `ai-drafted`, `human-reviewed`, `author-approved`
- `summary_en` ≥ 80 words (per SPEC §5)
- `summary_hu` present
- `data_used` ≥ 40 words
- `policy_relevance` ≥ 60 words
- `topics` non-empty
- `doi` present for articles
- `url_published` present
- co-authors — flag any `TBD` / `unknown` / single-name string

**Policy items (`data/policy/`):**
- `summary_en` present
- `policy_relevance` present (required by SPEC §2.6)
- `summary_hu`, `policy_relevance_hu`
- `linked_paper_id` opportunity check
- `outlet_kind` ∈ `{report, chapter, working_paper}`

**Press items (`data/press/`):**
- `title_hu` present for `language=hu` items
- `title` (English canonical) present
- `linked_paper_id` opportunity check
- `kind` ∈ `{op-ed, column, interview, podcast, blog, newspaper, radio-tv, event-talk}`
- `url` resolves (domain-level only)

### C. RePEc diff (only if `repec_id` is present)

1. Fetch `https://ideas.repec.org/e/<repec_id>.html`. Parser logic in
   `scripts/verify_repec.py` — read for reference.
2. Extract published-articles list.
3. For each article whose journal is on `data/journals.json` Tier A
   or B, check whether `data/papers/` has a matching slug. If not,
   list as missing.
4. Same for 2023+ NBER / CEPR / IZA / CESifo working papers.

If `repec_id` is missing, skip and flag as a high-priority gap.

### D. Press / policy coverage diff

Quick passes against the highest-yield outlets:

1. `site:portfolio.hu <name>`
2. `site:voxeu.org <name>`
3. `site:bruegel.org <name>`
4. `site:telex.hu <name>`
5. `site:index.hu defacto <name>`

Cap at 5 searches. The `media-scan` skill walks the full source list.
Items found that aren't in `data/press/` or `data/policy/` go in the
gap list.

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
  [P2] HU translation for <N> already-drafted papers:
       - <slug-1>
  [P3] Draft summary_en + policy_relevance for <N> Policy items:
       - <slug-1>

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

CATALOGUE GAPS (RePEc diff):
  Missing from data/papers/:
   - <Title>, <Journal> <Year>  [tier A]

EXTERNAL COVERAGE GAPS (media diff):
  Likely missing from data/press/:
   - Portfolio column, <date>, <title>  — <URL>

DATA HEALTH:
  - DOI broken on <slug>: <doi>
  - Co-author "TBD" on <slug>

NEXT STEPS:
  Run: research-author <slug>            (for fields gaps)
       draft-summary --research <slug>   (for P1 / P2)
       draft-summary --policy <slug>     (for P3)
       media-scan --author <slug>        (for external coverage)
```

Omit empty sections. A short report is the success case.

## Priority ordering

From the editor's stated preference:

1. Hungarian translations of already-drafted papers
2. First drafts of metadata-fetched policy items
3. First drafts of metadata-fetched research papers (esp. for authors with 0 drafts)
4. Author photos
5. Author bio review (stubs)
6. `qualifying_publication`
7. HU translations of EN-origin Press *(deferred)*
8. `linked_paper_id` cross-links
9. `repec_id` coverage

## Bulk mode

For a batch of authors ("audit X to Y", "audit all A–D"), use
`bulk_audit.py` instead of running this skill per author. The script
does the file-level checks (sections A and B) for the batch in one
pass; skip the web fetches (sections C and D) at scale and run them
per-author later as needed.

```
python .claude/skills/audit-author/bulk_audit.py --pattern '^[a-d]'
python .claude/skills/audit-author/bulk_audit_summary.py --pattern '^[a-d]'
```

## Stopping rules

- One author per invocation in single mode.
- 5 web fetches max for the external-coverage diff.
- If `data/authors/<slug>.json` does not exist, halt and suggest
  `research-author <slug>` to build the entry first.

## Out of scope

- Fixing anything (output only).
- Hungarian-eligibility check — defer to `hu-econ-verifier`.
- Global statistics — `build.py`.
