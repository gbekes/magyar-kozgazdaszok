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
  author. Outputs a JSON patch the editor can paste into
  `data/authors/<slug>.json` plus a numbered list of paper-slug
  suggestions for the catalogue.
---

# research-author

A research pass on one author at a time. Reads existing state, searches
the open web, returns a structured patch + a paper backlog. Default is
dry-run — only writes files when the user says "apply".

Read first, search second, write third. Never overwrite a non-null field
without telling the user; never invent affiliations, photos, IDs, or paper
metadata. If a fact is uncertain, leave the field at `null` and explain
in NOTES.

## Inputs

- An author slug (e.g. `simonovits-andras`) or a full name. If a name,
  resolve to the slug by checking `data/authors/*.json`. If no match,
  propose a slug as `surname-given.lower()` (diacritics stripped) and
  ask before creating.
- Optional plain-language flags: "just the bio", "just photo", "just
  papers", "everything". Default is everything.

## Step 1 — Read current state

1. `Read data/authors/<slug>.json` — note which fields are filled and
   the `review_status`.
2. `Glob data/papers/<slug>-*.json` and `Grep` for the slug in
   `authors` arrays — count what's already in the catalogue per
   `publication_type`.
3. Track which fields need work: `photo_url`, `bio_en`, `bio_hu`,
   `repec_id`, `scholar_id`, `orcid`, `qualifying_publication`,
   `affiliations`, `primary_fields`, `website`.

Don't search for things that are already filled unless the user said
"refresh".

## Step 2 — Web research, in this order

Stop early. Budget ~5–8 fetches total.

1. **RePEc / IDEAS author page.** Search `site:ideas.repec.org/e/
   <surname>` or `site:ideas.repec.org/f/p<initial><stem>.html`. The
   RePEc ID is the URL stem after `/e/` (e.g. `pbe115`). Highest-leverage
   page for catalogue diff and for confirming `repec_id`.
2. **Primary institution faculty page.** For Hungarian economists usually:
   - KRTK — `https://kti.krtk.hu/en/researchers/<slug>/` or HU equivalent
     at `kti.krtk.hu/researchers/<slug>/`
   - CEU — `https://economics.ceu.edu/people/<slug>` (Vienna era) or
     `https://people.ceu.edu/<slug>` (Budapest-era pages still live for
     emeritus faculty)
   - Corvinus — `https://www.uni-corvinus.hu/contributors/<slug>/`
   - MNB — search by name on `https://www.mnb.hu/`
   - Diaspora — Google `<full name> economist <institution>`. First
     non-news hit is almost always the personal or faculty page.
3. **Personal website.** RePEc usually links it. Otherwise Google
   `<name> economist site:.edu OR site:.com OR site:google.com/view`.
   Most reliable source for photo, current affiliations, ORCID,
   sometimes Scholar ID.
4. **Google Scholar profile.** Search `<name> site:scholar.google.com`.
   Scholar ID is the `user=` param. Confirm by checking 2–3 listed papers
   match the catalogue.
5. **Wikipedia (EN or HU).** Useful for senior / well-known economists.
   Verify against another source before pasting verbatim.
6. **ORCID.** Often linked from RePEc or the personal page; rarely worth
   a dedicated search.

### Diaspora-specific tips

Faculty pages follow predictable patterns:
`https://www.lse.ac.uk/economics/people/<slug>`,
`https://www.economics.ox.ac.uk/people/<slug>`,
`https://www.bocconi.it/en/people/<slug>`,
`https://vgsf.ac.at/faculty/<slug>`,
`https://www.crei.cat/people/<slug>`,
`https://www.bruegel.org/people/<slug>`.

### Photo notes

- Editor prefers institutional photos over personal-site ones (CEU >
  gaborbekes.com, KRTK > rjuhasz.com).
- Photo URL must point to a stable host (institution domain, RePEc,
  Wikipedia Commons). Do **not** use bsky.app, x.com, linkedin.com,
  or Google image cache URLs.
