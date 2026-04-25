# Core media sources — Magyar Közgazdászok

Curated list of outlets the editor watches for press / policy output by
Hungarian economists. Read by the `media-scan` skill. Edit this file to
add, remove, or reweight a source — the skill picks it up next run.

Format per entry:

```
### <Name>
- url_root: https://...
- lang: hu | en
- kind: press | policy
- search_pattern: <query template, "<NAME>" gets replaced>
- recency: rss | sitemap | google | manual
- notes: what to expect, what trips up the scan
```

`recency` controls how the skill finds recent items: prefer `rss` /
`sitemap` when available, fall back to `google` (a `site:` search) for
outlets without machine-readable indices.

---

## A. Hungarian short-form press (HU)

These are the outlets where Hungarian economists publish op-eds, columns,
and interviews in Hungarian. Highest yield — every prolific author has
something here.

### Portfolio.hu
- url_root: https://www.portfolio.hu/
- lang: hu
- kind: press
- search_pattern: `site:portfolio.hu "<NAME>"`
- recency: google
- notes: Biggest Hungarian econ/finance daily. Regular contributors include Békés, Köszegi, Köves, Madár István. Many pieces are columns; some are interviews; tag-based section pages exist per author for repeat columnists. URL pattern: `/cikk/<id>/<slug>` (paywalled after ~30 days for some). Author byline is reliable.

### Telex.hu
- url_root: https://telex.hu/
- lang: hu
- kind: press
- search_pattern: `site:telex.hu "<NAME>"`
- recency: rss
- notes: Independent successor to Index. Long-form analysis pieces ("Telex Analysis") are good catches. Look in `/gazdasag/` and `/velemeny/` sections. Bylines show full Hungarian name; sometimes the economist is interviewed rather than authoring.

### Index.hu (defacto)
- url_root: https://index.hu/
- lang: hu
- kind: press
- search_pattern: `site:index.hu defacto "<NAME>"`
- recency: google
- notes: The *defacto* econ blog at Index is mostly historical now (2010s). Köszegi, Csaba, Lengyel, others wrote regularly. Worth a sweep for older items not yet captured. URL pattern: `/gazdasag/defacto/<year>/<month>/<slug>/`.

### HVG (hvg.hu)
- url_root: https://hvg.hu/
- lang: hu
- kind: press
- search_pattern: `site:hvg.hu "<NAME>"`
- recency: rss
- notes: Weekly newsmagazine + daily site. Op-eds and interviews. Print-only pieces sometimes have a teaser on the site; flag those for editor to grab the print version.

### 24.hu
- url_root: https://24.hu/
- lang: hu
- kind: press
- search_pattern: `site:24.hu "<NAME>"`
- recency: rss
- notes: News portal. Mostly interviews / quotes; original op-eds rarer.

### Mérce
- url_root: https://merce.hu/
- lang: hu
- kind: press
- search_pattern: `site:merce.hu "<NAME>"`
- recency: rss
- notes: Left-leaning, occasional academic op-eds (Köves, Pogátsa). Lower volume but high signal.

### 444.hu
- url_root: https://444.hu/
- lang: hu
- kind: press
- search_pattern: `site:444.hu "<NAME>"`
- recency: rss
- notes: Independent news. Mostly news pieces quoting economists; occasional op-ed.

### Privátbankár.hu
- url_root: https://privatbankar.hu/
- lang: hu
- kind: press
- search_pattern: `site:privatbankar.hu "<NAME>"`
- recency: google
- notes: Finance columns (Berlinger, Dömötör territory). URL pattern includes year + slug.

### Népszava
- url_root: https://nepszava.hu/
- lang: hu
- kind: press
- search_pattern: `site:nepszava.hu "<NAME>"`
- recency: google
- notes: Labor-leaning daily. Kertesi, Köllő op-eds occasionally appear. Older archive (pre-2018) is uneven.

### Magyar Hang
- url_root: https://hang.hu/
- lang: hu
- kind: press
- search_pattern: `site:hang.hu "<NAME>"`
- recency: rss
- notes: Successor to 168 Óra. Long interviews with senior academics.

### Defacto.hu (standalone)
- url_root: https://defacto.hu/
- lang: hu
- kind: press
- search_pattern: `site:defacto.hu "<NAME>"`
- recency: rss
- notes: The *defacto* econ blog after it left Index. Same crew (Köszegi, Csaba, …). Likely overlaps with Index defacto archive — slug uniqueness matters.

### Klubrádió + ATV (interviews)
- url_root: https://www.klubradio.hu/, https://www.atv.hu/
- lang: hu
- kind: press (kind=radio-tv)
- search_pattern: `site:klubradio.hu "<NAME>"` / `site:atv.hu "<NAME>"`
- recency: google
- notes: Interview shows. Hard to slug cleanly — use date + topic. Sometimes only the show page is online, no transcript.

