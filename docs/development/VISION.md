# Evidence for Hungary

_A searchable, policy-facing catalogue of research by top Hungarian economists._

## One-paragraph pitch

A website that collects every paper written by top Hungarian economists — published articles and working papers — and presents each one in a form a policymaker can actually use: the original abstract, a plain-language summary, a description of the data behind it, and a short note on policy relevance. Searchable, browsable by topic (labor, trade, education, health, …), and available in English and Hungarian.

## Working title — pick one

These are candidates. The docs use **Evidence for Hungary** as a placeholder; swap throughout when a decision is made.

- **Evidence for Hungary** / _Bizonyíték Magyarországnak_ — names the mission
- **Hungarian Economics for Policy** / _Magyar közgazdaságtan a politikának_ — literal
- **HUEcon Briefs** — shorter, brandable
- **Policy Brief Hungary** — closest to the implicit genre
- **Magyar Közgazdászok** (Hungarian Economists) — simple, the literal list-name

## Why now

A new Hungarian government takes office in 2026. Hungarian economists have published hundreds of peer-reviewed papers directly relevant to the choices that government will face — on labor participation, demographics, skill formation, firm productivity, trade exposure, health, migration, housing. Most of that work is invisible to the people who would use it. This site closes that gap.

## Audience

1. **Primary: Hungarian policymakers and ministry staff.** Technocrats who need evidence fast, in Hungarian, with the methodology explained well enough to trust.
2. **Secondary: journalists, think tanks, civil society.** People who translate research into public debate.
3. **Tertiary: researchers and students.** A clean index of who's working on what.

Design decisions break in favor of audience 1 wherever they conflict.

## Scope — what gets in

**Authors:** Hungarian economists who have at least one publication in a top general-interest journal (AER, QJE, JPE, Econometrica, REStud, JEEA, AEJ suite) _or_ a top field journal (full list in `docs/SPEC.md`).

**Papers:** once an author qualifies, include all their published papers and recent working papers, across any journal/outlet. Filter later by topic and recency in the UI, not at ingestion.

**"Hungarian" means:** Hungarian nationality, born in Hungary, or primary affiliation at a Hungarian institution for ≥3 years. Kept deliberately broad; diaspora counts.

**Starting target: ~30 authors, ~300 papers by end of year one.** See `docs/SEED_ECONOMISTS.md` for the seed list.

## Site map

```
/                              landing: pitch + search + topic cards + featured papers
/papers                        paper index (filter: topic, author, journal, year, data, method)
/papers/[slug]                 paper detail (the six fields + tags + link out)
/authors                       author index
/authors/[slug]                author detail (bio + paper list)
/topics                        topic index (15 policy areas)
/topics/[slug]                 topic detail (description + papers + data landscape)
/about                         mission, methodology, how summaries are made
/contribute                    how to add papers (for author / editor)
```

Hungarian version at `/hu/...` mirroring the same structure. English and Hungarian share the same data; only UI strings and the two summary fields differ.

## MVP — what to build in the Claude Code session this afternoon

**Goal:** a deployable scaffold with 5–10 papers, not a finished content site. Content filling happens over weeks.

1. Astro + Tailwind + Pagefind scaffold (see `docs/SPEC.md` § Tech)
2. JSON data model in `/data/papers/*.json` and `/data/authors/*.json` (schemas in `docs/SPEC.md`)
3. All routes above, working against the JSON files
4. Topic taxonomy wired in (15 areas from `docs/TAXONOMY.md`)
5. Client-side search via Pagefind
6. Filter UI on `/papers` (topic, year, method at minimum)
7. Seed with the two example JSONs in `/data/` + ~5 more hand-entered papers
8. Deploy to Vercel or GitHub Pages
9. Placeholder Hungarian routes (`/hu/...`) with English fallbacks; translate later

**Explicitly out of scope for the afternoon:** AI summarization pipeline, admin UI, bulk import, citation counts, author photos, fancy visualizations.

## How to read the rest of this repo

- `docs/SPEC.md` — the full technical spec: inclusion criteria, data schemas, tech stack, site structure
- `docs/TAXONOMY.md` — policy areas, methods, data types, country tags
- `docs/WORKFLOW.md` — how to go from "name of economist" to "paper entry on the site"
- `docs/SEED_ECONOMISTS.md` — starter roster with sources
- `data/sample-paper.json` — example paper entry (use as template)
- `data/sample-author.json` — example author entry (use as template)

Read `SPEC.md` first. The rest makes sense in any order.

## Success criteria

- A ministry staffer searching "youth unemployment" finds 3–5 relevant papers in under a minute
- Each paper's policy-relevance paragraph can be pasted into a briefing note as-is
- Authors feel accurately represented and want to be listed
- Content grows by ≥20 papers/month once the pipeline is running
- Zero broken links to journal pages or PDFs

## Open questions for later

- Editorial governance: who writes / reviews the non-technical summaries? (Initially: AI-drafted, Gábor-reviewed.)
- Do we show citation counts? Source? (Probably Google Scholar, fetched once per quarter.)
- Do we accept author submissions? Review process?
- Funding for hosting and editorial time beyond year one?
- Hungarian-language launch timing — simultaneous, or 3 months after English?
