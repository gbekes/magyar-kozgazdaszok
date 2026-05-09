# Journal whitelist redesign — running notes

Status: open. Target: tighten the qualifying list from the current 54
hand-curated entries to roughly **100–150 journals**, picked by a public
ranking we can defend.

## Why we're doing this

The current `journals.json` has 54 entries (19 tier A + 35 tier B). It was
hand-built and is too narrow: many journals where catalogued authors
actually publish are absent (Economics Letters, GEB, Finance Research
Letters, EJOR, JEBO, JBF, World Development, Energy Economics, Small
Business Economics, etc. — none of them whitelisted).

We want a single ranking source we can sort by, set a cutoff on, and re-run
mechanically as journals get added or rebrand.

## What's in the catalogue today

- 209 distinct journals across all `data/papers/*.json`
- Already pulled per-journal stats from OpenAlex into
  `data/journal-rankings.json` (h-index, 2yr_mean_citedness, ISSN, country,
  publisher, OpenAlex source ID). 200 of 209 matched on first pass.

## Metric options considered

| Source | Metric | Free? | Programmatic? | Notes |
|---|---|---|---|---|
| OpenAlex | `h_index`, `2yr_mean_citedness` | Yes | **Yes** | What's loaded today. `2yr_mean_citedness` is mathematically the JIF formula (citations to last-2yr articles / articles). H-index is durable but rewards age. |
| Scopus / Elsevier | **CiteScore** | Yes | One-click manual download | Probably the best fit. Excel published annually at https://www.scopus.com/sources or https://www.elsevier.com/researcher/page/scopus-citescore-metrics. Has CiteScore + CiteScore Percentile (field-normalized) + ISSN. Cloudflare-protected for scraping; user downloads once, we match by ISSN. |
| Scopus | SNIP | Yes | Same CSV as CiteScore | Source-normalized impact per paper. Field-normalized, like CiteScore Percentile. |
| Clarivate / Web of Science | **JIF**, 5-yr JIF, JCI | **Paid** | Subscription only | Brand-name metric but not freely available. Skip unless we have JCR access. |
| Scimago | SJR, Quartile | Yes | Browser download only (Cloudflare blocks programmatic) | Same workflow as CiteScore. SJR is well-known but more econ-light coverage than CiteScore. |
| ABS / Academic Journal Guide | 4* / 4 / 3 / 2 / 1 | Yes (after free signup) | No bulk CSV | Widely cited in business schools but list circulates as PDF. |
| RePEc / IDEAS | Aggregate ranking | Yes | Yes (`ideas.repec.org/top/`) | Econ-only. Has its own ranking based on citations within RePEc. Good for cross-check but narrow. |

## Trade-offs we walked through

- **JIF vs CiteScore**: same idea, different windows (2yr vs 4yr) and different citation universes (WoS vs Scopus). CiteScore covers more journals (28k vs 12k) and is free. CiteScore Percentile is the cleanest field-normalized number for a public-facing page.
- **OpenAlex 2yr_mean_citedness**: mathematically equivalent to JIF, but lacks the brand recognition. Fine if internal; weaker as a public-facing label.
- **Combined-metric rules**: rules of the form "h>X OR 2yr>Y" reward both age and recent activity. Tested several variants; the cleanest tightening was `(h>75 AND 2y>1.0) OR h>150` — required both stature and recent activity, with a safety net for elite journals where 2yr can dip.

## Rule iterations explored

| Rule | Journals | Catalogue papers covered |
|---|---:|---:|
| current proposal: `h>70 OR 2y>1.5` + HUN3 | 174 | 702 |
| `h>75 OR 2y>1.5` + HUN3 | 171 | 695 |
| `h>80 OR 2y>1.5` + HUN3 | 169 | 693 |
| `h>70 OR 2y>2.0` + HUN3 | 170 | 698 |
| `h>80 OR 2y>2.0` + HUN3 | 162 | 683 |
| `h>100 OR 2y>2.0` + HUN3 | 151 | 649 |
| `(h>75 AND 2y>1.0) OR h>150` + HUN3 | 153 | 657 |
| User's last proposal: `HUN3 OR h>=70 OR 2yr>2 OR (50<h<70 AND 1.5<=2yr<=2)` | 172 | — |

`HUN3` = `{Közgazdasági Szemle, Szigma, Külgazdaság}` — explicit Hungarian carve-out.

To get into the 100–150 range with OpenAlex metrics, the cuts were
something like `h>100 OR 2y>2.0` (151 journals). Cleaner with CiteScore
Percentile if we adopt it (e.g. "top 25% in econ-finance area").

## Open data quality issue: journal renames

OpenAlex (and Scopus, and any source) sometimes splits a journal across
the rename. Concrete cases that came up:

- **Economics of Transition** → renamed to **Economics of Transition and Institutional Change** in 2018. OpenAlex has the old name with cumulative h=83, 2yr=0.00 (no recent papers under that title); the new name has h=19, 2yr=1.06. Issue link: https://onlinelibrary.wiley.com/journal/25776983 (ISSN 2577-6983).
- **Review of Finance** — formerly **European Finance Review** (renamed 2004). OpenAlex still indexes the legacy name with h=127.
- **Journal of Economic Behavior & Organization** — whitelist entry uses "and"; OpenAlex uses "&". Same journal.

Fix planned regardless of metric: a `data/journal-aliases.json` file mapping
each "wrong-name" → "canonical name" so the ranking lookup picks the right
record. ISSN-based matching (which we'll get from CiteScore) avoids this
class of error entirely.

## Next steps (when we pick this back up)

1. **Editor decides ranking source.** Probably CiteScore. If yes, manually
   download the latest CiteScore Metrics .xlsx from Elsevier and drop it in
   `data/external/citescore-metrics.xlsx`.
2. **Build alias map** for journal renames so legacy name → current
   ranking entry. Fixes the Economics of Transition / Review of Finance
   class of bug.
3. **Re-run cutoff analysis** with the chosen metric (e.g. "CiteScore
   Percentile ≥ 75 in Econ-Finance subject area, OR HUN3"). Aim ≈100–150
   journals.
4. **Update `journals.json`** with `{name, issn_l, citescore, percentile,
   tier}` per qualifying journal. Tier becomes derived from percentile, not
   hand-assigned.
5. **Update `journals.html`** to display the metric next to each entry,
   sortable.
6. **Re-run admission audit** on all 90 authors against the new whitelist,
   flag any who'd no longer qualify.

## Tooling already in place

- `scripts/fetch_journal_rankings.py` — pulls OpenAlex source-level data
  for every journal in the catalogue. Idempotent; `--no-refresh` skips
  already-fetched entries.
- `scripts/journal_ranking_report.py` — writes
  `pdf-lists/journal-ranking-report.md` with the cutoff-suggestion table
  and full list sorted by h-index.
- `data/journal-rankings.json` — current ranking data (OpenAlex-based).
- `pdf-lists/journal-ranking-report.md` — last computed report.

When we resume: pick the metric, run the alias map, regenerate.