---

## B. Hungarian long-form policy (HU)

### KRTK Working Papers + reports
- url_root: https://kti.krtk.hu/, https://www.krtk.hu/
- lang: hu (sometimes en)
- kind: policy
- search_pattern: `site:kti.krtk.hu "<NAME>"` and `site:krtk.hu "<NAME>"`
- recency: sitemap
- notes: Author-aligned WP series. Per the 2026-04-25 rule, only recent (2023+) NBER/CEPR/IZA/CESifo WPs are policy; KRTK WPs that aren't pre-publication for those series go in `data/papers/` as `working_paper`, not policy. Read carefully.

### Munkaerőpiaci Tükör (HU Labour Market Yearbook)
- url_root: https://kti.krtk.hu/munkaerőpiaci-tükör/ (and the yearly PDF)
- lang: hu
- kind: policy (outlet_kind=chapter)
- search_pattern: manual — fetch the year's table of contents
- notes: Annual edited volume. Each chapter is a separate policy item. Authors are catalogued already; sweep year-by-year for missed chapters. Telegdy, Horn, Hajdu, Kertesi, Hermann are heavy contributors.

### Budapest Institute (BI)
- url_root: https://www.budapestinstitute.eu/
- lang: hu (sometimes en)
- kind: policy
- search_pattern: `site:budapestinstitute.eu "<NAME>"`
- recency: sitemap
- notes: Adamecz's home base — 10 BI briefs (per 2026-04-25 handover). Brief PDFs are public. Co-authors often listed only on the PDF, not the index page; check both.

### Egyensúly Intézet
- url_root: https://www.equilibriuminstitute.hu/
- lang: hu
- kind: policy
- search_pattern: `site:equilibriuminstitute.hu "<NAME>"`
- recency: google
- notes: Centrist policy think-tank. Lower volume.

### MNB Szemle / MNB Working Papers
- url_root: https://www.mnb.hu/kiadvanyok/szakmai-cikkek
- lang: hu (some en)
- kind: policy
- search_pattern: manual via MNB publications index
- notes: Hungarian National Bank research output. Pre-2015 is sparser online.

### Kopint-Tárki, GKI, Századvég
- url_root: various
- lang: hu
- kind: policy
- search_pattern: `site:<domain> "<NAME>"`
- notes: Independent / partisan policy shops. Editor-judgement on whether a brief qualifies.

---

## C. English short-form press (EN)

The international press where Hungarian economists publish in English.
Lower volume per outlet but high prestige; worth thorough sweeps.

### VoxEU (CEPR)
- url_root: https://voxeu.org/
- lang: en
- kind: press (kind=column)
- search_pattern: `site:voxeu.org "<NAME>"`
- recency: rss
- notes: Highest-priority EN outlet for European economists. Most VoxEU columns popularize a CEPR DP — set `linked_paper_id` to the matching paper. Bekes, Koren, Lengyel, Telegdy, Halpern, Murakozy, Harasztosi all have multiple columns. URL pattern: `/article/<slug>`.

### Bruegel blog
- url_root: https://www.bruegel.org/
- lang: en
- kind: press (kind=blog)
- search_pattern: `site:bruegel.org/blog "<NAME>"`
- recency: rss
- notes: Zsolt Darvas's territory. Distinguish *blog posts* (Press) from *Bruegel reports / Blueprints / Policy Briefs* (Policy). Per 2026-04-25 rule, Bruegel WPs are reports → Policy.

### ProMarket (Stigler Center)
- url_root: https://www.promarket.org/
- lang: en
- kind: press (kind=column)
- search_pattern: `site:promarket.org "<NAME>"`
- recency: rss
- notes: Antitrust / competition-policy columns. Köszegi, Mátyás have appeared.

### VoxDev
- url_root: https://voxdev.org/
- lang: en
- kind: press (kind=column)
- search_pattern: `site:voxdev.org "<NAME>"`
- recency: rss
- notes: Development-focused VoxEU spinoff. Hornok (per the Hornok JDE 2025 entry), Gáspár, Juhász candidates.

### The Conversation
- url_root: https://theconversation.com/
- lang: en
- kind: press (kind=op-ed)
- search_pattern: `site:theconversation.com "<NAME>"`
- recency: rss
- notes: Academic op-ed platform. Lower volume from this list of authors but worth a check.

### Project Syndicate
- url_root: https://www.project-syndicate.org/
- lang: en
- kind: press (kind=op-ed)
- search_pattern: `site:project-syndicate.org "<NAME>"`
- recency: google
- notes: Senior commentators. Kornai had pieces; Csaba László is a regular.

---

