# Content stocktake — 2026-05-09

Goal: write `summary_en`, `data_used`, `policy_relevance` for all econ
papers that don't yet have them, with extra care on Hungarian-relevant work.
Hungarian summaries are explicitly out of scope this round.

## Scope

| | count |
|---|---|
| Total papers in `data/papers/` | **807** |
| Excluded: pol-sci / OR-math journals | 26 |
| **Econ papers in scope** | **781** |

**Excluded journals** (pure math / OR / political science — not econ):
APSR, QJPS, *J. Theoretical Politics*, *Mathematics of OR*,
*Mathematical Programming*, *European J. Operational Research*,
*OR Letters*, *Annals of OR*, *Central Eur. J. of OR*,
*Mathematical Social Sciences*, *J. of Mathematical Economics*,
*Statistics and Computing*. (26 papers total — mostly cooperative
game theory, matching algorithms, and OR. If you want any of these
treated as econ — e.g., the J. Math. Econ. or boundary EJOR pieces —
say so.)

## Coverage of the three policymaker-facing fields

`summary_en`, `data_used`, and `policy_relevance` are co-present —
when a paper has one, it has all three (drafts are written as a unit).

| | papers | % of 781 |
|---|---|---|
| Fully drafted (all three) | **678** | 86.8 % |
| **Missing all three** | **103** | 13.2 % |

So 103 econ papers need a draft.

## Breakdown of the 103 missing

| | papers | what to do |
|---|---|---|
| With abstract on file | **12** | draft straight from abstract — quick win |
| Without abstract | **91** | need to find PDF / WP / OpenAlex / Scholar first |

### By publication type
- 90 articles
- 11 chapters (Edward Elgar, Cambridge UP, Contributions to Econ.,
  Understanding Complex Systems — these tend to lack abstracts in OpenAlex)
- 2 working papers

### By topic
- 79 have **no `topics`** assigned (so they're invisible on topic pages too)
- The 24 that do have topics fall into: banking-finance (8),
  mechanism-design (8), firms-productivity (6), industrial-organization (5),
  macroeconomics (5), regional-urban (4), methods (4), behavioral (3),
  others (singles).

### By journal — the 91 hard cases (no abstract, no summary)

Concentrated in journals OpenAlex doesn't index well:
- *Közgazdasági Szemle* (6) — Hungarian-language, the 6 are all
  Berlinger / Megyeri pieces; PDFs available on `kszemle.hu`.
- *Games and Economic Behavior* (5)
- *International Journal of Game Theory* (4)
- *Journal of Economic Theory* (3), *IJIO* (3)
- 5 papers with `journal: null` — working papers without metadata.
- The rest is long tail (1–2 each across many outlets).

### Concentration by lead author

| author | missing | notes |
|---|---|---|
| berlinger-edina | 13 | finance / student-loan models; many in *Közgazdasági Szemle* and HU finance journals — likely all gettable |
| tobias-aron | 5 | mechanism-design / pure theory |
| eso-peter | 4 | auction theory |
| elekes-zoltan | 3 | regional / network / labour-flow papers — should have abstracts on author site |
| lorincz-laszlo, abraham-arpad, benczur-peter, halpern-laszlo, konya-istvan, szentes-balazs, telegdy-almos, vonyo-tamas | 2 each | mixed |
| ~50 authors | 1 each | the long tail |

(Berlinger alone is 13 % of the gap. Doing her queue first is the
single highest-leverage move.)

## Hungarian-relevant subset

Defined as: `countries_studied` includes `HU`, **or** "hungary"/"hungar"
appears in title / abstract / `data_used`.

| | papers |
|---|---|
| HU-relevant in scope | **203** |
| HU-relevant fully drafted | 194 |
| **HU-relevant missing draft** | **9** |

### The 9 HU papers needing drafts

1. `benczur-simon-et-al-2006-jopm` — *J. Policy Modeling*, "Social costs of consumer impatience in Hungary"
2. `berlinger-walter-2015-acta` — *Acta Oeconomica*, "Income Contingent Repayment Scheme for Non-Performing Mortgage Loans in Hungary"
3. `dobrinsky-korosi-et-al-2006-joce` — *JCE*, "Price markups and returns to scale in imperfect markets: Bulgaria and Hungary"
4. `horn-keller-et-al-2016-eepe` — Edward Elgar chapter, "Early tracking and competition — A recipe for major inequalities in Hungary"
5. `kertesi-koll-2002-rile` — *Research in Labor Economics*, "Economic transformation and the revaluation of human capital — Hungary, 1986–1999"
6. `koltai-lorincz-et-al-2025-ans` — *Applied Network Science*, "Do diversity and context collapse kill an online social network?" (uses iWiW Hungarian data)
7. `lorincz-koltai-et-al-2019-socnet` — *Social Networks*, "Collapse of an online social network: Burning social capital to create it?" (iWiW)
8. `ongena-schindele-vonnak-2018-jimf` — *JIMF*, "Why do firms default on their foreign currency loans? The case of Hungary"
9. `telegdy-2011-eepe` — Edward Elgar chapter, "Corporate governance and the structure of ownership of Hungarian corporations"

Of these 9: items 6 and 7 already have abstracts (easy). Items 4 and 9
are book chapters (probably need to consult the volume itself).
Items 1, 2, 3, 5, 8 are journal articles — abstracts findable on
publisher site / RePEc / Acta archive.

## Easy 12 (have abstract, need draft only)

1. `ertl-2022-ksz` (Közgazdasági Szemle, behavioral, Hungarian)
2. `galasso-mitchell-et-al-2016-ijio` (patent buyouts)
3. `galasso-mitchell-et-al-2017-rp` (innovation prizes)
4. `gierlinger-laczo-2018-ej` (risk sharing)
5. `greulich-laczo-marcet-2023-jpe` (optimal capital/labor taxes)
6. `ilyes-boza-et-al-2023-joeg` (residential mobility)
7. `koltai-lorincz-et-al-2025-ans` (HU — iWiW)
8. `laczo-2015-jeea` (risk sharing structural)
9. `lorincz-chihaya-et-al-2020-ans` (skills networks)
10. `lorincz-koltai-et-al-2019-socnet` (HU — iWiW)
11. `telegdy-2011-eepe` (HU — corporate governance, chapter)
12. `vonyo-2018-cupe` (post-war German export boom, history chapter)

## Plan if you give a green light

1. Draft the **12 easy** (abstract on file) — fastest, all in one pass.
2. Draft the **9 Hungarian** that aren't in #1 — top policy priority.
3. Work the **berlinger-edina queue (13)** — concentrated, mostly findable
   on `kszemle.hu` and the author's CEU page.
4. Sweep the rest of the 91 by author, prioritising those with public PDFs
   (RePEc / author website / SSRN / NBER WP versions). Use working-paper
   text where the journal is gated.
5. Anything I cannot find or cannot read goes in a **choke-points list**
   in `audit-content-chokepoints-2026-05-09.md` rather than guessing.

## Files written this pass

- `audit-content-2026-05-09.json` — per-paper machine-readable audit
  (every paper's status across the four fields, plus DOI/URL).
- `audit-content-hardlist-2026-05-09.txt` — the 91 no-abstract papers
  grouped by lead author for fast triage.
- `audit-content-2026-05-09.md` — this file (human-readable summary).
