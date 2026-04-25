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

## Core principle

The catalogue is the editor's; this skill brings candidates to them, with
enough metadata that approve-or-reject is a fast decision. Don't apply
anything; produce a review queue.

The source list (`sources.md` in this skill folder) is the canonical
list of outlets the editor watches. Update that file — not the skill —
when a new outlet should be added or dropped.

## Inputs

- **Author-driven** (`media-scan --author <slug>` in user phrasing):
  one author across all core outlets. ~5–8 fetches.
- **Outlet-driven** (`media-scan --outlet <name>` in user phrasing):
  recent posts at one outlet, filtered to authors in the catalogue.
  ~3–6 fetches.
- **Both** (`media-scan` alone with no qualifier): too broad; ask the
  user to pick.

## Step 1 — Load the source list

Read `.claude/skills/media-scan/sources.md`. It groups outlets by:

- **HU short-form press** (Portfolio, Telex, Index defacto, HVG, …)
- **HU long-form policy** (KRTK reports, Budapest Institute, MNB Szemle, …)
- **EN short-form press** (VoxEU, Bruegel blog, ProMarket, VoxDev, …)
- **EN long-form policy** (Bruegel reports, ECB / OECD / IMF working papers, …)
- **English major press** (FT, NYT, WSJ, Bloomberg, NPR, …)
- **Podcasts** (Trade Talks, Macro Musings, …)

Each entry has: `name`, `url_root`, `lang`, `kind` (press / policy),
`search_pattern` (e.g. `site:voxeu.org "<name>"`), and a short note
on what to expect.

## Step 2 — Fetch and filter

### Author-driven

For each outlet in the curated list (or a subset if the user named
specific ones):

1. Run `WebSearch` with the outlet's `search_pattern` and the
   author's `name_en` (and `name_hu` if it's a HU outlet).
2. Fetch the first 1–2 results that look like a piece **by** the
   author (not just mentioning them).
3. For each candidate, extract: title, date, URL, and identify
   `kind` from SPEC §2.7's enum (`op-ed`, `column`, `interview`,
   `podcast`, `blog`, `newspaper`, `radio-tv`, `event-talk`).
4. Generate a slug: `<surname>-<year>-<outletcode>-<topic-keyword>`.
   E.g. `bekes-2024-portfolio-spillovers`,
   `lengyel-2025-voxeu-disruptive`.
5. Check whether `data/press/<slug>.json` exists. Skip if yes.
6. For HU-origin items: capture `title` (translate to EN — your
   translation, flagged as such in NOTES) and `title_hu` (the
   original headline).

### Outlet-driven

For one outlet:

1. Fetch the outlet's index / recent-articles page (e.g.
   `https://www.portfolio.hu/`, `https://voxeu.org/columns`).
2. Scan the last ~30 article cards / RSS items / recent links.
3. Cross-reference each author byline against `data/authors/`. The
   match is on `name_en` or `name_hu`.
4. For matches, run the same metadata extraction as above and
   build the candidate JSON.

For outlets without a clean index page (rare — most have RSS or a
listing), fall back to `site:<domain>` Google searches scoped by
recent date.

## Step 3 — Output

For each candidate, return a block:

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
LINKED_PAPER_ID: <slug-of-paper-in-catalogue or null>
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

For Policy candidates, use the SPEC §2.6 schema instead and include
a brief draft `summary_en` (the policy items get summarised; press
doesn't). Flag policy candidates that need PDF download for the
`draft-summary` follow-up.

End with a summary line:

```
SCANNED: <N> outlets, <N> author matches.
NEW CANDIDATES: <N> press, <N> policy.
ALREADY IN CATALOGUE: <N> (skipped).
```

## Step 4 — `linked_paper_id` opportunity check

For each press candidate, do a quick check whether it's likely a
popularization of one of our research papers:

1. The press piece's title or first paragraph mentions a paper
   title or a topic + result.
2. The author has a paper in `data/papers/` from the last 5 years
   on that topic.
3. The dates are consistent (press piece is after or near the
   paper's publication).

If yes, set `linked_paper_id` in the proposed JSON. If the link is
suggestive but not certain, set null and flag in NOTES.

This pays off for Press → Paper coverage on the paper page (per
SPEC §4.3).

## Stopping rules

- 8 fetches max for author-driven mode, 6 for outlet-driven.
- If the same author shows up at 5+ outlets, return what you have
  with a note that more candidates exist; the editor reviews this
  batch first.
- Skip outlets behind hard paywalls (FT articles older than a year,
  WSJ except headlines) — flag the byline as "found in <outlet>
  search results, full content paywalled".

## Apply step

Default is dry-run. The editor reviews candidates and either:

- Approves a subset → "apply candidates 1, 3, 7" → write those JSON
  files to `data/press/` or `data/policy/`.
- Approves all → write all.
- Rejects with notes — add to a "skip list" in NOTES and don't
  re-surface next scan.

There's no batch apply script for press / policy as of 2026-04-25;
write the files directly with the proposed JSON. Each new file
should pass `python build.py` validation, so run that after a batch
write to confirm.

## What this skill does NOT do

- Draft summaries for the policy candidates it surfaces. Once
  written to `data/policy/`, hand off to `draft-summary --policy
  <slug>`.
- Verify the author is in the catalogue. If a byline doesn't match
  any `data/authors/` entry, flag it in NOTES — the editor decides
  whether to add the author (separate `research-author` workflow).
- Bulk-import RSS feeds. The skill is curated and slow on purpose.
- Translate existing EN press items to HU titles (editor deferred
  this — option b).

## Examples

### Author-driven

> "Media scan for Köszegi."

Process: load `sources.md` → for each outlet, search `<name> "Botond
Kőszegi"` → fetch likely hits → cross-check against `data/press/
koszegi-*.json` → return new candidates with proposed JSON. Cap 8
outlets.

### Outlet-driven

> "Sweep VoxEU for Hungarians since the last scan."

Process: fetch `https://voxeu.org/columns` recent listing → for
each item, check whether any byline matches a slug in
`data/authors/` → for matches, extract metadata → return new
candidates.
