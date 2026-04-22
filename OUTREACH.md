# Outreach — sending authors their dossier for review

Two-way pipeline:

- **Outgoing:** `scripts/generate_dossier.py` builds a self-contained Markdown
  dossier per author — bio, affiliations, every paper with summary / data /
  policy / tags, plus editing instructions. Lands in `outreach/<id>.md`
  (gitignored).
- **Incoming:** author replies land in `submissions/YYYY-MM-DD-<surname>.md`
  and flow through the existing author-correction workflow (see
  [submissions/README.md](submissions/README.md)).

## One-author pilot

```bash
python scripts/generate_dossier.py bekes-gabor
```

Produces `outreach/bekes-gabor.md` — a ~250-line Markdown file that is:

- Readable as plain text (for email paste) or rendered (GitHub, VS Code).
- Self-explanatory to the recipient: cover note + edit instructions + every
  field labelled as either "shown on site" or "reference only".
- **Emails never embedded.** Addressing is by first name only. Emails live in
  `not-shared/contacts.json`, sent separately by the editor.
- Status of every paper shown inline (`ai-drafted`, `metadata-fetched`, …)
  so the author can see what's polished vs placeholder.

## Mailing mechanics

The dossier is the *content*; emailing is up to the editor. Options:

1. **Paste:** copy the Markdown into the email body. Readable in Gmail /
   Outlook despite the monospace markers.
2. **Attach:** send as `<author>-dossier.md`. Most authors can open .md;
   otherwise rename to `.txt`.
3. **Gist / doc link:** paste into a private Gist or Google Doc and send
   the link. Lets the author edit in-browser.

Option 1 is usually simplest. Cover email template:

> Dear [First name],
>
> As part of the Evidence for Hungary / Magyar Közgazdászok catalogue I'd
> love your quick review of what we have about you. The full dossier is
> pasted below — please edit inline and send back, or just reply with notes.
>
> Takes ~15 minutes. Covers your bio, affiliations, and the N papers
> currently listed.
>
> Thanks,
> Gábor

## Returning corrections

Author replies go to the editor. Drop the reply verbatim — whether it's an
edited dossier, a bulleted list, or a short note — into:

```
submissions/YYYY-MM-DD-<surname>.md
```

Then ask Claude in a repo session to "process new submissions." The
standard workflow applies: per-submission commit, `review_status` flips to
`author-approved`, file moves to `submissions/DONE/`.

## Bulk generation

To produce dossiers for everyone:

```bash
for id in $(ls data/authors | sed 's/\.json//'); do
  python scripts/generate_dossier.py "$id"
done
```

Or a subset (e.g. CEU faculty, Hungary-based, most-cited first) via a short
Python filter over `data/index.json`.

## Contacts file

`scripts/generate_contacts.py` → `not-shared/contacts.json`. Regenerate
after adding authors; it preserves hand-entered emails across runs. Use
that file for mail merge; don't scrape emails out of individual JSONs (most
are empty). See the top of `generate_contacts.py` for schema.
