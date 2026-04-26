# BI policy briefs — authorship audit, 2026-04-26

While starting drafting on the 10 BI policy briefs filed under
`adamecz-anna` (per the 2026-04-25 handover's day-1 priority), I
found that most of them are not actually Adamecz's papers. The
slug pattern `adamecz-bi-*` was used as a convenient prefix during
ingest, but the PDF bylines tell a different story.

This file documents what I found. **No metadata fix has been
applied to the 9 affected items yet** — they need editor
sign-off, since several name authors who aren't currently in the
catalogue. The one clear single-author case (Simonovits's pension
paper) has been re-attributed and drafted; see commit `6b96d17`.

## Per-item findings

| Slug | Title | PDF byline | In catalogue? | Action |
|---|---|---|---|---|
| `adamecz-bi-pension-ageing` | Population ageing and strengthened progressivity of pensions: the case of Hungary | András Simonovits (sole author, BME) | YES | **Done** — renamed to `simonovits-2025-bi-pension-ageing`, drafted |
| `adamecz-2018-bi-admindata` | Using administrative data to improve policy making in the CEE | Ágota Scharle (sole author per colophon) | NO | flag |
| `adamecz-2020-bi-youth-outreach` | Impact of increased local cooperation on PES outreach to non-employed youths in Hungary | Márton Csillag and Ágota Scharle | NO (both) | flag |
| `adamecz-bi-neet-outreach` | How can Public Employment Services act to reach NEETs? | Márton Csillag and Ágota Scharle | NO (both) | flag |
| `adamecz-bi-homelessness-cee` | Ending homelessness in CEE — comparative report | Hegedüs, Somogyi (E.), Scharle, Teller, Váradi, Vass-Vígh | NO (all) | flag |
| `adamecz-bi-homelessness-hungary` | Ending homelessness in CEE — Hungary brief | (paired with CEE — same authors implied) | NO | flag |
| `adamecz-2011-bi-rehab` | The efficiency of employment rehabilitation subsidies in Hungary | (no PDF byline; brief references "Scharle, Ágota (2011)" as the underlying research) | Scharle: NO | flag — likely Scharle |
| `adamecz-2014-bi-ltu` | True and false remedies for long-term unemployment in Visegrad countries | (no PDF byline visible) | — | flag — author unknown |
| `adamecz-2021-bi-youth-employment` | Policy lessons from the evaluation of youth employment policies in Spain, Hungary, Italy and Poland | (institutional brief, no clear byline; same project as the youth-outreach pieces by Csillag + Scharle) | NO | flag — likely Csillag + Scharle |
| `adamecz-2022-bi-eu-funds` | Access to and quality of public data on EU fund allocations | (no PDF byline visible; project commissioned by Hungarian Helsinki Committee, 2022) | — | flag — likely Váradi or other BI staff |

So of the original 10 items:
- **1** correctly re-attributable (Simonovits, single author, in catalogue) — done.
- **5** have explicit PDF bylines naming authors not in the catalogue (Scharle x4, Csillag x2, Hegedüs et al. x1).
- **3** have no byline visible but the project context strongly suggests the same authors as their siblings (Scharle / Csillag).
- **1** (`adamecz-2014-bi-ltu`) genuinely unclear — needs the editor or a deeper PDF read.

## Why this matters

Drafting `summary_en` / `policy_relevance` for an item filed under the
wrong author would attach policy commentary to that author's public
page on the site. For Adamecz, that means visitors to her
`/authors/adamecz-anna/` page would read summaries of work she didn't
write — potentially including Simonovits's pension theory and
Hegedüs's homelessness reports, which are far outside her research
area.

## Editor decisions needed

### Q1 — Admit the BI authors as catalogue authors?

Per SPEC §1.2 (AND admission rule, just tightened):

- **Ágota Scharle** — runs Budapest Institute. Has academic
  publications (IZA WPs, journal articles) but I'd need to verify
  ≥1 Tier A/B + ≥3 EN articles. Likely passes.
- **Márton Csillag** — BI senior researcher. Same check needed.
- **József Hegedüs** — Metropolitan Research Institute, housing
  economics. Long publication record but mostly in the
  housing/urban-policy literature; Tier A/B status uncertain.
- **Eszter Somogyi (MRI)** — note: distinct from Róbert Somogyi
  who's already in the catalogue. Different person, different field.
- **Nóra Teller** — MRI, housing.
- **Balázs Váradi** — BI, often co-author on infrastructure /
  governance briefs.
- **Veronika Vass-Vígh** — BI.

Recommendation: run `research-author` for each, see who passes the
new AND rule.

### Q2 — How to handle the misattributed items meanwhile?

Three options:

- **(a)** Leave the 9 items in `data/policy/` filed under
  `adamecz-anna`, set their `review_status: needs-author-fix`, and
  exclude them from her public page until fixed. (Defensive.)
- **(b)** Move them out of `data/policy/` into a quarantine folder
  (e.g., `data/policy/_pending/`) so build.py doesn't surface them.
  (Cleaner, but invents a new convention.)
- **(c)** Rename slugs to `bi-<topic>-<year>` (no author prefix) and
  keep `authors: []` until editor confirms admissions. The build
  pipeline currently requires non-empty authors though — needs a
  small change.

My recommendation is **(a) with `needs-author-fix`** as the
shortest-path fix. The pages will simply not render until the
authors are sorted, and the file paths stay stable for re-attribution.

### Q3 — Slug renaming convention

When the actual authors are admitted, slugs should presumably move
from `adamecz-bi-X` to `<surname>-<year>-bi-X` (matching the pattern
already used for press items: `simonovits-2024-portfolio-...`).
Confirm before doing it as a bulk operation.

## What's already been done

Commit `6b96d17`:
- `adamecz-bi-pension-ageing.json` deleted
- `simonovits-2025-bi-pension-ageing.json` created with full draft
  (summary_en, summary_hu, policy_relevance, policy_relevance_hu,
  topics, countries_studied, policy_instruments)

## What I'm not doing in this session

- Touching the 9 misattributed items beyond this flag note. Re-
  attribution requires editor sign-off on author admissions.
- Drafting summaries for any of them. Cannot draft until the
  author attribution is correct.
- Researching the BI authors for catalogue admission. That's a
  `research-author` task per author; deferred until the editor
  decides whether to admit them.

## Pivot

For drafting work, moved on to Csóka's 4 abstract-available papers
in commit `6b96d17`, and continuing with other unblocked authors
in subsequent commits (Ambrus, Bíró A., Berlinger HU translations).
