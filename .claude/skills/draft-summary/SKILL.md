---
name: draft-summary
description: >
  Write the policymaker-facing fields (`summary_en`, `summary_hu`,
  `data_used`, `policy_relevance`, plus the HU twins) for a single paper,
  policy item, or press item in the Magyar Közgazdászok catalogue, OR for
  a batch defined by an author slug. Produces a JSON file matching the
  `apply_drafts.py` / `apply_summaries_hu.py` input format and (on user
  approval) applies it. Use when the user says "draft X", "write a summary
  for Y", "translate Z to Hungarian", "fill in policy_relevance for W",
  "do the drafts for author A", "draft Adamecz's BI briefs", or any phrasing
  about authoring the non-technical text fields. Follows the SPEC §5
  content contract (length, tone, no jargon, name the country, cite
  effect sizes).
---

# draft-summary

Authoring tool for the three written fields that appear on the public
site: `summary`, `data_used`, `policy_relevance`. Bilingual.

## Core principle

The summary fields are the entire content product. They're how a
policymaker decides whether to read the paper. Quality bar:

- A senior policy advisor should read the EN summary in 30 seconds
  and know whether this is relevant to their dossier.
- A Hungarian journalist should read the HU summary in 30 seconds
  and know whether to email the author for a quote.

Drafts written without that bar in mind are noise.

## What this skill drafts

Three target tables, each with slightly different fields:

| Target          | Fields drafted                                                    |
|-----------------|--------------------------------------------------------------------|
| `data/papers/`  | summary_en, summary_hu, data_used, data_used_hu, policy_relevance, policy_relevance_hu |
| `data/policy/`  | summary_en, summary_hu, policy_relevance, policy_relevance_hu      |
| `data/press/`   | (no summaries — press is intentionally minimal); only `title_hu` for HU-origin items |

Press items only get `title_hu` filled if missing and the original is
Hungarian-origin. No summary fields on press — that's per SPEC §2.7.

## The content contract (from SPEC §5)

| Field                | Length              | Answers                                                       |
|----------------------|---------------------|---------------------------------------------------------------|
| `summary_*`          | 80–150 words, 2–3 sentences | What question did the paper ask, and what did they find? |
| `data_used`          | 40–80 words         | What data, from where, what scale, what years?                |
| `policy_relevance`   | 60–120 words        | What should a Hungarian policymaker take from this?           |

### Hard rules

- **No jargon.** If a term must appear, define it in parentheses on
  first use. "RDD (regression discontinuity)" the first time, then
  just "RDD" thereafter.
- **Name the country / countries.** Open with the setting:
  "In Hungary, …" / "Across 24 EU countries, …" / "Using US firm
  data, …". Never start with "We find" — the reader doesn't know
  who "we" is.
- **Effect sizes with units.** "8% increase in employment", not
  "a positive effect on employment". "€450/month wage gap", not
  "a sizable wage gap".
- **Concrete data lines.** `data_used` is the trust signal: source
  agency, sample size, time window, unit of analysis. "NAV
  corporate tax filings 2010–2020, ~85,000 firms, annual panel" —
  not "rich administrative data".
- **Specific policy reader.** `policy_relevance` should name *who*
  uses it (ministry, agency) and *how* (program design, target
  population, instrument). External-validity caveats on non-HU
  papers go here, not buried.
- **Never copy the abstract.** Paraphrase entirely. Drafts that
  echo abstract phrasing fail review.
- **Hungarian is not a translation.** The HU draft answers the same
  questions but uses idiomatic Hungarian, not literal English-to-
  Hungarian. Hungarian academic register, Hungarian numbers
  conventions (vessző, not pont, for decimals).

### Soft rules

- Lead with the punchline if there is one. "Higher minimum wages
  raised employment in Hungarian retail by 4%" is better than
  saving the result for sentence 3.
- Active voice. "The authors track" not "12,000 firms are tracked".
- For Hungarian-context papers, the HU summary is primary; the EN
  is for the international reader. Don't shave Hungarian-specific
  detail out of the HU just because it doesn't translate cleanly.
- For non-Hungarian-context papers, lead the HU with "Az Egyesült
  Államokban …" / "Az Európai Unió 24 országában …" so the reader
  immediately knows the setting isn't Hungary.

## Inputs the skill needs

For each target item:

1. The catalogue JSON (read it — gives title, authors, journal,
   year, abstract, current state of fields).
2. The paper / policy abstract or full text. Sources, in order of
   preference:
   - `abstract` field already in the JSON
   - `url_published` → fetch DOI page
   - `url_pdf` → fetch PDF and run `pdf` skill to extract text
   - For BI / Bruegel / KRTK reports without abstracts: fetch the
     publication page; if there's only a press release, draft from
     that and flag in NOTES that the source was thin.

If neither abstract nor accessible PDF exists, halt and ask the
editor for one — drafting from the title alone produces hallucination.

