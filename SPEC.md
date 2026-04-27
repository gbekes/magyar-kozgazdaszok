# SPEC — Evidence for Hungary

The technical spec. Read `README.md` first for vision.

---

## 1. Inclusion criteria

### 1.1 Who counts as a "Hungarian economist"

An economist is eligible if **at least one** of the following holds:

- Hungarian nationality (current or at time of publication)
- Born in Hungary
- Primary research affiliation at a Hungarian institution for ≥3 years (KRTK, CEU [including its Budapest-era alumni], Corvinus, ELTE, MNB Research, Debrecen, Szeged, Pécs, etc.)

Diaspora is explicitly included. An economist at MIT who was born in Szeged counts. An economist at CEU Vienna who is Austrian but has worked at KRTK for five years counts.

We do **not** require research on Hungary. A Hungarian trade economist studying Chinese firms is in.

### 1.2 The top-journal filter (qualifies the _author_)

An author is admitted if they have **at least one publication** in any journal on the list below. Once admitted, _all_ their published papers and recent (last 10 years) working papers are eligible for inclusion.

**Tier A — top general interest (the "top 5" + immediate peers):**
- American Economic Review
- Quarterly Journal of Economics
- Journal of Political Economy
- Econometrica
- Review of Economic Studies
- Journal of the European Economic Association
- American Economic Journal: Applied / Macro / Micro / Policy
- Economic Journal
- International Economic Review
- Review of Economics and Statistics
- Journal of Economic Perspectives
- Theoretical Economics
- AEA Papers and Proceedings

**Tier B — top field journals:**
- _Labor_: Journal of Labor Economics, Labour Economics, Journal of Human Resources
- _Trade / international_: Journal of International Economics, Review of International Economics
- _Finance_: Journal of Finance, Review of Financial Studies, Journal of Financial Economics, Review of Finance, Journal of International Money and Finance, Finance Research Letters, Journal of International Financial Markets Institutions & Money, Emerging Markets Review
- _Macro / monetary_: Journal of Monetary Economics, Journal of Money, Credit and Banking
- _IO_: RAND Journal of Economics, International Journal of Industrial Organization
- _Public_: Journal of Public Economics
- _Development_: Journal of Development Economics
- _Econometrics_: Journal of Econometrics, Journal of Business and Economic Statistics, Econometric Theory
- _Theory_: Journal of Economic Theory, Economic Theory
- _Management_: Management Science, Strategic Management Journal, Organization Science
- _Urban / regional_: Journal of Urban Economics, Regional Science and Urban Economics
- _Health_: Journal of Health Economics, Health Economics
- _Environment_: Journal of Environmental Economics and Management, Journal of the Association of Environmental and Resource Economists
- _Economic history_: Journal of Economic History, Explorations in Economic History, European Review of Economic History

Store the full list as `data/journals.json` so it is editable without code changes.

**Admission rule:** an author is admitted if **both** conditions hold:

- (i) at least one publication in a journal on the Tier A / Tier B list above, **and**
- (ii) at least **3 publications in international, peer-reviewed good journals** — i.e., journals that appear on `data/journals.json` (any tier), excluding `B-hu` (Hungarian-language outlets like *Közgazdasági Szemle* or *Acta Oeconomica*, which are domestic regardless of peer review).

Rationale: the top-journal criterion (i) signals that the author has cleared a high editorial bar at least once; the volume criterion (ii) signals a sustained record of internationally-refereed work in the field. Either alone is too easy — a single lucky placement isn't a research career, and three workshop-tier publications aren't recognisable as one. The two together require both peak quality and consistency. Once admitted, all of the author's peer-reviewed papers and recent working papers are eligible for the catalogue (filter later in the UI). The journal whitelist is a guide, not a gate — borderline admissions remain editorial decisions.

**Recent changes to this list:**
- 2026-04-27: Tightened condition (ii) from "3 peer-reviewed English articles in any econ/finance/mgmt journal" to "3 publications in international good journals (on `data/journals.json`, excluding `B-hu`)".
- 2026-04-26: Admission rule tightened from OR to AND — both (i) and (ii) now required (previously either was sufficient).
- Added to Tier A: International Economic Review, Review of Economics and Statistics, Journal of Economic Perspectives, Theoretical Economics, AEA Papers and Proceedings.
- Added to Tier B: Journal of Economic Theory and Economic Theory (new _Theory_ field); Review of Finance and Journal of International Money and Finance (finance).
- Removed: Journal of International Business Studies, World Development. (Review of Economic Dynamics is back on Tier B as of 2026-04-26.)