## D. English long-form policy (EN)

### Bruegel reports / Blueprints / Policy Briefs / Policy Insights
- url_root: https://www.bruegel.org/sections/publications
- lang: en
- kind: policy (outlet_kind=report)
- search_pattern: `site:bruegel.org "<NAME>" -inurl:blog`
- recency: rss
- notes: Per 2026-04-25 rule, all Bruegel non-blog publications are Policy with `outlet_kind: report`. Darvas's 8 Bruegel pieces are the heavy uncovered set.

### CEPR Policy Insights / Discussion Papers (recent)
- url_root: https://cepr.org/publications
- lang: en
- kind: policy
- search_pattern: `site:cepr.org "<NAME>"`
- recency: rss
- notes: 2023+ CEPR DPs are eligible as `working_paper` policy items per SPEC §1.3 / 2026-04-25 rule. Older DPs go in `data/papers/` as `publication_type: working_paper`.

### IZA Policy Papers
- url_root: https://www.iza.org/publications/pp
- lang: en
- kind: policy
- search_pattern: `site:iza.org policy-paper "<NAME>"`
- recency: sitemap
- notes: IZA *Policy Paper* series only (not the regular IZA DPs, which are `data/papers`).

### OECD / IMF / World Bank / ECB working papers
- url_root: various
- lang: en
- kind: policy
- search_pattern: `site:<domain> "<NAME>"`
- recency: manual
- notes: Hungarian economists at international institutions: Hornok (Kiel + occasional Bundesbank), Temesváry (Fed Board), Manchin (formerly OECD). Cross-check institution pages.

---

## E. English major press

Lower volume but high editorial value when present.

### Financial Times
- url_root: https://www.ft.com/
- lang: en
- kind: press (kind=op-ed | newspaper)
- search_pattern: `site:ft.com "<NAME>"`
- recency: google
- notes: Hard paywall after first hit. Capture URL + title; editor pulls full text separately.

### NYT, WSJ, Washington Post, Boston Globe, Bloomberg
- url_root: nytimes.com, wsj.com, washingtonpost.com, bostonglobe.com, bloomberg.com
- lang: en
- kind: press
- search_pattern: `site:<domain> "<NAME>"`
- recency: google
- notes: Mostly op-eds and quoted-expert interviews. Same paywall rules.

### NPR + BBC
- url_root: npr.org, bbc.com
- lang: en
- kind: press (kind=radio-tv | newspaper)
- search_pattern: `site:npr.org "<NAME>"`
- recency: google
- notes: Interview / quote pieces. Köszegi, Juhász have been on NPR.

---

## F. Podcasts

### Trade Talks (Soumaya Keynes / Chad Bown — now Most Favoured Nation)
- url_root: https://piie.com/, RSS feeds
- lang: en
- kind: press (kind=podcast)
- search_pattern: `site:piie.com tradetalks "<NAME>"`
- notes: Trade economists. Juhász, Békés candidates.

### Macro Musings (David Beckworth)
- url_root: https://www.mercatus.org/macro-musings
- lang: en
- kind: press (kind=podcast)
- search_pattern: `site:mercatus.org macro-musings "<NAME>"`
- notes: Macro / monetary policy.

### VoxTalks Economics
- url_root: https://voxeu.org/voxtalks
- lang: en
- kind: press (kind=podcast)
- search_pattern: `site:voxeu.org voxtalks "<NAME>"`
- notes: VoxEU's podcast — high signal for European economists.

### EconTalk (Russ Roberts)
- url_root: https://www.econtalk.org/
- lang: en
- kind: press (kind=podcast)
- search_pattern: `site:econtalk.org "<NAME>"`
- notes: Long-form interviews.

### HU podcasts (Bartos Tibor, Az átverés, Kibic, Az Indoklás)
- url_root: various
- lang: hu
- kind: press (kind=podcast)
- search_pattern: episode listings on Spotify / podcast.hu
- notes: HU econ podcast scene is small; episode pages on Spotify are often the only durable URL. Capture episode title + show + date.

---

## How the skill uses this list

For an **author-driven** scan, the skill iterates through outlets in
section order (A → F) and stops after ~8 hits or after exhausting the
list.

For an **outlet-driven** scan, the skill picks one entry by name and
walks its recent items.

Recency strategy:
- `rss` → fetch the feed, last 30 items
- `sitemap` → fetch sitemap, filter by `lastmod` in last 90 days
- `google` → `site:<domain> "<NAME>" after:<date>` query
- `manual` → tell the editor to point at a specific index page

## Adding a new source

When the editor mentions a new outlet ("we should also check X"), append
an entry to the relevant section, fill in the fields, and note in the
commit message *why* it was added. The next `media-scan` run picks it
up automatically.
