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

The summary fields are the entire content product. A senior policy
advisor should read the EN summary in 30 seconds and know whether this
is relevant to their dossier; a Hungarian journalist should read the
HU and know whether to email the author. Drafts written without that
bar in mind are noise.

## What this skill drafts

| Target          | Fields drafted                                                    |
|-----------------|--------------------------------------------------------------------|
| `data/papers/`  | summary_en, summary_hu, data_used, data_used_hu, policy_relevance, policy_relevance_hu |
| `data/policy/`  | summary_en, summary_hu, policy_relevance, policy_relevance_hu      |
| `data/press/`   | only `title_hu` for HU-origin items missing it (no summary fields per SPEC §2.7) |

## Content contract (from SPEC §5)

| Field                | Length              | Answers                                                       |
|----------------------|---------------------|---------------------------------------------------------------|
| `summary_*`          | 80–150 words, 2–3 sentences | What question did the paper ask, and what did they find? |
| `data_used`          | 40–80 words         | What data, from where, what scale, what years?                |
| `policy_relevance`   | 60–120 words        | What should a Hungarian policymaker take from this?           |

### Hard rules

- **No jargon.** If a term must appear, define it in parentheses on
  first use. "RDD (regression discontinuity)" the first time, then
  "RDD" thereafter.
- **Name the country.** Open with the setting: "In Hungary, …" /
  "Across 24 EU countries, …" / "Using US firm data, …". Never start
  with "We find" — the reader doesn't know who "we" is.
- **Effect sizes with units.** "8% increase in employment", not
  "a positive effect on employment". "€450/month wage gap", not
  "a sizable wage gap".
- **Concrete data lines.** `data_used` is the trust signal: source
  agency, sample size, time window, unit of analysis. "NAV corporate
  tax filings 2010–2020, ~85,000 firms, annual panel" — not "rich
  administrative data".
- **Specific policy reader.** `policy_relevance` should name *who*
  uses it (ministry, agency) and *how* (program design, target
  population, instrument). External-validity caveats on non-HU
  papers go here.
- **Never copy the abstract.** Paraphrase entirely.
- **Hungarian is not a translation.** HU answers the same questions
  using idiomatic Hungarian, not literal English-to-Hungarian.
  Hungarian academic register, vessző (not pont) for decimals.

### Soft rules

- Lead with the punchline. "Higher minimum wages raised employment in
  Hungarian retail by 4%" beats saving the result for sentence 3.
- Active voice. "The authors track" not "12,000 firms are tracked".
- For Hungarian-context papers, the HU summary is primary. Don't shave
  Hungarian-specific detail just because it doesn't translate cleanly.
- For non-Hungarian-context papers, lead the HU with "Az Egyesült
  Államokban …" / "Az Európai Unió 24 országában …" so the reader
  knows the setting isn't Hungary.

## Inputs

For each target item:

1. The catalogue JSON (read it — gives title, authors, journal, year,
   abstract, current state of fields).
2. The abstract or full text. Sources, in order of preference:
   - `abstract` field already in the JSON
   - `url_published` → fetch DOI page
   - `url_pdf` → fetch PDF and run `pdf` skill to extract text
   - For BI / Bruegel / KRTK reports without abstracts: fetch the
     publication page; if there's only a press release, draft from
     that and flag in NOTES that the source was thin.

If neither abstract nor accessible PDF exists, halt and ask the editor.
Drafting from the title alone produces hallucination.

## Modes

### Single-item

Trigger: a specific slug or "draft this paper". Produces one JSON file
at `scripts/drafts_<slug>.json` and previews inline.

### Batch

Trigger: an author slug ("draft Adamecz's policy items"), a category
from the handover, or an explicit list.

1. Pull the target slug list (filter by `review_status:
   metadata-fetched` or by missing field).
2. Cap at 10 per batch. Beyond that, announce the boundary, process
   the first 10, wait for approval, continue.
3. Output one JSON at `scripts/drafts_<batch-tag>_<date>.json`.

### HU-only (translation)

Trigger: "translate X to Hungarian", "HU drafts for Y", or when EN
exists and HU is missing.

1. Read the existing `summary_en`, `data_used`, `policy_relevance`.
2. Write `summary_hu`, `data_used_hu`, `policy_relevance_hu`
   (idiomatic, not literal — see soft rules).
3. Output JSON for `apply_summaries_hu.py`:
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

### Research papers (matches `scripts/apply_drafts.py`)

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

Populate `topics`, `methods`, `data_types`, `countries_studied` only
if confident. Wrong tags are worse than empty arrays.

### Policy items

Same shape as papers, minus `methods` / `data_types`. `policy_relevance`
is required (SPEC §2.6) — never leave a policy item without it.

## Apply

Default is dry-run: write the JSON, print a preview, ask for approval.

When the editor says "apply" / "go ahead":

```bash
# EN drafts on papers
python scripts/apply_drafts.py scripts/drafts_<batch>.json

# HU translations (papers, policy)
python scripts/apply_summaries_hu.py scripts/drafts_<batch>_hu.json
```

For policy items, no dedicated apply script exists yet — extend
`apply_drafts.py` or write directly to `data/policy/<slug>.json`.
Note this in the response so the editor can decide.

After apply: print one line — `Applied N drafts to <targets>;
review_status set to ai-drafted; last_reviewed_at set to <today>`.

## Stopping rules

- 10 items per batch, hard cap.
- If a paper's abstract is unavailable, skip with a flag rather than
  fabricating.
- If `topics` / `methods` are unclear, leave empty — `apply_drafts.py`
  validates against the controlled vocabulary and rejects invalid tags.
- Never write a draft <50 words for an 80–150 word target. Flag the
  source as too thin instead.

## Out of scope

- Author photos, bios, any author-level field — `research-author`.
- Auditing draft quality — editor task.
- Eligibility / paper-existence checks — `hu-econ-verifier`.
- HU titles for EN-origin Press items (deferred per editor preference).

## Examples

### Single paper

> "Draft summaries for `koszegi-2006-qje-reference-points`."

Read JSON → read abstract → write EN summary, data_used,
policy_relevance → write HU twins → output to
`scripts/drafts_koszegi-2006-qje.json` → preview → wait for "apply".

### Author batch, EN drafts

> "Draft Adamecz's 10 BI briefs."

List `data/policy/adamecz-*.json` with `review_status=metadata-fetched`
→ fetch each BI PDF → draft EN `summary_en` and `policy_relevance` →
output to `scripts/drafts_adamecz_policy_<date>.json` → preview the
first two inline, summarise the rest as a list of word counts → wait.

### HU batch

> "HU drafts for the 16 Köszegi papers."

List `data/papers/koszegi-*.json` with `summary_en` non-null and
`summary_hu` null → write HU twins → output to
`scripts/summaries_hu_koszegi_<date>.json` → preview two → wait.