### 1.3 What papers to include for an admitted author

- All peer-reviewed articles in economics/finance journals (any tier)
- Working papers posted in last 10 years with a recognized series: NBER, CEPR, IZA, CESifo, SSRN (with identifiable version), arXiv (econ section), MNB Working Papers, KRTK Working Papers, and other institutional WP series of ministry / central-bank / university research groups
- Book chapters in academic volumes (include, but flag as `type: chapter`)
- **Excluded**: op-eds, blog posts, policy reports without abstract, popular books

Mark type with a `publication_type` field: `article | working_paper | chapter`. Let the UI filter.

---

## 2. Data model

Three primary entities: **Paper**, **Author**, **Topic**. Plus **Journal** and **Institution** as lookup tables.

### 2.1 Paper schema

```json
{
  "id": "bekes-halpern-kornai-kovacs-2023-jie",
  "title": "Foreign Firms and Domestic Employment",
  "authors": ["bekes-gabor", "halpern-laszlo", "kornai-julia", "kovacs-peter"],
  "publication_type": "article",
  "journal": "Journal of International Economics",
  "year": 2023,
  "volume": "142",
  "issue": "3",
  "pages": "103987",
  "doi": "10.1016/j.jinteco.2023.103987",
  "working_paper_series": null,
  "url_published": "https://doi.org/10.1016/j.jinteco.2023.103987",
  "url_pdf": "https://example.com/paper.pdf",
  "url_replication": "https://github.com/...",
  "abstract": "We study the effect of foreign ownership on domestic employment...",
  "summary_en": "When a foreign company buys a Hungarian firm, what happens to jobs? This paper tracks 12,000 firms over 15 years and finds that foreign-owned firms...",
  "summary_hu": "Amikor egy külföldi cég felvásárol egy magyar vállalatot, mi történik a munkahelyekkel? ...",
  "data_used": "Hungarian firm-level administrative data (NAV corporate tax filings) 2005–2020, linked to the Balance Sheet Register. ~12,000 firms, annual panel.",
  "data_used_hu": "Magyar vállalati szintű adminisztratív adatok (NAV) 2005–2020 ...",
  "policy_relevance": "Supports targeted FDI promotion over general subsidies. Foreign-acquired firms retained 94% of workers in the two years post-acquisition...",
  "policy_relevance_hu": "...",
  "topics": ["trade-fdi", "labor-markets", "firms-productivity"],
  "methods": ["diff-in-diff", "panel-data"],
  "countries_studied": ["HU"],
  "data_types": ["admin-firm", "admin-tax"],
  "policy_instruments": ["minimálbér", "FDI promotion (HIPA)"],
  "featured": false,
  "added_at": "2026-04-19",
  "last_reviewed_at": "2026-04-19",
  "review_status": "ai-drafted"
}
```

Required fields: `id`, `title`, `authors`, `publication_type`, `year`, `abstract`, `topics`.
Recommended: everything else. `review_status` ∈ `{ai-drafted, human-reviewed, author-approved}`.

`policy_instruments` is an **uncontrolled, free-text** array of 0 to 5 concrete
policy instruments / programs / levers the paper studies or directly informs.
This sits alongside the 15-topic controlled vocabulary and gives policymakers
a second way in — a policymaker can land on the paper because they typed
"minimálbér" into search, not just because they browsed the labor topic. Short
phrases, in whichever language makes sense for the paper's setting (Hungarian
terms for Hungarian-context papers; English for global/US-setting papers).
Not a replacement for `topics` — it's additive.

### 2.2 Author schema

