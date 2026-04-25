---
name: research-author
description: >
  Step-by-step research pass on a single Hungarian economist for the Magyar
  Közgazdászok catalogue. Builds or refreshes one author's full record:
  affiliations, bio (EN + HU), photo URL, RePEc / Scholar / ORCID IDs,
  qualifying publication, and a list of candidate papers from RePEc that
  are not yet in `data/papers/`. Use whenever the user wants to research,
  enrich, refresh, fill in, build out, or "do a proper pass on" an author —
  including phrasings like "research X", "build out Y's page", "fill in
  what's missing for Z", "find a photo for W", "what papers of P are we
  missing", "who is Q again", or when the user names a `bio_status: stub`
  author or one of the 14 review-status-stub authors. Outputs a JSON patch
  the editor can paste into `data/authors/<slug>.json` plus a numbered list
  of paper-slug suggestions for the catalogue.
---

# research-author

A focused research pass on one author at a time. Reads existing state,
searches the open web, returns a structured patch + a paper backlog. Does
not write files unless the user asks — the default product is a review
block.

## Core principle

Read first, search second, write third. Never overwrite a non-null field
without telling the user; never invent affiliations, photos, IDs, or paper
metadata. If a fact is uncertain, leave the field at `null` and explain
in NOTES what would resolve it.

## Inputs

- An author slug (e.g. `simonovits-andras`) or a full name. If a name,
  resolve to the slug by checking `data/authors/*.json` first; if no
  match, propose a slug as `surname-given.lower()` with diacritics
  stripped, and ask before creating.
- Optional flags the user might say in plain language: "just the bio",
  "just photo", "just papers", "everything". Default = everything.

## Step 1 — Read current state

1. `Read data/authors/<slug>.json` — capture which fields are already
   filled. Note `review_status` if present.
2. `Glob data/papers/<slug>-*.json` and `Grep` for the slug in
   `authors` arrays — count what's already in the catalogue per
   `publication_type`.
3. Check coverage flags: `photo_url`, `bio_en`, `bio_hu`, `repec_id`,
   `scholar_id`, `orcid`, `qualifying_publication`, `affiliations`,
   `primary_fields`, `website`.

This pre-flight tells you what's missing. Don't search for things that
are already filled unless the user said "refresh".

## Step 2 — Web research, in this order

Stop early when you have enough. Budget ~5–8 fetches total.

1. **RePEc / IDEAS author page.** Search `site:ideas.repec.org/e/
   <surname>` or `site:ideas.repec.org/f/p<initial><stem>.html`. The
   RePEc ID is the URL stem after `/e/` (e.g. `pbe115`). The page
   lists every published article with venue + year, every WP series
   they post in, and links to their personal site. **This is the
   single highest-leverage page** for catalogue diff and for
   confirming `repec_id`.
2. **The author's primary institution faculty page.** For Hungarian
   economists this is usually one of:
   - KRTK — `https://kti.krtk.hu/en/researchers/<slug>/` or the HU
     equivalent at `kti.krtk.hu/researchers/<slug>/`
   - CEU — `https://economics.ceu.edu/people/<slug>` (Vienna era) or
     `https://people.ceu.edu/<slug>` (legacy Budapest pages still up
     for some emeritus faculty)
   - Corvinus — `https://www.uni-corvinus.hu/contributors/<slug>/`
   - MNB — `https://www.mnb.hu/` (search by name)
   - For diaspora: Google `<full name> economist <institution>`. The
     first non-news hit is almost always the personal or faculty page.
3. **Personal website.** RePEc usually links it. If not, Google
   `<name> economist site:.edu OR site:.com OR site:google.com/view`.
   Personal sites are the most reliable source for: photo, current
   affiliations, ORCID, sometimes Scholar ID.
4. **Google Scholar profile.** Search `<name> site:scholar.google.com`.
   The Scholar ID is the `user=` param. Confirm it's the right person
   by checking that 2–3 of their listed papers match the catalogue.
5. **Wikipedia (EN or HU).** Useful for senior / well-known economists
   for a 2–3 sentence bio. Verify against another source before
   pasting verbatim.
6. **ORCID.** `https://orcid.org/0000-...`. Often linked from RePEc or
   the personal page; rarely worth a dedicated search.

### Diaspora-specific tips

- **LSE / Oxford / NYU / etc.** Faculty page URLs follow predictable
  patterns: `https://www.lse.ac.uk/economics/people/<slug>`,
  `https://www.economics.ox.ac.uk/people/<slug>`. Try those first.
- **Bocconi / VGSF / CREi.** `https://www.bocconi.it/en/people/<slug>`,
  `https://vgsf.ac.at/faculty/<slug>`, `https://www.crei.cat/people/<slug>`.
- **Bruegel.** `https://www.bruegel.org/people/<slug>` (Darvas's URL
  was scraped earlier with a bsky.app prefix bug — fetch direct).

### Photo-specific notes

- Editor prefers institutional photos over personal-site photos.
  CEU > gaborbekes.com for Békés. KRTK > rjuhasz.com for Juhász.
  When both exist, propose the institutional one.
- Photo URL must point to a stable host (institution domain, RePEc,
  Wikipedia Commons). Do **not** use bsky.app, x.com, linkedin.com,
  or Google image cache URLs.