## Workflow

### Single-item mode

Triggered by: a specific slug or "draft this paper". Produces one
JSON file at `scripts/drafts_<slug>.json` and previews the content
inline before writing.

### Batch mode

Triggered by: an author slug ("draft Adamecz's policy items"), a
TODO category from the handover ("first drafts for the 35 metadata-
fetched policy items"), or an explicit list.

For batch mode:

1. Pull the list of target slugs (filter by `review_status:
   metadata-fetched` or by missing field, depending on intent).
2. Cap at 10 items per batch. If the user's request exceeds 10,
   announce the batch boundary and process the first 10. The
   editor reviews + applies, then asks for the next batch.
3. Output one JSON file at `scripts/drafts_<batch-tag>_<date>.json`.

### Hungarian-only mode (translation)

Triggered by: "translate X to Hungarian", "HU drafts for Y", or
when the EN draft already exists and HU is missing.

For HU-only:

1. Read the existing `summary_en`, `data_used`, `policy_relevance`.
2. Write `summary_hu`, `data_used_hu`, `policy_relevance_hu`
   following the soft rule above (idiomatic, not literal).
3. Output JSON in the `apply_summaries_hu.py` format:
   ```json
   {
     "<paper-slug>": {
       "summary_hu": "...",
       "data_used_hu": "...",
       "policy_relevance_hu": "..."
     }
   }
   ```

## Output JSON formats

### For research papers (matches `scripts/apply_drafts.py`)

```json
{
  "<paper-slug>": {
    "summary_en": "...",
    "data_used": "...",
    "policy_relevance": "...",
    "topics": ["trade-fdi", "firms-productivity"],
    "methods": ["diff-in-diff", "panel-data"],
    "data_types": ["admin-firm"],
    "countries_studied": ["HU"]
  }
}
```

The skill should populate `topics`, `methods`, `data_types`,
`countries_studied` only if confident. Wrong tags are worse than
empty arrays.

### For policy items

Same shape as papers, minus `methods` / `data_types` (policy items
don't carry those). Include `policy_relevance` (required by SPEC
§2.6) — never leave a policy item without it.

### For HU-only translations

See "Hungarian-only mode" above.

## Apply step

Default is dry-run: write the JSON, print a preview, ask the editor
to approve before running the apply script.

When the editor says "apply" / "go ahead":

```bash
# for EN drafts on papers
python scripts/apply_drafts.py scripts/drafts_<batch>.json

# for HU translations (papers, policy)
python scripts/apply_summaries_hu.py scripts/drafts_<batch>_hu.json
```

For policy items, there's no dedicated apply script as of
2026-04-25 — extend `apply_drafts.py` or write the JSON straight to
`data/policy/<slug>.json` field-by-field. Note this in the response
so the editor can decide which path.

After apply, print a one-line summary: `Applied N drafts to
<targets>; review_status set to ai-drafted; last_reviewed_at set
to <today>.`

## Stopping rules

- 10 items per batch, hard cap.
- If a paper's abstract is unavailable from any source, skip it
  with a flag rather than fabricating.
- If `topics` / `methods` are unclear from the abstract, leave
  empty in the JSON — `apply_drafts.py` validates against the
  controlled vocabulary and will reject invalid tags anyway.
- Never write a draft that's <50 words for a 80–150-word target.
  Better to flag the source as too thin and ask for more.

## What this skill does NOT do

- Author photos, bios, or any author-level field — that's
  `research-author`.
- Auditing existing drafts for quality — that's an editor task.
- Verify the paper exists / verify the author is Hungarian — those
  are `hu-econ-verifier` (Check 1 / Check 2).
- Translate existing English Press item titles — editor deferred
  that ("option b") in 2026-04-25.

## Examples

### Single paper, full draft

> "Draft summaries for `koszegi-2006-qje-reference-points`."

Process: read JSON → read abstract → write EN summary, data_used,
policy_relevance → write HU twins → output one-paper JSON to
`scripts/drafts_koszegi-2006-qje.json` → preview inline → wait
for "apply".

### Author batch, EN drafts only

> "Draft Adamecz's 10 BI briefs."

Process: list `data/policy/adamecz-*.json` where
`review_status=metadata-fetched` → fetch each BI PDF (most have
public PDFs per handover) → draft EN `summary_en` and
`policy_relevance` for each → output to
`scripts/drafts_adamecz_policy_<date>.json` → preview the first
two inline, summarise the rest as a list of word counts → wait
for approval.

### HU translations, batch

> "HU drafts for the 16 Köszegi papers."

Process: list `data/papers/koszegi-*.json` where `summary_en` is
non-null and `summary_hu` is null → write HU twins for each → output
to `scripts/summaries_hu_koszegi_<date>.json` → preview two →
wait for `apply_summaries_hu.py` approval.