```json
{
  "id": "bekes-gabor",
  "name_en": "Gábor Békés",
  "name_hu": "Békés Gábor",
  "affiliations": [
    {"name": "Central European University", "role": "Associate Professor", "start": 2017},
    {"name": "HUN-REN KRTK", "role": "Senior Research Fellow", "start": 2005},
    {"name": "CEPR", "role": "Research Fellow", "start": 2015}
  ],
  "website": "https://sites.google.com/view/bekesgabor/",
  "email": "bekesg@ceu.edu",
  "repec_id": "pbe115",
  "scholar_id": "zZGPBPsAAAAJ",
  "orcid": "0000-0001-XXXX-XXXX",
  "primary_fields": ["international-trade", "firms-productivity"],
  "bio_en": "Gábor Békés studies how firms interact with the global economy...",
  "bio_hu": "Békés Gábor a vállalatok globális gazdaságban való viselkedését kutatja...",
  "photo_url": null,
  "qualifying_publication": {
    "title": "...",
    "journal": "Journal of International Economics",
    "year": 2014
  },
  "deceased": false,
  "died": null,
  "open_to_media_en": false,
  "open_to_media_hu": false,
  "media_note": null
}
```

- `deceased` / `died`: gentle denote. When `deceased: true`, the author's
  name on the listing gets a small † and the detail header shows "(deceased YYYY)".
  `died` is the four-digit year; optional.
