# Cowork session — fetch PDFs for the catalogue

You're in a Cowork session with the editor (Gábor Békés). Your job: fetch
PDFs of academic papers via the editor's browser/library access, then either
save the PDFs locally or paste their abstracts into the catalogue JSONs so a
later Claude session can draft summaries.

This file is self-contained — you don't need to read anything else first.

## Project in one sentence

Magyar Közgazdászok is a Quarto/HTML site cataloguing peer-reviewed research
by Hungarian economists, framed for policymakers. Each catalogued paper
lives at `data/papers/<slug>.json`. Some have full summaries; many don't,
because we lack their abstracts.

## What you need to do

For each paper in a `pdf-lists/<author>.txt` list:

1. **Open the URL** (it's a DOI link — `https://doi.org/...`).
2. **The editor is logged into their institution's proxy in the browser**, so
   the publisher should serve you the PDF or full HTML.
3. Pick **one** of two paths:

### Fast path — paste abstract only

This is enough 80% of the time.

- Read the abstract from the publisher's page or PDF.
- Open `data/papers/<slug>.json`.
- Set the `abstract` field to the raw abstract text (verbatim, no editing
  required — Claude will paraphrase later).
- Set `last_reviewed_at` to today's date.
- Save.

A later Claude session will run `audit-author` / `draft-summary` and produce
a SPEC §5-compliant summary from your pasted abstract.

### Full path — save the PDF

For papers where the abstract alone isn't enough (theory papers, short
abstracts, complex empirical setups), save the PDF:

- Save to `not-shared/pdfs/<slug>.pdf`. The folder is gitignored.
- Create the folder if it doesn't exist: `mkdir -p not-shared/pdfs`.
- Don't rename — keep the slug as the filename.

A later Claude session can read the PDF via the `pdf` skill (extracts text
to `.txt`, then drafts).

## Where to find the work

- **Master list**: `pdf-lists/_all.csv` — all 247 papers needing PDFs, with
  columns: `slug, tier, year, journal, title, authors, doi, url`. Sort by
  whatever you want.
- **Per-author lists**: `pdf-lists/<author-slug>.txt` — 44 files, each one
  author's papers. One DOI URL per line, with comment headers giving slug
  + journal + year + title. Recommended starting point.
- **Priority doc**: `pdfs-needed-2026-04-27.md` (at repo root) — the same
  data in markdown, grouped by tier. Read this if you want context on
  which papers matter most.

## Suggested batch order

Top-yield batches (consistent journal access within author):

| Author | Papers | Where to fetch |
|---|---|---|
| temesvary-judit | 14 | Mostly Elsevier (JoBF/JIMF/JIE/JFS) |
| ambrus-attila | 12 | JET (Elsevier), AER (AEAweb), QJE (OUP), ResStud (OUP) |
| virag-gabor | 10 | JET, GEB (Elsevier), AEJ:Micro |
| csoka-peter | 10 | Elsevier mostly |
| szerb-laszlo | 10 | Springer (Small Business Econ), Taylor (Regional Studies) |
| biro-aniko | 8 | Elsevier (Health Econ), Springer |
| bekes-gabor | 7 | mixed |
| koszegi-botond | 7 | OUP, ResStud, AER |

Highest priority overall (regardless of author): start with the **9 papers
flagged as having bad abstracts** in the catalogue — those have wrong
metadata live on the public site and need fixing first. Listed at the top
of `pdfs-needed-2026-04-27.md` under "Flagged bad-abstract".

## What to do when

### A DOI link is broken
- Search the title on Google Scholar; the publisher version usually shows
  up. Update the URL in `data/papers/<slug>.json` `url_published` if the
  DOI was wrong, then proceed.

### The publisher is paywalled despite proxy access
- Try the author's personal/institutional page first (often a free
  preprint — for many authors check `data/authors/<slug>.json` `website`
  field).
- Try Sci-Hub if the editor has authorised that route. Don't assume.
- If neither, paste a note in the JSON `abstract` field: `"PAYWALLED — no
  abstract available"` and move on. A future session can revisit.

### The paper turns out to be a different person (namesake)
- Hungarian-name namesake issues are common (multiple Tóths, Vargas,
  Nagy/Nagys, etc.). Compare the actual paper authors with the catalogue
  author's bio (`data/authors/<slug>.json`). If wrong:
  - Update the paper's `authors` array — replace the wrong slug with the
    actual author's name as a string (not a slug, since they're not in
    the catalogue).
  - If no remaining catalogue author after fix: flag in a comment / leave
    for editor; don't delete the file.
  - **Don't add new authors to the catalogue** without editor approval.

### The paper turns out not to be a research paper
- Conference reports, book reviews, errata, replies-to-other-papers — flag
  by setting `abstract` to e.g. `"Conference report — not a research
  paper, consider dropping"`.
- Don't delete files; the editor decides.

## How to verify your work

Each completed paper should:
1. Have a non-empty `abstract` field, OR a saved PDF at `not-shared/pdfs/<slug>.pdf`.
2. Have `last_reviewed_at` set to today.

Quick check at the end of the session:

```bash
# Count papers with abstracts (should go up by N where N = papers you did)
python -c "import json,glob; print(sum(1 for f in glob.glob('data/papers/*.json') if json.load(open(f,encoding='utf-8')).get('abstract','').strip()))"
```

## Don't

- Don't draft summaries (`summary_en`, `policy_relevance`, etc.) yourself.
  That's a separate Claude session's job. Just provide the input
  (abstract or PDF).
- Don't delete papers, even ones that look low-quality. Editor's call.
- Don't add new author entries. Hungarian-economist admission is an
  editorial decision.
- Don't push or commit unless the editor asks. Cowork is for moving
  the work forward, not finalising it.

## When you're done with a batch

Tell the editor: "Done with batch X. Y papers got abstracts pasted, Z
PDFs saved, W flagged for editor (broken DOI / paywalled / namesake /
not-research)."

The editor will trigger a separate Claude session to draft summaries from
the abstracts/PDFs you've just unlocked.

## Edge case: the editor's browser session expires

If publisher access stops mid-batch (proxy cookies expired), pause and ask
the editor to re-authenticate. Don't try fetching without proxy — you'll
just hit paywalls.