- Verify the URL resolves (200 OK, image/* content type) before
  proposing. Broken photo URLs are worse than null.

## Step 3 — Bio writing

If bio is missing or `review_status: stub`:

- **bio_en**: 2–3 sentences. (1) who they are and where (current
  primary affiliation). (2) what they research, in plain English.
  (3) optional: one notable contribution or recognition. No verbatim
  quotes from their site.
- **bio_hu**: same structure, idiomatic Hungarian — not a literal
  translation. Hungarian academic register ("közgazdász", "kutató",
  "egyetemi tanár"). HU-style name order in HU prose (Békés Gábor,
  not Gábor Békés).
- For `deceased: true`, fill `died` (year) if RePEc / Wikipedia
  confirms; otherwise leave both `false` / null.

## Step 4 — qualifying_publication

If null and the author has any catalogue paper:

1. Read `data/journals.json` for tier rankings. Tiers used: `A`, `B`,
   `B-hu`, `C`, `?`.
2. Pick the catalogue paper with the highest tier. Tier A beats B beats
   B-hu.
3. Within tier, prefer most recent. Within year, prefer first-authored.
4. Set:
   ```json
   "qualifying_publication": {
     "title": "<exact title>",
     "journal": "<exact journal name from data/journals.json>",
     "year": <YYYY>
   }
   ```

If the author has no catalogue paper yet, leave null.

## Step 5 — Paper backlog from RePEc

Diff RePEc author page against `data/papers/`:

1. Extract every published article from the RePEc profile.
2. For each, check whether the journal is on `data/journals.json`
   tier A or B. Skip if not — those don't qualify.
3. Generate proposed slug `<surname>-<year>-<journalcode>` and check
   whether `data/papers/<slug>.json` exists. If not, candidate.
4. Also include 2023+ working papers in NBER / CEPR / IZA / CESifo
   series (per SPEC §1.3).

Output the backlog as a numbered list, max 20 items, sorted by tier
then year desc.

## Output format

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

PAPER BACKLOG (RePEc diff, qualifying journals only, top 20):
  1. <slug>  — <title>, <journal> <year>  [tier A]
  2. <slug>  — <title>, <journal> <year>  [tier B]

NOTES:
  - <ambiguity, name clash, deceased status, anything to sanity-check>
```

## When to actually write the file

Default is dry-run. Write `data/authors/<slug>.json` only when the user
says "apply", "patch it", "go ahead", or similar. When applying:

- Never overwrite a non-null field unless the user said "refresh"
- Set `last_reviewed_at: <today>`
- Bump `review_status` from `stub` → `human-reviewed` only if the user
  confirmed bio quality

Don't auto-create paper JSON files. The backlog is a list for the
editor to walk through; creating papers is `scripts/ingest.py`.

## Stopping rules

- 5–8 web fetches max. After 5, return what you have with `null`s and
  note what's missing.
- If RePEc returns 0 hits for the name, stop and ask: is this person
  on a non-economics RePEc list, or is the spelling/slug different?
- If `hu-econ-verifier` (Check 1) returns `no` or `uncertain`, halt
  and flag — don't enrich an author who shouldn't be in the catalogue.

## Out of scope

- Hungarian-eligibility check — `hu-econ-verifier`.
- Drafting summaries — `draft-summary`.
- Auditing existing entries — `audit-author`.
- Bulk processing.

## Example

> "Research Simonovits András — he has 0 drafts and 15 papers."

1. Read `data/authors/simonovits-andras.json` and the 15 paper files.
2. Confirm RePEc profile (`https://ideas.repec.org/e/psi174.html`).
3. Pull KRTK staff page for current photo + affiliation.
4. Diff RePEc published articles vs catalogue → backlog.
5. Return the block above. Don't draft summaries; flag him for
   `draft-summary --research simonovits-andras` as a follow-up.