- `open_to_media_en` / `open_to_media_hu` / `media_note`: authors can opt
  in per language to signal they're open to interviews, op-eds, policy
  briefings. Default is off for both. The author page always shows a
  small "Open to media: EN · HU" row below Links; each language pill is
  bright/coloured when opted in and a thin grey when off. `media_note`
  is an optional scoping note (e.g., "interviews on labor economics,
  op-eds in HVG / Telex / Portfolio") and is shown under the row when
  at least one language is on. Only changed via a submission from the
  author.

### 2.3 Topic schema (static, curated — see `TAXONOMY.md`)

```json
{
  "id": "labor-markets",
  "name_en": "Labor markets and employment",
  "name_hu": "Munkaerőpiac és foglalkoztatás",
  "description_en": "Research on wages, employment, unemployment, job search, workplace training...",
  "description_hu": "...",
  "policy_framing_en": "Relevant to: employment policy, minimum wage, active labor market programs...",
  "policy_framing_hu": "...",
  "icon": "briefcase"
}
```

### 2.4 File layout

```
data/
  journals.json           # lookup: tier, full name, subfield
  institutions.json       # lookup
  authors/
    bekes-gabor.json
    koren-miklos.json
    ...
  papers/                 # academic research (whitelisted journals + qualifying WPs + academic chapters)
    bekes-halpern-kornai-kovacs-2023-jie.json
    koren-szeidl-2012-qje.json
    ...
  policy/                 # institutional reports / WPs / policy chapters
    bekes-koren-halpern-murakozy-2011-bruegel-bp15.json
    adamecz-2025-bi-disability.json
    ...
  press/                  # short-form: op-eds, columns, interviews, podcasts, blog posts
    bekes-2021-portfolio-spillovers.json
    lengyel-voxeu-disruptive.json
    ...
  topics.json             # all 19 topics with metadata
```

### 2.5 Three content categories

The catalogue distinguishes three categories of authored output. Each lives in its own directory with its own schema; they share the topic taxonomy and reference the same authors.

**Research** (`data/papers/`) — academic peer-reviewed work. Articles in whitelisted journals; qualifying CEPR/NBER/IZA/CESifo working papers from 2023+; academic book chapters (Handbook of Economic Growth, etc.).

**Policy** (`data/policy/`) — long-form institutional output: OECD / ECB / IMF / World Bank / MNB / KRTK / Bruegel / Budapest Institute reports and discussion papers; chapters in the *Hungarian Labour Market Yearbook* (Munkaerőpiaci Tükör) and similar policy edited volumes; CEPR Policy Insights, IZA Policy Papers; ministry-commissioned reports. The substantive long-form policy work that doesn't pass the academic-journal filter but isn't a 1500-word op-ed either.

**Press** (`data/press/`) — short-form: op-eds, columns (incl. VoxEU, Bruegel blog, Index *defacto*, Telex analysis), interviews, podcasts, newspaper articles, event talks, blog posts. Anything short.

The boundary rule is **length / institutional weight**: long institutional output → Policy; everything short → Press. VoxEU columns are Press because they're popularizations, not primary policy documents. ECB / OECD / Bruegel reports are Policy because they're the institutional primary.

### 2.6 Policy schema

```json
{
  "id": "bekes-koren-halpern-murakozy-2011-bruegel-bp15",
  "title": "Still Standing: How European Firms Weathered the Crisis",
  "title_hu": null,
  "authors": ["bekes-gabor", "koren-miklos", "halpern-laszlo", "murakozy-balazs"],
  "outlet_kind": "report",
  "outlet": "Bruegel Blueprint Series",
  "outlet_issue": "#15",
  "institution": "Bruegel",
  "year": 2011,
  "language": "en",
  "url": "https://www.bruegel.org/...",
  "doi": null,
  "summary_en": "...",
  "summary_hu": null,
  "policy_relevance": "...",
  "policy_relevance_hu": null,
  "topics": ["trade-fdi", "firms-productivity"],
  "countries_studied": ["EU", "HU"],
  "policy_instruments": ["export-promotion (HIPA)", "trade finance", "FDI promotion"],
  "linked_paper_id": null,
  "added_at": "...",
  "last_reviewed_at": "...",
  "review_status": "ai-drafted"
}
```

`outlet_kind` ∈ `{report, chapter, working_paper}`. `linked_paper_id` is optional and points to a `data/papers/<slug>.json` if the policy item is a popularization or follow-up of one of our research papers (the paper page renders these as "Press & policy coverage of this paper"). `policy_relevance` is required for Policy items — the whole point of the section is the policy hook.

### 2.7 Press schema

```json
{
  "id": "bekes-2021-portfolio-spillovers",
  "title": "Hungarian firms steal ideas from each other — and the whole country benefits",
  "title_hu": "A magyar cégek egymástól lesik el az ötleteket...",
  "authors": ["bekes-gabor"],
  "kind": "column",
  "venue": "Portfolio",
  "date": "2021-09-05",
  "language": "hu",
  "url": "https://www.portfolio.hu/...",
  "blurb": null,
  "linked_paper_id": "bekes-harasztosi-2019-rowe",
  "added_at": "...",
  "last_reviewed_at": "...",
  "review_status": "ai-drafted"
}
```

`kind` ∈ `{op-ed, column, interview, podcast, blog, newspaper, radio-tv, event-talk}`. `blurb` is optional one-liner. `linked_paper_id` same semantics as Policy. No `summary_en` / `policy_relevance` / `topics` — Press is intentionally minimal.

**Bilingual titles.** `title` is the canonical English title (always); `title_hu` is the Hungarian title. For Hungarian-origin items the editor (or a translator) supplies the English `title` and the original headline lives in `title_hu`. Renderer prefers the page-language version and falls back to whichever is set. The `language` field still indicates the **article's** language (so the reader knows clicking through gets a Hungarian source). Same convention applies to Policy items.

One JSON per paper, one per author. Trivial to diff, review, and edit by hand. Build-time aggregation into search indexes and topic pages.

---

## 3. Tech stack

**Decision: Astro + Tailwind + Pagefind, deployed as static site.**

Rationale:
- Astro is content-first and handles many static pages well (we'll have ~500–2000 paper pages)
- Pagefind is Astro-native, builds a client-side search index at compile time, works offline, no server needed
- Tailwind matches the "looks professional, minimal custom CSS" requirement
- Static export = free hosting on Vercel / Netlify / GitHub Pages, no ops
- JSON files in repo = Claude Code and humans can edit them the same way
- i18n via Astro's built-in routing

**Alternatives considered and rejected:**
- Next.js: overkill, needs Vercel for full featureset, more JS than needed
- Plain HTML + Fuse.js: works for <200 papers, but loads all data client-side; doesn't scale to 1000+
- WordPress / static CMS: overhead and less Claude-Code-friendly

**Libraries:**
- Astro ≥ 4
- `@astrojs/tailwind`
- `pagefind` for search
- `@astrojs/sitemap`
- Optional: `shadcn-astro` or hand-rolled components with Tailwind
- `lucide-astro` for icons

**Hosting:** Vercel for preview deploys + production. Custom domain when name is decided.

---

## 4. Site UX

### 4.1 Landing (`/`)

- One-sentence mission in large type
- Prominent search bar (Pagefind)
- 4×4 grid of topic cards, each with paper count
- "Featured this month" — 3 papers, editor-picked
- "Recently added" — 6 most recent papers
- Secondary nav: Authors · Topics · About · Contribute

### 4.2 Paper index (`/papers`)

- Filter sidebar: topic (multi), year range, method, data type, publication type (article/WP), author (search)
- Sort: year desc (default), year asc, title
- Default view: card list (title, authors, journal · year, first 25 words of summary, topic tags)
- Infinite scroll or pagination at 25 per page
- Active filters shown as removable chips at top

### 4.3 Paper detail (`/papers/[slug]`)

Page sections, in order:

1. **Title, authors, journal · year** — clickable author names, journal name
2. **At a glance** — 3-icon row: the primary topic, the method, the data type
3. **Non-technical summary** (English; toggle Hungarian) — the main draw
4. **Data used** — always show, prominently. This is the trust signal
5. **Policy relevance** — the action point
6. **Abstract** (original) — collapsed by default, expandable
7. **Tags** — topics, methods, data types, countries
8. **Links** — DOI, PDF, replication package, journal page
9. **Cite this** — APA + BibTeX, click to copy
10. **Related papers** — 3 from same topic or same author

### 4.4 Author detail (`/authors/[slug]`)

- Name, affiliations, links (website, RePEc, Scholar, ORCID)
- Short bio
- Primary fields as tags
- Paper list, grouped by year desc, with publication type flag
- "Qualifying publication" badge on the one that got them admitted

### 4.5 Topic detail (`/topics/[slug]`)

- Topic name + description + policy framing
- "The data landscape" — auto-generated: which data types show up in this topic, rough counts (signals what evidence exists)
- All papers in topic, sorted by year desc
- Related topics

### 4.6 Search UX

Pagefind does full-text across title, summary (both languages), abstract, author name, topic name. Results grouped: Papers, Authors, Topics. Keyboard shortcut `/` to focus.

### 4.7 Bilingual behavior

- Top-right language toggle (EN ⇄ HU)
- Site chrome translates fully
- Paper pages: the two summary fields switch; other metadata stays
- If `summary_hu` is missing, show a "Translation coming soon" note under the English with a small translate-it-yourself link
- URL structure: `/papers/[slug]` for EN, `/hu/papers/[slug]` for HU

---

## 5. Non-technical summary specification

This is the content contract. Each paper on the site has three written fields, each short, each answering a specific question:

| Field | Length | Answers |
|---|---|---|
| `summary_*` | 80–150 words, 2–3 sentences | What question did the paper ask, and what did they find? |
| `data_used` | 40–80 words | What data, from where, what scale, what years? Concrete and specific. |
| `policy_relevance` | 60–120 words | What should a Hungarian policymaker take from this? Include caveats on external validity. |

Writing rules:
- No jargon. If a term must appear, define it in parentheses.
- Numbers and effect sizes with units, not just "large effect"
- Name the country/countries studied. "In the US, …" not "We find …"
- For policy relevance, be specific about _who_ would use it (ministry, agency) and _how_ (design of program X, target Y)
- Never copy from the abstract. Paraphrase entirely.

AI prompt template in `docs/WORKFLOW.md` § 3.

---

## 6. What Claude Code builds this afternoon

Concrete deliverables for the build session:

1. `npm create astro@latest` with the content collections starter, Tailwind enabled
2. Content collections configured for `authors`, `papers`, `topics`, `journals`
3. Zod schemas matching § 2 above
4. All routes in § 4 implemented and rendering from the JSON files
5. Pagefind integrated; search works from the landing page
6. Filter UI on `/papers` working for topic + year + method at minimum
7. Bilingual routing set up; EN fully populated, HU stubbed with fallback
8. Two sample files committed (`data/sample-paper.json`, `data/sample-author.json`) — see `/data/` in this repo
9. 5 more seeded papers hand-entered by Gábor from the seed list
10. GitHub repo + Vercel deploy, site live at a temporary URL

**Not needed:** admin UI, auth, database, AI pipeline, comments, analytics beyond basic. Those come later.
