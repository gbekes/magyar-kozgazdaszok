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
- _Finance_: Journal of Finance, Review of Financial Studies, Journal of Financial Economics, Review of Finance, Journal of International Money and Finance
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

**Admission rule:** any journal on this list qualifies an author for inclusion — Tier A or Tier B. Once admitted, all of the author's peer-reviewed papers and recent working papers are eligible for the catalogue (filter later in the UI).

**Recent changes to this list:**
- Added to Tier A: International Economic Review, Review of Economics and Statistics, Journal of Economic Perspectives, Theoretical Economics, AEA Papers and Proceedings.
- Added to Tier B: Journal of Economic Theory and Economic Theory (new _Theory_ field); Review of Finance and Journal of International Money and Finance (finance).
- Removed: Review of Economic Dynamics, Journal of International Business Studies, World Development.

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
  "featured": false,
  "added_at": "2026-04-19",
  "last_reviewed_at": "2026-04-19",
  "review_status": "ai-drafted"
}
```

Required fields: `id`, `title`, `authors`, `publication_type`, `year`, `abstract`, `topics`.
Recommended: everything else. `review_status` ∈ `{ai-drafted, human-reviewed, author-approved}`.

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
  }
}
```

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
  papers/
    bekes-halpern-kornai-kovacs-2023-jie.json
    koren-szeidl-2012-qje.json
    ...
  topics.json             # all 15 topics with metadata
```

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