- Verify the URL resolves to an image (200 OK, image/* content type)
  before proposing it — broken photo URLs are worse than null.

## Step 3 — Bio writing

If bio is missing or `review_status: stub`:

- **bio_en**: 2–3 sentences. Sentence 1: who they are and where
  (current primary affiliation). Sentence 2: what they research, in
  plain English. Sentence 3 (optional): one notable contribution or
  recognition. No quotes from their own site verbatim.
- **bio_hu**: same structure, idiomatic Hungarian. Not a literal
  translation of `bio_en`. Use Hungarian academic phrasing
  ("közgazdász", "kutató", "egyetemi tanár"). Order names HU-style
  (Békés Gábor, not Gábor Békés) when in HU prose.
- For the **deceased** field, set `true` and fill `died` (year)
  if RePEc / Wikipedia confirms; otherwise leave both `false`/null.

## Step 4 — qualifying_publication

If the field is null and the author has any catalogue paper:

1. Read `data/journals.json` to get tier rankings.
2. Among the author's papers in `data/papers/`, pick the one whose
   journal has the highest tier. Tier A beats Tier B.
3. Within the same tier, prefer the most recent year. Within the same
   year, prefer first-authored.
4. Set:
   ```json
   "qualifying_publication": {
     "title": "<exact title>",
     "journal": "<exact journal name from data/journals.json>",
     "year": <YYYY>
   }
   ```

If the author has no catalogue paper yet, leave null — the field gets
populated after the first paper is added.

## Step 5 — Paper backlog from RePEc

Run a diff between the RePEc author page and `data/papers/`:

1. Extract every published article from RePEc (these are the rows
   under "Published Articles" on the author profile, usually with a
   journal abbreviation and year).
2. For each, check whether the journal is on `data/journals.json`
   (tier A or B). Skip if not — those don't qualify.
3. For qualifying articles, generate the proposed slug
   `<surname>-<year>-<journalcode>` and check whether
   `data/papers/<slug>.json` exists. If not, it's a candidate.
4. Also include 2023+ working papers in NBER / CEPR / IZA / CESifo
   series (per SPEC §1.3).

Output the backlog as a numbered list, max 20 items, sorted by
journal tier then year desc.

## Output format

Return one block, in this order:

```
AUTHOR: <slug>  (<name_en>)
CURRENT STATE:
  filled:  bio_en, bio_hu, repec_id, ...
  missing: photo_url, scholar_id, qualifying_publication
  review_status: stub

PROPOSED PATCH (paste into data/authors/<slug>.json):
{
  "photo_url": "https://...",
  "repec_id": "p...",
  "scholar_id": "...",
  "qualifying_publication": { ... },
  "bio_en": "...",
  "bio_hu": "..."
}

EVIDENCE:
  - <URL> — what this confirmed
  - <URL> — what this confirmed
  - ...

PAPER BACKLOG (RePEc diff, qualifying journals only, top 20):
  1. <slug>  — <title>, <journal> <year>  [tier A]
  2. <slug>  — <title>, <journal> <year>  [tier B]
  ...

NOTES:
  - <ambiguity, name clash, deceased status, anything the editor
    should sanity-check>
```

## When to actually write the file

Default is dry-run. Only write `data/authors/<slug>.json` if the user
explicitly says "apply", "patch it", "go ahead", or similar. When
applying:

- Never overwrite a non-null field unless the user said "refresh"
- Set `last_reviewed_at: <today>`
- Bump `review_status` from `stub` → `human-reviewed` only if the
  user confirmed bio quality; otherwise leave as `stub`

Don't auto-create paper JSON files. The backlog is a list for the
editor to walk through; creating papers is a separate workflow
(`scripts/ingest.py`).

## What this skill does NOT do

- Verify Hungarian eligibility — that's `hu-econ-verifier` (Check 1).
  If you're researching someone whose eligibility is in doubt, run
  that skill first and stop here if the verdict is `no`.
- Draft summaries for the catalogue papers — that's `draft-summary`.
- Audit existing entries against current state — that's `audit-author`.
- Bulk processing. One author per invocation.

## Stopping rules

- 5–8 web fetches max. If after 5 you can't find a photo or bio,
  return what you have with `null`s and note what's missing.
- If RePEc returns 0 hits for the name, stop and ask the editor:
  is this person on a non-economics RePEc list, or is the
  spelling/slug different?
- If the eligibility check (`hu-econ-verifier`) returns `no` or
  `uncertain`, halt with a flag for the editor — don't enrich an
  author who shouldn't be in the catalogue.

## Example invocation

> "Research Simonovits András — he has 0 drafts and 15 papers."

Expected behaviour:
1. Read `data/authors/simonovits-andras.json` and the 15 paper files.
2. Confirm RePEc profile (`https://ideas.repec.org/e/psi39.html` or
   similar — verify).
3. Pull KRTK staff page for current photo + affiliation.
4. Diff RePEc published articles vs catalogue → backlog.
5. Return the block above. Don't draft summaries (that's a separate
   skill); flag him for `draft-summary --research --slug simonovits-andras`
   as a follow-up.
