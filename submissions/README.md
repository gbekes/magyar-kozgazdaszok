# submissions/ — author corrections queue

This folder is the editor–Claude workflow for author corrections. It's how an
author-sent email turns into a live site update without anyone writing JSON
by hand.

**Audience:** only listed authors in this catalogue. Anyone else (policymakers
spotting errors, readers with suggestions, self-promoters) files a GitHub issue
or emails the editor instead.

## How it works

1. **Author** sends the editor free-form corrections — any channel: email, DM,
   a Google Doc link, even a voice note that the editor types out. No template.
2. **Editor** (Gábor) drops the content into a new file:
   `submissions/YYYY-MM-DD-<author-surname>.md`.
3. **Editor** opens a Claude Code session in the repo and says
   "process new submissions" (or equivalent).
4. **Claude** reads each file, applies changes to the right JSON fields,
   commits per submission, and moves the file to `submissions/DONE/`
   (which is gitignored — local archive only).
5. **Editor** reviews the git diff and pushes. Live in ~2 min via GitHub Pages.

## File format

Free-form markdown or plain text. No strict template. Helpful to include:

- Author's name
- Date
- Which paper(s) or author bio the corrections target — slug if known,
  otherwise enough context for Claude to match

Things the author can change (non-exhaustive):

- Summary / data description / policy bullets (per paper, EN or HU).
- `policy_highlights` — explicit bullet list overriding the auto-split prose.
- Bio (EN or HU).
- Affiliations, website, email, Scholar/RePEc/ORCID IDs.
- `popular_links` (add/remove entries).
- Tags (topic, method, data-type, countries studied).
- **`open_to_media`** — turn on the "Open to media" slot on the author page,
  optionally with a scoping note (`media_note`), e.g. "interviews on labor
  economics in HU/EN; op-eds in Telex, Portfolio, HVG". Opt-in only —
  default is off.

Example:

```markdown
# Author: Attila Lindner
# Date: 2026-04-22

## Paper: lindner-harasztosi-2019-aer

Replace the policy bullets with:
- The Hungarian 60% minimum wage hike raised the average firm's wage bill
  by about 2% and output prices by about 1.5%
- Employment fell only modestly, concentrated at firms with weak worker
  bargaining power
- Most of the cost was passed on to consumers rather than absorbed through
  lower profits
- For Hungarian policymakers: moderate minimum-wage hikes deliver the
  redistributive goal without major job losses, but consumers pay

## My bio

Could you change "Attila Lindner is Professor of Economics at UCL…" to
"Attila Lindner is Professor of Economics at University College London and
a Fellow at IFS. His research focuses on labor-market policy — minimum
wages, job search, and pension systems — largely using Hungarian admin
data. He holds an ERC Consolidator Grant."

Leave the Hungarian bio as-is — I don't write Hungarian academic prose well.
```

That's it. Anything a Hungarian-speaking reader can make sense of, Claude can
process. No need for the author to learn tagging, slug conventions, or JSON.

## Bilingual handling

Authors typically send in one language. Claude updates the matching `_en` or
`_hu` field and leaves the other alone. **One language is enough.**

Exceptions — where Claude will also touch the other language:

- The author explicitly asks ("please translate to Hungarian").
- The correction is a factual change (e.g. data years, numbers) that makes
  the other-language version actively wrong. In this case Claude carries the
  factual change across and flags it in the commit message.

## What Claude does automatically

- Sets `review_status` on affected papers/authors to `author-approved`.
  That removes the "AI-drafted" warning banner on those pages.
- Writes commit messages like
  `Apply correction from Attila Lindner (2026-04-22): bio + policy bullets on lindner-harasztosi-2019-aer`.
- Moves the file to `submissions/DONE/` when the commit is made.
- Runs `python build.py` to refresh `data/index.json`.

## What Claude flags instead of doing

If any of these come up, Claude appends a `# QUESTION` section to the
submission file and does **not** commit. Editor answers, re-submits.

- **New author not in the catalogue.** Admission is an editorial decision.
  Claude flags instead of creating a new author JSON.
- **Ambiguous target** — e.g. "change my 2015 paper" when the author has
  three 2015 papers. Claude asks which one.
- **Destructive changes** — "delete my paper entirely", "remove me from the
  site". Editor confirms explicitly.
- **Admission rules / taxonomy changes** — "add this journal to the list",
  "create a new topic tag". Separate editorial process.
- **Contradictory edits within one submission.** Claude shows both versions
  and asks which to apply.

## Archive

`submissions/DONE/` is gitignored. Processed files accumulate there on the
editor's local machine but are never pushed. If long-run provenance beyond the
commit messages is wanted, just don't gitignore DONE.

## Filename convention

`YYYY-MM-DD-<author-surname>.md` — keeps the queue sortable. If a single
author sends two corrections in a day, add `-b`, `-c`, etc.:
`2026-04-22-lindner-b.md`.
