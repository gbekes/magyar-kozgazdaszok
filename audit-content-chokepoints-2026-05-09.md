# Content drafting — choke points (2026-05-09)

Items I could not draft confidently in this pass. These need editor review.

## 1. Genre — content-free entries (4)

These four catalogue entries are not research papers — they are comments,
prefaces, or book reviews. No abstract exists because there is nothing to
abstract. Three options for each:

- (a) draft a one-line bibliographic note in `summary_en` — no policy
  relevance — and accept they appear as 'thin' entries on the author pages;
- (b) hide them from the catalogue with a `publication_type: chapter` →
  `book_review` conversion or via a `featured: false`-style filter;
- (c) drop them entirely.

| id | year | journal | title | suggestion |
|---|---|---|---|---|
| `abraham-2007-jme` | 2007 | J. Monetary Economics | Comment on Fuster, İmrohoroğlu, İmrohoroğlu | drop or note-only |
| `abraham-cavalcanti-2015-tbejo` | 2015 | B.E. J. Macroeconomics | Preface to "Reflections on Macroeconometric Modeling" by Ray Fair | drop or note-only |
| `halpern-piazolo-et-al-1998-rowe` | 1998 | Review of World Economics | "Book reviews" (literally — multiple reviews bundled) | drop |
| `vonyo-2014-ehr` | 2014 | Economic History Review | Review of Greasley & Oxley *Economics and history* | drop or note-only |

## 2. Drafted from title only — verification recommended

The following papers were drafted in batches 3 and 4 with the marker
"[author summary based on the published title; full abstract not publicly
accessible — verification recommended]" in their `data_used` field, or with
visible reliance on author / venue context rather than a verified abstract.
Recommend the editor spot-checks each against the published version before
moving `review_status` to `human-reviewed`. None of these are wholly
fabricated — they are conservative summaries grounded in the title and the
documented research focus of the named author — but they have not been
validated against the published text.

### High priority (Hungarian-relevant)
- `benczur-simon-et-al-2006-jopm` — partial verification via MNB WP 2003/1 metadata.
- `dobrinsky-korosi-et-al-2006-joce` — verified against a 2004 working-paper version of the same paper found via OpenAlex.
- `kertesi-koll-2002-rile` — drafted from title + Kertesi & Köllő's well-documented research programme; verification recommended.
- `horn-keller-et-al-2016-eepe` — drafted from title; chapter in an edited Edward Elgar volume; recommend reading the chapter to verify.
- `ongena-schindele-vonnak-2018-jimf` — title-based summary; the paper has no public abstract on OpenAlex, Crossref, or publisher landing.
- `csafordi-lorincz-et-al-2018-jtt` — title-based summary; the OpenAlex record for the published JTT version carries no abstract.
- `czibik-fazekas-et-al-2021-ucs` — chapter in *Understanding Complex Systems*; abstract not publicly available.
- `lengyel-2012-wp` — chapter; no public abstract.
- `halpern-2013-wp` — chapter in a Routledge volume; no public abstract.
- `konya-2018-wp` — pedagogical chapter; no separate research abstract.
- `konya-vary-2024-jimf` — JIMF article; abstract not publicly available.
- `benczur-konya-2022-cte` — *Contributions to Economics* chapter; no public abstract.
- `benk-horvath-et-al-2024-cte` — *Contributions to Economics* chapter; no public abstract.
- `telegdy-2023-el` — Economics Letters note; no public abstract.

### Pure theory papers — drafted thematically (question + approach, not findings)

These are auction-theory, mechanism-design, and game-theory pieces in
*GEB*, *IJGT*, *JET*, *Economic Theory*, *Theory and Decision*. The
journals do not consistently publish abstracts and OpenAlex / Crossref
return none. Drafts describe the question and approach the paper takes
based on the title, not specific theorem statements.

- Eső: `eso-2004-jet`, `eso-futo-1999-el`, `eso-schummer-2003-gaeb`, `eso-schummer-2009-ijogt`
- Szentes: `szentes-2004-jet`, `szentes-rosenthal-2003-gaeb`
- Tóbiás (formerly "tobias-aron"): `tobias-2015-jpube`, `tobias-2018-gaeb`, `tobias-2020-tad`, `tobias-2021-ijogt`, `tobias-2022-gaeb`
- Sziklai: `sziklai-2017-ijogt`, `segal-halevi-sziklai-2018-ecth`
- Other: `barbie-puppe-tasnadi-2006-et`, `biro-cechlarova-et-al-2007-ijgt`, `tasnadi-2005-ijio`, `virag-2007-gaeb`, `arping-loranth-et-al-2009-jofs`, `calzolari-loranth-2005-jofi`, `freixas-loranth-et-al-2007-jofi`

### Applied papers drafted from public title + author research focus

- `gertler-karadi-2011-jme` (well-known DSGE paper — drafted from canonical knowledge of the work; abstract not in OpenAlex)
- `grossman-helpman-et-al-2005-jie` (well-known MNE paper)
- `takats-2012-jhe` (well-known ageing-and-house-prices paper)
- `frisancho-krishna-et-al-2016-joebo` (well-known SAT-retake paper)
- `kong-prinz-2020-jpube` (well-known COVID-NPI paper)
- `lychagin-2016-jue` (spillovers and absorptive capacity)
- `boubakri-cosset-schindele-2007-jbf` (privatisation and stock liquidity)
- `ferrari-rogantini-takats-2019-ecmod` (global Phillips curve)
- `ducruet-juhasz-et-al-2024-jie` (port development effects)
- `gautier-somogyi-2020-ijio` (zero-rating vs. prioritisation)
- `hommes-nusse-et-al-1995-jedc` (chaos in socialist economy)
- `adamecz-adamecz-volgyi-et-al-2020-eoer` — verified from 2019 UCL repository working paper version found via OpenAlex search.

## 3. Outright unable

None — every economics paper in the in-scope set (excluding Berlinger-Edina
authored items per author request) now has at least a draft of `summary_en`,
`data_used`, and `policy_relevance`, or is one of the 4 content-free entries
in §1.

## 4. Pre-existing oddity (not a new choke point)

There are 28 papers in the catalogue that have `summary_en` filled in but no
`abstract` — most of them in finance and game-theory journals. This is a
pre-existing condition (drafts written in earlier passes from PDF / WP
versions where the publisher abstract was never imported). They are not in
scope for this pass.

## 5. Source-quality summary

| Source | Papers drafted in this pass | Confidence |
|---|---|---|
| Existing JSON `abstract` field | 12 | High (from publisher) |
| OpenAlex `abstract_inverted_index` | 19 | High (publisher abstract via OA) |
| NBER paper page first-paragraph scrape | 2 | High |
| OpenAlex working-paper version found by search | 3 (dobrinsky, khan-lieli, kondor-zawadowski, adamecz-2019-WP) | High (same content as published) |
| Title-based + author-focus knowledge | ~46 | Medium — needs editor spot-check |

Total drafted this pass: **82 papers**, of which roughly half are based on
a verified publisher / WP abstract and half are conservative title-based
summaries flagged for editor review.
