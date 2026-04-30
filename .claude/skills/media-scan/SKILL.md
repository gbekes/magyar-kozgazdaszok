---
name: media-scan
description: >
  Scan a curated set of "core" media outlets for press / policy items by
  Hungarian economists not yet in the Magyar Közgazdászok catalogue. Either
  outlet-driven (walk one outlet's recent contributors) or author-driven
  (sweep all core outlets for one author). Outputs a list of candidate items
  with proposed JSON for `data/press/<slug>.json` or `data/policy/<slug>.json`.
  Use when the user says "scan press", "find new columns", "check media
  coverage of X", "what did we miss on Portfolio recently", "sweep VoxEU
  for Hungarians", "media scan", "check the press sources", or asks about
  filling press / policy gaps from external sources. Reads the curated
  source list at `.claude/skills/media-scan/sources.md`.
---

# media-scan

Walk a curated set of media outlets and surface candidate Press / Policy
items for the catalogue. Two modes: outlet-driven and author-driven.

The catalogue is the editor's; this skill brings candidates with enough
metadata that approve-or-reject is a fast decision. Default is dry-run.

The source list (`sources.md`) is the canonical list of outlets the
editor watches. Update that file — not this skill — when an outlet is
added, dropped, or its search pattern changes.

## Inputs

- **Author-driven** (`media-scan --author <slug>`): one author across
  all core outlets. ~5–8 fetches.
- **Outlet-driven** (`media-scan --outlet <name>`): recent posts at
  one outlet, filtered to authors in the catalogue. ~3–6 fetches.
- **Both** (`media-scan` alone): too broad; ask the user to pick.

## Step 1 — Load `sources.md`

Six sections:

- **A.** HU short-form press (Portfolio, Telex, Index defacto, HVG,
  G7, Qubit, 24.hu, Magyar Narancs, Origo, Partizán, Mérce, 444,
  Privátbankár, Népszava, Magyar Hang, Defacto, Klubrádió/ATV)
- **B.** HU long-form policy (KRTK, MT yearbook, BI, Egyensúly, MNB)
- **C.** EN short-form press (VoxEU, Bruegel blog, ProMarket, VoxDev,
  The Conversation, Project Syndicate)
- **D.** EN long-form policy (Bruegel reports, CEPR Policy Insights,
  IZA Policy Papers, OECD/IMF/World Bank/ECB)
- **E.** EN major press (FT, NYT, WSJ, WaPo, Bloomberg, NPR, BBC)
- **F.** Podcasts

Each entry has: `name`, `url_root`, `lang`, `kind`, `search_pattern`,
`recency`.

## Step 2 — Fetch and filter

### Author-driven

For each outlet (or a subset if the user named specific ones):

1. `WebSearch` with the outlet's `search_pattern` and the author's
   `name_en` (and `name_hu` for HU outlets).
2. Fetch the first 1–2 results that look like a piece *by* the
   author (not just mentioning them).
3. Extract: title, date, URL. Identify `kind` from the SPEC §2.7 enum.
4. Generate slug: `<surname>-<year>-<outletcode>-<topic-keyword>`.
   E.g. `bekes-2024-portfolio-spillovers`.
5. Check whether the slug exists in `data/press/`. Skip if yes.
6. For HU-origin items: capture `title` (your translation, flagged in
   NOTES) and `title_hu` (original headline).

### Outlet-driven

For one outlet:

1. Fetch the outlet's index / RSS / recent listing.
2. Scan the last ~30 article cards.
3. Cross-reference each byline against `data/authors/` (match on
   `name_en` or `name_hu`).
4. For matches, run the same metadata extraction as above.

For outlets without a clean index, fall back to `site:<domain>` Google
searches scoped by recent date.

## Step 3 — Output

For each candidate:

```
CANDIDATE: <proposed-slug>
AUTHOR: <slug>  (matched to data/authors/<slug>.json)
TITLE: <as it appears>
TITLE_HU: <if HU-origin>
KIND: <op-ed | column | interview | podcast | blog | newspaper | radio-tv | event-talk>
VENUE: <outlet>
DATE: <YYYY-MM-DD>
LANGUAGE: <en | hu>
URL: <https://...>
LINKED_PAPER_ID: <slug or null>
NOTES: <translation flag, paywall, missing date, etc.>

PROPOSED JSON (paste into data/press/<proposed-slug>.json):
{
  "id": "<proposed-slug>",
  "title": "...",
  "title_hu": "...",
  "authors": ["<slug>"],
  "kind": "...",
  "venue": "...",
  "date": "...",
  "language": "...",
  "url": "...",
  "blurb": null,
  "linked_paper_id": null,
  "added_at": "<today>",
  "last_reviewed_at": "<today>",
  "review_status": "ai-drafted"
}
```

For Policy candidates, use the SPEC §2.6 schema and include a brief
draft `summary_en`. Flag policy candidates that need PDF download
for the `draft-summary` follow-up.

End with:

```
SCANNED: <N> outlets, <N> author matches.
NEW CANDIDATES: <N> press, <N> policy.
ALREADY IN CATALOGUE: <N> (skipped).
```

## Step 4 — `linked_paper_id` opportunity check

For each press candidate, check whether it's likely a popularization
of one of our research papers:

1. The press piece's title or first paragraph mentions a paper title
   or topic + result.
2. The author has a paper in `data/papers/` from the last 5 years on
   that topic.
3. Dates are consistent (press piece is after or near the paper's
   publication).

If yes, set `linked_paper_id`. If suggestive but not certain, set
null and flag in NOTES.

## Stopping rules

- 8 fetches max for author-driven, 6 for outlet-driven.
- If the same author shows up at 5+ outlets, return what you have
  with a note that more candidates exist; the editor reviews this
  batch first.
- Skip outlets behind hard paywalls — flag the byline as "found in
  search results, full content paywalled".

## Apply

Editor reviews candidates and either:

- Approves a subset → write those JSON files to `data/press/` /
  `data/policy/`.
- Approves all → write all.
- Rejects with notes — log in NOTES and don't re-surface next scan.

No batch apply script for press / policy; write the files directly.
Each new file should pass `python build.py`; run that after a batch
write.

## Out of scope

- Drafting summaries for surfaced policy candidates — hand off to
  `draft-summary --policy <slug>` after the file is written.
- Verifying the author is in the catalogue — flag unknown bylines in
  NOTES; don't auto-add authors (`research-author` does that).
- Bulk RSS imports.
- Translating EN press titles to HU (deferred per editor preference).

## Examples

### Author-driven

> "Media scan for Köszegi."

Load `sources.md` → for each outlet, search `<name> "Botond Kőszegi"`
→ fetch likely hits → cross-check against `data/press/koszegi-*.json`
→ return new candidates. Cap 8 outlets.

### Outlet-driven

> "Sweep VoxEU for Hungarians since the last scan."

Fetch `https://voxeu.org/columns` → for each item, check whether any
byline matches a slug in `data/authors/` → for matches, extract
metadata → return new candidates.
